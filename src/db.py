# src/db.py

import sqlite3
from datetime import datetime
from pathlib import Path
from src.config import DB_PATH

Path('./data').mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    approved INTEGER DEFAULT 0,
    requested_at TIMESTAMP
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    ts TIMESTAMP
)
''')

conn.commit()

def add_or_update_request(user_id, username):
    cur.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
    if cur.fetchone():
        cur.execute('UPDATE users SET username=?, requested_at=? WHERE user_id=?',
                    (username, datetime.utcnow(), user_id))
    else:
        cur.execute('INSERT INTO users (user_id, username, requested_at) VALUES (?,?,?)',
                    (user_id, username, datetime.utcnow()))
    conn.commit()

def approve_user(user_id):
    cur.execute('UPDATE users SET approved=1 WHERE user_id=?', (user_id,))
    conn.commit()

def deny_user(user_id):
    cur.execute('DELETE FROM users WHERE user_id=?', (user_id,))
    conn.commit()

def is_approved(user_id):
    cur.execute('SELECT approved FROM users WHERE user_id=?', (user_id,))
    r = cur.fetchone()
    return bool(r and r[0] == 1)

def list_pending():
    cur.execute('SELECT user_id, username, requested_at FROM users WHERE approved=0')
    return cur.fetchall()

def log_action(user_id, action):
    cur.execute('INSERT INTO logs (user_id, action, ts) VALUES (?,?,?)',
                (user_id, action, datetime.utcnow()))
    conn.commit()
