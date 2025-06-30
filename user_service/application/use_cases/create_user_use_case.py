"""
Use Case para crear usuarios
Sigue Clean Architecture y SOLID principles
"""
from typing import Protocol
from ...domain.dto.requests.user_requests import CreateUserRequest
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.entities.user import User
from ...domain.exceptions.user_exceptions import UserException


class UserRepository(Protocol):
    """Protocolo para el repositorio de usuarios"""
    async def create(self, user_data: CreateUserRequest) -> User:
        """Crear usuario en la base de datos"""
        ...


class AuthServiceClient(Protocol):
    """Protocolo para el cliente de Auth Service"""
    async def create_user(self, request: CreateUserRequest) -> dict:
        """Crear usuario en el proveedor de autenticación"""
        ...


class CreateUserUseCase:
    """
    Use Case para crear usuarios
    
    Responsabilidades:
    - Orquestar la creación de usuario en el proveedor de auth y PostgreSQL
    - Manejar errores y rollback si es necesario
    - Garantizar consistencia de datos
    """
    
    def __init__(self, user_repository: UserRepository, auth_service_client: AuthServiceClient):
        """
        Inicializar el use case
        
        Args:
            user_repository: Repositorio para operaciones de base de datos
            auth_service_client: Cliente para comunicarse con Auth Service
        """
        self.user_repository = user_repository
        self.auth_service_client = auth_service_client
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        """
        Ejecutar la creación de usuario
        
        Flujo:
        1. Crear usuario en el proveedor de auth (Auth Service)
        2. Si es exitoso, crear usuario en PostgreSQL
        3. Si el auth falla, no tocar la base de datos
        
        Args:
            request: Datos del usuario a crear
            
        Returns:
            UserResponse: Usuario creado exitosamente
            
        Raises:
            UserException: Si falla la creación en el auth o PostgreSQL
        """
        try:
            # Paso 1: Crear usuario en el proveedor de auth (Auth Service)
            auth_user = await self._create_user_in_auth(request)
            
            # Paso 2: Crear usuario en PostgreSQL
            user = await self._create_user_in_database(request, auth_user)
            
            # Paso 3: Retornar respuesta
            return UserResponse.model_validate(user)
            
        except UserException:
            # Re-lanzar errores de dominio
            raise
        except Exception as e:
            # Convertir errores inesperados en errores de dominio
            raise UserException(
                f"Error inesperado al crear usuario: {str(e)}"
            )
    
    async def _create_user_in_auth(self, request: CreateUserRequest) -> dict:
        """
        Crear usuario en el proveedor de autenticación a través de Auth Service
        
        Args:
            request: Datos del usuario
            
        Returns:
            dict: Datos del usuario creado en el auth
            
        Raises:
            UserException: Si falla la creación en el auth
        """
        try:
            return await self.auth_service_client.create_user(request)
        except UserException as e:
            # Log del error para debugging
            print(f"❌ Error al crear usuario en auth: {e.message}")
            raise
    
    async def _create_user_in_database(self, request: CreateUserRequest, auth_user: dict) -> User:
        """
        Crear usuario en la base de datos PostgreSQL
        
        Args:
            request: Datos del usuario
            auth_user: Datos del usuario creado en el auth
            
        Returns:
            User: Usuario creado en la base de datos
            
        Raises:
            UserException: Si falla la creación en la base de datos
        """
        try:
            # Actualizar el auth_uid con el ID del proveedor de auth
            request.auth_uid = auth_user.get("user_id")
            
            return await self.user_repository.create(request)
            
        except Exception as e:
            # Log del error para debugging
            print(f"❌ Error al crear usuario en base de datos: {str(e)}")
            raise UserException(
                f"Error al crear usuario en base de datos: {str(e)}"
            ) 