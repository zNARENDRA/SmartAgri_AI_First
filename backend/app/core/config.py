import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_RAW = os.path.join(DATA_DIR, "raw")
DATA_PROCESSED = os.path.join(DATA_DIR, "processed")
DATA_SAMPLES = os.path.join(DATA_DIR, "samples")
MODELS_DIR = os.path.join(BASE_DIR, "models")
SQLITE_DB_PATH = os.path.join(DATA_DIR, "krishi_kalyan.db")

PROJECT_NAME = "KrishiKalyan AI"
VERSION = "1.0.0"
API_V1_STR = "/api"

# Default fallback coordinates (e.g. Pune / Central Maharashtra)
DEFAULT_LAT = 18.5204
DEFAULT_LON = 73.8567
DEFAULT_LOCATION = "Pune, Maharashtra"
