"""API Gateway - Orquestador principal de microservicios"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
from api_gateway.domain.exceptions import GatewayError
from api_gateway.domain.dto.responses import ErrorResponse
from api_gateway.infrastructure.container import container
from api_gateway.api.routes import auth_router, user_router, admin_router
from api_gateway.config import GatewayConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    config_info = GatewayConfig.get_service_info()
    service_urls = GatewayConfig.get_service_urls()
    
    logging.info("🚀 Iniciando API Gateway...")
    logging.info(f"📄 .env encontrado: {os.path.exists('.env')}")
    logging.info(f"📂 Directorio actual: {os.getcwd()}")
    logging.info(f"🌐 API Version: {config_info['api_version']}")
    logging.info(f"🔗 Auth Service URL: {service_urls['auth']}")
    logging.info(f"👥 User Service URL: {service_urls['user']}")
    logging.info(f"📍 Location Service URL: {service_urls['location']}")
    
    yield
    
    logging.info("🛑 Cerrando API Gateway...")


def create_app() -> FastAPI:
    """Factory para crear la aplicación FastAPI"""
    
    # Validar configuración mínima
    if not GatewayConfig.validate_configuration():
        raise ValueError(
            "🚨 Servicios no configurados!\n\n"
            "Soluciones:\n"
            "1. Crear archivo .env en la raíz con AUTH_SERVICE_URL y USER_SERVICE_URL\n"
            f"2. Directorio actual: {os.getcwd()}\n"
            f"3. Archivo .env existe: {os.path.exists('.env')}"
        )
    
    # Configurar logging
    logging.basicConfig(level=getattr(logging, GatewayConfig.LOG_LEVEL))
    
    # Obtener información del servicio
    service_info = GatewayConfig.get_service_info()
    
    app = FastAPI(
        title=f"{service_info['name']} API",
        version=service_info['version'],
        description=f"API Gateway - Orquestador de microservicios - API {service_info['api_version']}",
        lifespan=lifespan,
        docs_url=GatewayConfig.DOCS_URL,
        redoc_url=GatewayConfig.REDOC_URL,
        openapi_url=GatewayConfig.OPENAPI_URL
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=GatewayConfig.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Middleware para agregar headers estándar
    @app.middleware("http")
    async def add_standard_headers(request: Request, call_next):
        # Generar Request ID único
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Procesar la respuesta
        response = await call_next(request)
        
        # Agregar headers estándar
        response.headers["X-Request-ID"] = request_id
        response.headers["X-API-Version"] = service_info['api_version']
        response.headers["X-Service-Name"] = service_info['name']
        response.headers["X-Service-Version"] = service_info['version']
        
        return response
    
    # Exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        # Si el detail es un diccionario (nuestro error personalizado), usarlo directamente
        if isinstance(exc.detail, dict):
            error_response = exc.detail
        else:
            # Si es un string, crear un error genérico
            error_response = ErrorResponse(
                error="http_error",
                message=str(exc.detail),
                error_code="HTTP_ERROR",
                timestamp=datetime.now().isoformat()
            ).model_dump()
        
        # Agregar request_id si está disponible
        if hasattr(request.state, 'request_id'):
            error_response["request_id"] = request.state.request_id
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    
    @app.exception_handler(GatewayError)
    async def gateway_error_handler(request: Request, exc: GatewayError):
        error_response = ErrorResponse(
            error="gateway_error",
            message=str(exc),
            error_code=exc.error_code,
            timestamp=datetime.now().isoformat()
        ).model_dump()
        
        # Agregar request_id si está disponible
        if hasattr(request.state, 'request_id'):
            error_response["request_id"] = request.state.request_id
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        error_response = ErrorResponse(
            error="internal_error",
            message="Error interno del servidor",
            error_code="INTERNAL_ERROR",
            timestamp=datetime.now().isoformat()
        ).model_dump()
        
        # Agregar request_id si está disponible
        if hasattr(request.state, 'request_id'):
            error_response["request_id"] = request.state.request_id
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )
    
    # Health check
    @app.get(GatewayConfig.HEALTH_CHECK_PATH)
    async def health_check():
        service_info = GatewayConfig.get_service_info()
        service_urls = GatewayConfig.get_service_urls()
        
        return {
            "status": "healthy", 
            "service": service_info['name'],
            "version": service_info['version'],
            "api_version": service_info['api_version'],
            "auth_service_url": service_urls['auth'],
            "user_service_url": service_urls['user'],
            "location_service_url": service_urls['location'],
            "timestamp": datetime.now().isoformat(),
            "debug": {
                "env_file_exists": os.path.exists(".env"),
                "current_directory": os.getcwd(),
                "has_auth_service": bool(service_urls['auth']),
                "has_user_service": bool(service_urls['user']),
                "has_location_service": bool(service_urls['location'])
            }
        }
    
    # Incluir rutas con prefijo de versión centralizado
    app.include_router(
        auth_router, 
        prefix=f"{GatewayConfig.API_PREFIX}/auth", 
        tags=["Authentication"]
    )
    app.include_router(
        user_router, 
        prefix=f"{GatewayConfig.API_PREFIX}/users", 
        tags=["Users"]
    )
    app.include_router(
        admin_router, 
        prefix=f"{GatewayConfig.API_PREFIX}/admin", 
        tags=["Administration"]
    )
    
    # Configurar autenticación en OpenAPI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        
        # Agregar esquema de autenticación
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Firebase ID Token obtenido desde tu aplicación web"
            }
        }
        
        # Agregar seguridad global
        openapi_schema["security"] = [
            {
                "BearerAuth": []
            }
        ]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
    # Agregar rutas de documentación con prefijo /api/ para compatibilidad
    @app.get(GatewayConfig.API_DOCS_REDIRECT_PATH, include_in_schema=False)
    async def api_docs_redirect():
        """Redirigir a la documentación principal"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=GatewayConfig.DOCS_URL)
    
    @app.get(GatewayConfig.API_REDOC_REDIRECT_PATH, include_in_schema=False)
    async def api_redoc_redirect():
        """Redirigir a ReDoc"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=GatewayConfig.REDOC_URL)
    
    @app.get(GatewayConfig.API_OPENAPI_REDIRECT_PATH, include_in_schema=False)
    async def api_openapi_redirect():
        """Redirigir a OpenAPI JSON"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=GatewayConfig.OPENAPI_URL)
    
    return app


# Crear instancia de la aplicación
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    service_info = GatewayConfig.get_service_info()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=service_info['port'],
        reload=True,
        log_level=GatewayConfig.LOG_LEVEL.lower()
    ) 