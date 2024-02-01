"""Workflow models."""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class TriggerType(str, Enum):
    EVENT = "event"
    SCHEDULE = "schedule"
    SEGMENT = "segment_change"


class ActionType(str, Enum):
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"
    UPDATE_SEGMENT = "update_segment"
    WEBHOOK = "webhook"
    DELAY = "delay"


class WorkflowNode(BaseModel):
    id: str
    type: str
    config: dict = {}
    next_nodes: list[str] = []


class Workflow(BaseModel):
    id: str
    name: str
    description: str = ""
    status: WorkflowStatus = WorkflowStatus.DRAFT
    trigger: TriggerType
    trigger_config: dict = {}
    nodes: List[WorkflowNode] = []
    created_at: datetime
    updated_at: datetime
    created_by: str = "system"


class WorkflowExecution(BaseModel):
    id: str
    workflow_id: str
    customer_id: str
    current_node: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
