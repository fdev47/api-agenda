"""
Cliente para comunicarse con User Service
"""
import httpx
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()

from commons.config import config

class UserServiceClient:
    """Cliente para comunicarse con User Service"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.USER_SERVICE_URL
        self.api_prefix = config.API_PREFIX
        self.timeout = 10.0  # 10 segundos timeout
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear usuario en User Service
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/users/"
                
                response = await client.post(url, json=user_data)
                
                if response.status_code == 201:
                    return response.json()
                else:
                    error_data = response.json()
                    raise Exception(f"Error al crear usuario: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con User Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con User Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Obtener usuario por ID
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/users/{user_id}"
                
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    error_data = response.json()
                    raise Exception(f"Error al obtener usuario: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con User Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con User Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def get_current_user(self, token: str) -> Dict[str, Any]:
        """
        Obtener usuario actual
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/users/me"
                
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    error_data = response.json()
                    raise Exception(f"Error al obtener usuario actual: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con User Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con User Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Listar usuarios
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/users/?skip={skip}&limit={limit}"
                
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    error_data = response.json()
                    raise Exception(f"Error al listar usuarios: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con User Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con User Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar usuario
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/users/{user_id}"
                
                response = await client.put(url, json=user_data)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    error_data = response.json()
                    raise Exception(f"Error al actualizar usuario: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con User Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con User Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Eliminar usuario
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/users/{user_id}"
                
                response = await client.delete(url)
                
                if response.status_code == 204:
                    return True
                else:
                    error_data = response.json()
                    raise Exception(f"Error al eliminar usuario: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con User Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con User Service: {str(e)}")
        except Exception as e:
            raise e 