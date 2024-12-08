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
    Streams both text and image responses incrementally.
    This function uses Server-Sent Events (SSE) format: each message is prefixed with 'data:'.
    """
    # agent.run with stream=True should return a generator of RunResponse-like objects
    response_generator = agent.run(user_input, stream=True)
    plot_image = None
    full_content = ""

    for chunk in response_generator:
        # Extract text content from the chunk object
        # Adjust this if `RunResponse` uses a different attribute name, such as `chunk.message.content`.
        if hasattr(chunk, "content"):
            content_chunk = chunk.content
        else:
            # Fallback to string conversion if no .content attribute exists
            content_chunk = str(chunk)

        full_content += content_chunk

        # Check for Base64-encoded images in this chunk of text
        base64_match = re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", content_chunk)
        if base64_match and not plot_image:
            plot_image = base64_match.group(1)

        # Yield updates incrementally as SSE
        yield f"data: {json.dumps({'content': full_content, 'plot_image': plot_image})}\n\n"

    # After streaming ends, if an image was found, remove the embedded image markdown from the text
    if plot_image:
        full_content = re.sub(
            r"!\[.*?\]\(data:image/png;base64,[A-Za-z0-9+/=]+\)", 
            "", 
            full_content
        ).strip()

    # Final yield to provide the cleaned-up content
    yield f"data: {json.dumps({'content': full_content, 'plot_image': plot_image})}\n\n"

@router.post("/agent/chat/stream")
async def agent_chat_stream(request: ChatRequest) -> StreamingResponse:
    """
    Endpoint to stream the assistant's response incrementally, including images if present.
    Returns a text/event-stream response that can be read incrementally by the frontend.
    """
    try:
        user_prompt = request.prompt
        return StreamingResponse(
            stream_response(user_prompt),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
