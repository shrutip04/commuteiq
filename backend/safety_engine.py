"""
safety_engine.py — Context-aware safety scoring engine.

No ML retraining needed. Works by re-weighting existing ML predictions
based on user profile (gender, mode, time of day).

How it works:
  ML predicts: crowding_pct, delay_minutes, confidence_score
  Safety engine: applies multipliers and penalties on top of those scores
  Result: trust_score changes → routes reorder → user sees safer/faster route first
"""

from datetime import datetime


def get_safety_profile(user_mode: str, gender: str, hour: int) -> dict:
    """
    Build a safety profile dict that defines scoring weights for this user+context.
    No ML needed — pure logic on top of existing predictions.
    """
    is_night      = hour >= 21 or hour <= 5
    is_late_night = hour >= 23 or hour <= 4
    is_peak       = (8 <= hour <= 10) or (17 <= hour <= 19)
    is_female     = gender == "female"

    profile = {
        "mode":           user_mode,
        "gender":         gender,
        "hour":           hour,
        "is_night":       is_night,
        "is_late_night":  is_late_night,
        "is_peak":        is_peak,
        "is_female":      is_female,

        # Weights: how much each factor matters (0–1 scale)
        "weight_crowding":    0.35,
        "weight_delay":       0.25,
        "weight_confidence":  0.40,

        # Mode-specific bonuses/penalties per transport type
        "mode_bonus": {
            "Local Train": 0,
            "Metro":       0,
            "Bus":         0,
            "Auto/Cab":    0,
        },

        # Crowding threshold above which route is penalised
        "crowding_penalty_threshold": 65,
        "crowding_penalty_pts":       0,

        # Low crowd penalty (isolated routes)
        "low_crowd_penalty_threshold": 20,
        "low_crowd_penalty_pts":       0,

        # Speed bonus (for Late mode)
        "speed_bonus_pts":         0,
        "speed_bonus_threshold":   20,   # minutes

        # Sort key override: "trust" or "speed"
        "sort_by": "trust",

        # Human-readable explanation of what changed
        "applied_rules": [],
    }

    # ── NORMAL MODE ────────────────────────────────────────────────────────────
    if user_mode == "normal":
        profile["applied_rules"].append("Standard balanced routing — no adjustments")

    # ── ANXIOUS MODE ───────────────────────────────────────────────────────────
    elif user_mode == "anxious":
        profile["weight_crowding"]   = 0.55   # crowding matters much more
        profile["weight_confidence"] = 0.35
        profile["weight_delay"]      = 0.10

        profile["crowding_penalty_threshold"] = 50  # lower threshold
        profile["crowding_penalty_pts"]       = 18

        profile["mode_bonus"]["Auto/Cab"] = -12   # unpredictable = bad
        profile["mode_bonus"]["Local Train"] = +5
        profile["mode_bonus"]["Metro"] = +5

        profile["sort_by"] = "trust"
        profile["applied_rules"] = [
            "Crowding weighted 55% (vs 35% normal) — avoids packed routes",
            "Auto/Cab penalised −12 pts (less predictable environment)",
            "Train & Metro boosted +5 pts (structured, monitored)",
            "Routes sorted by safety score, not speed",
        ]

    # ── ALONE AT NIGHT ─────────────────────────────────────────────────────────
    elif user_mode == "alone_night":
        profile["weight_crowding"]   = 0.45
        profile["weight_confidence"] = 0.40
        profile["weight_delay"]      = 0.15

        # Want some crowd (not isolated), but not packed
        profile["crowding_penalty_threshold"] = 75   # only penalise very crowded
        profile["crowding_penalty_pts"]       = 8
        profile["low_crowd_penalty_threshold"] = 25  # penalise too-empty routes
        profile["low_crowd_penalty_pts"]       = 15  # isolated = dangerous

        profile["mode_bonus"]["Local Train"] = +15
        profile["mode_bonus"]["Metro"]       = +15
        profile["mode_bonus"]["Bus"]         = +5
        profile["mode_bonus"]["Auto/Cab"]    = -18  # alone in auto at night = risky

        if is_late_night:
            # After 11pm: even stronger penalties
            profile["mode_bonus"]["Auto/Cab"]    -= 5
            profile["mode_bonus"]["Local Train"] += 5
            profile["applied_rules"].append("Late night (11pm+): Auto/Cab penalised further")

        profile["sort_by"] = "trust"
        profile["applied_rules"] += [
            "Train & Metro boosted +15 pts (well-lit, monitored, busy)",
            "Auto/Cab penalised −18 pts (unsafe alone at night)",
            "Very low-crowd routes penalised (isolated = higher risk)",
            "Routes sorted by safety, not speed",
        ]

    # ── FEMALE ALONE AT NIGHT (extra safety layer) ─────────────────────────────
    if is_female and is_night and user_mode in ("alone_night", "anxious"):
        profile["mode_bonus"]["Auto/Cab"]    -= 10   # extra penalty
        profile["mode_bonus"]["Local Train"] += 8
        profile["mode_bonus"]["Metro"]       += 8
        profile["low_crowd_penalty_pts"]     += 10   # stronger isolation penalty

        profile["applied_rules"].append(
            "Female safety profile: Auto/Cab penalised −10 extra pts, "
            "trains boosted +8 extra pts, isolated routes heavily penalised"
        )

    # ── RUNNING LATE ───────────────────────────────────────────────────────────
    elif user_mode == "late":
        profile["weight_crowding"]   = 0.10   # barely matters
        profile["weight_delay"]      = 0.50   # delay = top priority
        profile["weight_confidence"] = 0.40

        profile["speed_bonus_pts"]       = 12
        profile["speed_bonus_threshold"] = 25   # routes under 25 min get bonus

        profile["mode_bonus"]["Auto/Cab"] = +8   # fastest door-to-door
        profile["mode_bonus"]["Metro"]    = +5   # fast + no traffic

        profile["sort_by"] = "speed"
        profile["applied_rules"] = [
            "Delay weighted 50% — minimising wait time is top priority",
            "Crowding almost ignored (10% weight) — comfort sacrificed for speed",
            "Auto/Cab boosted +8 pts (fastest door-to-door option)",
            "Routes under 25 min get +12 pts bonus",
            "Routes sorted by travel time (fastest first)",
        ]

    return profile


def apply_safety_scoring(routes: list, user_mode: str, gender: str, hour: int) -> list:
    """
    Re-score all routes using the safety profile.
    Returns routes with updated trust_score and mode_notes, sorted correctly.

    No ML retraining needed — works entirely on existing predicted values.
    """
    if user_mode == "normal":
        return routes

    profile = get_safety_profile(user_mode, gender, hour)

    for route in routes:
        crowding    = route.get("crowding_pct", 50)
        delay       = route.get("delay_minutes", 5)
        confidence  = route.get("confidence_score", 0.7)
        travel_time = route.get("travel_time", 30)
        modes       = route.get("modes", [])
        primary_mode = modes[0] if modes else "Local Train"

        # Start from existing trust score
        base = route.get("trust_score", 70)
        delta = 0
        notes = []

        # 1. Mode bonus/penalty
        mode_delta = profile["mode_bonus"].get(primary_mode, 0)
        if mode_delta != 0:
            delta += mode_delta
            sign = "+" if mode_delta > 0 else ""
            notes.append(f"{primary_mode}: {sign}{mode_delta} pts (mode preference)")

        # 2. Crowding penalty
        if crowding > profile["crowding_penalty_threshold"] and profile["crowding_penalty_pts"] > 0:
            pen = -profile["crowding_penalty_pts"]
            delta += pen
            notes.append(f"High crowd ({crowding:.0f}%): {pen} pts")

        # 3. Low crowd penalty (isolated)
        if crowding < profile["low_crowd_penalty_threshold"] and profile["low_crowd_penalty_pts"] > 0:
            pen = -profile["low_crowd_penalty_pts"]
            delta += pen
            notes.append(f"Very low crowd ({crowding:.0f}%): {pen} pts (isolated)")

        # 4. Speed bonus
        if travel_time <= profile["speed_bonus_threshold"] and profile["speed_bonus_pts"] > 0:
            delta += profile["speed_bonus_pts"]
            notes.append(f"Fast route ({travel_time} min): +{profile['speed_bonus_pts']} pts")

        new_trust = max(0, min(100, base + delta))
        route["trust_score"]      = new_trust
        route["trust_delta"]      = delta
        route["mode_notes"]       = notes
        route["emotional_mode"]   = user_mode
        route["safety_profile"]   = profile["applied_rules"]

    # Sort
    if profile["sort_by"] == "speed":
        routes.sort(key=lambda r: r["travel_time"])
    else:
        routes.sort(key=lambda r: -r["trust_score"])

    return routes, profile