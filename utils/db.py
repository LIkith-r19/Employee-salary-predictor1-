from pathlib import Path
import sqlite3
import pandas as pd
import json
import time

DB_PATH = Path(__file__).resolve().parents[1] / "salary_history.db"

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER,
            education TEXT,
            experience INTEGER,
            role TEXT,
            department TEXT,
            location TEXT,
            predicted_salary REAL,
            model_r2 REAL
        )"""
    )
    conn.commit()
    conn.close()

def insert_record(education, experience, role, department, location, predicted_salary, model_r2):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO history (ts, education, experience, role, department, location, predicted_salary, model_r2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (int(time.time()), education, experience, role, department, location, float(predicted_salary), float(model_r2))
    )
    conn.commit()
    conn.close()

def fetch_history(limit=None):
    conn = _get_conn()
    query = "SELECT * FROM history ORDER BY ts DESC"
    if limit is not None:
        query += f" LIMIT {int(limit)}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        df["ts"] = pd.to_datetime(df["ts"], unit="s")
    return df

def clear_history():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM history")
    conn.commit()
    conn.close()
