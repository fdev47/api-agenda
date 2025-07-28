"""
Rutas para Customer
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from uuid import UUID
from ...domain.dto.requests.customer_requests import CreateCustomerRequest, UpdateCustomerRequest
from ...domain.dto.responses.customer_responses import (
    CustomerResponse,
    CustomerListResponse,
    CustomerUpdatedResponse,
    CustomerDeletedResponse
)
from ...application.use_cases.create_customer_use_case import CreateCustomerUseCase
from ...application.use_cases.get_customer_use_case import GetCustomerUseCase
from ...application.use_cases.list_customers_use_case import ListCustomersUseCase
from ...application.use_cases.update_customer_use_case import UpdateCustomerUseCase
from ...application.use_cases.delete_customer_use_case import DeleteCustomerUseCase
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
async def get_customers(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de elementos")
):
    """Obtener todos los customers"""
    try:
        list_use_case = container.list_customers_use_case()
        result = await list_use_case.execute(skip=skip, limit=limit)
        return result
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: UUID):
    """Obtener un customer por ID"""
    try:
        get_use_case = container.get_customer_use_case()
        result = await get_use_case.execute(customer_id)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.put("/{customer_id}", response_model=CustomerUpdatedResponse)
async def update_customer(customer_id: UUID, request: UpdateCustomerRequest):
    """Actualizar un customer"""
    try:
        update_use_case = container.update_customer_use_case()
        result = await update_use_case.execute(customer_id, request)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.delete("/{customer_id}", response_model=CustomerDeletedResponse)
async def delete_customer(customer_id: UUID):
    """Eliminar un customer"""
    try:
        delete_use_case = container.delete_customer_use_case()
        result = await delete_use_case.execute(customer_id)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}") 