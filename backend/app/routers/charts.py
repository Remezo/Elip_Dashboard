import os
import csv
from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np

from app.database import engine
from app.models import SectorChartsResponse, ChartConfig, TraceData

router = APIRouter()

# Valid sector names (must match DataSummary.csv "Sector" column)
VALID_SECTORS = {
    "Signs of Excess",
    "Operating Fundamentals",
    "Yield Spreads",
    "Global Growth",
}


def _read_data_summary():
    """Read DataSummary.csv and return as list of dicts."""
    base_dir = os.environ.get(
        "APP_BASE_DIR",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )
    csv_path = os.path.join(base_dir, "input", "DataSummary.csv")
    rows = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def _safe_to_list(series):
    """Convert a pandas Series to a JSON-safe list (NaN → None)."""
    return [None if (v is None or (isinstance(v, float) and np.isnan(v))) else v for v in series.tolist()]


def _safe_dates(series):
    """Convert dates column to list of strings."""
    return [str(d) for d in series.tolist()]


@router.get("/charts/{sector}", response_model=SectorChartsResponse)
def get_sector_charts(sector: str):
    if sector not in VALID_SECTORS:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found. Valid sectors: {list(VALID_SECTORS)}",
        )

    # Read DataSummary.csv to get metrics for this sector
    all_rows = _read_data_summary()
    sector_rows = [r for r in all_rows if r["Sector"] == sector]

    if not sector_rows:
        raise HTTPException(status_code=404, detail=f"No data found for sector '{sector}'")

    # Load all needed dataframes from DB
    raw_frames = {}
    processed_frames = {}
    for freq in ["Daily", "Monthly", "Quarterly"]:
        try:
            raw_frames[freq] = (
                pd.read_sql(f'SELECT * FROM "raw_{freq}"', con=engine)
                .replace(".", 0)
            )
            if "Unnamed: 0" in raw_frames[freq].columns:
                raw_frames[freq] = raw_frames[freq].drop("Unnamed: 0", axis=1)
        except Exception:
            raw_frames[freq] = pd.DataFrame()

        try:
            processed_frames[freq] = pd.read_sql(f'SELECT * FROM "{freq}"', con=engine)
        except Exception:
            processed_frames[freq] = pd.DataFrame()

    charts = []
    for row in sector_rows:
        data_key = row["Data"]
        frequency = row["Frequency"]
        name = row["Name"]
        processing = row["Processing"] if row["Processing"] else None

        # Skip if USREC is the metric itself (it's used as overlay, not a standalone chart)
        if data_key == "USREC":
            continue

        raw_df = raw_frames.get(frequency, pd.DataFrame())
        proc_df = processed_frames.get(frequency, pd.DataFrame())

        if raw_df.empty or proc_df.empty:
            continue
        if data_key not in raw_df.columns or data_key not in proc_df.columns:
            continue
        if "Dates" not in raw_df.columns or "Dates" not in proc_df.columns:
            continue

        # Build raw trace
        raw_trace = TraceData(
            x=_safe_dates(raw_df["Dates"]),
            y=_safe_to_list(pd.to_numeric(raw_df[data_key], errors="coerce")),
        )

        # Build processed trace
        proc_values = pd.to_numeric(proc_df[data_key], errors="coerce")
        processed_trace = TraceData(
            x=_safe_dates(proc_df["Dates"]),
            y=_safe_to_list(proc_values),
        )

        # Build recession trace
        # Match Streamlit logic: uses USREC from the frequency-matched processed table
        # For Daily/Monthly frequency, recession comes from Monthly processed
        # For Quarterly, from Quarterly processed
        if frequency in ("Daily", "Monthly"):
            rec_df = processed_frames.get("Monthly", pd.DataFrame())
        else:
            rec_df = processed_frames.get("Quarterly", pd.DataFrame())

        if not rec_df.empty and "USREC" in rec_df.columns and "Dates" in rec_df.columns:
            usrec = pd.to_numeric(rec_df["USREC"], errors="coerce").fillna(0)
            # Recession bar height = USREC * max of processed data for this metric
            max_val = proc_values.max()
            if pd.isna(max_val) or max_val == 0:
                max_val = 1
            recession_y = usrec * max_val
            recession_trace = TraceData(
                x=_safe_dates(rec_df["Dates"]),
                y=_safe_to_list(recession_y),
            )
        else:
            recession_trace = TraceData(x=[], y=[])

        charts.append(
            ChartConfig(
                name=name,
                data_key=data_key,
                frequency=frequency,
                processing=processing,
                raw_trace=raw_trace,
                processed_trace=processed_trace,
                recession_trace=recession_trace,
            )
        )

    return SectorChartsResponse(sector=sector, charts=charts)
