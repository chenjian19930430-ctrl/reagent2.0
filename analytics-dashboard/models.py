"""Analytics models."""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MetricQuery(BaseModel):
    start_date: date
    end_date: date
    metric: str
    granularity: str = "day"
    filters: dict = {}


class TimeSeriesPoint(BaseModel):
    timestamp: str
    value: float


class MetricResult(BaseModel):
    metric: str
    data: List[TimeSeriesPoint]
    total: float
    avg: float
    min_val: float
    max_val: float


class DashboardWidget(BaseModel):
    id: str
    title: str
    type: str
    config: dict = {}
    position: dict = {}


class DashboardConfig(BaseModel):
    id: str
    name: str
    widgets: List[DashboardWidget]
    created_at: datetime
    updated_at: datetime
