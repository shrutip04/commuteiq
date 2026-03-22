"""
database.py — SQLite database with user profile (gender, safety preferences).
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "commuteiq.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # User preferences — extended with gender + safety profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            preference TEXT NOT NULL DEFAULT 'balanced',
            home_location TEXT DEFAULT '',
            work_location TEXT DEFAULT '',
            gender TEXT DEFAULT 'prefer_not_to_say',
            user_mode TEXT DEFAULT 'normal',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Add gender column if upgrading existing DB
    try:
        cursor.execute("ALTER TABLE user_preferences ADD COLUMN gender TEXT DEFAULT 'prefer_not_to_say'")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE user_preferences ADD COLUMN user_mode TEXT DEFAULT 'normal'")
    except Exception:
        pass

    # Emergency contacts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'personal',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized.")