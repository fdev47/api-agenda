"""
Use Case para crear usuarios en la base de datos
Sigue Clean Architecture y SOLID principles
"""
from typing import Protocol
from ...domain.dto.requests.user_requests import CreateUserRequest
from ...domain.dto.responses.user_responses import UserResponse
from ...domain.entities.user import User
from ...domain.exceptions.user_exceptions import UserException, UserAlreadyExistsException


class UserRepository(Protocol):
    """Protocolo para el repositorio de usuarios"""
    async def create(self, user_data: CreateUserRequest) -> User:
        """Crear usuario en la base de datos"""
        ...


class CreateUserUseCase:
    """
    Use Case para crear usuarios en la base de datos
    
    Responsabilidades:
    - Crear usuario en PostgreSQL
    - Validar que el usuario no exista
    - Manejar errores de dominio
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializar el use case
        
        Args:
            user_repository: Repositorio para operaciones de base de datos
        """
        self.user_repository = user_repository
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        """
        Ejecutar la creación de usuario en la base de datos
        
        Args:
            request: Datos del usuario a crear (debe incluir auth_uid)
            
        Returns:
            UserResponse: Usuario creado exitosamente
            
        Raises:
            UserAlreadyExistsException: Si el usuario ya existe
            UserException: Si falla la creación en la base de datos
        """
        try:
            # Validar que se proporcione auth_uid
            if not request.auth_uid:
                raise UserException("auth_uid es requerido para crear usuario en la base de datos")
            
            # Crear usuario en la base de datos
            user = await self.user_repository.create(request)
            
            # Retornar respuesta
            return UserResponse.model_validate(user)
            
        except UserAlreadyExistsException:
            # Re-lanzar errores específicos de dominio
            raise
        except UserException:
            # Re-lanzar errores de dominio
            raise
        except Exception as e:
            # Convertir errores inesperados en errores de dominio
            raise UserException(
                f"Error inesperado al crear usuario en la base de datos: {str(e)}"
            ) 