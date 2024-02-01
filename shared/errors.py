"""Error handling and exceptions."""


class ReAgentError(Exception):
    """Base exception for ReAgent."""
    pass


class ProfileNotFoundError(ReAgentError):
    pass


class WorkflowExecutionError(ReAgentError):
    pass


class RecommendationError(ReAgentError):
    pass
