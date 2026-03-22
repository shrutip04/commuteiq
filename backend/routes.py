"""
routes.py — All API endpoints for CommuteIQ (extended with advanced features).
"""

import random
from flask import Blueprint, request, jsonify, g
from functools import wraps
from datetime import datetime

from database import get_db
from auth import decode_token, generate_token, hash_password, verify_password
from utils import generate_routes, generate_routes_with_transit, generate_heatmap_data, format_response
from explain import generate_explanation
from simulate_alert import simulate_disruption
from simulate_scenario import simulate_scenario
from ml_engine import compute_trust_score, predict_future_risk

api = Blueprint("api", __name__)


# ── Auth Middleware ────────────────────────────────────────────────────────────

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)
        if payload is None:
            return jsonify({"error": "Token expired or invalid"}), 401
        g.user_id = payload["user_id"]
        g.username = payload["username"]
        return f(*args, **kwargs)
    return decorated


def _enrich_route(route: dict, hour: int) -> dict:
    """Add trust_score and risk prediction to a route dict."""
    route["_hour"] = hour
    route["trust_score"] = compute_trust_score({**route, "_hour": hour})
    features = {
        "hour": hour,
        "is_peak": int((8 <= hour <= 10) or (17 <= hour <= 19)),
        "distance_km": route.get("distance_km", 10),
        "num_stops": route.get("num_stops", 5),
        "transport_mode": 1,
        "weather_score": 0.8,
        "day_of_week": datetime.now().weekday(),
    }
    route["risk"] = predict_future_risk(features)
    return route


def _apply_emotional_mode(route: dict, user_mode: str, hour: int) -> dict:
    """
    Apply emotional safety mode adjustments to route scoring.
    This ACTUALLY changes trust scores and adds mode-specific warnings.
    """
    is_night = hour >= 21 or hour <= 5
    crowding = route.get("crowding_pct", 50)
    route["emotional_mode"] = user_mode
    route["mode_notes"] = []

    if user_mode == "anxious":
        # Penalise crowded routes heavily
        if crowding > 60:
            route["trust_score"] = max(0, route["trust_score"] - 20)
            route["mode_notes"].append("😰 High crowd avoided — safety re-weighted for anxious mode")
        elif crowding > 40:
            route["trust_score"] = max(0, route["trust_score"] - 8)
            route["mode_notes"].append("😰 Moderate crowd detected — slight penalty applied")
        else:
            route["trust_score"] = min(100, route["trust_score"] + 5)
            route["mode_notes"].append("✅ Low crowding — ideal for anxious traveller")
        # Prefer trains over auto
        if "Auto/Cab" in route.get("modes", []):
            route["trust_score"] = max(0, route["trust_score"] - 10)
            route["mode_notes"].append("⚠️ Auto/Cab less preferred in anxious mode — less predictable")

    elif user_mode == "alone_night":
        # Night alone: strongly prefer busy/well-lit routes (trains/metro)
        if is_night:
            route["mode_notes"].append("🌙 Night mode: prioritising well-lit, busy transport")
        if "Local Train" in route.get("modes", []) or "Metro" in route.get("modes", []):
            route["trust_score"] = min(100, route["trust_score"] + 12)
            route["mode_notes"].append("✅ Train/Metro preferred — safer at night")
        if "Auto/Cab" in route.get("modes", []):
            route["trust_score"] = max(0, route["trust_score"] - 15)
            route["mode_notes"].append("⚠️ Auto/Cab less safe when alone at night — avoided")
        if crowding < 20:
            route["trust_score"] = max(0, route["trust_score"] - 8)
            route["mode_notes"].append("⚠️ Very low crowd — less safe when alone")

    elif user_mode == "late":
        # Late: prioritise speed, ignore crowding
        route["trust_score"] = min(100, route["trust_score"] + 8)
        route["mode_notes"].append("🏃 Late mode: speed optimised, safety tolerance increased")
        if route.get("travel_time", 999) < 20:
            route["trust_score"] = min(100, route["trust_score"] + 5)

    return route


# ── Auth Endpoints ─────────────────────────────────────────────────────────────

@api.route("/signup", methods=["GET", "POST", "OPTIONS"])
def signup():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    db = get_db()
    try:
        password_hash = hash_password(password)
        db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                   (username, email, password_hash))
        db.commit()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        token = generate_token(user["id"], user["username"])
        return jsonify(format_response({
            "token": token,
            "user": {"id": user["id"], "username": user["username"], "email": user["email"]},
        })), 201
    except Exception as e:
        if "UNIQUE constraint" in str(e):
            return jsonify({"error": "Username or email already exists"}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@api.route("/login", methods=["GET", "POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.get_json() or {}
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    db = get_db()
    try:
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user or not verify_password(password, user["password_hash"]):
            return jsonify({"error": "Invalid email or password"}), 401
        token = generate_token(user["id"], user["username"])
        return jsonify(format_response({
            "token": token,
            "user": {"id": user["id"], "username": user["username"], "email": user["email"]},
        }))
    finally:
        db.close()


@api.route("/me", methods=["GET"])
@require_auth
def me():
    db = get_db()
    try:
        user = db.execute("SELECT id, username, email, created_at FROM users WHERE id = ?",
                          (g.user_id,)).fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(format_response(dict(user)))
    finally:
        db.close()


# ── Journey Endpoints ──────────────────────────────────────────────────────────

@api.route("/plan_journey", methods=["POST"])
@require_auth
def plan_journey():
    data        = request.get_json()
    source      = data.get("source", "CST")
    destination = data.get("destination", "Andheri")
    time_str    = data.get("time", "09:00")
    preference  = data.get("preference", "balanced")
    user_mode   = data.get("user_mode", "normal")

    try:
        hour = int(time_str.split(":")[0]) if time_str else datetime.now().hour
    except Exception:
        hour = datetime.now().hour

    if not source or not destination:
        return jsonify({"error": "source and destination are required"}), 400

    try:
        routes = generate_routes_with_transit(source, destination, time_str, preference)

        # Enrich all routes with trust score + risk
        enriched = []
        for r in routes:
            r = _enrich_route(r, hour)
            enriched.append(r)

        # Fetch user gender from DB for safety scoring
        gender = "prefer_not_to_say"
        try:
            from safety_engine import apply_safety_scoring
            db_temp = get_db()
            prefs = db_temp.execute(
                "SELECT gender FROM user_preferences WHERE user_id = ?", (g.user_id,)
            ).fetchone()
            db_temp.close()
            if prefs and prefs["gender"]:
                gender = prefs["gender"]
            enriched, safety_profile = apply_safety_scoring(enriched, user_mode, gender, hour)
        except Exception as e:
            print(f"[Safety] Scoring error: {e}")
            safety_profile = {"applied_rules": []}

        return jsonify(format_response({
            "routes": enriched,
            "query": {
                "source": source,
                "destination": destination,
                "time": time_str,
                "preference": preference,
                "user_mode": user_mode,
            },
        }))
    except Exception as e:
        return jsonify({"error": f"Route generation failed: {str(e)}"}), 500


@api.route("/simulate_alert", methods=["POST"])
@require_auth
def simulate_alert():
    data     = request.get_json()
    routes   = data.get("routes", [])
    disruption_type = data.get("disruption_type")
    if not routes:
        return jsonify({"error": "routes array is required"}), 400
    try:
        result = simulate_disruption(routes, disruption_type)
        # Re-enrich updated routes
        hour = datetime.now().hour
        result["updated_routes"] = [_enrich_route(r, hour) for r in result["updated_routes"]]
        return jsonify(format_response(result))
    except Exception as e:
        return jsonify({"error": f"Simulation failed: {str(e)}"}), 500


@api.route("/route_explanation", methods=["POST"])
@require_auth
def route_explanation():
    data           = request.get_json()
    selected_route = data.get("selected_route")
    alternatives   = data.get("alternatives", [])
    if not selected_route:
        return jsonify({"error": "selected_route is required"}), 400
    result = generate_explanation(selected_route, alternatives)
    return jsonify(format_response(result))


@api.route("/heatmap_data", methods=["GET"])
@require_auth
def heatmap_data():
    src_lat = float(request.args.get("src_lat", 19.076))
    src_lng = float(request.args.get("src_lng", 72.877))
    dst_lat = float(request.args.get("dst_lat", 19.076))
    dst_lng = float(request.args.get("dst_lng", 72.877))
    points = generate_heatmap_data(src_lat, src_lng, dst_lat, dst_lng)
    return jsonify(format_response({"points": points, "count": len(points)}))


# ── What-If Simulation ─────────────────────────────────────────────────────────

@api.route("/simulate_scenario", methods=["POST"])
@require_auth
def simulate_scenario_endpoint():
    """What-if scenario: apply delay, weather, night mode to a route."""
    data        = request.get_json()
    route       = data.get("route")
    delay_added = float(data.get("delay_added", 0))
    weather     = data.get("weather", "clear")      # clear | rain | heavy_rain
    is_night    = bool(data.get("is_night", False))
    user_mode   = data.get("user_mode", "normal")

    if not route:
        return jsonify({"error": "route is required"}), 400

    try:
        updated = simulate_scenario(route, delay_added, weather, is_night, user_mode)
        return jsonify(format_response({"route": updated}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Live Monitor ───────────────────────────────────────────────────────────────

@api.route("/live_monitor", methods=["GET"])
@require_auth
def live_monitor():
    """Simulate real-time risk monitoring during a journey."""
    hour = datetime.now().hour
    is_peak = (8 <= hour <= 10) or (17 <= hour <= 19)

    # Simulate probabilistic alerts
    alert_probability = 0.35 if is_peak else 0.15
    alert = random.random() < alert_probability

    messages = [
        "⚠️ Crowding increasing ahead. Consider the alternate route.",
        "⚠️ Signal delay detected — platform 2 congested.",
        "⚠️ Risk rising due to peak hour surge. Safer route available.",
        "⚠️ Unscheduled maintenance causing delays on next segment.",
    ]
    safe_messages = [
        "✅ All clear — your route is running smoothly.",
        "✅ On-time service detected. No disruptions ahead.",
        "✅ Low crowding on current route segment.",
    ]

    return jsonify(format_response({
        "alert": alert,
        "message": random.choice(messages if alert else safe_messages),
        "risk_level": "HIGH" if alert and is_peak else ("MEDIUM" if alert else "LOW"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }))


# ── User Preferences ───────────────────────────────────────────────────────────

@api.route("/user_preferences", methods=["POST"])
@require_auth
def save_preferences():
    data          = request.get_json() or {}
    preference    = data.get("preference", "balanced")
    home_location = data.get("home_location", "")
    work_location = data.get("work_location", "")
    user_mode     = data.get("user_mode", "normal")
    gender        = data.get("gender", "prefer_not_to_say")

    db = get_db()
    try:
        existing = db.execute("SELECT id FROM user_preferences WHERE user_id = ?",
                              (g.user_id,)).fetchone()
        if existing:
            db.execute("""UPDATE user_preferences
                          SET preference=?, home_location=?, work_location=?,
                              gender=?, user_mode=?, updated_at=CURRENT_TIMESTAMP
                          WHERE user_id=?""",
                       (preference, home_location, work_location, gender, user_mode, g.user_id))
        else:
            db.execute("""INSERT INTO user_preferences
                          (user_id, preference, home_location, work_location, gender, user_mode)
                          VALUES (?,?,?,?,?,?)""",
                       (g.user_id, preference, home_location, work_location, gender, user_mode))
        db.commit()
        return jsonify(format_response({"saved": True, "preference": preference, "gender": gender, "user_mode": user_mode}))
    finally:
        db.close()


@api.route("/user_preferences", methods=["GET"])
@require_auth
def get_preferences():
    db = get_db()
    try:
        prefs = db.execute("SELECT * FROM user_preferences WHERE user_id = ?",
                           (g.user_id,)).fetchone()
        if not prefs:
            return jsonify(format_response({
                "preference": "balanced",
                "home_location": "",
                "work_location": "",
                "gender": "prefer_not_to_say",
                "user_mode": "normal",
            }))
        d = dict(prefs)
        if "gender" not in d: d["gender"] = "prefer_not_to_say"
        if "user_mode" not in d: d["user_mode"] = "normal"
        return jsonify(format_response(d))
    finally:
        db.close()


# ── Guardian Mode ──────────────────────────────────────────────────────────────

@api.route("/guardian_check", methods=["POST"])
@require_auth
def guardian_check():
    """
    Guardian mode real-time check.
    Receives simulated location + journey state and returns safety alerts.
    """
    data = request.get_json() or {}
    event_type   = data.get("event_type", "normal")   # inactive | deviation | risk_spike | normal
    location     = data.get("location", {})
    route_id     = data.get("route_id", "")
    elapsed_min  = data.get("elapsed_min", 0)
    user_mode    = data.get("user_mode", "normal")

    hour = datetime.now().hour
    is_night = hour >= 21 or hour <= 5

    ALERTS = {
        "inactive": {
            "level": "WARNING",
            "icon": "⚠️",
            "title": "Are you safe?",
            "message": f"You've been inactive for {elapsed_min} minutes. Tap to confirm you're okay.",
            "action": "CONFIRM_SAFE",
            "color": "#f59e0b",
            "suggest_contact": True,
        },
        "deviation": {
            "level": "WARNING",
            "icon": "🗺️",
            "title": "Route Deviation Detected",
            "message": "You've left the recommended safe path. Recalculating safer route.",
            "action": "REROUTE",
            "color": "#f97316",
            "suggest_contact": False,
        },
        "risk_spike": {
            "level": "DANGER",
            "icon": "🚨",
            "title": "Safety Alert",
            "message": "Area ahead has elevated risk. An alternate route has been found — 4 min longer but significantly safer.",
            "action": "ALTERNATE_ROUTE",
            "color": "#ef4444",
            "suggest_contact": user_mode == "anxious" or is_night,
        },
        "normal": {
            "level": "OK",
            "icon": "✅",
            "title": "Journey Safe",
            "message": "All clear. You're on track and safe.",
            "action": None,
            "color": "#10b981",
            "suggest_contact": False,
        },
    }

    alert = ALERTS.get(event_type, ALERTS["normal"])

    # Night + anxious mode: escalate warnings
    if is_night and event_type != "normal":
        alert["suggest_contact"] = True
        if event_type == "inactive":
            alert["message"] = f"🌙 Night mode: You've been inactive {elapsed_min} min. Auto-alerting trusted contact."

    # Simulate trusted contact notification
    contact_notified = False
    if alert.get("suggest_contact"):
        contact_notified = True

    return jsonify(format_response({
        "alert": alert,
        "contact_notified": contact_notified,
        "trusted_contact": "Mom 📱" if contact_notified else None,
        "is_night": is_night,
        "user_mode": user_mode,
    }))


@api.route("/guardian_scenario", methods=["POST"])
@require_auth
def guardian_scenario():
    """
    What-If simulation: returns impact analysis for delay/rain/night scenarios.
    """
    data        = request.get_json() or {}
    route       = data.get("route", {})
    delay_added = float(data.get("delay_added", 0))
    weather     = data.get("weather", "clear")
    is_night    = bool(data.get("is_night", False))
    user_mode   = data.get("user_mode", "normal")

    from simulate_scenario import simulate_scenario
    updated = simulate_scenario(route, delay_added, weather, is_night, user_mode)

    # Compute impact narrative
    orig_trust  = route.get("trust_score", 70)
    new_trust   = updated.get("trust_score", 70)
    trust_delta = new_trust - orig_trust

    orig_risk   = route.get("risk", {}).get("current_pct", 30)
    new_risk    = updated.get("risk", {}).get("current_pct", 30)
    risk_delta  = new_risk - orig_risk

    # Build impact sentences
    impacts = []
    if delay_added > 0:
        impacts.append(f"⏰ +{int(delay_added)} min delay drops safety score from {orig_trust} → {new_trust} ({abs(trust_delta)} pts {'↓' if trust_delta < 0 else '↑'})")
    if weather == "rain":
        impacts.append(f"🌧️ Rain increases accident risk by ~{abs(risk_delta)}% and crowding by ~15%")
    elif weather == "heavy_rain":
        impacts.append(f"⛈️ Heavy rain raises risk by ~{abs(risk_delta)}% — major delays expected across all routes")
    if is_night:
        impacts.append(f"🌙 Night mode: service frequency drops, safety score penalised by ~10 pts")
    if user_mode == "anxious":
        impacts.append(f"😰 Anxious mode active: route safety re-weighted — crowded areas penalised further")

    if not impacts:
        impacts.append("✅ No significant impact detected under current scenario")

    return jsonify(format_response({
        "original": {"trust_score": orig_trust, "risk_pct": orig_risk},
        "simulated": {"trust_score": new_trust, "risk_pct": new_risk},
        "trust_delta": trust_delta,
        "risk_delta": risk_delta,
        "impacts": impacts,
        "updated_route": updated,
        "warnings": updated.get("scenario_warnings", []),
    }))


# ── Cost Options ──────────────────────────────────────────────────────────────

@api.route("/cost_options", methods=["POST"])
@require_auth
def cost_options():
    """
    Return multi-modal cost breakdown for a journey.
    POST body: { source, destination, distance }
    """
    data        = request.get_json() or {}
    source      = data.get("source", "")
    destination = data.get("destination", "")
    distance    = float(data.get("distance", 10))

    # If distance not provided, compute from geocodes
    if distance <= 0 and source and destination:
        try:
            from utils import geocode, haversine_distance
            slat, slng = geocode(source)
            dlat, dlng = geocode(destination)
            distance = haversine_distance(slat, slng, dlat, dlng) * 1.3
        except Exception:
            distance = 10

    try:
        from cost_engine import generate_cost_options
        result = generate_cost_options(distance)
        return jsonify(format_response(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 500