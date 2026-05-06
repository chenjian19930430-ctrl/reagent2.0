"""Error handling and exception hierarchy."""

from __future__ import annotations


class ReAgentError(Exception):
    """Base exception for ReAgent."""
    code: str = "REAGENT_ERROR"
    http_status: int = 500

    def __init__(self, message: str = "", detail: dict | None = None):
        self.message = message or self.__class__.__name__
        self.detail = detail or {}

    def to_dict(self) -> dict:
        return {
            "error": self.code,
            "message": self.message,
            "detail": self.detail,
        }


class AIAdapterError(ReAgentError):
    code = "AI_ADAPTER_ERROR"
    http_status = 502


class ModelNotAvailableError(AIAdapterError):
    code = "MODEL_NOT_AVAILABLE"
    http_status = 503


class ContentGenerationError(ReAgentError):
    code = "CONTENT_GENERATION_ERROR"
    http_status = 500


class ProfileAnalysisError(ReAgentError):
    code = "PROFILE_ANALYSIS_ERROR"
    http_status = 422


class AutomationError(ReAgentError):
    code = "AUTOMATION_ERROR"
    http_status = 500


class RuleValidationError(ReAgentError):
    code = "RULE_VALIDATION_ERROR"
    http_status = 422


class ConfigurationError(ReAgentError):
    code = "CONFIGURATION_ERROR"
    http_status = 500
