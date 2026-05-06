"""Action handlers — 规则匹配后的动作执行器。"""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Callable

import httpx
from loguru import logger

from reagent.automation.schema import Action, ActionType, RuleExecution


class ActionHandler:
    """Handles execution of automation actions.

    Supported actions:
    - Send message
    - Update segment
    - Trigger campaign
    - Call webhook
    - Assign tag
    - Update profile
    - Generate content (AI)
    """

    def __init__(self):
        self._custom_handlers: dict[ActionType, Callable] = {}
        logger.info("ActionHandler initialized")

    def register_handler(self, action_type: ActionType, handler: Callable) -> None:
        """Register a custom action handler."""
        self._custom_handlers[action_type] = handler

    async def execute(self, action: Action, user_id: str, context: dict) -> str:
        """Execute a single action.

        Returns:
            String describing the action result.
        """
        logger.info(f"Executing action: {action.type} for user {user_id}")

        # Check for custom handler first
        if action.type in self._custom_handlers:
            return await self._custom_handlers[action.type](action, user_id, context)

        # Built-in actions
        handlers = {
            ActionType.SEND_MESSAGE: self._send_message,
            ActionType.UPDATE_SEGMENT: self._update_segment,
            ActionType.TRIGGER_CAMPAIGN: self._trigger_campaign,
            ActionType.CALL_WEBHOOK: self._call_webhook,
            ActionType.ASSIGN_TAG: self._assign_tag,
            ActionType.UPDATE_PROFILE: self._update_profile,
        }

        handler = handlers.get(action.type)
        if handler:
            return await handler(action, user_id, context)

        raise ValueError(f"Unknown action type: {action.type}")

    async def execute_batch(self, actions: list[Action], user_id: str, context: dict) -> list[str]:
        """Execute multiple actions, respecting delays."""
        results = []
        for action in actions:
            if action.delay_minutes > 0:
                logger.info(f"Delaying action {action.type} for {action.delay_minutes} minutes")
                await asyncio.sleep(action.delay_minutes * 60)

            result = await self.execute(action, user_id, context)
            results.append(result)

        return results

    async def _send_message(self, action: Action, user_id: str, context: dict) -> str:
        """Send a message to a user."""
        channel = action.config.get("channel", "in_app")
        template = action.config.get("template", "")
        logger.info(f"Sending message via {channel}: template={template}")
        return f"message_sent:{channel}"

    async def _update_segment(self, action: Action, user_id: str, context: dict) -> str:
        """Update user segment."""
        segment = action.config.get("segment", "")
        operation = action.config.get("operation", "add")  # add, remove, set
        logger.info(f"Updating segment: {operation} '{segment}' for user {user_id}")
        return f"segment_{operation}:{segment}"

    async def _trigger_campaign(self, action: Action, user_id: str, context: dict) -> str:
        """Trigger another campaign."""
        campaign_id = action.config.get("campaign_id", "")
        logger.info(f"Triggering campaign {campaign_id} for user {user_id}")
        return f"campaign_triggered:{campaign_id}"

    async def _call_webhook(self, action: Action, user_id: str, context: dict) -> str:
        """Call an external webhook."""
        url = action.config.get("url", "")
        method = action.config.get("method", "POST")
        payload = {
            "user_id": user_id,
            "action_config": action.config,
            "context": context,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.request(method, url, json=payload)
                resp.raise_for_status()
                logger.info(f"Webhook {method} {url}: {resp.status_code}")
                return f"webhook_sent:{resp.status_code}"
        except Exception as e:
            logger.error(f"Webhook failed: {e}")
            return f"webhook_failed:{str(e)}"

    async def _assign_tag(self, action: Action, user_id: str, context: dict) -> str:
        """Assign a tag to a user."""
        tags = action.config.get("tags", [])
        logger.info(f"Assigning tags {tags} to user {user_id}")
        return f"tags_assigned:{','.join(tags)}"

    async def _update_profile(self, action: Action, user_id: str, context: dict) -> str:
        """Update a user profile field."""
        field = action.config.get("field", "")
        value = action.config.get("value", "")
        logger.info(f"Updating profile field {field}={value} for user {user_id}")
        return f"profile_updated:{field}"
