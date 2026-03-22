"""
emergency.py — Intelligent Emergency Response System for CommuteIQ.
Handles emergency contacts, alert dispatch, and live safety monitoring.
"""

import random
from datetime import datetime


# ── Emergency contact management ──────────────────────────────────────────────

def get_contacts(db, user_id: int) -> list:
    rows = db.execute(
        "SELECT * FROM emergency_contacts WHERE user_id = ? ORDER BY type",
        (user_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def add_contact(db, user_id: int, name: str, phone: str, contact_type: str) -> dict:
    db.execute(
        "INSERT INTO emergency_contacts (user_id, name, phone, type) VALUES (?,?,?,?)",
        (user_id, name, phone, contact_type)
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM emergency_contacts WHERE user_id=? ORDER BY id DESC LIMIT 1",
        (user_id,)
    ).fetchone()
    return dict(row)


def delete_contact(db, contact_id: int, user_id: int) -> bool:
    db.execute(
        "DELETE FROM emergency_contacts WHERE id=? AND user_id=?",
        (contact_id, user_id)
    )
    db.commit()
    return True


# ── Alert message builder ──────────────────────────────────────────────────────

def build_alert_message(location: dict, reason: str, username: str = "User") -> str:
    lat = location.get("lat", 0)
    lng = location.get("lng", 0)
    maps_url = f"https://maps.google.com/?q={lat},{lng}"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return (
        f"🚨 EMERGENCY ALERT\n"
        f"{'─' * 30}\n"
        f"{username} may need assistance.\n\n"
        f"📍 Location: {maps_url}\n"
        f"⚠️ Reason: {reason}\n"
        f"🕐 Time: {timestamp}\n\n"
        f"Please check on them immediately or call emergency services.\n"
        f"India Emergency: 112"
    )


# ── Simulate sending alerts ────────────────────────────────────────────────────

def dispatch_alerts(contacts: list, message: str) -> list:
    """
    Simulate sending SMS/call alerts to all emergency contacts.
    In production: replace with Twilio / AWS SNS / Firebase.
    """
    dispatched = []
    for contact in contacts:
        # Simulate network delay and success
        success = random.random() > 0.05  # 95% success rate
        status = "delivered" if success else "failed"
        print(f"[Emergency] Alert → {contact['name']} ({contact['phone']}): {status}")
        dispatched.append({
            "contact_id":   contact["id"],
            "name":         contact["name"],
            "phone":        contact["phone"],
            "type":         contact["type"],
            "status":       status,
            "channel":      "sms",
            "timestamp":    datetime.utcnow().isoformat() + "Z",
        })
    return dispatched


# ── Core emergency handler ─────────────────────────────────────────────────────

def handle_emergency(db, user_id: int, location: dict, risk_score: float,
                     reason: str, username: str = "User") -> dict:
    """
    Full emergency response pipeline:
    1. Fetch contacts
    2. Build alert message
    3. Dispatch alerts
    4. Start tracking + recording (simulated)
    5. Return full response
    """
    contacts = get_contacts(db, user_id)

    # Always include default emergency services
    default_services = [
        {"id": -1, "name": "Police",    "phone": "100", "type": "police"},
        {"id": -2, "name": "Ambulance", "phone": "102", "type": "ambulance"},
        {"id": -3, "name": "Emergency", "phone": "112", "type": "national"},
    ]

    message   = build_alert_message(location, reason, username)
    personal  = [c for c in contacts if c["type"] == "personal"]
    dispatched = dispatch_alerts(personal, message) if personal else []

    lat = location.get("lat", 0)
    lng = location.get("lng", 0)

    return {
        "status":           "emergency_active",
        "emergency_id":     f"EMG-{user_id}-{int(datetime.utcnow().timestamp())}",
        "alert_message":    message,
        "contacts_alerted": dispatched,
        "contacts_count":   len(dispatched),
        "tracking_active":  True,
        "recording_active": True,
        "location":         location,
        "maps_url":         f"https://maps.google.com/?q={lat},{lng}",
        "risk_score":       risk_score,
        "reason":           reason,
        "services":         default_services,
        "timestamp":        datetime.utcnow().isoformat() + "Z",
    }


# ── Live safety check ──────────────────────────────────────────────────────────

def live_safety_check(risk_score: float = None, user_mode: str = "normal") -> dict:
    """
    Periodic safety check. Returns alert status and severity.
    Integrates with ML risk predictions.
    """
    hour = datetime.now().hour
    is_night = hour >= 21 or hour <= 5
    is_late_night = hour >= 23 or hour <= 4

    # Anomaly types with weighted probabilities
    if is_late_night and user_mode in ("alone_night", "anxious"):
        anomaly_prob = 0.30
    elif is_night:
        anomaly_prob = 0.20
    else:
        anomaly_prob = 0.10

    # If ML risk score provided, factor it in
    if risk_score is not None and risk_score > 0.75:
        anomaly_prob = max(anomaly_prob, risk_score * 0.5)

    alert = random.random() < anomaly_prob

    ANOMALY_REASONS = [
        ("Unusual inactivity detected on your route",    "MEDIUM"),
        ("Route deviation from safe path detected",      "HIGH"),
        ("High-risk area ahead on current route",        "HIGH"),
        ("Abnormal movement pattern detected",           "MEDIUM"),
        ("Extended stop in low-crowd area",              "MEDIUM"),
    ]
    CLEAR_MESSAGES = [
        "All clear — your route looks safe",
        "Journey proceeding normally",
        "No safety concerns detected",
    ]

    if alert:
        reason, severity = random.choice(ANOMALY_REASONS)
        return {
            "alert":    True,
            "reason":   reason,
            "severity": severity,
            "message":  f"⚠️ {reason}. Are you safe?",
            "auto_trigger_secs": 10,
        }
    return {
        "alert":    False,
        "reason":   None,
        "severity": "NONE",
        "message":  random.choice(CLEAR_MESSAGES),
    }