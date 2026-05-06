"""Marketing Automation Engine — 核心编排引擎。

将 RuleEvaluator、TriggerManager、ActionHandler 串联为统一引擎。
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from loguru import logger

from reagent.automation.schema import (
    AutomationRule,
    AutomationEvent,
    Action,
    RuleExecution,
    Campaign,
    TriggerType,
)
from reagent.automation.rules import RuleEvaluator
from reagent.automation.triggers import TriggerManager
from reagent.automation.actions import ActionHandler


class AutomationEngine:
    """Marketing automation engine — 核心编排器。

    Responsibilities:
    - Rule lifecycle management (deploy/update/remove)
    - Event dispatching and rule evaluation
    - Action execution with cooldown/delay
    - Execution audit trail
    """

    def __init__(self):
        self._evaluator = RuleEvaluator()
        self._trigger_mgr = TriggerManager(self._evaluator)
        self._action_handler = ActionHandler()
        self._rules: dict[str, AutomationRule] = {}
        self._campaigns: dict[str, Campaign] = {}
        self._executions: dict[str, RuleExecution] = {}
        self._cooldowns: dict[str, dict[str, datetime]] = {}  # rule_id -> {user_id: last_exec}

        # Wire trigger manager to execute actions on match
        self._trigger_mgr.on_match(self._on_rule_matched)

        logger.info("AutomationEngine initialized")

    # ── Rule Lifecycle ──

    def deploy_rule(self, rule: AutomationRule) -> str:
        """Deploy a new automation rule."""
        errors = self._evaluator.validate_rule(rule)
        if errors:
            raise ValueError(f"Rule validation failed: {'; '.join(errors)}")

        self._rules[rule.id] = rule
        self._trigger_mgr.register_rule(rule)
        logger.info(f"Rule deployed: {rule.name} ({rule.id})")
        return rule.id

    def update_rule(self, rule: AutomationRule) -> None:
        """Update an existing rule."""
        if rule.id not in self._rules:
            raise ValueError(f"Rule {rule.id} not found")
        self._trigger_mgr.unregister_rule(rule.id)
        self._rules[rule.id] = rule
        self._trigger_mgr.register_rule(rule)
        logger.info(f"Rule updated: {rule.name}")

    def remove_rule(self, rule_id: str) -> None:
        """Remove a rule."""
        self._trigger_mgr.unregister_rule(rule_id)
        self._rules.pop(rule_id, None)
        logger.info(f"Rule removed: {rule_id}")

    def get_rule(self, rule_id: str) -> Optional[AutomationRule]:
        return self._rules.get(rule_id)

    def list_rules(self) -> list[AutomationRule]:
        return list(self._rules.values())

    # ── Campaign Lifecycle ──

    def create_campaign(self, campaign: Campaign) -> str:
        self._campaigns[campaign.id] = campaign
        for rule in campaign.rules:
            self.deploy_rule(rule)
        logger.info(f"Campaign created: {campaign.name} ({campaign.id})")
        return campaign.id

    def activate_campaign(self, campaign_id: str) -> None:
        if campaign := self._campaigns.get(campaign_id):
            campaign.status = "active"
            logger.info(f"Campaign activated: {campaign.name}")

    def pause_campaign(self, campaign_id: str) -> None:
        if campaign := self._campaigns.get(campaign_id):
            campaign.status = "paused"
            logger.info(f"Campaign paused: {campaign.name}")

    # ── Event Processing ──

    async def process_event(self, event: AutomationEvent, profile: dict) -> list[dict]:
        """Process an automation event.

        Returns results from matched rule actions.
        """
        logger.info(f"Processing event: {event.event_type} for {event.user_id}")
        return await self._trigger_mgr.dispatch_event(event, profile)

    async def _on_rule_matched(self, rule: AutomationRule, profile: dict, event: Optional[AutomationEvent]) -> list[str]:
        """Callback when a rule matches — execute actions."""
        user_id = profile.get("user_id", event.user_id if event else "unknown")

        # Check cooldown
        if self._in_cooldown(rule.id, user_id):
            logger.info(f"Rule {rule.id} in cooldown for user {user_id}, skipping")
            return []

        # Execute actions
        context = {
            "profile": profile,
            "event": event.model_dump() if event else None,
        }

        action_results = await self._action_handler.execute_batch(
            rule.actions, user_id, context
        )

        # Record execution
        execution = RuleExecution(
            id=f"exec_{uuid.uuid4().hex[:8]}",
            rule_id=rule.id,
            user_id=user_id,
            status="completed",
            triggered_at=datetime.now(),
            matched=True,
            actions_taken=action_results,
        )
        self._executions[execution.id] = execution

        # Update cooldown
        cooldown_hours = max((a.cooldown_hours for a in rule.actions), default=0)
        if cooldown_hours > 0:
            self._update_cooldown(rule.id, user_id, cooldown_hours)

        return action_results

    def _in_cooldown(self, rule_id: str, user_id: str) -> bool:
        """Check if a rule+user is in cooldown."""
        if rule_id not in self._cooldowns:
            return False
        if user_id not in self._cooldowns[rule_id]:
            return False
        return datetime.now() < self._cooldowns[rule_id][user_id]

    def _update_cooldown(self, rule_id: str, user_id: str, hours: int) -> None:
        from datetime import timedelta
        if rule_id not in self._cooldowns:
            self._cooldowns[rule_id] = {}
        self._cooldowns[rule_id][user_id] = datetime.now() + timedelta(hours=hours)

    # ── Auditing ──

    def get_executions(self, limit: int = 50) -> list[RuleExecution]:
        execs = list(self._executions.values())
        execs.sort(key=lambda x: x.triggered_at, reverse=True)
        return execs[:limit]

    def get_execution(self, execution_id: str) -> Optional[RuleExecution]:
        return self._executions.get(execution_id)


# Global singleton
engine = AutomationEngine()
