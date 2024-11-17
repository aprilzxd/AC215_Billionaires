from fastapi import FastAPI
from .routers import agent_router

app = FastAPI()

app.include_router(agent_router.router, tags=["Agent"])

@app.get("/")
async def root():
    return {"message": "Welcome to the OpenAI API Example!"}
