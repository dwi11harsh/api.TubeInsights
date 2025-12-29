from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
def talk_to_llm():
    """
    initializes a chat with llm and works using websockets
    """
    return None

