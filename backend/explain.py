"""
explain.py — Context-aware AI explanation that understands safety mode penalties.
"""

import random


def _crowding_label(pct):
    return "low" if pct < 35 else ("moderate" if pct < 65 else "high")

def _delay_label(minutes):
    return "minimal" if minutes < 3 else ("mild" if minutes < 8 else "significant")

def _trust_label(score):
    return "excellent" if score >= 75 else ("good" if score >= 60 else ("poor" if score >= 40 else "very poor"))

def _risk_label(pct):
    return "low" if pct < 30 else ("moderate" if pct < 60 else "high")


def generate_explanation(route: dict, alternatives: list) -> dict:
    """
    Generate AI explanation bullets that are consistent with trust score,
    safety mode penalties, and risk forecast.
    """
    crowding      = route.get("crowding_pct", 50)
    delay         = route.get("delay_minutes", 5)
    confidence    = route.get("confidence_score", 0.7)
    trust         = route.get("trust_score", 70)
    travel_time   = route.get("travel_time", 30)
    modes         = route.get("modes", ["Transit"])
    primary_mode  = modes[0] if modes else "Transit"
    risk          = route.get("risk", {})
    current_pct   = risk.get("current_pct", 30)
    future_pct    = risk.get("future_pct", 30)
    trend         = risk.get("trend", "stable")
    user_mode     = route.get("emotional_mode", "normal")
    mode_notes    = route.get("mode_notes", [])
    trust_delta   = route.get("trust_delta", 0)

    best_alt = min(alternatives, key=lambda x: x["travel_time"]) if alternatives else None
    time_diff = (best_alt["travel_time"] - travel_time) if best_alt else 0

    bullets = []

    # ── BULLET 1: Performance (speed/crowding) ────────────────────────────────
    crowding_word = _crowding_label(crowding)
    delay_word    = _delay_label(delay)

    if time_diff > 5:
        perf = f"Fastest option — {abs(time_diff)} min quicker than alternatives, with {delay_word} delays ({delay:.0f} min) and {crowding_word} crowding ({crowding:.0f}%)."
    elif time_diff > 0:
        perf = f"Slightly faster by {abs(time_diff)} min. Crowding is {crowding_word} at {crowding:.0f}% with {delay_word} delays."
    elif time_diff < -5:
        perf = f"Slower than alternatives by {abs(time_diff)} min, but offers {crowding_word} crowding ({crowding:.0f}%) and {delay_word} delays."
    else:
        perf = f"Similar travel time to alternatives. Crowding is {crowding_word} at {crowding:.0f}% with {delay_word} delays."

    bullets.append(perf)

    # ── BULLET 2: Trust score — explain WHY it is what it is ──────────────────
    trust_word = _trust_label(trust)

    if user_mode != "normal" and trust_delta != 0 and mode_notes:
        # Safety mode changed the score — explain this clearly
        direction = "penalised" if trust_delta < 0 else "boosted"
        delta_abs = abs(trust_delta)

        if primary_mode == "Auto/Cab" and user_mode == "alone_night":
            trust_bullet = (
                f"Trust score {trust}/100 ({trust_word}): Auto/Cab was penalised "
                f"−{delta_abs} pts by your 'Alone at Night' safety mode — "
                f"it's fast but less safe when travelling alone at night. "
                f"Consider the train option for better safety."
            )
        elif primary_mode == "Auto/Cab" and user_mode == "anxious":
            trust_bullet = (
                f"Trust score {trust}/100 ({trust_word}): Auto/Cab was penalised "
                f"−{delta_abs} pts in Anxious mode — less predictable than trains. "
                f"The train route scores higher for peace of mind."
            )
        elif trust_delta < 0 and crowding > 60:
            trust_bullet = (
                f"Trust score {trust}/100 ({trust_word}): Penalised {delta_abs} pts "
                f"due to high crowding ({crowding:.0f}%) in your current safety mode. "
                f"A less crowded route may suit you better right now."
            )
        elif trust_delta > 0:
            trust_bullet = (
                f"Trust score {trust}/100 ({trust_word}): Boosted +{delta_abs} pts "
                f"by your safety mode — {primary_mode} is preferred for your current context."
            )
        else:
            trust_bullet = (
                f"Trust score {trust}/100 ({trust_word}): Your safety mode "
                f"({user_mode.replace('_', ' ')}) adjusted this score by {trust_delta:+d} pts "
                f"based on mode and crowding."
            )
    elif trust >= 75:
        trust_bullet = (
            f"Trust score {trust}/100 ({trust_word}): High confidence ({int(confidence*100)}%) "
            f"with consistent historical performance on this route."
        )
    elif trust >= 50:
        trust_bullet = (
            f"Trust score {trust}/100 ({trust_word}): Moderate reliability — "
            f"some variability due to {'crowding' if crowding > 50 else 'occasional delays'}. "
            f"Allow a small buffer."
        )
    else:
        trust_bullet = (
            f"Trust score {trust}/100 ({trust_word}): Lower reliability right now. "
            f"{'High crowding' if crowding > 60 else 'Delays'} and "
            f"{'safety mode penalties ' if trust_delta < 0 else ''}are reducing confidence. "
            f"Consider a higher-trust alternative."
        )

    bullets.append(trust_bullet)

    # ── BULLET 3: Risk outlook ─────────────────────────────────────────────────
    risk_word = _risk_label(current_pct)

    if trend == "up" and future_pct - current_pct > 10:
        risk_bullet = (
            f"⚠️ Risk rising: currently {current_pct}% → predicted {future_pct}% in ~15 min. "
            f"Conditions are getting worse — leaving sooner is advisable."
        )
    elif trend == "down" and current_pct - future_pct > 10:
        risk_bullet = (
            f"✅ Improving conditions: risk dropping {current_pct}% → {future_pct}% in ~15 min. "
            f"Waiting a few minutes could mean a smoother journey."
        )
    elif current_pct < 30:
        risk_bullet = (
            f"✅ Low risk ({current_pct}%) — conditions are good right now. "
            f"Stable for the next 15 min."
        )
    elif current_pct > 60:
        risk_bullet = (
            f"🔴 High risk zone ({current_pct}%). "
            f"{'Expected to ease to ' + str(future_pct) + '% shortly.' if future_pct < current_pct else 'No relief expected in next 15 min — plan accordingly.'}"
        )
    else:
        risk_bullet = (
            f"🟡 Moderate risk ({current_pct}%), stable at ~{future_pct}% in 15 min. "
            f"No major changes expected."
        )

    bullets.append(risk_bullet)

    # Summary — one clean sentence
    if trust < 50 and user_mode != "normal":
        summary = (
            f"This route is fast but your safety mode has flagged it as lower trust. "
            f"Check the alternatives for a safer option."
        )
    elif trust >= 70:
        summary = f"Reliable route with {trust_word} trust and {risk_word} risk right now."
    else:
        summary = f"Usable route — trust is {trust_word} ({trust}/100). Consider the safety notes above."

    return {
        "bullets": bullets,
        "summary": summary,
        "trust_score": trust,
        "risk": risk,
    }