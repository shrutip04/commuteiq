"""
auth.py — Authentication helpers: password hashing, JWT token generation & validation
"""

import bcrypt
import jwt
import datetime
import os

SECRET_KEY = os.environ.get("JWT_SECRET", "commuteiq-super-secret-2024")
TOKEN_EXPIRY_HOURS = 24


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against the stored hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def generate_token(user_id: int, username: str) -> str:
    """Generate a JWT token for the given user."""
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRY_HOURS),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token: str) -> dict | None:
    """Decode and validate a JWT token. Returns payload or None on failure."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
