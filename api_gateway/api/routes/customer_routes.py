"""
Rutas de customers para API Gateway
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Optional
from ...infrastructure.container import Container
from ..middleware import auth_middleware
from ...domain.dto.responses.customer.customer_responses import CustomerResponse
from ...domain.dto.requests.customer.customer_requests import CreateCustomerRequest

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