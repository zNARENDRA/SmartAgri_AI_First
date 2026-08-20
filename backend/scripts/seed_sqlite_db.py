import os
import sys
import json
import sqlite3
import pandas as pd

# Ensure backend root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.config import DATA_PROCESSED, SQLITE_DB_PATH
from app.db.database import init_tables

import datetime

def save_raw_file_to_db(conn, cursor, file_path, dataset_name):
    if not os.path.exists(file_path):
        return
    filename = os.path.basename(file_path)
    file_type = "CSV" if filename.endswith(".csv") else "JSON"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.strip().split("\n")
    rec_count = max(0, len(lines) - 1) if filename.endswith(".csv") else len(lines)
    
    cursor.execute("""
    INSERT OR REPLACE INTO raw_csv_files (filename, dataset_name, file_type, csv_content, record_count, ingested_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (filename, dataset_name, file_type, content, rec_count, datetime.datetime.now().isoformat()))
    conn.commit()

def seed_database():
    print(f"[*] Initializing SQLite Database at: {SQLITE_DB_PATH}")
    os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(SQLITE_DB_PATH)
    init_tables(conn)
    cursor = conn.cursor()
    
    # 1. Crop Recommendations
    crop_rec_path = os.path.join(DATA_PROCESSED, "crop_recommendation_cleaned.csv")
    if os.path.exists(crop_rec_path):
        print(" -> Ingesting crop_recommendation_cleaned.csv...")
        df_crop = pd.read_csv(crop_rec_path)
        cursor.execute("DELETE FROM crop_recommendations;")
        cursor.execute("DELETE FROM raw_crop_recommendations;")
        df_crop.to_sql("crop_recommendations", conn, if_exists="append", index=False)
        df_crop.to_sql("raw_crop_recommendations", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, crop_rec_path, "Dataset 1: Crop Recommendation")
        print(f"    [OK] {len(df_crop)} crop recommendation records inserted.")

    # 2. Crop Yields
    crop_yield_path = os.path.join(DATA_PROCESSED, "crop_yield_cleaned.csv")
    if os.path.exists(crop_yield_path):
        print(" -> Ingesting crop_yield_cleaned.csv...")
        df_yield = pd.read_csv(crop_yield_path)
        col_map = {
            "Crop": "crop",
            "Crop_Year": "crop_year",
            "Season": "season",
            "State": "state",
            "Area": "area",
            "Production": "production",
            "Annual_Rainfall": "annual_rainfall",
            "Fertilizer": "fertilizer",
            "Pesticide": "pesticide",
            "Yield": "yield"
        }
        df_yield_renamed = df_yield.rename(columns=col_map)
        cursor.execute("DELETE FROM crop_yields;")
        cursor.execute("DELETE FROM raw_crop_yields;")
        df_yield_renamed.to_sql("crop_yields", conn, if_exists="append", index=False)
        df_yield_renamed.to_sql("raw_crop_yields", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, crop_yield_path, "Dataset 3: Crop Yield")
        print(f"    [OK] {len(df_yield)} crop yield records inserted.")

    # 3. Mandi Prices
    mandi_prices_path = os.path.join(DATA_PROCESSED, "mandi_prices_cleaned.csv")
    if os.path.exists(mandi_prices_path):
        print(" -> Ingesting mandi_prices_cleaned.csv...")
        df_mandi = pd.read_csv(mandi_prices_path)
        col_map = {
            "State": "state",
            "District": "district",
            "Market": "market",
            "Commodity": "commodity",
            "Variety": "variety",
            "Arrival_Date": "arrival_date",
            "Min_Price": "min_price",
            "Max_Price": "max_price",
            "Modal_Price": "modal_price"
        }
        df_mandi_renamed = df_mandi.rename(columns=col_map)
        cursor.execute("DELETE FROM mandi_prices;")
        cursor.execute("DELETE FROM raw_mandi_prices;")
        df_mandi_renamed.to_sql("mandi_prices", conn, if_exists="append", index=False)
        df_mandi_renamed.to_sql("raw_mandi_prices", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, mandi_prices_path, "Dataset 4: Mandi Commodity Prices")
        print(f"    [OK] {len(df_mandi)} mandi price records inserted.")

    # 4. Mandi Analytics Metadata
    analytics_path = os.path.join(DATA_PROCESSED, "mandi_analytics.json")
    if os.path.exists(analytics_path):
        print(" -> Ingesting mandi_analytics.json...")
        with open(analytics_path, "r", encoding="utf-8") as f:
            analytics_data = json.load(f)
        cursor.execute("DELETE FROM mandi_analytics;")
        cursor.execute(
            "INSERT INTO mandi_analytics (key, data_json) VALUES (?, ?);",
            ("main_analytics", json.dumps(analytics_data))
        )
        save_raw_file_to_db(conn, cursor, analytics_path, "Dataset 4: Mandi Analytics Metadata")
        print("    [OK] Mandi analytics metadata inserted.")

    # 5. Government Schemes
    schemes_path = os.path.join(DATA_PROCESSED, "government_schemes_cleaned.json")
    if os.path.exists(schemes_path):
        print(" -> Ingesting government_schemes_cleaned.json...")
        with open(schemes_path, "r", encoding="utf-8") as f:
            schemes = json.load(f)
        cursor.execute("DELETE FROM government_schemes;")
        scheme_rows = []
        for s in schemes:
            scheme_rows.append((
                s.get("id"),
                s.get("scheme_name", ""),
                s.get("short_name", ""),
                s.get("category", ""),
                s.get("sponsoring_agency", ""),
                s.get("level", "Central"),
                s.get("description", ""),
                s.get("benefits", ""),
                json.dumps(s.get("eligibility_criteria", {})),
                s.get("target_beneficiaries", ""),
                json.dumps(s.get("documents_required", [])),
                s.get("application_process", ""),
                s.get("official_url", ""),
                s.get("myscheme_url", ""),
                s.get("helpdesk_contact", "")
            ))
        cursor.executemany("""
        INSERT INTO government_schemes (
            id, scheme_name, short_name, category, sponsoring_agency, level, description,
            benefits, eligibility_criteria_json, target_beneficiaries,
            documents_required_json, application_process, official_url, myscheme_url, helpdesk_contact
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, scheme_rows)
        save_raw_file_to_db(conn, cursor, schemes_path, "Dataset 5: Government Schemes")
        print(f"    [OK] {len(schemes)} government scheme records inserted.")

    # 6. Disease Remedies
    remedies_path = os.path.join(DATA_PROCESSED, "disease_remedies.json")
    if os.path.exists(remedies_path):
        print(" -> Ingesting disease_remedies.json...")
        with open(remedies_path, "r", encoding="utf-8") as f:
            remedies = json.load(f)
        cursor.execute("DELETE FROM disease_remedies;")
        remedy_rows = []
        for cls_id, rem in remedies.items():
            remedy_rows.append((
                cls_id,
                rem.get("crop", cls_id.split("___")[0]),
                rem.get("condition", cls_id.split("___")[-1]),
                rem.get("status", "Healthy" if "healthy" in cls_id.lower() else "Diseased"),
                rem.get("severity", "None" if "healthy" in cls_id.lower() else "Moderate"),
                rem.get("pathogen", "N/A"),
                rem.get("symptoms", ""),
                rem.get("immediate_action", ""),
                rem.get("organic_treatment", ""),
                rem.get("chemical_treatment", ""),
                rem.get("prevention", "")
            ))
        cursor.executemany("""
        INSERT INTO disease_remedies (
            class_id, crop, condition, status, severity, pathogen, symptoms,
            immediate_action, organic_treatment, chemical_treatment, prevention
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, remedy_rows)
        save_raw_file_to_db(conn, cursor, remedies_path, "Dataset 2: Disease Remedies")
        print(f"    [OK] {len(remedies)} plant disease remedy records inserted.")

    # 7. Historical Yield + Weather (Dataset 6)
    hyw_path = os.path.join(DATA_PROCESSED, "historical_yield_weather_cleaned.csv")
    if os.path.exists(hyw_path):
        print(" -> Ingesting historical_yield_weather_cleaned.csv...")
        df_hyw = pd.read_csv(hyw_path)
        cursor.execute("DELETE FROM historical_yield_weather;")
        cursor.execute("DELETE FROM raw_historical_yield_weather;")
        df_hyw.to_sql("historical_yield_weather", conn, if_exists="append", index=False)
        df_hyw.to_sql("raw_historical_yield_weather", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, hyw_path, "Dataset 6: Historical Yield Weather")
        print(f"    [OK] {len(df_hyw)} historical yield-weather records inserted.")

    # 8. Crop Yield + Soil + Weather (Dataset 7)
    cysw_path = os.path.join(DATA_PROCESSED, "crop_yield_soil_weather_cleaned.csv")
    if os.path.exists(cysw_path):
        print(" -> Ingesting crop_yield_soil_weather_cleaned.csv...")
        df_cysw = pd.read_csv(cysw_path)
        cursor.execute("DELETE FROM crop_yield_soil_weather;")
        cursor.execute("DELETE FROM raw_crop_yield_soil_weather;")
        df_cysw.to_sql("crop_yield_soil_weather", conn, if_exists="append", index=False)
        df_cysw.to_sql("raw_crop_yield_soil_weather", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, cysw_path, "Dataset 7: Crop Yield Soil Weather")
        print(f"    [OK] {len(df_cysw)} crop yield-soil-weather records inserted.")

    # 9. GoI District Crop Production (Dataset 8)
    dcp_path = os.path.join(DATA_PROCESSED, "district_crop_production_cleaned.csv")
    if os.path.exists(dcp_path):
        print(" -> Ingesting district_crop_production_cleaned.csv...")
        df_dcp = pd.read_csv(dcp_path)
        cursor.execute("DELETE FROM district_crop_production;")
        cursor.execute("DELETE FROM raw_district_crop_production;")
        df_dcp.to_sql("district_crop_production", conn, if_exists="append", index=False)
        df_dcp.to_sql("raw_district_crop_production", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, dcp_path, "Dataset 8: GoI District Crop Production")
        print(f"    [OK] {len(df_dcp)} district crop production records inserted.")

    # 10. GoI IMD Rainfall Baseline & Anomalies (Dataset 9)
    imd_path = os.path.join(DATA_PROCESSED, "imd_rainfall_cleaned.csv")
    if os.path.exists(imd_path):
        print(" -> Ingesting imd_rainfall_cleaned.csv...")
        df_imd = pd.read_csv(imd_path)
        cursor.execute("DELETE FROM imd_rainfall;")
        cursor.execute("DELETE FROM raw_imd_rainfall;")
        df_imd.to_sql("imd_rainfall", conn, if_exists="append", index=False)
        df_imd.to_sql("raw_imd_rainfall", conn, if_exists="append", index=False)
        save_raw_file_to_db(conn, cursor, imd_path, "Dataset 9: GoI IMD Rainfall Baseline")
        print(f"    [OK] {len(df_imd)} IMD rainfall baseline records inserted.")

    # 11. Pest & Insect Remedies (Dataset 10)
    pest_path = os.path.join(DATA_PROCESSED, "pest_remedies_cleaned.json")
    if os.path.exists(pest_path):
        print(" -> Ingesting pest_remedies_cleaned.json...")
        with open(pest_path, "r", encoding="utf-8") as f:
            pests = json.load(f)
        cursor.execute("DELETE FROM pest_remedies;")
        pest_rows = []
        for p in pests:
            pest_rows.append((
                p.get("pest_id"),
                p.get("crop", ""),
                p.get("pest_name", ""),
                p.get("damage_pattern", ""),
                p.get("organic_control", ""),
                p.get("chemical_control", ""),
                p.get("prevention", "")
            ))
        cursor.executemany("""
        INSERT INTO pest_remedies (
            pest_id, crop, pest_name, damage_pattern, organic_control, chemical_control, prevention
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, pest_rows)
        save_raw_file_to_db(conn, cursor, pest_path, "Dataset 10: Pest Remedies")
        print(f"    [OK] {len(pests)} pest & insect remedy records inserted.")

    # 12. ICAR Weather-Based Crop Advisories (Dataset 11 RAG)
    icar_path = os.path.join(DATA_PROCESSED, "icar_advisories_cleaned.json")
    if os.path.exists(icar_path):
        print(" -> Ingesting icar_advisories_cleaned.json...")
        with open(icar_path, "r", encoding="utf-8") as f:
            advisories = json.load(f)
        cursor.execute("DELETE FROM icar_advisories;")
        icar_rows = []
        for a in advisories:
            icar_rows.append((
                a.get("id"),
                a.get("crop", ""),
                a.get("state", ""),
                a.get("season", ""),
                a.get("weather_trigger", ""),
                a.get("advisory_text", ""),
                a.get("source_org", "")
            ))
        cursor.executemany("""
        INSERT INTO icar_advisories (
            id, crop, state, season, weather_trigger, advisory_text, source_org
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, icar_rows)
        save_raw_file_to_db(conn, cursor, icar_path, "Dataset 11: ICAR Advisories")
        print(f"    [OK] {len(advisories)} ICAR Weather-Based Crop Advisories inserted.")

    conn.commit()
    conn.close()
    
    # Remove processed and raw CSV & JSON dataset files since they are now safely stored in SQLite database
    cleanup_files = [
        os.path.join(DATA_PROCESSED, "crop_recommendation_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "crop_yield_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "mandi_prices_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "disease_classes.json"),
        os.path.join(DATA_PROCESSED, "disease_remedies.json"),
        os.path.join(DATA_PROCESSED, "government_schemes_cleaned.json"),
        os.path.join(DATA_PROCESSED, "mandi_analytics.json"),
        os.path.join(DATA_PROCESSED, "historical_yield_weather_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "crop_yield_soil_weather_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "district_crop_production_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "imd_rainfall_cleaned.csv"),
        os.path.join(DATA_PROCESSED, "pest_remedies_cleaned.json"),
        os.path.join(DATA_PROCESSED, "icar_advisories_cleaned.json"),
    ]
    removed_count = 0
    for file_path in cleanup_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                removed_count += 1
            except Exception as e:
                print(f"[!] Warning removing {os.path.basename(file_path)}: {e}")
                
    if removed_count > 0:
        print(f" -> Removed {removed_count} redundant raw/processed CSV & JSON dataset files from disk.")

    print("\n[SUCCESS] SQLite database seeding completed successfully!\n")

if __name__ == "__main__":
    seed_database()
