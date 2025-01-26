from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from fastapi.openapi.utils import get_openapi
import httpx, asyncio, logging

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SwApp API Gateway", version="1.0.0")

# OpenAPI Schema URL for each microservice 
MICROSERVICES = {
    "auth_service": "http://0.0.0.0:8000/api/schema/",
    "profile_service": "http://0.0.0.0:8001/api/schema/",
    "trade_service": "http://0.0.0.0:8002/api/schema/",
    "home_service": "http://0.0.0.0:8003/api/schema/",
}

# Cache para armazenar o schema consolidado
SCHEMA_CACHE = None

async def fetch_service_schema(client, name, url):
    """
        Fetch OpenAPI schema from a microservice.
    """
    try:
        response = await client.get(url)
        response.raise_for_status()
        logger.info(f"Schema fetched from {name}")
        return name, response.json()
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch schema from {name}: {e}")
        return name, None


@app.get("/openapi.json")
async def consolidated_openapi():
    """
        Consolidates the OpenAPI schemas of microservices.
    """
    global SCHEMA_CACHE
    if SCHEMA_CACHE:  # Return cached schema if available
        return SCHEMA_CACHE

    # Consolidate schemas
    consolidated_schema = {
        "openapi": "3.0.0",
        "info": {"title": "SwApp APIs", "version": "1.0.0"},
        "paths": {},
        "components": {"schemas": {}},
    }

    async with httpx.AsyncClient() as client:
        tasks = [fetch_service_schema(client, name, url) for name, url in MICROSERVICES.items()]
        results = await asyncio.gather(*tasks)

        for name, service_schema in results:
            if service_schema is None:
                continue
            # Consolidate endpoints
            for path, methods in service_schema.get("paths", {}).items():
                prefixed_path = f"/{name}{path}"
                consolidated_schema["paths"][prefixed_path] = methods

            # Consolidate components
            for schema_name, schema in service_schema.get("components", {}).get("schemas", {}).items():
                consolidated_schema["components"]["schemas"][f"{name}_{schema_name}"] = schema

    SCHEMA_CACHE = consolidated_schema  # Cache the result
    return consolidated_schema

@app.get("/docs", include_in_schema=False)
async def get_docs():
    """
        Shows the consolidated Swagger documentation.
    """

    schema_url = "/openapi.json"
    return get_swagger_ui_html(openapi_url=schema_url, title="SwApp API Gateway")

@app.get("/redoc", include_in_schema=False)
async def get_redoc():
    """
        Shows the consolidated ReDoc documentation.
    """

    schema_url = "/openapi.json"
    return get_redoc_html(openapi_url=schema_url, title="SwApp API Gateway")


@app.on_event("startup")
async def warm_up_cache():
    """
        Pre-fetch schemas during startup to warm up the cache.
    """
    logger.info("Warming up schema cache...")
    await consolidated_openapi()
    logger.info("Schema cache warmed up.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
