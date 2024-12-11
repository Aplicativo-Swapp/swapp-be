from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import httpx

app = FastAPI(title="SwApp API Gateway", version="1.0.0")

# OpenAPI Schema URL for each microservice 
MICROSERVICES = {
    "auth_service": "http://auth_service:8000/api/schema/",
    "profile_service": "http://profile_service:8001/api/schema/",
    "trade_service": "http://trade_service:8002/api/schema/",
    "home_service": "http://home_service:8003/api/schema/",
}

@app.get("/openapi.json")
async def consolidated_openapi():
    """
        Consolidates the OpenAPI schemas of microservices.
    """
    consolidated_schema = {
        "openapi": "3.0.0",
        "info": {"title": "SwApp APIs", "version": "1.0.0"},
        "paths": {},
        "components": {"schemas": {}},
    }
    async with httpx.AsyncClient() as client:
        for name, url in MICROSERVICES.items():
            try:
                response = await client.get(url)
                response.raise_for_status()
                service_schema = response.json()

                # Consolidate endpoints
                for path, methods in service_schema.get("paths", {}).items():
                    consolidated_schema["paths"][f"/{name}{path}"] = methods

                # Consolidate components
                for schema_name, schema in service_schema.get("components", {}).get("schemas", {}).items():
                    consolidated_schema["components"]["schemas"][f"{name}_{schema_name}"] = schema

            except httpx.RequestError as e:
                print(f"Erro ao conectar ao serviço {name}: {e}")
    
    return consolidated_schema

@app.get("/docs", include_in_schema=False)
async def get_docs():
    """
        Shows the consolidated Swagger documentation.
    """

    from fastapi.openapi.docs import get_swagger_ui_html

    schema_url = "/openapi.json"
    return get_swagger_ui_html(openapi_url=schema_url, title="SwApp API Gateway")
