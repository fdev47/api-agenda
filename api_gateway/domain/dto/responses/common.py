"""
DTOs de respuesta comunes para el API Gateway
"""
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Respuesta de éxito genérica"""
    message: str
    timestamp: str 