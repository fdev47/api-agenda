"""
Response DTO para números de pedido
"""
from pydantic import BaseModel, Field
from typing import Optional


class OrderNumberResponse(BaseModel):
    """Response para un número de pedido"""
    code: str = Field(..., description="Código del pedido")
    description: Optional[str] = Field(None, description="Descripción del pedido") 