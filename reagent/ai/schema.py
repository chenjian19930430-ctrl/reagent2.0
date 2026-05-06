"""AI Adapter — data schemas."""

from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    LITELLM = "litellm"


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """A single message in a conversation."""
    role: MessageRole
    content: str


class ToolCall(BaseModel):
    """Function/tool call from the model."""
    name: str
    arguments: dict


class ModelRequest(BaseModel):
    """Request to an AI model."""
    provider: ModelProvider = ModelProvider.OPENAI
    model: str = ""
    messages: list[Message]
    system_prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False
    tools: Optional[list[dict]] = None

    model_config = {"use_enum_values": False}


class ModelResponse(BaseModel):
    """Response from an AI model."""
    provider: ModelProvider
    model: str
    content: str = ""
    tool_calls: list[ToolCall] = []
    usage: dict = Field(default_factory=lambda: {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    })
    finish_reason: str = "stop"


class ModelCapability(str, Enum):
    """Capabilities a model supports."""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    IMAGE_UNDERSTANDING = "image_understanding"
    TOOL_USE = "tool_use"
    STRUCTURED_OUTPUT = "structured_output"


class ModelInfo(BaseModel):
    """Metadata about a registered model."""
    provider: ModelProvider
    model_id: str
    display_name: str = ""
    capabilities: list[ModelCapability] = []
    max_tokens: int = 4096
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
