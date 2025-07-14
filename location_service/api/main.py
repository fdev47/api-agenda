"""
API principal del servicio de ubicaciones
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import os
import logging
from datetime import datetime
import uuid

# ⭐ CARGAR .env AL INICIO
from dotenv import load_dotenv
load_dotenv()  # Busca .env en el directorio actual y directorios padre

from commons.config import config
from ..domain.exceptions import LocationDomainException
from ..domain.dto.responses import ErrorResponse
from .routes import country_router, state_router, city_router, local_router, branch_router
from ..infrastructure.container import container
from .middleware import error_handler_middleware


def get_settings():
    """Función simple para obtener configuración"""
    return {
        "database_url": config.DATABASE_URL,
        "cors_origins": config.LOCATION_CORS_ORIGINS,
        "log_level": config.LOG_LEVEL,
        "environment": config.ENVIRONMENT,
        "service_port": config.LOCATION_SERVICE_PORT,
        "service_name": os.getenv("LOCATION_SERVICE_NAME", "location-service"),
        "service_version": os.getenv("LOCATION_SERVICE_VERSION", "1.0.0"),
        "api_version": config.API_VERSION,
        "api_prefix": config.API_PREFIX
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    print("🚀 Location Service iniciando...")
    settings = get_settings()
    print(f"📋 Configuración: {settings}")
    
    yield
    
    # Shutdown
    print("🛑 Location Service deteniendo...")


# Crear aplicación FastAPI
app = FastAPI(
    title="Location Service API",
    description="API para gestión de ubicaciones, países, estados, ciudades, locales y sucursales",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el contenedor de dependencias
app.container = container

# Configurar middleware de manejo de errores
@app.middleware("http")
async def error_middleware(request: Request, call_next):
    return await error_handler_middleware(request, call_next)

# Configurar Swagger UI
def custom_openapi():
    """Configuración personalizada de OpenAPI"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Configurar autenticación Bearer Token
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Exception handlers
@app.exception_handler(LocationDomainException)
async def location_exception_handler(request: Request, exc: LocationDomainException):
    """Manejador de excepciones del dominio de ubicación"""
    error_response = ErrorResponse(
        error=True,
        message=exc.message,
        error_code=exc.error_code,
        timestamp=datetime.utcnow().isoformat(),
        path=request.url.path
    )
    return JSONResponse(
        status_code=400,
        content=error_response.model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador de excepciones HTTP"""
    error_response = ErrorResponse(
        error=True,
        message=exc.detail,
        error_code="HTTP_ERROR",
        timestamp=datetime.utcnow().isoformat(),
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejador de excepciones generales"""
    error_response = ErrorResponse(
        error=True,
        message="Error interno del servidor",
        error_code="INTERNAL_ERROR",
        timestamp=datetime.utcnow().isoformat(),
        path=request.url.path
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


# Rutas
app.include_router(country_router, prefix="/api/v1")
app.include_router(state_router, prefix="/api/v1")
app.include_router(city_router, prefix="/api/v1")
app.include_router(local_router, prefix="/api/v1")
app.include_router(branch_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Location Service API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "service": "location-service"}


# Configurar Swagger UI personalizado
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "list",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 