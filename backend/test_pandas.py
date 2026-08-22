import sys
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.db.database import query_as_dataframe, query_as_dicts
from app.core.config import SQLITE_DB_PATH

print("DB Path:", SQLITE_DB_PATH)

try:
    df = query_as_dataframe(
        "SELECT state as State, district as District, market as Market, commodity as Commodity, variety as Variety, arrival_date as Arrival_Date, min_price as Min_Price, max_price as Max_Price, modal_price as Modal_Price FROM mandi_prices"
    )
    print("Mandi prices df shape:", df.shape)
except Exception as e:
    print("Error querying mandi_prices:", e)

try:
    db_rows = query_as_dicts("SELECT * FROM government_schemes")
    print("Schemes length:", len(db_rows))
except Exception as e:
    print("Error querying government_schemes:", e)
