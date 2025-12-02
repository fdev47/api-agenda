"""
Request DTO para exportar reservas
"""
from pydantic import BaseModel, Field
from typing import Optional


class ExportReservationsRequest(BaseModel):
    """Request para exportar reservas"""
    
    # Filtros por usuario/cliente
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    
    # Filtros por sucursal
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    branch_code: Optional[str] = None
    
    # Filtros por sector
    sector_id: Optional[int] = None
    sector_name: Optional[str] = None
    
    # Filtros por cliente
    customer_ruc: Optional[str] = None
    company_name: Optional[str] = None
    
    # Filtros por fecha (como strings para parsear en el use case)
    reservation_date_from: Optional[str] = None
    reservation_date_to: Optional[str] = None
    
    # Filtros por estado
    reservation_status: Optional[str] = None
    
    # Filtros por pedido
    order_code: Optional[str] = None
    
    # Filtros por tipo de carga
    cargo_type: Optional[str] = None

