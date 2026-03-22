"""
cost_engine.py — Multi-modal commute cost calculator for Mumbai.
Uses realistic fare models for auto, cab, bus, and local train.
"""

# ── FARE RULES ────────────────────────────────────────────────────────────────

FARE_RULES = {
    "auto":  {"base": 30,  "per_km": 12,  "min": 30},
    "cab":   {"base": 50,  "per_km": 18,  "min": 50},
    "bus":   {"base": 0,   "per_km": 3,   "min": 10},
    "train": {"base": 0,   "per_km": 2,   "min": 5},
}

# Approximate speed (km/h) per mode — used to estimate time
MODE_SPEED = {
    "auto":  22,
    "cab":   28,
    "bus":   16,
    "train": 38,
}

MODE_LABELS = {
    "auto":  "Auto",
    "cab":   "Cab (Ola/Uber)",
    "bus":   "BEST Bus",
    "train": "Local Train",
}

MODE_ICONS = {
    "auto":  "🛺",
    "cab":   "🚕",
    "bus":   "🚌",
    "train": "🚆",
}

MODE_COLORS = {
    "auto":  "#f59e0b",
    "cab":   "#6366f1",
    "bus":   "#10b981",
    "train": "#8b5cf6",
}


# ── COST FUNCTIONS ────────────────────────────────────────────────────────────

def calculate_auto_cost(distance_km: float) -> float:
    r = FARE_RULES["auto"]
    return max(r["min"], r["base"] + r["per_km"] * distance_km)

def calculate_cab_cost(distance_km: float) -> float:
    r = FARE_RULES["cab"]
    return max(r["min"], r["base"] + r["per_km"] * distance_km)

def calculate_bus_cost(distance_km: float) -> float:
    r = FARE_RULES["bus"]
    return max(r["min"], r["per_km"] * distance_km)

def calculate_train_cost(distance_km: float) -> float:
    r = FARE_RULES["train"]
    return max(r["min"], r["per_km"] * distance_km)

COST_FN = {
    "auto":  calculate_auto_cost,
    "cab":   calculate_cab_cost,
    "bus":   calculate_bus_cost,
    "train": calculate_train_cost,
}

def calc_cost(mode: str, distance_km: float) -> int:
    return round(COST_FN[mode](distance_km))

def calc_time(mode: str, distance_km: float) -> int:
    """Estimate travel time in minutes."""
    speed = MODE_SPEED[mode]
    # Add wait/boarding time per mode
    wait = {"auto": 5, "cab": 4, "bus": 8, "train": 6}[mode]
    return round((distance_km / speed) * 60) + wait


# ── SINGLE-MODE OPTIONS ───────────────────────────────────────────────────────

def _single_option(mode: str, distance_km: float) -> dict:
    cost = calc_cost(mode, distance_km)
    time = calc_time(mode, distance_km)
    return {
        "id":    mode,
        "mode":  MODE_LABELS[mode],
        "icon":  MODE_ICONS[mode],
        "color": MODE_COLORS[mode],
        "segments": [{
            "type":     mode,
            "label":    MODE_LABELS[mode],
            "icon":     MODE_ICONS[mode],
            "distance": round(distance_km, 1),
            "cost":     cost,
            "time":     time,
            "color":    MODE_COLORS[mode],
        }],
        "total_cost": cost,
        "total_time": time,
        "transfers":  0,
        "labels":     [],
    }


# ── MULTI-MODAL OPTIONS ───────────────────────────────────────────────────────

def _dual_option(mode1: str, mode2: str, distance_km: float, split: float = 0.65) -> dict:
    """
    Split total distance into two segments (split% + (1-split)%).
    mode1 covers the longer first leg, mode2 the shorter last leg.
    """
    d1 = round(distance_km * split, 1)
    d2 = round(distance_km * (1 - split), 1)

    c1 = calc_cost(mode1, d1)
    c2 = calc_cost(mode2, d2)
    t1 = calc_time(mode1, d1)
    t2 = calc_time(mode2, d2)
    transfer_time = 5  # 5 min to change modes

    return {
        "id":    f"{mode1}+{mode2}",
        "mode":  f"{MODE_LABELS[mode1]} + {MODE_LABELS[mode2]}",
        "icon":  f"{MODE_ICONS[mode1]}{MODE_ICONS[mode2]}",
        "color": MODE_COLORS[mode1],
        "segments": [
            {
                "type":     mode1,
                "label":    MODE_LABELS[mode1],
                "icon":     MODE_ICONS[mode1],
                "distance": d1,
                "cost":     c1,
                "time":     t1,
                "color":    MODE_COLORS[mode1],
            },
            {
                "type":     mode2,
                "label":    MODE_LABELS[mode2],
                "icon":     MODE_ICONS[mode2],
                "distance": d2,
                "cost":     c2,
                "time":     t2,
                "color":    MODE_COLORS[mode2],
            },
        ],
        "total_cost": c1 + c2,
        "total_time": t1 + t2 + transfer_time,
        "transfers":  1,
        "labels":     [],
    }


# ── MAIN GENERATOR ────────────────────────────────────────────────────────────

def generate_cost_options(distance_km: float) -> list:
    """
    Generate all single and multi-modal cost options for a given distance.
    Returns list sorted by total_cost, with label badges assigned.
    """
    distance_km = max(1.0, distance_km)

    options = []

    # Single modes
    for mode in ["train", "bus", "auto", "cab"]:
        options.append(_single_option(mode, distance_km))

    # Dual combinations
    combos = [
        ("train", "train", 0.60),
        ("bus",   "bus",   0.55),
        ("bus",   "train", 0.50),
        ("train", "bus",   0.65),
        ("auto",  "train", 0.30),   # auto to station, then train
        ("auto",  "bus",   0.25),
        ("train", "auto",  0.70),   # train most of the way, auto last mile
        ("bus",   "auto",  0.65),
    ]
    for m1, m2, split in combos:
        options.append(_dual_option(m1, m2, distance_km, split))

    # ── ASSIGN LABELS ─────────────────────────────────────────────────────────
    cheapest = min(options, key=lambda o: o["total_cost"])
    fastest  = min(options, key=lambda o: o["total_time"])

    # Best value = lowest score of (normalised_cost * 0.5 + normalised_time * 0.5)
    max_cost = max(o["total_cost"] for o in options)
    max_time = max(o["total_time"] for o in options)
    for o in options:
        o["_score"] = (o["total_cost"] / max_cost) * 0.5 + (o["total_time"] / max_time) * 0.5
    best_value = min(options, key=lambda o: o["_score"])

    for o in options:
        o.pop("_score", None)
        o["labels"] = []

    cheapest["labels"].append("cheapest")
    fastest["labels"].append("fastest")
    if best_value["id"] not in (cheapest["id"], fastest["id"]):
        best_value["labels"].append("best_value")
    elif "best_value" not in cheapest["labels"] and "best_value" not in fastest["labels"]:
        best_value["labels"].append("best_value")

    # ── SAVINGS INSIGHT ───────────────────────────────────────────────────────
    cab_cost   = next(o["total_cost"] for o in options if o["id"] == "cab")
    train_cost = next(o["total_cost"] for o in options if o["id"] == "train")
    savings    = cab_cost - train_cost

    return {
        "options":  options,
        "cheapest": cheapest["id"],
        "fastest":  fastest["id"],
        "best_value": best_value["id"],
        "savings_insight": (
            f"💡 Taking local train instead of cab saves ₹{savings}"
            if savings > 0 else None
        ),
        "distance_km": round(distance_km, 1),
    }