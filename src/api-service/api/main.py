from fastapi import FastAPI
from .routers import agent_router, plot_router

# Initialize the FastAPI app with metadata
app = FastAPI(
    title="Finance Chatbot API",
    description="Backend API for the Finance Chatbot. Handles user queries, integrates tools, and provides responses.",
    version="1.0.0",
)

app.include_router(agent_router.router, tags=["Agent"])
app.include_router(plot_router.plot_router, tags=["Plot"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Finance Chatbot API!"}
