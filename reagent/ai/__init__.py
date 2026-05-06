"""AI Model Adapter Layer — 多模型统一接入层。

支持 OpenAI / Anthropic / Local (Ollama) / LiteLLM 等多模型热切换。
"""

from reagent.ai.registry import AIAdapterRegistry
from reagent.ai.schema import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    Message,
    ToolCall,
)
from reagent.ai.base import BaseAIAdapter, GenerationResult
