"""
Request DTO para filtrar reservas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReservationFilterRequest(BaseModel):
    """Request para filtrar reservas"""
    
    # Filtros por usuario/cliente
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    
    # Filtros por sucursal
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    
    # Filtros por sector
    sector_id: Optional[int] = None
    sector_name: Optional[str] = None
    
    # Filtros por cliente
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    
    # Filtros por fecha
    reservation_date_from: Optional[datetime] = None
    reservation_date_to: Optional[datetime] = None
    
    # Filtros por estado
    status: Optional[str] = None
    
    # Filtros por pedido
    order_code: Optional[str] = None
    
    # Paginación
    page: int = Field(1, ge=1, description="Número de página")
    limit: int = Field(10, ge=1, le=100, description="Elementos por página")
    
    @property
    def offset(self) -> int:
        """Calcular offset para paginación"""
        return (self.page - 1) * self.limit 