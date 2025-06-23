"""FastAPI application"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging

# ⭐ CARGAR .env AL INICIO
from dotenv import load_dotenv
load_dotenv()  # Busca .env en el directorio actual y directorios padre

from auth_service.infrastructure.container import AuthServiceContainer
from auth_service.api.schemas import *
from auth_service.api.middleware import AuthMiddleware
from auth_service.domain.models import AuthError, AuthErrorCode


def get_settings():
    """Función simple para obtener configuración"""
    return {
        "firebase_credentials_path": os.getenv("FIREBASE_CREDENTIALS_PATH"),
        "firebase_project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.info("🚀 Iniciando Auth Service...")
    logging.info(f"📄 .env encontrado: {os.path.exists('.env')}")
    logging.info(f"📂 Directorio actual: {os.getcwd()}")
    logging.info(f"🔑 Firebase Project ID: {settings['firebase_project_id']}")
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
        title="Auth Service",
        version="1.0.0",
        description="Servicio de autenticación y autorización con Firebase",
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings["cors_origins"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Container de dependencias
    container = AuthServiceContainer(
        settings["firebase_credentials_path"], 
        settings["firebase_project_id"]
    )
    auth_middleware = AuthMiddleware(container)
    
    # Exception handlers
    @app.exception_handler(AuthError)
    async def auth_error_handler(request: Request, exc: AuthError):
        status_mapping = {
            AuthErrorCode.INVALID_CREDENTIALS.value: status.HTTP_401_UNAUTHORIZED,
            AuthErrorCode.USER_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
            AuthErrorCode.EMAIL_ALREADY_EXISTS.value: status.HTTP_409_CONFLICT,
            AuthErrorCode.WEAK_PASSWORD.value: status.HTTP_400_BAD_REQUEST,
            AuthErrorCode.INVALID_TOKEN.value: status.HTTP_401_UNAUTHORIZED,
            AuthErrorCode.TOKEN_EXPIRED.value: status.HTTP_401_UNAUTHORIZED,
            AuthErrorCode.USER_DISABLED.value: status.HTTP_403_FORBIDDEN,
        }
        
        status_code = status_mapping.get(exc.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse(
                error="auth_error",
                message=str(exc),
                error_code=exc.error_code
            ).dict()
        )
    
    # Helper function
    def map_user_to_response(user) -> UserResponse:
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            display_name=user.display_name,
            phone_number=user.phone_number,
            email_verified=user.email_verified,
            roles=user.custom_claims.get('roles', []),
            permissions=user.custom_claims.get('permissions', []),
            organization_id=user.custom_claims.get('organization_id'),
            created_at=user.created_at.isoformat(),
            last_sign_in=user.last_sign_in.isoformat() if user.last_sign_in else None
        )
    
    # Routes
    @app.get("/health")
    async def health_check():
        settings = get_settings()
        return {
            "status": "healthy", 
            "service": "auth-service",
            "firebase_configured": bool(settings["firebase_project_id"] or settings["firebase_credentials_path"]),
            "debug": {
                "env_file_exists": os.path.exists(".env"),
                "current_directory": os.getcwd(),
                "has_project_id": bool(settings["firebase_project_id"]),
                "has_credentials_path": bool(settings["firebase_credentials_path"])
            }
        }
    
    @app.post("/users", response_model=UserResponse)
    async def create_user(request: CreateUserRequest):
        from auth_service.domain.models import UserRegistration
        
        registration = UserRegistration(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
            phone_number=request.phone_number
        )
        
        user = container.create_user_use_case.execute(registration, request.initial_role)
        return map_user_to_response(user)
    
    @app.post("/validate-token", response_model=UserResponse)
    async def validate_token(request: ValidateTokenRequest):
        user = container.validate_token_use_case.execute(request.token)
        return map_user_to_response(user)
    
    @app.get("/me", response_model=UserResponse)
    async def get_current_user_info(current_user=Depends(auth_middleware.require_auth)):
        return map_user_to_response(current_user)
    
    @app.get("/users/{user_id}", response_model=UserResponse)
    async def get_user_by_id(user_id: str, current_user=Depends(auth_middleware.require_auth)):
        user = container.auth_provider.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return map_user_to_response(user)
    
    @app.post("/users/assign-role", response_model=SuccessResponse)
    async def assign_role(
        request: AssignRoleRequest,
        current_user=Depends(auth_middleware.require_role("admin"))
    ):
        container.manage_roles_use_case.assign_role(request.user_id, request.role)
        return SuccessResponse(message=f"Rol '{request.role}' asignado al usuario {request.user_id}")
    
    @app.post("/users/assign-permission", response_model=SuccessResponse)
    async def assign_permission(
        request: AssignPermissionRequest,
        current_user=Depends(auth_middleware.require_role("admin"))
    ):
        container.manage_roles_use_case.assign_permission(request.user_id, request.permission)
        return SuccessResponse(message=f"Permiso '{request.permission}' asignado al usuario {request.user_id}")
    
    @app.delete("/users/{user_id}", response_model=SuccessResponse)
    async def delete_user(
        user_id: str,
        current_user=Depends(auth_middleware.require_role("admin"))
    ):
        container.auth_provider.delete_user(user_id)
        return SuccessResponse(message=f"Usuario {user_id} eliminado exitosamente")
    
    return app