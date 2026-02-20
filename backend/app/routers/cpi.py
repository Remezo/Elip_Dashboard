from fastapi import APIRouter
import pandas as pd
import numpy as np

from app.database import engine
from app.models import CPIResponse

router = APIRouter()


def _safe_to_list(series):
    """Convert a pandas Series to a JSON-safe list (NaN → None)."""
    return [None if (v is None or (isinstance(v, float) and np.isnan(v))) else v for v in series.tolist()]


@router.get("/cpi", response_model=CPIResponse)
def get_cpi_data():
    df = pd.read_sql('SELECT * FROM "CPIWeightedChange"', con=engine)

    # Dates column is "Unnamed: 0" in the CPIWeightedChange table
    dates = [str(d) for d in df["Unnamed: 0"].tolist()]

    # All items column (red line)
    all_items = _safe_to_list(pd.to_numeric(df["All items"], errors="coerce"))

    # Category columns (everything except "Unnamed: 0" and "All items")
    # The Streamlit code uses: categories = df.columns[2:-1]
    # But we'll be explicit: exclude "Unnamed: 0", "Unnamed: 0.1" (if exists), and "All items"
    exclude_cols = {"Unnamed: 0", "Unnamed: 0.1", "All items", "index"}
    category_cols = [c for c in df.columns if c not in exclude_cols]

    categories = {}
    for col in category_cols:
        categories[col] = _safe_to_list(pd.to_numeric(df[col], errors="coerce"))

    return CPIResponse(dates=dates, categories=categories, all_items=all_items)
