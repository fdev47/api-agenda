"""
DTO de response para número de pedido en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional


class OrderNumberResponse(BaseModel):
    """DTO para número de pedido"""
    code: str = Field(..., description="Código del pedido")
    description: Optional[str] = Field(None, description="Descripción del pedido") 