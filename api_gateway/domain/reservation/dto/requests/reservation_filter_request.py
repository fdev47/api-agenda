"""
DTO de request para filtros de reserva en el API Gateway
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ReservationFilterRequest(BaseModel):
    """DTO para filtrar reservas"""
    # Filtros por usuario/cliente
    user_id: Optional[int] = Field(None, gt=0, description="ID del usuario")
    customer_id: Optional[int] = Field(None, gt=0, description="ID del cliente")
    
    # Filtros por sucursal
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")
    branch_name: Optional[str] = Field(None, description="Nombre de la sucursal")
    
    # Filtros por sector
    sector_id: Optional[int] = Field(None, gt=0, description="ID del sector")
    sector_type_id: Optional[int] = Field(None, gt=0, description="ID del tipo de sector")
    
    # Filtros por fecha
    start_date: Optional[datetime] = Field(None, description="Fecha de inicio para filtrar")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin para filtrar")
    
    # Filtros por estado
    status: Optional[str] = Field(None, description="Estado de la reserva")
    status_list: Optional[List[str]] = Field(None, description="Lista de estados")
    
    # Filtros por pedido
    order_code: Optional[str] = Field(None, description="Código de pedido")
    
    # Paginación
    skip: int = Field(default=0, ge=0, description="Número de registros a omitir")
    limit: int = Field(default=100, ge=1, le=1000, description="Número máximo de registros")
    
    # Ordenamiento
    sort_by: Optional[str] = Field(None, description="Campo para ordenar")
    sort_order: Optional[str] = Field(None, description="Orden (asc/desc)") 