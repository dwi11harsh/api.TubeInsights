from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def check_server_health():
    """
    Health check endpoint to verify the server is running and responsive.
    
    Returns:
        dict: A dictionary with 'ok' set to True indicating the server is healthy.
        
    Example:
        {
            "ok": True
        }
    """
    return {
        'ok': True
    }

