"""
Rutas de customers para API Gateway
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from typing import Optional
from uuid import UUID
from ...infrastructure.container import Container
from ..middleware import auth_middleware
from ...domain.customer.dto.responses.customer_responses import CustomerResponse, CustomerListResponse, CustomerUpdatedResponse, CustomerDeletedResponse
from ...domain.customer.dto.requests.customer_requests import CreateCustomerRequest, UpdateCustomerRequest

router = APIRouter()


def get_container() -> Container:
    """Obtener el container de dependencias"""
    return Container()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    request: CreateCustomerRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Crear nuevo customer (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Crear customer usando el use case
    create_customer_use_case = container.create_customer_use_case()
    customer = await create_customer_use_case.execute(request, access_token)
    
    return customer


@router.get("/me", response_model=CustomerResponse)
async def get_current_customer(
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener información del customer actual"""
    auth_uid = current_user["user_id"]
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Obtener customer usando el use case
    get_customer_use_case = container.get_customer_use_case()
    customer = await get_customer_use_case.execute(auth_uid, access_token)
    
    return customer


@router.get("/by-username/{username}", response_model=CustomerResponse)
async def get_customer_by_username(
    username: str,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Obtener customer por username (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Obtener customer por username usando el use case
    get_customer_by_username_use_case = container.get_customer_by_username_use_case()
    customer = await get_customer_by_username_use_case.execute(username, access_token)
    
    return customer


@router.get("/", response_model=CustomerListResponse)
async def list_customers(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(100, ge=1, le=1000, description="Número de registros por página"),
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Listar customers (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Obtener lista de customers usando el use case
    list_customers_use_case = container.list_customers_use_case()
    customers = await list_customers_use_case.execute(page=page, size=size, access_token=access_token)
    
    return customers


@router.put("/{customer_id}", response_model=CustomerUpdatedResponse)
async def update_customer(
    customer_id: UUID,
    request: UpdateCustomerRequest,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Actualizar customer (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Actualizar customer usando el use case
    update_customer_use_case = container.update_customer_use_case()
    customer = await update_customer_use_case.execute(customer_id, request, access_token)
    
    return customer


@router.delete("/{customer_id}", response_model=CustomerDeletedResponse)
async def delete_customer(
    customer_id: UUID,
    container: Container = Depends(get_container),
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """Eliminar customer (requiere autenticación)"""
    access_token = authorization.replace("Bearer ", "") if authorization else ""
    
    # Eliminar customer usando el use case
    delete_customer_use_case = container.delete_customer_use_case()
    result = await delete_customer_use_case.execute(customer_id, access_token)
    
    return result 