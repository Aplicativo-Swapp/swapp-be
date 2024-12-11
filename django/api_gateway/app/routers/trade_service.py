from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/trade_service", tags=["Trade Service"])

TRADE_SERVICE_URL = "http://trade_service:8002"

@router.get("/health")
async def trade_service_health():
    """
        Check health status of the Trade Service.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRADE_SERVICE_URL}/health")
        return response.json()

@router.get("/trades/")
async def get_trades():
    """
        Proxy endpoint for fetching trades.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRADE_SERVICE_URL}/trades/")
        return response.json()
