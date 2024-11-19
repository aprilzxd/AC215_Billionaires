from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.finance_assistant import assistant

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@router.post("/agent/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):

    try:
        user_prompt = request.prompt
        response_generator = assistant.run(user_prompt, stream=False)
        full_response = "".join(response_generator)
        return ChatResponse(response=full_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
