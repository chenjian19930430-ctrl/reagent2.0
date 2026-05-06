"""Marketing automation API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from reagent.automation.schema import (
    AutomationRule,
    AutomationEvent,
    RuleExecution,
    Campaign,
    ActionType,
    TriggerType,
)
from reagent.automation.engine import engine

router = APIRouter(prefix="/api/v1/automation", tags=["automation"])


# ── Rule Endpoints ──


@router.post("/rules", response_model=dict)
async def create_rule(rule: AutomationRule):
    """Create and deploy a new automation rule."""
    try:
        rule_id = engine.deploy_rule(rule)
        return {"id": rule_id, "status": "deployed"}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules", response_model=list[AutomationRule])
async def list_rules():
    """List all deployed automation rules."""
    return engine.list_rules()


@router.get("/rules/{rule_id}", response_model=AutomationRule)
async def get_rule(rule_id: str):
    """Get a specific automation rule."""
    rule = engine.get_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.put("/rules/{rule_id}", response_model=dict)
async def update_rule(rule_id: str, rule: AutomationRule):
    """Update an existing rule."""
    rule.id = rule_id
    try:
        engine.update_rule(rule)
        return {"status": "updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/rules/{rule_id}", response_model=dict)
async def delete_rule(rule_id: str):
    """Remove an automation rule."""
    engine.remove_rule(rule_id)
    return {"status": "removed"}


# ── Campaign Endpoints ──


@router.post("/campaigns", response_model=dict)
async def create_campaign(campaign: Campaign):
    """Create a new campaign with rules."""
    campaign_id = engine.create_campaign(campaign)
    return {"id": campaign_id, "status": "created"}


@router.post("/campaigns/{campaign_id}/activate", response_model=dict)
async def activate_campaign(campaign_id: str):
    """Activate a campaign."""
    engine.activate_campaign(campaign_id)
    return {"status": "activated"}


@router.post("/campaigns/{campaign_id}/pause", response_model=dict)
async def pause_campaign(campaign_id: str):
    """Pause a campaign."""
    engine.pause_campaign(campaign_id)
    return {"status": "paused"}


# ── Event Processing ──


@router.post("/events/process", response_model=dict)
async def process_event(event: AutomationEvent, profile: dict = {}):
    """Process an automation event."""
    results = await engine.process_event(event, profile)
    return {"event_id": f"evt_{event.event_type}", "matched_rules": len(results), "results": results}


# ── Audit / Monitoring ──


@router.get("/executions", response_model=list[RuleExecution])
async def list_executions(limit: int = 50):
    """Get recent rule execution records."""
    return engine.get_executions(limit=limit)


@router.get("/executions/{execution_id}", response_model=RuleExecution)
async def get_execution(execution_id: str):
    """Get a specific execution record."""
    execution = engine.get_execution(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution
