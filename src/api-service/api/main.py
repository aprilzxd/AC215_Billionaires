from fastapi import FastAPI
from .routers import openai_router
from .routers import agent_router

app = FastAPI()

app.include_router(openai_router.router, prefix="/api/v1", tags=["OpenAI"])
app.include_router(agent_router.router, tags=["Agent"])

@app.get("/")
async def root():
    return {"message": "Welcome to the OpenAI API Example!"}
