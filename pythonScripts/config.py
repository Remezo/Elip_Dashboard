import datetime
import os

# BLS API Key - from environment variable
API_KEY = os.environ.get("BLS_API_KEY", "e04cd03600d84bcf8d7ca6e6028bb076")

# FRED API Key - from environment variable
FRED_API_KEY = os.environ.get("FRED_API_KEY", "387a905393cc2ed7a711a24149359f52")

END_YEAR = datetime.date.today().year
START_YEAR = END_YEAR - 9

# Base paths - use environment variable or default
BASE_DIR = os.environ.get("APP_BASE_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

CPI_ItemCodes = os.path.join(INPUT_FOLDER, "CPIitemCodes.csv")
Data_summary = os.path.join(INPUT_FOLDER, "DataSummary.csv")

# Database connection
def get_db_connection_string():
    user = os.environ.get("POSTGRES_USER", "ascentris")
    password = os.environ.get("POSTGRES_PASSWORD", "Ascentris2023")
    host = os.environ.get("POSTGRES_HOST", "postgres")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "ascentris_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
