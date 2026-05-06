"""Automation engine schemas."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ConditionOperator(str, Enum):
    """Supported comparison operators for rule conditions."""
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    GREATER_OR_EQ = "gte"
    LESS_THAN = "lt"
    LESS_OR_EQ = "lte"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"
    MATCHES = "matches"  # regex
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"


class ActionType(str, Enum):
    """Supported automation action types."""
    SEND_MESSAGE = "send_message"       # Send notification/message
    UPDATE_SEGMENT = "update_segment"   # Change user segment
    TRIGGER_CAMPAIGN = "trigger_campaign"  # Launch a campaign
    CALL_WEBHOOK = "call_webhook"       # External webhook
    ASSIGN_TAG = "assign_tag"           # Tag user
    UPDATE_PROFILE = "update_profile"   # Update profile field
    GENERATE_CONTENT = "generate_content"  # AI content generation


class TriggerType(str, Enum):
    """Trigger types for automation rules."""
    EVENT = "event"             # On specific event
    SCHEDULE = "schedule"       # Time-based (cron)
    SEGMENT_ENTER = "segment_enter"   # User enters a segment
    SEGMENT_EXIT = "segment_exit"     # User exits a segment
    PROFILE_CHANGE = "profile_change" # Profile field changes
    MANUAL = "manual"           # Manually triggered


class Condition(BaseModel):
    """A single condition in a rule."""
    field: str                          # Profile field / event field
    operator: ConditionOperator
    value: object
    field_source: str = "profile"         # 'profile' | 'event' | 'system'


class Action(BaseModel):
    """An action to execute when a rule triggers."""
    type: ActionType
    config: dict = Field(default_factory=dict)
    delay_minutes: int = 0               # Optional delay before execution
    cooldown_hours: int = 0              # Prevent re-execution


class AutomationRule(BaseModel):
    """A single automation rule."""
    id: str
    name: str
    description: str = ""
    enabled: bool = True
    trigger: TriggerType
    trigger_config: dict = Field(default_factory=dict)  # e.g. event_name, cron_expr
    conditions: list[Condition] = []     # All must match (AND logic)
    any_condition: list[Condition] = []  # Any can match (OR logic)
    actions: list[Action] = []
    priority: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class RuleExecution(BaseModel):
    """Record of a rule execution."""
    id: str
    rule_id: str
    user_id: str
    status: str = "pending"   # pending, running, completed, failed
    triggered_at: datetime
    completed_at: Optional[datetime] = None
    matched: bool = False
    actions_taken: list[str] = []
    error: Optional[str] = None
    context: dict = Field(default_factory=dict)


class AutomationEvent(BaseModel):
    """An event that can trigger automation rules."""
    event_type: str
    user_id: str
    payload: dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    source: str = "system"


class Campaign(BaseModel):
    """A marketing campaign composed of rules."""
    id: str
    name: str
    description: str = ""
    rules: list[AutomationRule] = []
    status: str = "draft"   # draft, active, paused, completed
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
