"""
Cliente para comunicarse con Location Service
"""
import httpx
import asyncio
import os
from typing import Optional, Dict, Any, List
from uuid import UUID
from dotenv import load_dotenv

load_dotenv()

from commons.config import config

class LocationServiceClient:
    """Cliente para comunicarse con Location Service"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.LOCATION_SERVICE_URL
        self.api_prefix = config.API_PREFIX
        self.timeout = 10.0  # 10 segundos timeout
    
    async def get_country(self, country_id: UUID) -> Optional[Dict[str, Any]]:
        """Obtener país por ID"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/v1/countries/{country_id}"
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    raise Exception(f"Error al obtener país: {response.status_code}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con Location Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con Location Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def get_state(self, state_id: UUID) -> Optional[Dict[str, Any]]:
        """Obtener estado por ID"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/v1/states/{state_id}"
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    raise Exception(f"Error al obtener estado: {response.status_code}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con Location Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con Location Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def get_city(self, city_id: UUID) -> Optional[Dict[str, Any]]:
        """Obtener ciudad por ID"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{self.api_prefix}/v1/cities/{city_id}"
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    raise Exception(f"Error al obtener ciudad: {response.status_code}")
                    
        except httpx.TimeoutException:
            raise Exception("Timeout al comunicarse con Location Service")
        except httpx.RequestError as e:
            raise Exception(f"Error de comunicación con Location Service: {str(e)}")
        except Exception as e:
            raise e
    
    async def get_location_details(self, country_id: UUID, state_id: UUID, city_id: UUID) -> Dict[str, Any]:
        """Obtener detalles completos de ubicación"""
        try:
            # Obtener todos los datos en concurrencia
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                country_url = f"{self.base_url}{self.api_prefix}/v1/countries/{country_id}"
                state_url = f"{self.base_url}{self.api_prefix}/v1/states/{state_id}"
                city_url = f"{self.base_url}{self.api_prefix}/v1/cities/{city_id}"
                
                # Hacer requests en concurrencia
                responses = await asyncio.gather(
                    client.get(country_url),
                    client.get(state_url),
                    client.get(city_url),
                    return_exceptions=True
                )
                
                # Procesar respuestas
                country_data = None
                state_data = None
                city_data = None
                
                if not isinstance(responses[0], Exception) and responses[0].status_code == 200:
                    country_data = responses[0].json()
                
                if not isinstance(responses[1], Exception) and responses[1].status_code == 200:
                    state_data = responses[1].json()
                
                if not isinstance(responses[2], Exception) and responses[2].status_code == 200:
                    city_data = responses[2].json()
                
                return {
                    "country": country_data,
                    "state": state_data,
                    "city": city_data
                }
                
        except Exception as e:
            raise Exception(f"Error al obtener detalles de ubicación: {str(e)}")
    
    async def validate_location_ids(self, country_id: UUID, state_id: UUID, city_id: UUID) -> bool:
        """Validar que los IDs de ubicación existen y son consistentes"""
        try:
            # Obtener ciudad y verificar que pertenece al estado
            city_data = await self.get_city(city_id)
            if not city_data:
                return False
            
            # Verificar que la ciudad pertenece al estado
            if city_data.get("state_id") != str(state_id):
                return False
            
            # Obtener estado y verificar que pertenece al país
            state_data = await self.get_state(state_id)
            if not state_data:
                return False
            
            # Verificar que el estado pertenece al país
            if state_data.get("country_id") != str(country_id):
                return False
            
            # Verificar que el país existe
            country_data = await self.get_country(country_id)
            if not country_data:
                return False
            
            return True
            
        except Exception:
            return False 