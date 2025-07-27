"""
Request DTO para números de pedido
"""
from pydantic import BaseModel, Field
from typing import Optional


class OrderNumberRequest(BaseModel):
    """Request para un número de pedido"""
    code: str = Field(..., min_length=1, max_length=50, description="Código del pedido")
    description: Optional[str] = Field(None, max_length=200, description="Descripción opcional del pedido") 