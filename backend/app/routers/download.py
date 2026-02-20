from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import pandas as pd

from app.database import engine

router = APIRouter()


@router.get("/download/excel")
def download_excel():
    """Generate and return the same Excel file as the Streamlit download page."""
    cpi_df = pd.read_sql('SELECT * FROM "CPIWeightedChange"', con=engine)
    daily_df = pd.read_sql('SELECT * FROM "Daily"', con=engine)
    monthly_df = pd.read_sql('SELECT * FROM "Monthly"', con=engine)
    quarterly_df = pd.read_sql('SELECT * FROM "Quarterly"', con=engine)

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        cpi_df.to_excel(writer, index=False, sheet_name="CPI_weighted")
        daily_df.to_excel(writer, index=False, sheet_name="Daily")
        monthly_df.to_excel(writer, index=False, sheet_name="Monthly")
        quarterly_df.to_excel(writer, index=False, sheet_name="Quarterly")

    excel_buffer.seek(0)

    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=scraped_data.xlsx"},
    )
