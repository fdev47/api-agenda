"""
Utilidad para hacer solicitudes HTTP a las APIs
"""
import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional
from urllib.parse import urljoin, urlencode


class APIClient:
    """Cliente para hacer solicitudes HTTP a las APIs"""
    
    def __init__(self, base_url: str, access_token: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Context manager entry"""
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)
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
        
        # Construir URL con parámetros codificados correctamente
        url = urljoin(self.base_url, endpoint)
        
        # Codificar parámetros de query si existen
        if params:
            # Filtrar parámetros None y convertir a string
            filtered_params = {}
            for k, v in params.items():
                if v is not None:
                    # Manejar diferentes tipos de datos
                    if isinstance(v, (list, tuple)):
                        # Para listas, mantener como lista para doseq=True
                        filtered_params[k] = v
                    elif isinstance(v, bool):
                        # Para booleanos, convertir a string
                        filtered_params[k] = str(v).lower()
                    elif isinstance(v, (int, float)):
                        # Para números, convertir a string
                        filtered_params[k] = str(v)
                    else:
                        # Para strings y otros tipos, convertir a string
                        filtered_params[k] = str(v)
            
            if filtered_params:
                # Usar urlencode para codificar correctamente los parámetros
                # Preservar la 'T' en fechas ISO usando safe='T'
                encoded_params = urlencode(filtered_params, doseq=True, safe='T')
                # Agregar parámetros a la URL
                separator = '&' if '?' in url else '?'
                url = f"{url}{separator}{encoded_params}"
        
        headers = self._get_headers(additional_headers)
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                json=data,
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
                
                # Manejar diferentes tipos de respuesta
                if response.status == 204:  # No Content
                    return {}
                
                if response_text:
                    # Intentar parsear como JSON
                    try:
                        return json.loads(response_text)
                    except json.JSONDecodeError:
                        # Si no es JSON, devolver como texto
                        return {"content": response_text, "content_type": "text"}
                
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
    
    async def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud PUT"""
        return await self._make_request('PUT', endpoint, data=data, params=params, additional_headers=headers)
    
    async def patch(self, endpoint: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud PATCH"""
        return await self._make_request('PATCH', endpoint, data=data, additional_headers=headers)
    
    async def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud DELETE"""
        return await self._make_request('DELETE', endpoint, additional_headers=headers)
    
    async def head(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud HEAD"""
        return await self._make_request('HEAD', endpoint, params=params, additional_headers=headers)
    
    async def options(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realizar solicitud OPTIONS"""
        return await self._make_request('OPTIONS', endpoint, params=params, additional_headers=headers)


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
def create_api_client(base_url: str, access_token: Optional[str] = None, timeout: int = 30) -> APIClient:
    """Crear un cliente API con la configuración especificada"""
    return APIClient(base_url, access_token, timeout) 