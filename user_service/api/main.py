"""FastAPI application para User Service"""

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
from ..domain.exceptions import UserError
from ..domain.dto.responses.error_responses import ErrorResponse
from .routes import user_router, admin_router


def get_settings():
    """Función simple para obtener configuración"""
    return {
        "database_url": config.DATABASE_URL,
        "cors_origins": config.USER_CORS_ORIGINS,
        "log_level": config.LOG_LEVEL,
        "environment": config.ENVIRONMENT,
        "service_port": config.USER_SERVICE_PORT,
        "service_name": os.getenv("USER_SERVICE_NAME", "user-service"),
        "service_version": os.getenv("USER_SERVICE_VERSION", "1.0.0"),
        "api_version": config.API_VERSION,
        "api_prefix": config.API_PREFIX,
        "auth_service_url": config.AUTH_SERVICE_URL
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.info("🚀 Iniciando User Service...")
    logging.info(f"📄 .env encontrado: {os.path.exists('.env')}")
    logging.info(f"📂 Directorio actual: {os.getcwd()}")
    logging.info(f"🗄️ Database URL configurado: {bool(settings['database_url'])}")
    logging.info(f"🌐 API Version: {settings['api_version']}")
    logging.info(f"🔗 Auth Service URL: {settings['auth_service_url']}")
    yield
    logging.info("🛑 Cerrando User Service...")


def create_app() -> FastAPI:
    """Factory para crear la aplicación FastAPI"""
    
    # Obtener configuración
    settings = get_settings()
    
    # Configurar logging
    logging.basicConfig(level=getattr(logging, settings["log_level"]))
    
    # Validar configuración mínima
    if not settings["database_url"]:
        raise ValueError(
            "🚨 Base de datos no configurada!\n\n"
            "Soluciones:\n"
            "1. Crear archivo .env en la raíz con: DATABASE_URL=postgresql://...\n"
            f"2. Directorio actual: {os.getcwd()}\n"
            f"3. Archivo .env existe: {os.path.exists('.env')}"
        )
    
    app = FastAPI(
        title=f"{settings['service_name']} API",
        version=settings["service_version"],
        description=f"Servicio de gestión de usuarios - API {settings['api_version']}",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings["cors_origins"],
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
        response.headers["X-API-Version"] = settings["api_version"]
        response.headers["X-Service-Name"] = settings["service_name"]
        response.headers["X-Service-Version"] = settings["service_version"]
        
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
    
    @app.exception_handler(UserError)
    async def user_error_handler(request: Request, exc: UserError):
        error_response = ErrorResponse(
            error="user_error",
            message=str(exc),
            error_code=exc.error_code,
            timestamp=datetime.now().isoformat()
        ).model_dump()
        
        # Agregar request_id si está disponible
        if hasattr(request.state, 'request_id'):
            error_response["request_id"] = request.state.request_id
        
        return JSONResponse(
            status_code=400,
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
    @app.get("/health")
    async def health_check():
        settings = get_settings()
        return {
            "status": "healthy", 
            "service": settings["service_name"],
            "version": settings["service_version"],
            "api_version": settings["api_version"],
            "database_configured": bool(settings["database_url"]),
            "auth_service_url": settings["auth_service_url"],
            "timestamp": datetime.now().isoformat(),
            "debug": {
                "env_file_exists": os.path.exists(".env"),
                "current_directory": os.getcwd(),
                "has_database_url": bool(settings["database_url"])
            }
        }
    
    # Incluir rutas con prefijo de versión centralizado
    app.include_router(
        user_router, 
        prefix=f"{settings['api_prefix']}/users", 
        tags=["Users"]
    )
    app.include_router(
        admin_router, 
        prefix=f"{settings['api_prefix']}/admin", 
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
    @app.get("/api/docs", include_in_schema=False)
    async def api_docs_redirect():
        """Redirigir a la documentación principal"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/docs")
    
    @app.get("/api/redoc", include_in_schema=False)
    async def api_redoc_redirect():
        """Redirigir a ReDoc"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/redoc")
    
    @app.get("/api/openapi.json", include_in_schema=False)
    async def api_openapi_redirect():
        """Redirigir a OpenAPI JSON"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/openapi.json")
    
    return app


# Instancia de la aplicación para uvicorn
app = create_app() 