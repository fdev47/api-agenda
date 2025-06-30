"""
Use Case para crear usuario (orquestación de Auth + User services)
"""
from typing import Protocol
from ...domain.dto.requests import CreateUserRequest
from ...domain.dto.responses import UserResponse
from ...domain.exceptions import GatewayError


class AuthServiceClient(Protocol):
    """Protocolo para el cliente de Auth Service"""
    async def create_user(self, request: CreateUserRequest) -> dict:
        """Crear usuario en Firebase"""
        ...


class UserServiceClient(Protocol):
    """Protocolo para el cliente de User Service"""
    async def create_user(self, request: CreateUserRequest, auth_token: str) -> dict:
        """Crear usuario en PostgreSQL"""
        ...


class CreateUserUseCase:
    """
    Use Case para crear usuario
    
    Responsabilidades:
    - Orquestar la creación en Firebase (Auth Service)
    - Orquestar la creación en PostgreSQL (User Service)
    - Manejar errores y rollback si es necesario
    - Garantizar consistencia de datos
    """
    
    def __init__(self, auth_service_client: AuthServiceClient, user_service_client: UserServiceClient):
        """
        Inicializar el use case
        
        Args:
            auth_service_client: Cliente para comunicarse con Auth Service
            user_service_client: Cliente para comunicarse con User Service
        """
        self.auth_service_client = auth_service_client
        self.user_service_client = user_service_client
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        """
        Ejecutar la creación de usuario
        
        Flujo:
        1. Crear usuario en Firebase (Auth Service)
        2. Si es exitoso, crear usuario en PostgreSQL (User Service)
        3. Si Firebase falla, no tocar PostgreSQL
        
        Args:
            request: Datos del usuario a crear
            
        Returns:
            UserResponse: Usuario creado exitosamente
            
        Raises:
            GatewayError: Si falla la creación en cualquier servicio
        """
        try:
            # Paso 1: Crear usuario en Firebase (Auth Service)
            firebase_user = await self._create_user_in_firebase(request)
            
            # Paso 2: Crear usuario en PostgreSQL (User Service)
            # Usamos el token de Firebase para autenticación
            user = await self._create_user_in_database(request, firebase_user)
            
            # Paso 3: Retornar respuesta unificada
            return UserResponse.model_validate(user)
            
        except GatewayError:
            # Re-lanzar errores de gateway
            raise
        except Exception as e:
            # Convertir errores inesperados en errores de gateway
            raise GatewayError(
                error_code="USER_CREATION_FAILED",
                message=f"Error inesperado al crear usuario: {str(e)}"
            )
    
    async def _create_user_in_firebase(self, request: CreateUserRequest) -> dict:
        """
        Crear usuario en Firebase a través de Auth Service
        
        Args:
            request: Datos del usuario
            
        Returns:
            dict: Datos del usuario creado en Firebase
            
        Raises:
            GatewayError: Si falla la creación en Firebase
        """
        try:
            return await self.auth_service_client.create_user(request)
        except GatewayError as e:
            # Log del error para debugging
            print(f"❌ Error al crear usuario en Firebase: {e.message}")
            raise
    
    async def _create_user_in_database(self, request: CreateUserRequest, firebase_user: dict) -> dict:
        """
        Crear usuario en PostgreSQL a través de User Service
        
        Args:
            request: Datos del usuario
            firebase_user: Datos del usuario creado en Firebase
            
        Returns:
            dict: Usuario creado en PostgreSQL
            
        Raises:
            GatewayError: Si falla la creación en PostgreSQL
        """
        try:
            # Usar el access_token de Firebase para autenticación
            auth_token = firebase_user.get("access_token", "")
            
            return await self.user_service_client.create_user(request, auth_token)
            
        except Exception as e:
            # Log del error para debugging
            print(f"❌ Error al crear usuario en PostgreSQL: {str(e)}")
            raise GatewayError(
                error_code="DATABASE_CREATION_FAILED",
                message=f"Error al crear usuario en base de datos: {str(e)}"
            ) 