from fastapi import FastAPI

app = FastAPI(
    title="api.TubeInsights",
    description="AI backend for TubeInsights - ",
    version="1.0.0",
)

@app.get("/health")
def read_root():
    """
    returns ok status 200
    """
    return {
        "hello": "world"
    }

@app.post("/hard-work")
def fetch_transcript_and_embed():
    """
    fetches the transcript -> parses it -> generates(+stores) embeddings -> returns failed and passed urls, title, thumbnail
    """
    
    return None


@app.post("/chat")
def talk_to_llm():
    """
    initializes a chat with llm and works using websockets
    """
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
