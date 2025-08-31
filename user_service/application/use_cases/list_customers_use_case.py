"""
Caso de uso para listar customers
"""
from typing import List, Optional
from uuid import UUID
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.responses.customer_responses import CustomerListResponse, CustomerResponse
from ...domain.exceptions.user_exceptions import UserException

class ListCustomersUseCase:
    """Caso de uso para listar customers"""

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100,
        username: Optional[str] = None,
        company_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        ruc: Optional[str] = None,
        address_id: Optional[UUID] = None
    ) -> CustomerListResponse:
        """Ejecutar el caso de uso"""
        try:
            customers = await self.customer_repository.get_all(
                skip=skip, 
                limit=limit,
                username=username,
                company_name=company_name,
                is_active=is_active,
                ruc=ruc,
                address_id=address_id
            )
            total = len(customers)  # TODO: Implementar count en repository
            
            customer_responses = [CustomerResponse.model_validate(customer) for customer in customers]
            
            return CustomerListResponse(
                customers=customer_responses,
                total=total,
                skip=skip,
                limit=limit
            )
            
        except UserException:
            raise
        except Exception as e:
            raise UserException(f"Error inesperado al listar customers: {str(e)}") 