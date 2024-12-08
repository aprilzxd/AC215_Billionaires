# src/api-service/api/routers/agent_router.py
from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from utils.finance_assistant import agent
from typing import Generator
import json
import re

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

def stream_response(user_input: str) -> Generator[str, None, None]:
    """
    Streams text responses incrementally.
    Uses a synchronous generator since agent.run(..., stream=True) returns a sync generator.
    """
    response_generator = agent.run(user_input, stream=True)
    full_content = ""

    for chunk in response_generator:
        # Extract text content from the chunk (assuming chunk.content contains the text)
        if hasattr(chunk, "content"):
            content_chunk = chunk.content
        else:
            content_chunk = str(chunk)

        full_content += content_chunk
        
        yield f"data: {json.dumps({'content': full_content})}\n\n"

    # Final message
    yield f"data: {json.dumps({'content': full_content})}\n\n"

@router.post("/agent/chat/stream")
def agent_chat_stream(request: ChatRequest) -> StreamingResponse:
    """
    Endpoint to stream the assistant's response incrementally.
    """
    try:
        user_prompt = request.prompt
        return StreamingResponse(
            stream_response(user_prompt),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
