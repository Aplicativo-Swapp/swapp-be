from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/auth_service", tags=["Auth Service"])

AUTH_SERVICE_URL = "http://auth_service:8000"

@router.get("/health")
async def auth_service_health():
    """
        Check health status of the Auth Service.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/health")
        return response.json()

@router.get("/users/")
async def get_users():
    """
        Proxy endpoint for fetching users.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/users/")
        return response.json()
