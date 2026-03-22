"""
ml_engine.py — ML model for predicting route crowding and delay probabilities.
Uses a RandomForest trained on synthetic data. Falls back to rule-based logic
if the model file is unavailable.
"""

import os
import pickle
import random
import numpy as np

try:
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("[ML] scikit-learn not available. Using rule-based fallback.")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "route_model.pkl")


def _generate_synthetic_data(n_samples: int = 2000) -> "pd.DataFrame":
    """Generate synthetic commute training data."""
    random.seed(42)
    np.random.seed(42)

    hours = np.random.choice(range(6, 23), n_samples)
    is_peak = ((hours >= 8) & (hours <= 10)) | ((hours >= 17) & (hours <= 19))

    data = {
        "hour": hours,
        "is_peak": is_peak.astype(int),
        "distance_km": np.random.uniform(2, 30, n_samples),
        "num_stops": np.random.randint(1, 15, n_samples),
        "transport_mode": np.random.choice([0, 1, 2, 3], n_samples),  # bus/metro/walk/bike
        "weather_score": np.random.uniform(0, 1, n_samples),
        "day_of_week": np.random.randint(0, 7, n_samples),
        # Targets
        "crowding_pct": np.clip(
            40 * is_peak.astype(float)
            + np.random.normal(30, 15, n_samples)
            + 5 * (np.random.randint(0, 4, n_samples) == 0),
            0, 100
        ),
        "delay_minutes": np.clip(
            8 * is_peak.astype(float)
            + np.random.exponential(3, n_samples)
            + 2 * (np.random.uniform(0, 1, n_samples) < 0.3).astype(float),
            0, 45
        ),
    }
    return pd.DataFrame(data)


def train_and_save_model():
    """Train the RandomForest model and save to disk."""
    if not ML_AVAILABLE:
        return False
    print("[ML] Training model on synthetic data…")
    df = _generate_synthetic_data()

    features = ["hour", "is_peak", "distance_km", "num_stops",
                 "transport_mode", "weather_score", "day_of_week"]
    X = df[features]

    models = {}
    for target in ["crowding_pct", "delay_minutes"]:
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print(f"[ML] {target} R²: {score:.3f}")
        models[target] = model

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(models, f)
    print(f"[ML] Model saved to {MODEL_PATH}")
    return True


def _load_models():
    """Load models from disk, training if necessary."""
    if not os.path.exists(MODEL_PATH):
        success = train_and_save_model()
        if not success:
            return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def _rule_based_predict(features: dict) -> dict:
    """Fallback rule-based prediction when ML is unavailable."""
    hour = features.get("hour", 12)
    is_peak = 1 if (8 <= hour <= 10 or 17 <= hour <= 19) else 0
    distance = features.get("distance_km", 10)

    crowding = 30 + 35 * is_peak + random.gauss(0, 10)
    delay = 2 + 8 * is_peak + distance * 0.3 + random.gauss(0, 2)

    return {
        "crowding_pct": round(max(0, min(100, crowding)), 1),
        "delay_minutes": round(max(0, delay), 1),
    }


def predict_route(features: dict) -> dict:
    """
    Predict crowding and delay for a route.

    Args:
        features: dict with keys:
            hour, is_peak, distance_km, num_stops,
            transport_mode (0=bus,1=metro,2=walk,3=bike),
            weather_score (0-1), day_of_week (0=Mon)

    Returns:
        dict with crowding_pct and delay_minutes
    """
    if not ML_AVAILABLE:
        return _rule_based_predict(features)

    try:
        models = _load_models()
        if models is None:
            return _rule_based_predict(features)

        feature_order = ["hour", "is_peak", "distance_km", "num_stops",
                         "transport_mode", "weather_score", "day_of_week"]
        X = np.array([[features.get(f, 0) for f in feature_order]])

        crowding = float(models["crowding_pct"].predict(X)[0])
        delay = float(models["delay_minutes"].predict(X)[0])

        return {
            "crowding_pct": round(max(0, min(100, crowding)), 1),
            "delay_minutes": round(max(0, delay), 1),
        }
    except Exception as e:
        print(f"[ML] Prediction error: {e}. Using fallback.")
        return _rule_based_predict(features)


# Train model on import if not already saved
if ML_AVAILABLE and not os.path.exists(MODEL_PATH):
    train_and_save_model()


# ── TRUST SCORE ───────────────────────────────────────────────────────────────

def compute_trust_score(route: dict) -> int:
    """
    Compute a 0-100 trust score for a route based on:
    confidence, crowding, delay, and time of day.
    """
    confidence  = route.get("confidence_score", 0.7)
    crowding    = route.get("crowding_pct", 50) / 100
    delay       = min(route.get("delay_minutes", 5) / 30, 1.0)
    hour        = route.get("_hour", 12)

    # Time-of-day penalty: night (22-5) and rush hour
    if 22 <= hour or hour <= 5:
        time_penalty = 0.85
    elif (8 <= hour <= 10) or (17 <= hour <= 19):
        time_penalty = 0.90
    else:
        time_penalty = 1.0

    raw = (0.4 * confidence + 0.35 * (1 - crowding) + 0.25 * (1 - delay)) * time_penalty
    return max(0, min(100, int(raw * 100)))


# ── FUTURE RISK PREDICTION ────────────────────────────────────────────────────

def predict_future_risk(features: dict) -> dict:
    """
    Predict current and future (next ~15-20 min) risk score for a route.
    Simulates how conditions might change based on time progression.
    Returns dict with current_risk and future_risk (both 0-1).
    """
    # Current risk from existing model
    current_pred = predict_route(features)
    current_crowding = current_pred["crowding_pct"] / 100
    current_delay    = min(current_pred["delay_minutes"] / 30, 1.0)
    current_risk     = round((current_crowding * 0.5 + current_delay * 0.5), 3)

    # Simulate future conditions (+1 hour)
    future_features = features.copy()
    future_hour = (features.get("hour", 12) + 1) % 24
    future_features["hour"] = future_hour

    # Peak transition logic
    is_current_peak = (8 <= features.get("hour", 12) <= 10) or (17 <= features.get("hour", 12) <= 19)
    is_future_peak  = (8 <= future_hour <= 10) or (17 <= future_hour <= 19)

    if is_future_peak and not is_current_peak:
        # Heading INTO peak — risk increases
        future_features["weather_score"] = features.get("weather_score", 0.7) * 0.8
    elif not is_future_peak and is_current_peak:
        # Leaving peak — risk decreases
        future_features["weather_score"] = min(1.0, features.get("weather_score", 0.7) * 1.1)

    future_features["is_peak"] = int(is_future_peak)

    future_pred    = predict_route(future_features)
    future_crowding = future_pred["crowding_pct"] / 100
    future_delay    = min(future_pred["delay_minutes"] / 30, 1.0)
    future_risk     = round((future_crowding * 0.5 + future_delay * 0.5), 3)

    trend = "up" if future_risk > current_risk + 0.05 else ("down" if future_risk < current_risk - 0.05 else "stable")

    return {
        "current_risk":  current_risk,
        "future_risk":   future_risk,
        "current_pct":   int(current_risk * 100),
        "future_pct":    int(future_risk * 100),
        "trend":         trend,
    }