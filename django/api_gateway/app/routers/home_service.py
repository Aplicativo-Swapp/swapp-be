from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/home_service", tags=["Home Service"])

HOME_SERVICE_URL = "http://0.0.0.0:8003/api"

@router.get("/health")
async def home_service_health():
    """
        Check health status of the Home Service.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HOME_SERVICE_URL}/health")
        return response.json()

@router.get("/home/")
async def get_home():
    """
        Proxy endpoint for fetching home data.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HOME_SERVICE_URL}/home/")
        return response.json()
