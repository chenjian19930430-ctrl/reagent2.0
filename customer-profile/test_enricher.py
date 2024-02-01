"""Tests for profile enricher."""
import pytest
from .enricher import ProfileEnricher


def test_compute_segment_high_value():
    enricher = ProfileEnricher()
    segment = enricher._compute_segment({"engagement_score": 0.9})
    assert segment == "high_value"


def test_compute_engagement():
    enricher = ProfileEnricher()
    score = enricher._compute_engagement({"page_visits": 50, "click_count": 10, "purchase_count": 3})
    assert 0.0 <= score <= 1.0


def test_enrich_creates_computed_fields():
    enricher = ProfileEnricher()
    result = enricher.enrich("cust_001", {"page_visits": 100})
    assert "computed_segment" in result
    assert "engagement_score" in result
