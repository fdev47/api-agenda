"""
Utilidad para hacer solicitudes HTTP a las APIs
"""
import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional
from urllib.parse import urljoin


class APIClient:
    """Cliente para hacer solicitudes HTTP a las APIs"""
    
    def __init__(self, base_url: str, access_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Obtener headers para la solicitud"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        additional_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Realizar solicitud HTTP"""
        if not self.session:
            raise RuntimeError("APIClient debe usarse como context manager")
        
        url = urljoin(self.base_url, endpoint)
        headers = self._get_headers(additional_headers)
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            ) as response:
                response_text = await response.text()
                
                if response.status >= 400:
                    print(f"❌ Error HTTP {response.status}: {response_text}")
                    raise HTTPError(
                        status_code=response.status,
                        message=response_text,
                        url=url
                    )
                
                if response_text:
                    return json.loads(response_text)
                return {}
                
        except aiohttp.ClientError as e:
            print(f"❌ Error de conexión: {e}")
            raise ConnectionError(f"Error de conexión a {url}: {e}")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud GET"""
        return await self._make_request('GET', endpoint, params=params, additional_headers=headers)
    
    async def post(self, endpoint: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud POST"""
        return await self._make_request('POST', endpoint, data=data, additional_headers=headers)
    
    async def put(self, endpoint: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud PUT"""
        return await self._make_request('PUT', endpoint, data=data, additional_headers=headers)
    
    async def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud DELETE"""
        return await self._make_request('DELETE', endpoint, additional_headers=headers)


class HTTPError(Exception):
    """Excepción para errores HTTP"""
    
    def __init__(self, status_code: int, message: str, url: str):
        self.status_code = status_code
        self.message = message
        self.url = url
        super().__init__(f"HTTP {status_code}: {message}")


class ConnectionError(Exception):
    """Excepción para errores de conexión"""
    pass


# Función de conveniencia para crear cliente API
def create_api_client(base_url: str, access_token: Optional[str] = None) -> APIClient:
    """Crear un cliente API con la configuración especificada"""
    return APIClient(base_url, access_token) 