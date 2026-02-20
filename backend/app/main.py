from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_table_row_counts
from app.models import HealthResponse
from app.routers import cpi, charts, download

app = FastAPI(
    title="Ascentris Research API",
    description="API for the Ascentris Research Dashboard",
    version="1.0.0",
    root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cpi.router)
app.include_router(charts.router)
app.include_router(download.router)


@app.get("/health", response_model=HealthResponse)
def health_check():
    counts = get_table_row_counts()
    return HealthResponse(status="ok", table_counts=counts)
