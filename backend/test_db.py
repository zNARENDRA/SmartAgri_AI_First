import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "data", "smartagri.db")
print(f"DB Path: {db_path}, Exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    for t in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
        print(f"Table {t[0]}: {count} rows")
    
    print("\nSample from mandi_prices:")
    rows = cursor.execute("SELECT * FROM mandi_prices LIMIT 1;").fetchall()
    print(rows)
