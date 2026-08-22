import os
from app.core.config import SQLITE_DB_PATH, DATA_PROCESSED

print("CWD:", os.getcwd())
print("SQLITE_DB_PATH:", SQLITE_DB_PATH)
print("Exists:", os.path.exists(SQLITE_DB_PATH))

from app.services.scheme_service import scheme_service
print("Schemes length:", len(scheme_service.schemes_raw))

from app.services.market_service import market_service
print("Market DF shape:", market_service.df.shape)
