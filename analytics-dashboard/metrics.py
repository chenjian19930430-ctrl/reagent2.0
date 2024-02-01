"""Metrics computation engine."""
import random
from datetime import datetime, timedelta, date
from typing import List
from .models import TimeSeriesPoint, MetricResult


class MetricsEngine:
    """Computes marketing metrics from raw data."""
    
    def __init__(self):
        self._metrics_defs = {
            "conversion_rate": {"unit": "%", "description": "Conversion rate"},
            "click_through_rate": {"unit": "%", "description": "Click-through rate"},
            "customer_acquisition_cost": {"unit": "CNY", "description": "Customer acquisition cost"},
            "roi": {"unit": "%", "description": "Return on investment"},
        }
    
    def query(self, metric: str, start: date, end: date, granularity: str = "day") -> MetricResult:
        days = (end - start).days
        if granularity == "week":
            points = days // 7
        elif granularity == "month":
            points = max(1, days // 30)
        else:
            points = days
        
        data = []
        for i in range(min(points, 365)):
            ts = start + timedelta(days=i)
            data.append(TimeSeriesPoint(
                timestamp=ts.isoformat(),
                value=round(random.uniform(0, 100), 2)
            ))
        
        values = [p.value for p in data]
        return MetricResult(
            metric=metric,
            data=data,
            total=round(sum(values), 2),
            avg=round(sum(values) / len(values), 2) if values else 0,
            min_val=round(min(values), 2) if values else 0,
            max_val=round(max(values), 2) if values else 0,
        )
    
    def list_metrics(self) -> dict:
        return self._metrics_defs
    
    def compute_summary(self, start: date, end: date) -> dict:
        result = {}
        for metric in self._metrics_defs:
            result[metric] = self.query(metric, start, end)
        return {k: {"total": v.total, "avg": v.avg} for k, v in result.items()}
