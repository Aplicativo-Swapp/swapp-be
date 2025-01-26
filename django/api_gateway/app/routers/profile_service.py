from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/profile_service", tags=["Profile Service"])

PROFILE_SERVICE_URL = "http://0.0.0.0:8001/api"

@router.get("/health")
async def profile_service_health():
    """
        Check health status of the Profile Service.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PROFILE_SERVICE_URL}/health")
        return response.json()

@router.get("/profiles/")
async def get_profiles():
    """
        Proxy endpoint for fetching profiles.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PROFILE_SERVICE_URL}/profiles/")
        return response.json()
