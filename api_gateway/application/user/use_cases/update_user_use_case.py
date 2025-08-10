"""
Use case para actualizar usuarios usando auth_service y user_service
"""
from uuid import UUID
from typing import Optional
from commons.api_client import APIClient
from commons.config import config
from commons.error_codes import ErrorCode
from commons.error_utils import raise_internal_error, raise_not_found_error
from ....domain.user.dto.requests.user_requests import UpdateUserRequest
from ....domain.user.dto.responses.user_responses import UserResponse


class UpdateUserUseCase:
    """Use case para actualizar usuarios usando auth_service y user_service"""
    
    def __init__(self):
        self.auth_service_url = config.AUTH_SERVICE_URL
        self.user_service_url = config.USER_SERVICE_URL
    
    async def execute(self, user_id: UUID, request: UpdateUserRequest, access_token: str = None) -> UserResponse:
        """
        Actualizar usuario en Firebase (si es necesario) y en la base de datos
        
        Args:
            user_id: ID del usuario a actualizar
            request: DTO con los datos a actualizar
            access_token: Token de acceso para las llamadas a los servicios
            
        Returns:
            UserResponse: Usuario actualizado
        """
        try:
            # 1. Obtener información del usuario para obtener el auth_uid
            user_info = await self._get_user_info(user_id, access_token)
            auth_uid = user_info["auth_uid"]
            
            # 2. Determinar si necesitamos actualizar Firebase
            needs_firebase_update = self._needs_firebase_update(request)
            
            if needs_firebase_update:
                await self._update_firebase_user(auth_uid, request, access_token)
            
            # 3. Actualizar usuario en la base de datos
            updated_user = await self._update_db_user(user_id, request, access_token)
            
            return updated_user
            
        except Exception as error:
            # Convertir string a dict
            import ast
            try:
                error_str = str(error)
                # Separar la parte después de los ":" para aislar el dict
                _, dict_part = error_str.split(":", 1)
                error_dict = ast.literal_eval(dict_part.strip())
                
                message = error_dict.get('message', 'Mensaje no disponible')
                error_code = error_dict.get('error_code', 'Código no disponible')

                print("Mensaje:", message)
                print("Código de error:", error_code)
                
                # Mapear el código de error a nuestros códigos
                if error_code == 'PHONE_NUMBER_EXISTS':
                    raise_internal_error(
                        message="El número de teléfono ya existe en el sistema. Intente con otro número.",
                        error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
                    )
                elif error_code == 'EMAIL_ALREADY_EXISTS':
                    raise_internal_error(
                        message="El email ya existe en el sistema. Intente con otro email.",
                        error_code=ErrorCode.USER_ALREADY_EXISTS.value
                    )
                elif error_code == 'WEAK_PASSWORD':
                    raise_internal_error(
                        message="La contraseña es demasiado débil.",
                        error_code=ErrorCode.VALIDATION_ERROR.value
                    )
                else:
                    # Usar el mensaje del error original
                    raise_internal_error(
                        message=message,
                        error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                    )
                    
            except Exception as parse_error:
                raise_internal_error(
                    message=f"Error actualizando usuario: {str(error)}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                )
    
    async def _get_user_info(self, user_id: UUID, access_token: str) -> dict:
        """Obtener información del usuario para obtener el auth_uid"""
        try:
            async with APIClient(self.user_service_url, access_token) as client:
                response = await client.get(f"{config.API_PREFIX}/users/{user_id}")
                return response
        except Exception as e:
            if "not found" in str(e).lower():
                raise_not_found_error(
                    message=f"Usuario con ID '{user_id}' no encontrado",
                    error_code=ErrorCode.USER_NOT_FOUND.value
                )
            else:
                raise_internal_error(
                    message=f"Error obteniendo información del usuario: {str(e)}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                )
    
    def _needs_firebase_update(self, request: UpdateUserRequest) -> bool:
        """Determinar si se necesita actualizar Firebase"""
        # Solo actualizar Firebase si se cambia email o phone
        return request.email is not None or request.phone is not None or request.cellphone_number is not None
    
    async def _update_firebase_user(self, auth_uid: str, request: UpdateUserRequest, access_token: str):
        """Actualizar usuario en Firebase"""
        try:
            async with APIClient(self.auth_service_url, access_token) as client:
                # Preparar datos para Firebase
                firebase_data = {}
                
                if request.email is not None:
                    firebase_data["email"] = request.email
                
                if request.phone is not None or request.cellphone_number is not None:
                    # Determinar el número de teléfono
                    if request.cellphone_number and request.cellphone_country_code:
                        firebase_data["phone_number"] = f"{request.cellphone_country_code}{request.cellphone_number}"
                    elif request.cellphone_number:
                        firebase_data["phone_number"] = request.cellphone_number
                    elif request.phone:
                        firebase_data["phone_number"] = request.phone
                
                # Solo actualizar si hay datos para Firebase
                if firebase_data:
                    await client.put(f"{config.API_PREFIX}/auth/users/{auth_uid}", data=firebase_data)
                
        except Exception as e:
            error_message = str(e)
            
            # Convertir string a dict usando la misma lógica
            import ast
            try:
                # Separar la parte después de los ":" para aislar el dict
                _, dict_part = error_message.split(":", 1)
                error_dict = ast.literal_eval(dict_part.strip())
                
                message = error_dict.get('message', 'Mensaje no disponible')
                error_code = error_dict.get('error_code', 'Código no disponible')
                
                # Mapear el código de error a nuestros códigos
                if error_code == 'PHONE_NUMBER_EXISTS':
                    raise_internal_error(
                        message="El número de teléfono ya existe en el sistema. Intente con otro número.",
                        error_code=ErrorCode.PHONE_NUMBER_EXISTS.value
                    )
                elif error_code == 'EMAIL_ALREADY_EXISTS':
                    raise_internal_error(
                        message="El email ya existe en el sistema. Intente con otro email.",
                        error_code=ErrorCode.USER_ALREADY_EXISTS.value
                    )
                elif error_code == 'WEAK_PASSWORD':
                    raise_internal_error(
                        message="La contraseña es demasiado débil.",
                        error_code=ErrorCode.VALIDATION_ERROR.value
                    )
                else:
                    # Usar el mensaje del error original
                    raise_internal_error(
                        message=message,
                        error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                    )
                    
            except Exception:
                # Si falla el parsing, usar el mensaje original
                raise_internal_error(
                    message=f"Error actualizando usuario en Firebase: {error_message}",
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
                )
    
    async def _update_db_user(self, user_id: UUID, request: UpdateUserRequest, access_token: str) -> UserResponse:
        """Actualizar usuario en la base de datos"""
        try:
            async with APIClient(self.user_service_url, access_token) as client:
                # Preparar datos para la BD (excluir campos que no se pueden actualizar)
                db_data = {}
                
                if request.email is not None:
                    db_data["email"] = request.email
                if request.first_name is not None:
                    db_data["first_name"] = request.first_name
                if request.last_name is not None:
                    db_data["last_name"] = request.last_name
                if request.phone is not None:
                    db_data["phone"] = request.phone
                if request.cellphone_number is not None:
                    db_data["cellphone_number"] = request.cellphone_number
                if request.cellphone_country_code is not None:
                    db_data["cellphone_country_code"] = request.cellphone_country_code
                if request.is_active is not None:
                    db_data["is_active"] = request.is_active
                if request.user_type is not None:
                    db_data["user_type"] = request.user_type
                if request.profile_ids is not None:
                    db_data["profile_ids"] = request.profile_ids
                
                response = await client.put(f"{config.API_PREFIX}/users/{user_id}", data=db_data)
                return response
                
        except Exception as e:
            raise_internal_error(
                message=f"Error actualizando usuario en la base de datos: {str(e)}",
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value
            )
