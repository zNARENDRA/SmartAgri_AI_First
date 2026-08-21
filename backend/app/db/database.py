import sqlite3
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from contextlib import contextmanager
from app.core.config import SQLITE_DB_PATH

@contextmanager
def get_db_connection(db_path: str = SQLITE_DB_PATH):
    """
    Context manager for SQLite database connection.
    Sets row_factory to sqlite3.Row for dict-like row access.
    """
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def query_as_dicts(query: str, params: Tuple = (), db_path: str = SQLITE_DB_PATH) -> List[Dict[str, Any]]:
    """
    Executes a SELECT query and returns the results as a list of dictionaries.
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def query_as_dataframe(query: str, params: Tuple = (), db_path: str = SQLITE_DB_PATH) -> pd.DataFrame:
    """
    Executes a SELECT query and returns a pandas DataFrame.
    """
    with get_db_connection(db_path) as conn:
        return pd.read_sql_query(query, conn, params=params)

def execute_statement(statement: str, params: Tuple = (), db_path: str = SQLITE_DB_PATH) -> int:
    """
    Executes an INSERT/UPDATE/DELETE statement and commits changes.
    Returns affected row count.
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(statement, params)
        conn.commit()
        return cursor.rowcount

def init_tables(conn: sqlite3.Connection):
    """
    Initializes SQLite tables and indexes for SmartAgri AI datasets.
    """
    cursor = conn.cursor()
    
    # 1. Crop Recommendations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        N INTEGER NOT NULL,
        P INTEGER NOT NULL,
        K INTEGER NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        ph REAL NOT NULL,
        rainfall REAL NOT NULL,
        label TEXT NOT NULL
    );
    """)

    # 2. Crop Yields
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_yields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        crop_year INTEGER,
        season TEXT,
        state TEXT,
        area REAL,
        production REAL,
        annual_rainfall REAL,
        fertilizer REAL,
        pesticide REAL,
        yield REAL
    );
    """)

    # 3. Mandi Wholesale Prices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mandi_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        market TEXT NOT NULL,
        commodity TEXT NOT NULL,
        variety TEXT,
        arrival_date TEXT NOT NULL,
        min_price INTEGER NOT NULL,
        max_price INTEGER NOT NULL,
        modal_price INTEGER NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mandi_state_commodity ON mandi_prices (state, commodity);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mandi_market ON mandi_prices (market);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mandi_arrival_date ON mandi_prices (arrival_date);")

    # 4. Mandi Analytics Metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mandi_analytics (
        key TEXT PRIMARY KEY,
        data_json TEXT NOT NULL
    );
    """)

    # 5. Government Schemes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS government_schemes (
        id TEXT PRIMARY KEY,
        scheme_name TEXT NOT NULL,
        short_name TEXT,
        category TEXT NOT NULL,
        sponsoring_agency TEXT,
        level TEXT,
        description TEXT,
        benefits TEXT,
        eligibility_criteria_json TEXT,
        target_beneficiaries TEXT,
        documents_required_json TEXT,
        application_process TEXT,
        official_url TEXT,
        myscheme_url TEXT,
        helpdesk_contact TEXT
    );
    """)

    # 6. Disease Remedies & Classes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_remedies (
        class_id TEXT PRIMARY KEY,
        crop TEXT NOT NULL,
        condition TEXT NOT NULL,
        status TEXT NOT NULL,
        severity TEXT,
        pathogen TEXT,
        symptoms TEXT,
        immediate_action TEXT,
        organic_treatment TEXT,
        chemical_treatment TEXT,
        prevention TEXT
    );
    """)

    # 7. Historical Yield + Weather (Dataset 6)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_yield_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        crop_year INTEGER NOT NULL,
        season TEXT NOT NULL,
        area REAL NOT NULL,
        production REAL NOT NULL,
        yield REAL NOT NULL,
        temperature REAL,
        humidity REAL,
        rainfall REAL,
        wind_speed REAL,
        solar_radiation REAL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hyw_crop_state ON historical_yield_weather (crop, state);")

    # 8. Crop Yield + Soil + Weather (Dataset 7)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_yield_soil_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        state TEXT NOT NULL,
        N INTEGER NOT NULL,
        P INTEGER NOT NULL,
        K INTEGER NOT NULL,
        ph REAL NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        rainfall REAL NOT NULL,
        yield REAL NOT NULL
    );
    """)

    # 9. GoI District Crop Production (Dataset 8)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS district_crop_production (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        crop TEXT NOT NULL,
        season TEXT NOT NULL,
        crop_year INTEGER NOT NULL,
        area REAL NOT NULL,
        production REAL NOT NULL,
        yield_ha REAL NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dcp_state_dist_crop ON district_crop_production (state, district, crop);")

    # 10. GoI IMD Rainfall Baseline & Anomalies (Dataset 9)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS imd_rainfall (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subdivision TEXT NOT NULL,
        state TEXT NOT NULL,
        month TEXT NOT NULL,
        season TEXT NOT NULL,
        normal_mm REAL NOT NULL,
        actual_mm REAL NOT NULL,
        departure_pct REAL NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_imd_state_sub ON imd_rainfall (state, subdivision);")

    # 11. Pest & Insect Remedies (Dataset 10)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pest_remedies (
        pest_id TEXT PRIMARY KEY,
        crop TEXT NOT NULL,
        pest_name TEXT NOT NULL,
        damage_pattern TEXT,
        organic_control TEXT,
        chemical_control TEXT,
        prevention TEXT
    );
    """)

    # 12. ICAR Weather-Based Crop Advisories (Dataset 11 RAG)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS icar_advisories (
        id TEXT PRIMARY KEY,
        crop TEXT NOT NULL,
        state TEXT NOT NULL,
        season TEXT NOT NULL,
        weather_trigger TEXT NOT NULL,
        advisory_text TEXT NOT NULL,
        source_org TEXT NOT NULL
    );
    """)

    # 13. Central Raw CSV Files Storage Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_csv_files (
        filename TEXT PRIMARY KEY,
        dataset_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        csv_content TEXT NOT NULL,
        record_count INTEGER NOT NULL,
        ingested_at TEXT NOT NULL
    );
    """)

    # 14. Raw Datasets Replica Tables
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_crop_recommendations AS SELECT * FROM crop_recommendations WHERE 1=0;")
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_crop_yields AS SELECT * FROM crop_yields WHERE 1=0;")
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_mandi_prices AS SELECT * FROM mandi_prices WHERE 1=0;")
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_historical_yield_weather AS SELECT * FROM historical_yield_weather WHERE 1=0;")
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_crop_yield_soil_weather AS SELECT * FROM crop_yield_soil_weather WHERE 1=0;")
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_district_crop_production AS SELECT * FROM district_crop_production WHERE 1=0;")
    cursor.execute("CREATE TABLE IF NOT EXISTS raw_imd_rainfall AS SELECT * FROM imd_rainfall WHERE 1=0;")

    conn.commit()
