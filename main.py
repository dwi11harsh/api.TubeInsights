from fastapi import FastAPI
from routes import health, hard_work, chat

app = FastAPI(
    title="api.TubeInsights",
    description="AI backend for TubeInsights - ",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(hard_work.router)
app.include_router(chat.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
