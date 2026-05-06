"""Trigger system — 事件与定时触发器。"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta
from typing import Callable, Optional

from loguru import logger

from reagent.automation.schema import (
    TriggerType,
    AutomationEvent,
    AutomationRule,
)
from reagent.automation.rules import RuleEvaluator


class TriggerManager:
    """Manages event and schedule-based triggers.

    Handles:
    - Event subscription and dispatching
    - Schedule/cron-based triggers
    - Segment entry/exit detection
    """

    def __init__(self, rule_evaluator: RuleEvaluator):
        self._evaluator = rule_evaluator
        self._event_handlers: dict[str, list[AutomationRule]] = {}
        self._scheduled_tasks: dict[str, asyncio.Task] = {}
        self._on_match_callback: Optional[Callable] = None
        logger.info("TriggerManager initialized")

    def on_match(self, callback: Callable) -> None:
        """Register callback for when a rule matches."""
        self._on_match_callback = callback

    def register_rule(self, rule: AutomationRule) -> None:
        """Register a rule with its trigger."""
        if rule.trigger == TriggerType.EVENT:
            event_name = rule.trigger_config.get("event_name", "")
            if event_name:
                if event_name not in self._event_handlers:
                    self._event_handlers[event_name] = []
                self._event_handlers[event_name].append(rule)
                logger.info(f"Rule '{rule.name}' registered for event: {event_name}")

        elif rule.trigger == TriggerType.SCHEDULE:
            # Schedule-based rules are managed externally (via cron)
            logger.info(f"Rule '{rule.name}' registered for schedule: {rule.trigger_config}")

    def unregister_rule(self, rule_id: str) -> None:
        """Remove a rule from all triggers."""
        for event_name in list(self._event_handlers.keys()):
            self._event_handlers[event_name] = [
                r for r in self._event_handlers[event_name] if r.id != rule_id
            ]
            if not self._event_handlers[event_name]:
                del self._event_handlers[event_name]

    async def dispatch_event(self, event: AutomationEvent, profile: dict) -> list[dict]:
        """Dispatch an event and evaluate matching rules.

        Returns:
            List of action results.
        """
        logger.info(f"Dispatching event: {event.event_type} for user {event.user_id}")
        results = []

        rules = self._event_handlers.get(event.event_type, [])
        for rule in rules:
            if not rule.enabled:
                continue

            matched = self._evaluator.evaluate_rule(rule, profile, event.model_dump())
            if matched and self._on_match_callback:
                logger.info(f"Rule '{rule.name}' matched for event '{event.event_type}'")
                action_results = await self._on_match_callback(rule, profile, event)
                results.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "matched": True,
                    "actions": action_results,
                })

        return results

    async def check_scheduled_rules(self, rules: list[AutomationRule]) -> list[dict]:
        """Check schedule-based rules against current time."""
        results = []
        now = datetime.now()

        for rule in rules:
            if not rule.enabled or rule.trigger != TriggerType.SCHEDULE:
                continue

            # Simple schedule check: evaluate conditions on system time
            profile = {"_last_check": now.isoformat()}
            matched = self._evaluator.evaluate_rule(rule, profile)
            if matched and self._on_match_callback:
                action_results = await self._on_match_callback(rule, profile, None)
                results.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "matched": True,
                    "actions": action_results,
                })

        return results
