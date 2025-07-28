"""
Rutas para Customer
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...domain.dto.requests.customer_requests import CreateCustomerRequest, UpdateCustomerRequest
from ...domain.dto.responses.customer_responses import (
    CustomerResponse,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdatedResponse,
    CustomerDeletedResponse
)
from ...application.use_cases.create_customer_use_case import CreateCustomerUseCase
from ...infrastructure.container import container
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse)
async def create_customer(request: CreateCustomerRequest):
    """Crear un nuevo customer"""
    try:
        create_use_case = container.create_customer_use_case()
        result = await create_use_case.execute(request)
        return result
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/", response_model=CustomerListResponse)
async def get_customers():
    """Obtener todos los customers"""
    try:
        # TODO: Implementar list customers use case
        raise HTTPException(status_code=501, detail="Not implemented yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str):
    """Obtener un customer por ID"""
    try:
        # TODO: Implementar get customer use case
        raise HTTPException(status_code=501, detail="Not implemented yet")
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.put("/{customer_id}", response_model=CustomerUpdatedResponse)
async def update_customer(customer_id: str, request: UpdateCustomerRequest):
    """Actualizar un customer"""
    try:
        # TODO: Implementar update customer use case
        raise HTTPException(status_code=501, detail="Not implemented yet")
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.delete("/{customer_id}", response_model=CustomerDeletedResponse)
async def delete_customer(customer_id: str):
    """Eliminar un customer"""
    try:
        # TODO: Implementar delete customer use case
        raise HTTPException(status_code=501, detail="Not implemented yet")
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}") 