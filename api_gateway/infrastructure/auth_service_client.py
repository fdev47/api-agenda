"""
Cliente para comunicarse con Auth Service
"""
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

from commons.config import config

class AuthServiceClient:
    """Cliente para comunicarse con Auth Service"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.AUTH_SERVICE_URL
        self.api_prefix = config.API_PREFIX
        self.timeout = 10.0  # 10 segundos timeout
    
    async def create_user(self, email: str, password: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear usuario en Firebase a través del Auth Service
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/auth/create-user"
                
                payload = {
                    "email": email,
                    "password": password
                }
                
                if display_name:
                    payload["display_name"] = display_name
                
                response = await client.post(url, json=payload)
                
                if response.status_code == 201:
                    return response.json()
                else:
                    error_data = response.json()
                    raise Exception(f"Error al crear usuario: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con Auth Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con Auth Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validar token de Firebase a través del Auth Service
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/auth/validate-token"
                
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        return data.get("user", {})
                    else:
                        raise Exception(data.get("message", "Token inválido"))
                else:
                    error_data = response.json()
                    raise Exception(f"Error al validar token: {error_data.get('message', 'Error desconocido')}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con Auth Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con Auth Service: {str(e)}")
        except Exception as e:
            raise e 