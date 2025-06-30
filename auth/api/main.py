"""FastAPI application"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging
from datetime import datetime
import uuid

# ⭐ CARGAR .env AL INICIO
from dotenv import load_dotenv
load_dotenv()  # Busca .env en el directorio actual y directorios padre

from commons.config import config
from ..domain.exceptions import AuthError, AuthErrorCode
from ..domain.dto.responses import AuthErrorResponse, ErrorResponse
from .routes import auth_router


def get_settings():
    """Función simple para obtener configuración"""
    return {
        "firebase_credentials_path": config.FIREBASE_CREDENTIALS_PATH,
        "firebase_project_id": config.FIREBASE_PROJECT_ID,
        "cors_origins": config.AUTH_CORS_ORIGINS,
        "log_level": config.LOG_LEVEL,
        "environment": config.ENVIRONMENT,
        "service_port": config.AUTH_SERVICE_PORT,
        "service_name": os.getenv("AUTH_SERVICE_NAME", "auth-service"),
        "service_version": os.getenv("AUTH_SERVICE_VERSION", "1.0.0"),
        "api_version": config.API_VERSION,
        "api_prefix": config.API_PREFIX
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.info("🚀 Iniciando Auth Service...")
    logging.info(f"📄 .env encontrado: {os.path.exists('.env')}")
    logging.info(f"📂 Directorio actual: {os.getcwd()}")
    logging.info(f"🔑 Firebase Project ID: {settings['firebase_project_id']}")
    logging.info(f"🌐 API Version: {settings['api_version']}")
    yield
    logging.info("🛑 Cerrando Auth Service...")


def create_app() -> FastAPI:
    """Factory para crear la aplicación FastAPI"""
    
    # Obtener configuración
    settings = get_settings()
    
    # Configurar logging
    logging.basicConfig(level=getattr(logging, settings["log_level"]))
    
    # Validar configuración mínima
    if not settings["firebase_project_id"] and not settings["firebase_credentials_path"]:
        raise ValueError(
            "🚨 Firebase no configurado!\n\n"
            "Soluciones:\n"
            "1. Crear archivo .env en la raíz con: FIREBASE_PROJECT_ID=tu-project-id\n"
            "2. O usar: FIREBASE_CREDENTIALS_PATH=path/to/credentials.json\n"
            f"3. Directorio actual: {os.getcwd()}\n"
            f"4. Archivo .env existe: {os.path.exists('.env')}"
        )
    
    app = FastAPI(
        title=f"{settings['service_name']} API",
        version=settings["service_version"],
        description=f"Servicio de autenticación y autorización con Firebase - API {settings['api_version']}",
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
            error_response = AuthErrorResponse(
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
    
    @app.exception_handler(AuthError)
    async def auth_error_handler(request: Request, exc: AuthError):
        status_mapping = {
            AuthErrorCode.INVALID_CREDENTIALS.value: 401,
            AuthErrorCode.USER_NOT_FOUND.value: 404,
            AuthErrorCode.EMAIL_ALREADY_EXISTS.value: 409,
            AuthErrorCode.WEAK_PASSWORD.value: 400,
            AuthErrorCode.INVALID_TOKEN.value: 401,
            AuthErrorCode.TOKEN_EXPIRED.value: 401,
            AuthErrorCode.USER_DISABLED.value: 403,
        }
        
        status_code = status_mapping.get(exc.error_code, 500)
        
        error_response = AuthErrorResponse(
            error="auth_error",
            message=str(exc),
            error_code=exc.error_code,
            token_expired=exc.error_code == AuthErrorCode.TOKEN_EXPIRED.value,
            timestamp=datetime.now().isoformat()
        ).model_dump()
        
        # Agregar request_id si está disponible
        if hasattr(request.state, 'request_id'):
            error_response["request_id"] = request.state.request_id
        
        return JSONResponse(
            status_code=status_code,
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
            "firebase_configured": bool(settings["firebase_project_id"] or settings["firebase_credentials_path"]),
            "timestamp": datetime.now().isoformat(),
            "debug": {
                "env_file_exists": os.path.exists(".env"),
                "current_directory": os.getcwd(),
                "has_project_id": bool(settings["firebase_project_id"]),
                "has_credentials_path": bool(settings["firebase_credentials_path"])
            }
        }
    
    # Incluir solo rutas de autenticación con prefijo centralizado
    app.include_router(
        auth_router, 
        prefix=f"{settings['api_prefix']}/auth", 
        tags=["Authentication"]
    )
    
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


# Crear la aplicación
app = create_app()