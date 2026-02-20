from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class TraceData(BaseModel):
    x: List[str]
    y: List[Any]


class ChartConfig(BaseModel):
    name: str
    data_key: str
    frequency: str
    processing: Optional[str] = None
    raw_trace: TraceData
    processed_trace: TraceData
    recession_trace: TraceData


class SectorChartsResponse(BaseModel):
    sector: str
    charts: List[ChartConfig]


class CPIResponse(BaseModel):
    dates: List[str]
    categories: Dict[str, List[Any]]
    all_items: List[Any]


class HealthResponse(BaseModel):
    status: str
    table_counts: Dict[str, Optional[int]]
