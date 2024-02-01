"""Report generation."""
from datetime import datetime, date, timedelta
from typing import Optional
from .metrics import MetricsEngine


class ReportGenerator:
    """Generates automated marketing reports."""
    
    def __init__(self, engine: Optional[MetricsEngine] = None):
        self.engine = engine or MetricsEngine()
    
    def generate_weekly_report(self, end_date: Optional[date] = None) -> dict:
        end = end_date or date.today()
        start = end - timedelta(days=7)
        return {
            "type": "weekly",
            "period": f"{start.isoformat()} - {end.isoformat()}",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": self.engine.compute_summary(start, end),
        }
    
    def generate_monthly_report(self, year: int, month: int) -> dict:
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)
        end -= timedelta(days=1)
        return {
            "type": "monthly",
            "period": f"{start.isoformat()} - {end.isoformat()}",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": self.engine.compute_summary(start, end),
        }
