"""Tests for Marketing Automation Engine."""

import pytest
from datetime import datetime
from reagent.automation.schema import (
    AutomationRule, AutomationEvent, Action, Condition, Campaign,
    ActionType, TriggerType, ConditionOperator,
)
from reagent.automation.rules import RuleEvaluator
from reagent.automation.engine import AutomationEngine


class TestAutomationSchemas:
    """Test automation schema models."""

    def test_condition(self):
        c = Condition(field="total_spent", operator=ConditionOperator.GREATER_THAN, value=100)
        assert c.field == "total_spent"
        assert c.operator == ConditionOperator.GREATER_THAN
        assert c.value == 100

    def test_action(self):
        a = Action(type=ActionType.SEND_MESSAGE, config={"channel": "email"})
        assert a.type == ActionType.SEND_MESSAGE
        assert a.config["channel"] == "email"

    def test_automation_rule(self):
        rule = AutomationRule(
            id="rule_1",
            name="高价值用户欢迎",
            trigger=TriggerType.EVENT,
            trigger_config={"event_name": "user.created"},
            conditions=[Condition(field="plan", operator=ConditionOperator.EQUALS, value="premium")],
            actions=[Action(type=ActionType.SEND_MESSAGE, config={})],
        )
        assert rule.id == "rule_1"
        assert rule.trigger == TriggerType.EVENT
        assert len(rule.conditions) == 1
        assert len(rule.actions) == 1

    def test_automation_event(self):
        event = AutomationEvent(
            event_type="purchase.completed",
            user_id="u_123",
            payload={"amount": 199, "product": "VIP套餐"},
        )
        assert event.event_type == "purchase.completed"
        assert event.payload["amount"] == 199

    def test_campaign(self):
        campaign = Campaign(
            id="camp_1",
            name="复活老用户",
            rules=[],
            status="draft",
        )
        assert campaign.id == "camp_1"
        assert campaign.status == "draft"


class TestRuleEvaluator:
    """Test rule condition evaluation."""

    def setup_method(self):
        self.evaluator = RuleEvaluator()

    def test_equals_match(self):
        c = Condition(field="plan", operator=ConditionOperator.EQUALS, value="premium")
        assert self.evaluator._evaluate_single(c, {"plan": "premium"})

    def test_equals_no_match(self):
        c = Condition(field="plan", operator=ConditionOperator.EQUALS, value="premium")
        assert not self.evaluator._evaluate_single(c, {"plan": "free"})

    def test_greater_than(self):
        c = Condition(field="total_spent", operator=ConditionOperator.GREATER_THAN, value=100)
        assert self.evaluator._evaluate_single(c, {"total_spent": 200})
        assert not self.evaluator._evaluate_single(c, {"total_spent": 50})

    def test_contains(self):
        c = Condition(field="email", operator=ConditionOperator.CONTAINS, value="@company.com")
        assert self.evaluator._evaluate_single(c, {"email": "user@company.com"})
        assert not self.evaluator._evaluate_single(c, {"email": "user@gmail.com"})

    def test_in_list(self):
        c = Condition(field="role", operator=ConditionOperator.IN, value=["admin", "owner"])
        assert self.evaluator._evaluate_single(c, {"role": "admin"})
        assert not self.evaluator._evaluate_single(c, {"role": "viewer"})

    def test_null_field(self):
        c = Condition(field="missing_field", operator=ConditionOperator.EQUALS, value="x")
        assert not self.evaluator._evaluate_single(c, {"plan": "premium"})

    def test_exists(self):
        c = Condition(field="plan", operator=ConditionOperator.EXISTS, value=1)
        assert self.evaluator._evaluate_single(c, {"plan": "premium"})
        assert not self.evaluator._evaluate_single(c, {"other": "value"})

    def test_event_field_resolution(self):
        c = Condition(field="amount", operator=ConditionOperator.GREATER_THAN, value=50, field_source="event")
        event = {"event_type": "test", "user_id": "u1", "payload": {"amount": 100}}
        # With event field_source, it looks at the event
        # event["amount"] doesn't exist directly
        assert not self.evaluator._evaluate_single(c, {"plan": "premium"}, event)

    def test_and_conditions(self):
        conditions = [
            Condition(field="plan", operator=ConditionOperator.EQUALS, value="premium"),
            Condition(field="total_spent", operator=ConditionOperator.GREATER_THAN, value=500),
        ]
        assert self.evaluator._evaluate_all(conditions, {"plan": "premium", "total_spent": 1000})
        assert not self.evaluator._evaluate_all(conditions, {"plan": "premium", "total_spent": 100})

    def test_or_conditions(self):
        conditions = [
            Condition(field="role", operator=ConditionOperator.EQUALS, value="admin"),
            Condition(field="role", operator=ConditionOperator.EQUALS, value="owner"),
        ]
        assert self.evaluator._evaluate_any(conditions, {"role": "admin"})
        assert not self.evaluator._evaluate_any(conditions, {"role": "viewer"})


class TestAutomationEngine:
    """Test the full automation engine."""

    def setup_method(self):
        self.engine = AutomationEngine()

    def test_deploy_rule(self):
        rule = AutomationRule(
            id="test_1",
            name="Test Rule",
            trigger=TriggerType.EVENT,
            trigger_config={"event_name": "test.event"},
            conditions=[Condition(field="plan", operator=ConditionOperator.EQUALS, value="premium")],
            actions=[Action(type=ActionType.SEND_MESSAGE, config={"channel": "email"})],
        )
        rule_id = self.engine.deploy_rule(rule)
        assert rule_id == "test_1"
        assert self.engine.get_rule("test_1") is not None

    def test_deploy_invalid_rule(self):
        rule = AutomationRule(
            id="bad", name="",  # empty name
            trigger=TriggerType.EVENT,
            conditions=[],
            actions=[],
        )
        with pytest.raises(ValueError, match="validation failed"):
            self.engine.deploy_rule(rule)

    def test_remove_rule(self):
        rule = AutomationRule(
            id="r1", name="R1",
            trigger=TriggerType.EVENT,
            conditions=[Condition(field="x", operator=ConditionOperator.EQUALS, value=1)],
            actions=[Action(type=ActionType.SEND_MESSAGE, config={})],
        )
        self.engine.deploy_rule(rule)
        self.engine.remove_rule("r1")
        assert self.engine.get_rule("r1") is None

    def test_campaign_lifecycle(self):
        campaign = Campaign(
            id="camp_test",
            name="Test Campaign",
            status="draft",
        )
        campaign_id = self.engine.create_campaign(campaign)
        assert campaign_id == "camp_test"

        self.engine.activate_campaign("camp_test")
        assert self.engine._campaigns["camp_test"].status == "active"

        self.engine.pause_campaign("camp_test")
        assert self.engine._campaigns["camp_test"].status == "paused"
