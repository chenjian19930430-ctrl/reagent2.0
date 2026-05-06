"""Rule definitions — 规则定义与条件评估引擎。"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from loguru import logger

from reagent.automation.schema import (
    Condition,
    ConditionOperator,
    AutomationRule,
    TriggerType,
)


class RuleEvaluator:
    """Evaluates automation rule conditions against user data.

    Supports:
    - AND logic (all conditions must match)
    - OR logic (any condition can match)
    - Field sources: profile, event, system
    - Multiple comparison operators
    """

    def __init__(self):
        logger.info("RuleEvaluator initialized")

    def evaluate_rule(self, rule: AutomationRule, profile: dict, event: dict | None = None) -> bool:
        """Evaluate all conditions in a rule.

        Returns:
            True if the rule conditions are satisfied.
        """
        # Evaluate AND conditions (all must match)
        if rule.conditions:
            if not self._evaluate_all(rule.conditions, profile, event):
                return False

        # Evaluate OR conditions (any can match)
        if rule.any_condition:
            if rule.any_condition and not self._evaluate_any(rule.any_condition, profile, event):
                return False

        # No conditions = always matches
        return True

    def _evaluate_all(self, conditions: list[Condition], profile: dict, event: dict | None = None) -> bool:
        """All conditions must match (AND)."""
        return all(self._evaluate_single(c, profile, event) for c in conditions)

    def _evaluate_any(self, conditions: list[Condition], profile: dict, event: dict | None = None) -> bool:
        """Any condition can match (OR)."""
        return any(self._evaluate_single(c, profile, event) for c in conditions)

    def _evaluate_single(self, condition: Condition, profile: dict, event: dict | None = None) -> bool:
        """Evaluate a single condition."""
        # Get actual value from data source
        actual = self._resolve_field(condition.field, condition.field_source, profile, event)

        if condition.operator in (ConditionOperator.EXISTS,):
            return actual is not None
        if condition.operator in (ConditionOperator.NOT_EXISTS,):
            return actual is None

        if actual is None:
            return False

        expected = condition.value
        op = condition.operator

        try:
            if op == ConditionOperator.EQUALS:
                return actual == expected
            elif op == ConditionOperator.NOT_EQUALS:
                return actual != expected
            elif op == ConditionOperator.GREATER_THAN:
                return float(actual) > float(expected)
            elif op == ConditionOperator.GREATER_OR_EQ:
                return float(actual) >= float(expected)
            elif op == ConditionOperator.LESS_THAN:
                return float(actual) < float(expected)
            elif op == ConditionOperator.LESS_OR_EQ:
                return float(actual) <= float(expected)
            elif op == ConditionOperator.CONTAINS:
                return str(expected) in str(actual)
            elif op == ConditionOperator.NOT_CONTAINS:
                return str(expected) not in str(actual)
            elif op == ConditionOperator.IN:
                return actual in (expected if isinstance(expected, list) else [expected])
            elif op == ConditionOperator.NOT_IN:
                return actual not in (expected if isinstance(expected, list) else [expected])
            elif op == ConditionOperator.MATCHES:
                return bool(re.match(str(expected), str(actual)))
        except (ValueError, TypeError) as e:
            logger.warning(f"Condition evaluation error: {e}")
            return False

        return False

    def _resolve_field(self, field: str, source: str, profile: dict, event: dict | None = None) -> Any:
        """Resolve a field value from profile or event data."""
        if source == "profile" and field in profile:
            return profile.get(field)

        if source == "event" and event:
            # Supports dot notation: payload.amount
            parts = field.split(".")
            data = event
            for part in parts:
                if isinstance(data, dict):
                    data = data.get(part)
                else:
                    return None
            return data

        if source == "system":
            if field == "now":
                return datetime.now()
            if field == "today":
                return datetime.now().strftime("%Y-%m-%d")

        return None

    def validate_rule(self, rule: AutomationRule) -> list[str]:
        """Validate a rule definition, returning list of errors."""
        errors = []

        if not rule.name.strip():
            errors.append("Rule name is required")

        if not rule.conditions and not rule.any_condition:
            errors.append("At least one condition is required")

        if not rule.actions:
            errors.append("At least one action is required")

        if rule.trigger == TriggerType.SCHEDULE and "cron" not in rule.trigger_config:
            errors.append("Schedule trigger requires 'cron' in trigger_config")

        return errors
