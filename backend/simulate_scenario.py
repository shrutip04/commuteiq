"""
simulate_scenario.py — What-If scenario simulation engine.
Modifies route parameters based on user-controlled inputs.
"""

import copy
from ml_engine import compute_trust_score, predict_future_risk


def simulate_scenario(route: dict, delay_added: float, weather: str, is_night: bool, user_mode: str = "normal") -> dict:
    """
    Simulate a what-if scenario on a route.

    Args:
        route: Original route dict
        delay_added: Extra delay in minutes (0-20)
        weather: "clear" | "rain" | "heavy_rain"
        is_night: bool
        user_mode: "normal" | "anxious" | "late"

    Returns:
        Modified route with updated trust_score, risk, and warnings
    """
    r = copy.deepcopy(route)
    warnings = []

    # Apply delay
    if delay_added > 0:
        r["delay_minutes"] = round(r["delay_minutes"] + delay_added, 1)
        r["travel_time"]   = r["travel_time"] + int(delay_added * 0.9)
        if delay_added >= 10:
            warnings.append(f"⚠️ +{delay_added} min delay significantly impacts travel time")

    # Apply weather effects
    if weather == "rain":
        r["crowding_pct"]   = min(100, r["crowding_pct"] * 1.15)
        r["delay_minutes"]  = round(r["delay_minutes"] * 1.2, 1)
        r["confidence_score"] = max(0.3, r["confidence_score"] - 0.08)
        warnings.append("🌧️ Rain increases crowding by ~15% and adds delay")
    elif weather == "heavy_rain":
        r["crowding_pct"]   = min(100, r["crowding_pct"] * 1.35)
        r["delay_minutes"]  = round(r["delay_minutes"] * 1.5, 1)
        r["confidence_score"] = max(0.2, r["confidence_score"] - 0.20)
        warnings.append("⛈️ Heavy rain severely impacts all routes — expect major delays")

    # Night mode
    if is_night:
        r["crowding_pct"]   = max(5, r["crowding_pct"] * 0.6)
        r["confidence_score"] = max(0.3, r["confidence_score"] - 0.10)
        warnings.append("🌙 Night conditions: lower crowding but reduced service frequency")

    # User mode adjustments
    if user_mode == "anxious":
        # Penalize high crowding more
        if r["crowding_pct"] > 60:
            r["confidence_score"] = max(0.2, r["confidence_score"] - 0.15)
            warnings.append("😰 High crowding detected — not ideal for anxious travellers")
    elif user_mode == "late":
        # Accept higher risk for speed
        r["travel_time"] = int(r["travel_time"] * 0.92)
        warnings.append("🏃 Late mode: optimising for speed, risk tolerance increased")

    # Recompute trust score
    r["crowding_pct"] = round(min(100, max(0, r["crowding_pct"])), 1)
    hour = r.get("_hour", 22 if is_night else 12)
    r["trust_score"] = compute_trust_score({**r, "_hour": hour})

    # Recompute risk
    features = {
        "hour":           hour,
        "is_peak":        int((8 <= hour <= 10) or (17 <= hour <= 19)),
        "distance_km":    r.get("distance_km", 10),
        "num_stops":      r.get("num_stops", 5),
        "transport_mode": 1,
        "weather_score":  0.3 if weather == "heavy_rain" else (0.6 if weather == "rain" else 1.0),
        "day_of_week":    3,
    }
    r["risk"] = predict_future_risk(features)
    r["scenario_warnings"] = warnings

    return r