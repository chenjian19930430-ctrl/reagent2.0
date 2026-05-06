"""AI Model Adapter API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from reagent.ai.registry import registry
from reagent.ai.schema import (
    ModelRequest,
    ModelResponse,
    ModelProvider,
    ModelInfo,
    Message,
    MessageRole,
)

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


class GenerateRequest(BaseModel):
    """Request body for AI text generation."""
    provider: str = ""
    model: str = ""
    system_prompt: str = ""
    messages: list[dict] = []
    temperature: float = 0.7
    max_tokens: int = 4096


class GenerateResponse(BaseModel):
    """Response body for AI text generation."""
    content: str
    provider: str
    model: str
    usage: dict


@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text using AI models with automatic provider routing."""
    ai_request = ModelRequest(
        provider=ModelProvider(request.provider) if request.provider else ModelProvider.OPENAI,
        model=request.model,
        messages=[Message(role=MessageRole(m["role"]), content=m["content"]) for m in request.messages],
        system_prompt=request.system_prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    adapter = registry.resolve(ai_request)
    result = await adapter.generate(ai_request)

    return GenerateResponse(
        content=result.text,
        provider=result.model_info.provider.value,
        model=result.model_info.model_id,
        usage=result.usage,
    )


@router.get("/models", response_model=list[ModelInfo])
async def list_models():
    """List all available AI models."""
    return await registry.list_available_models()


@router.post("/generate/stream")
async def generate_stream(request: GenerateRequest):
    """Stream text generation.

    NOTE: This endpoint returns a streaming response.
    """
    from fastapi.responses import StreamingResponse
    import json

    ai_request = ModelRequest(
        provider=ModelProvider(request.provider) if request.provider else ModelProvider.OPENAI,
        model=request.model,
        messages=[Message(role=MessageRole(m["role"]), content=m["content"]) for m in request.messages],
        system_prompt=request.system_prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )

    adapter = registry.resolve(ai_request)

    async def event_stream():
        async for token in adapter.generate_stream(ai_request):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
