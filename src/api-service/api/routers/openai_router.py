import openai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@router.post("/openai/chat")
async def openai_chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt},
            ],
            max_tokens=request.max_tokens,
        )
        completion = response.choices[0].message.content
        return {"response": completion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")