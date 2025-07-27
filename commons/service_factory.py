"""
Factory común para crear servicios FastAPI estandarizados - CORREGIDO OpenAPI
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
from typing import Optional, Dict, Any, List, Callable, Union, Tuple
from pydantic import BaseModel

from .config import config
from .middleware import auth_middleware_dict
from .database import create_tables, test_connection


class ServiceConfig:
    """Configuración estándar para servicios"""
    
    def __init__(
        self,
        service_name: str,
        service_version: str,
        service_port: int,
        cors_origins: List[str],
        database_url: str,
        api_version: str,
        api_prefix: str,
        title: str,
        description: str,
        tags: List[str] = None,
        additional_settings: Dict[str, Any] = None
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.service_port = service_port
        self.cors_origins = cors_origins
        self.database_url = database_url
        self.api_version = api_version
        self.api_prefix = api_prefix
        self.title = title
        self.description = description
        self.tags = tags or []
        self.additional_settings = additional_settings or {}


class RouterConfig:
    """Configuración para routers con prefijos personalizados"""
    
    def __init__(
        self,
        router: Any,
        prefix: str = "",
        tags: List[str] = None
    ):
        self.router = router
        self.prefix = prefix
        self.tags = tags or []


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: bool = True
    message: str
    error_code: str
    timestamp: str
    path: Optional[str] = None
    request_id: Optional[str] = None


def create_service_factory(
    service_config: ServiceConfig,
    base_model: Optional[Any] = None,
    routers: List[Union[Any, RouterConfig]] = None,
    custom_exception_handlers: Dict[type, Callable] = None,
    custom_middleware: List[Callable] = None,
    enable_auth: bool = True,
    enable_auto_tables: bool = False
) -> FastAPI:
    """
    Factory para crear servicios FastAPI estandarizados
    """
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Gestión del ciclo de vida de la aplicación"""
        # Startup
        print(f"🚀 {service_config.service_name} iniciando...")
        print(f"📋 Configuración: {service_config.__dict__}")
        
        # Crear tablas automáticamente si está habilitado
        if enable_auto_tables and base_model:
            try:
                print("🔍 Probando conexión a la base de datos...")
                if await test_connection():
                    print("✅ Conexión exitosa a la base de datos")
                    print("📋 Creando tablas automáticamente...")
                    await create_tables(base_model)
                    print("✅ Tablas creadas/verificadas exitosamente")
                else:
                    print("❌ Error: No se pudo conectar a la base de datos")
            except Exception as e:
                print(f"⚠️ Advertencia: Error creando tablas: {str(e)}")
                print("El servicio continuará sin las tablas...")
        
        yield
        
        # Shutdown
        print(f"🛑 {service_config.service_name} deteniendo...")
    
    # Crear aplicación FastAPI
    app = FastAPI(
        title=service_config.title,
        description=service_config.description,
        version=service_config.service_version,
        docs_url=None,  # Deshabilitamos para usar uno personalizado
        redoc_url=None,
        lifespan=lifespan
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=service_config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Middleware de autenticación
    if enable_auth:
        print(f"🔐 MIDDLEWARE DE AUTENTICACIÓN ACTIVADO para {service_config.service_name}")
        @app.middleware("http")
        async def auth_middleware_handler(request: Request, call_next):
            return await auth_middleware_dict["auth_middleware"](request, call_next)
    else:
        print(f"🔓 MIDDLEWARE DE AUTENTICACIÓN DESHABILITADO para {service_config.service_name}")
    
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
        response.headers["X-API-Version"] = service_config.api_version
        response.headers["X-Service-Name"] = service_config.service_name
        response.headers["X-Service-Version"] = service_config.service_version
        
        return response
    
    # Middleware personalizado adicional
    if custom_middleware:
        for middleware in custom_middleware:
            app.add_middleware(middleware)
    
    # Exception handlers estándar
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Manejador de excepciones HTTP estándar"""
        from .error_codes import ErrorCode
        
        # Manejar caso donde exc.detail es un diccionario con error_code
        if isinstance(exc.detail, dict):
            message = exc.detail.get('message', str(exc.detail))
            error_code = exc.detail.get('error_code', ErrorCode.UNEXPECTED_ERROR.value)
        else:
            message = str(exc.detail)
            error_code = ErrorCode.UNEXPECTED_ERROR.value
            
        error_response = ErrorResponse(
            message=message,
            error_code=error_code,
            timestamp=datetime.utcnow().isoformat(),
            path=request.url.path,
            request_id=getattr(request.state, 'request_id', None)
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Manejador de excepciones generales estándar"""
        from .error_codes import get_error_code_by_exception, ErrorCode
        
        error_code = get_error_code_by_exception(exc)
        
        error_response = ErrorResponse(
            message="Error interno del servidor",
            error_code=error_code,
            timestamp=datetime.utcnow().isoformat(),
            path=request.url.path,
            request_id=getattr(request.state, 'request_id', None)
        )
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )
    
    # Manejadores de excepciones personalizados
    if custom_exception_handlers:
        for exception_type, handler in custom_exception_handlers.items():
            app.exception_handler(exception_type)(handler)
    
    # Incluir routers
    if routers:
        for router_item in routers:
            if isinstance(router_item, RouterConfig):
                # Router con configuración personalizada
                app.include_router(
                    router_item.router,
                    prefix=f"{service_config.api_prefix}{router_item.prefix}",
                    tags=router_item.tags
                )
            else:
                # Router directo
                app.include_router(router_item, prefix=service_config.api_prefix)
    
    # Endpoints estándar
    @app.get("/")
    async def root():
        """Endpoint raíz estándar"""
        return {
            "message": f"{service_config.service_name} API",
            "version": service_config.service_version,
            "docs": "/docs"
        }
    
    @app.get("/health")
    async def health_check():
        """Endpoint de verificación de salud estándar"""
        return {
            "status": "healthy",
            "service": service_config.service_name,
            "version": service_config.service_version,
            "api_version": service_config.api_version,
            "database_configured": bool(service_config.database_url),
            "timestamp": datetime.utcnow().isoformat(),
            "debug": {
                "env_file_exists": os.path.exists(".env"),
                "current_directory": os.getcwd(),
                "has_database_url": bool(service_config.database_url)
            }
        }
    
    # Configurar OpenAPI personalizado con autenticación Bearer
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
        
        # CRÍTICO: Configurar autenticación Bearer Token
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}
        
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Ingrese su token JWT (sin 'Bearer')"
            }
        }
        
        # CRÍTICO: Aplicar seguridad a TODAS las rutas protegidas
        public_paths = {
            "/",
            "/health",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/debug/openapi",
            "/debug/swagger-config",
            "/debug/test-auth"  # Para debugging
        }
        
        for path, path_item in openapi_schema.get("paths", {}).items():
            # Solo aplicar seguridad a rutas que no sean públicas
            if path not in public_paths:
                for method in ["get", "post", "put", "delete", "patch", "options", "head", "trace"]:
                    if method in path_item:
                        # Aplicar seguridad Bearer a esta operación
                        if "security" not in path_item[method]:
                            path_item[method]["security"] = [{"BearerAuth": []}]
                        
                        # Debug: imprimir qué rutas tienen seguridad aplicada
                        print(f"🔐 Seguridad aplicada a: {method.upper()} {path}")
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
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
                "persistAuthorization": True,
                "displayRequestDuration": True,
                "tryItOutEnabled": True,
                "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"]
            }
        )
    
    # Endpoint adicional para debugging OpenAPI
    @app.get("/debug/openapi", include_in_schema=False)
    async def debug_openapi():
        """Endpoint para debuggear la configuración de OpenAPI"""
        schema = app.openapi()
        return {
            "security_schemes": schema.get("components", {}).get("securitySchemes", {}),
            "paths_with_security": {
                path: {
                    method: operation.get("security", "NO_SECURITY")
                    for method, operation in path_item.items()
                    if isinstance(operation, dict) and method in ["get", "post", "put", "delete", "patch"]
                }
                for path, path_item in schema.get("paths", {}).items()
            }
        }
    
    return app


def run_service(app: FastAPI, service_config: ServiceConfig):
    """Función estándar para ejecutar un servicio"""
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=service_config.service_port,
        log_level="info"
    )