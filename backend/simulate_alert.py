"""
simulate_alert.py — Disruption simulation engine.
Modifies route parameters to simulate real-world incidents (accidents,
signal failures, congestion spikes) and triggers dynamic rerouting.
"""

import random
import copy
from datetime import datetime


DISRUPTION_TYPES = [
    {
        "type": "signal_failure",
        "label": "Signal Failure",
        "icon": "⚡",
        "crowding_delta": +20,
        "delay_delta": +12,
        "confidence_delta": -0.15,
        "message": "Signal failure detected on this line. Expect significant delays.",
    },
    {
        "type": "accident",
        "label": "Road Accident",
        "icon": "🚨",
        "crowding_delta": +15,
        "delay_delta": +18,
        "confidence_delta": -0.20,
        "message": "Accident reported ahead. Traffic is heavily congested.",
    },
    {
        "type": "congestion_spike",
        "label": "Congestion Spike",
        "icon": "🚗",
        "crowding_delta": +25,
        "delay_delta": +10,
        "confidence_delta": -0.10,
        "message": "Sudden congestion spike detected. Crowding levels very high.",
    },
    {
        "type": "service_disruption",
        "label": "Service Disruption",
        "icon": "🔧",
        "crowding_delta": +30,
        "delay_delta": +20,
        "confidence_delta": -0.25,
        "message": "Scheduled maintenance causing service disruptions on this route.",
    },
    {
        "type": "weather_event",
        "label": "Severe Weather",
        "icon": "⛈️",
        "crowding_delta": +10,
        "delay_delta": +15,
        "confidence_delta": -0.12,
        "message": "Adverse weather conditions slowing traffic across all routes.",
    },
]


def simulate_disruption(routes: list, disruption_type: str = None) -> dict:
    """
    Simulate a disruption on the current routes and return updated recommendations.

    Args:
        routes: List of current route dicts
        disruption_type: Optional specific disruption type key (random if None)

    Returns:
        dict with disruption info and updated routes
    """
    if not routes:
        return {"error": "No routes to simulate disruption on."}

    # Select disruption
    if disruption_type:
        disruption = next(
            (d for d in DISRUPTION_TYPES if d["type"] == disruption_type),
            random.choice(DISRUPTION_TYPES)
        )
    else:
        disruption = random.choice(DISRUPTION_TYPES)

    # Apply disruption to first route (primary route gets hit)
    updated_routes = copy.deepcopy(routes)

    # The worst-affected route (usually route 0 — the "recommended" one)
    affected_index = 0
    affected = updated_routes[affected_index]
    affected["crowding_pct"] = min(100, affected["crowding_pct"] + disruption["crowding_delta"])
    affected["delay_minutes"] = round(affected["delay_minutes"] + disruption["delay_delta"], 1)
    affected["confidence_score"] = max(0.1, affected["confidence_score"] + disruption["confidence_delta"])
    affected["travel_time"] = affected["travel_time"] + int(disruption["delay_delta"] * 0.8)
    affected["disrupted"] = True

    # Slightly affect other routes too (spillover)
    for i, route in enumerate(updated_routes):
        if i != affected_index:
            route["crowding_pct"] = min(100, route["crowding_pct"] + disruption["crowding_delta"] // 3)
            route["delay_minutes"] = round(route["delay_minutes"] + disruption["delay_delta"] // 4, 1)
            route["confidence_score"] = max(0.1, route["confidence_score"] - 0.05)
            route["disrupted"] = False

    # Re-rank routes by composite score
    def composite_score(r):
        return (
            r["travel_time"] * 0.4
            + r["crowding_pct"] * 0.3
            + r["delay_minutes"] * 0.2
            - r["confidence_score"] * 20
        )

    updated_routes.sort(key=composite_score)

    # Add reroute suggestion if severe
    reroute_suggestion = None
    if disruption["delay_delta"] >= 15:
        reroute_suggestion = {
            "available": True,
            "message": f"CommuteIQ has found an alternative route avoiding the {disruption['label'].lower()}.",
            "time_saved": random.randint(5, 15),
        }

    return {
        "disruption": {
            "type": disruption["type"],
            "label": disruption["label"],
            "icon": disruption["icon"],
            "message": disruption["message"],
            "severity": "HIGH" if disruption["delay_delta"] >= 15 else "MEDIUM",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        "updated_routes": updated_routes,
        "reroute_suggestion": reroute_suggestion,
    }
