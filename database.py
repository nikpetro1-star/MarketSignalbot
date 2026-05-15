import sqlite3
import time

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    start_time INTEGER
)
""")
conn.commit()


def add_user(user_id):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (user_id, start_time) VALUES (?, ?)",
            (user_id, int(time.time()))
        )
        conn.commit()


def get_expired(hours):
    cutoff = int(time.time()) - hours * 3600
    cur.execute("SELECT user_id FROM users WHERE start_time < ?", (cutoff,))
    return cur.fetchall()
