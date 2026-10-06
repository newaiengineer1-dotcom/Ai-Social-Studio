import sqlite3
from pathlib import Path
import json

DB_PATH = Path("social_studio.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    con = get_connection()
    con.execute("""CREATE TABLE IF NOT EXISTS campaigns(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT, website TEXT, topic TEXT, payload TEXT, result TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    con.execute("""CREATE TABLE IF NOT EXISTS calendar(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT, title TEXT, scheduled_at TEXT, status TEXT)""")
    con.commit()
    con.close()

def save_campaign(payload, result):
    con = get_connection()
    con.execute("INSERT INTO campaigns(company,website,topic,payload,result) VALUES (?,?,?,?,?)",
                (payload.get("company",""), payload.get("website",""), payload.get("topic",""),
                 json.dumps(payload), json.dumps(result)))
    con.commit()
    con.close()
