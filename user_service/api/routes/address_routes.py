"""
Rutas para Address
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.dto.requests.address_requests import CreateAddressRequest, UpdateAddressRequest
from ...domain.dto.responses.address_responses import (
    AddressResponse, 
    AddressListResponse, 
    AddressCreatedResponse,
    AddressUpdatedResponse,
    AddressDeletedResponse
)
from ...application.use_cases.create_address_use_case import CreateAddressUseCase
from ...application.use_cases.get_address_use_case import GetAddressUseCase
from ...application.use_cases.list_addresses_use_case import ListAddressesUseCase
from ...application.use_cases.update_address_use_case import UpdateAddressUseCase
from ...application.use_cases.delete_address_use_case import DeleteAddressUseCase
from ...infrastructure.container import container
from ...infrastructure.connection import get_db_session
from ...domain.exceptions.user_exceptions import UserException, UserNotFoundException

router = APIRouter(tags=["Addresses"])

@router.post("/", response_model=AddressCreatedResponse)
async def create_address(
    request: CreateAddressRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Crear una nueva dirección"""
    try:
        container.db_session.override(db)
        create_use_case = container.create_address_use_case()
        result = await create_use_case.execute(request)
        return result
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/", response_model=AddressListResponse)
async def get_addresses(db: AsyncSession = Depends(get_db_session)):
    """Obtener todas las direcciones"""
    try:
        container.db_session.override(db)
        list_use_case = container.list_addresses_use_case()
        result = await list_use_case.execute()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Obtener una dirección por ID"""
    try:
        container.db_session.override(db)
        get_use_case = container.get_address_use_case()
        result = await get_use_case.execute(address_id)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.put("/{address_id}", response_model=AddressUpdatedResponse)
async def update_address(
    address_id: str, 
    request: UpdateAddressRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Actualizar una dirección"""
    try:
        container.db_session.override(db)
        update_use_case = container.update_address_use_case()
        result = await update_use_case.execute(address_id, request)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.delete("/{address_id}", response_model=AddressDeletedResponse)
async def delete_address(
    address_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Eliminar una dirección"""
    try:
        container.db_session.override(db)
        delete_use_case = container.delete_address_use_case()
        result = await delete_use_case.execute(address_id)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}") 