"""Analytics dashboard API."""
from datetime import date
from fastapi import APIRouter, Query
from .models import MetricResult, DashboardConfig, DashboardWidget
from .metrics import MetricsEngine
from .reports import ReportGenerator

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
engine = MetricsEngine()
reporter = ReportGenerator()


@router.get("/metrics/{metric_name}", response_model=MetricResult)
async def get_metric(
    metric_name: str,
    start: str = Query(...),
    end: str = Query(...),
    granularity: str = "day"
):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    return engine.query(metric_name, start_date, end_date, granularity)


@router.get("/metrics", response_model=dict)
async def list_metrics():
    return engine.list_metrics()


@router.get("/reports/weekly", response_model=dict)
async def weekly_report():
    return reporter.generate_weekly_report()


@router.get("/reports/monthly", response_model=dict)
async def monthly_report(year: int, month: int):
    return reporter.generate_monthly_report(year, month)
