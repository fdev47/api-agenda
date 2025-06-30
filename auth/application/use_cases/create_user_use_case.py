"""
Caso de uso para crear usuarios
"""
from ...domain.interfaces import IAuthProvider, IUserClaimsManager
from ...domain.entities import UserRegistration, AuthenticatedUser
from ...domain.dto.requests import RegisterRequest
from ...domain.dto.responses import UserInfoResponse
from ...domain.exceptions import AuthError, AuthErrorCode


class CreateUserUseCase:
    """Caso de uso para crear usuarios"""
    
    def __init__(self, auth_provider: IAuthProvider, claims_manager: IUserClaimsManager):
        self._auth_provider = auth_provider
        self._claims_manager = claims_manager
    
    def execute(self, request: RegisterRequest) -> UserInfoResponse:
        """Ejecutar el caso de uso"""
        try:
            # Convertir request a entidad de dominio
            registration = UserRegistration(
                email=request.email,
                password=request.password,
                display_name=request.display_name,
                phone_number=request.phone_number
            )
            
            # Crear usuario
            user = self._auth_provider.create_user(registration)
            
            # Asignar rol inicial por defecto
            initial_role = "user"
            self._claims_manager.set_user_role(user.user_id, initial_role)
            
            # Obtener usuario actualizado con claims
            updated_user = self._auth_provider.get_user_by_id(user.user_id)
            
            if not updated_user:
                raise AuthError("Error al obtener usuario creado", AuthErrorCode.USER_NOT_FOUND.value)
            
            # Convertir a response DTO
            return UserInfoResponse(
                user_id=updated_user.user_id,
                email=updated_user.email,
                display_name=updated_user.display_name,
                phone_number=updated_user.phone_number,
                email_verified=updated_user.email_verified,
                custom_claims=updated_user.custom_claims,
                created_at=updated_user.created_at,
                last_sign_in=updated_user.last_sign_in
            )
            
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Error al crear usuario: {str(e)}", AuthErrorCode.USER_NOT_FOUND.value) 