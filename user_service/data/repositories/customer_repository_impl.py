"""
Implementación del repositorio de Customer
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.entities.customer import Customer
from ...domain.exceptions.user_exceptions import (
    CustomerAuthUidAlreadyExistsException,
    CustomerRucAlreadyExistsException,
    CustomerEmailAlreadyExistsException,
    CustomerUsernameAlreadyExistsException
)
from ...infrastructure.models.customer import CustomerDB


class CustomerRepositoryImpl(CustomerRepository):
    """Implementación del repositorio de Customer"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, customer: Customer) -> Customer:
        """Crear un nuevo customer"""
        customer_db = CustomerDB(
            auth_uid=customer.auth_uid,
            ruc=customer.ruc,
            company_name=customer.company_name,
            email=customer.email,
            username=customer.username,
            phone=customer.phone,
            cellphone_number=customer.cellphone_number,
            cellphone_country_code=customer.cellphone_country_code,
            address_id=customer.address_id,
            is_active=customer.is_active
        )

        self.session.add(customer_db)
        
        try:
            await self.session.commit()
            await self.session.refresh(customer_db)
        except IntegrityError as e:
            await self.session.rollback()
            error_msg = str(e.orig).lower()
            
            if 'auth_uid' in error_msg or 'customers_auth_uid_key' in error_msg:
                raise CustomerAuthUidAlreadyExistsException(customer.auth_uid)
            elif 'ruc' in error_msg or 'customers_ruc_key' in error_msg:
                raise CustomerRucAlreadyExistsException(customer.ruc)
            elif 'email' in error_msg or 'customers_email_key' in error_msg:
                raise CustomerEmailAlreadyExistsException(customer.email)
            elif 'username' in error_msg or 'customers_username_key' in error_msg:
                raise CustomerUsernameAlreadyExistsException(customer.username)
            else:
                raise

        return Customer(
            id=customer_db.id,
            auth_uid=customer_db.auth_uid,
            ruc=customer_db.ruc,
            company_name=customer_db.company_name,
            email=customer_db.email,
            username=customer_db.username,
            phone=customer_db.phone,
            cellphone_number=customer_db.cellphone_number,
            cellphone_country_code=customer_db.cellphone_country_code,
            address_id=customer_db.address_id,
            is_active=customer_db.is_active
        )

    async def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """Obtener un customer por ID"""
        result = await self.session.execute(
            select(CustomerDB).where(CustomerDB.id == customer_id)
        )
        customer_db = result.scalar_one_or_none()

        if not customer_db:
            return None

        return Customer(
            id=customer_db.id,
            auth_uid=customer_db.auth_uid,
            ruc=customer_db.ruc,
            company_name=customer_db.company_name,
            email=customer_db.email,
            username=customer_db.username,
            phone=customer_db.phone,
            cellphone_number=customer_db.cellphone_number,
            cellphone_country_code=customer_db.cellphone_country_code,
            address_id=customer_db.address_id,
            is_active=customer_db.is_active
        )

    async def get_by_auth_uid(self, auth_uid: str) -> Optional[Customer]:
        """Obtener un customer por auth_uid"""
        result = await self.session.execute(
            select(CustomerDB).where(CustomerDB.auth_uid == auth_uid)
        )
        customer_db = result.scalar_one_or_none()

        if not customer_db:
            return None

        return Customer(
            id=customer_db.id,
            auth_uid=customer_db.auth_uid,
            ruc=customer_db.ruc,
            company_name=customer_db.company_name,
            email=customer_db.email,
            username=customer_db.username,
            phone=customer_db.phone,
            cellphone_number=customer_db.cellphone_number,
            cellphone_country_code=customer_db.cellphone_country_code,
            address_id=customer_db.address_id,
            is_active=customer_db.is_active
        )

    async def get_by_username(self, username: str) -> Optional[Customer]:
        """Obtener un customer por username"""
        result = await self.session.execute(
            select(CustomerDB).where(CustomerDB.username == username)
        )
        customer_db = result.scalar_one_or_none()

        if not customer_db:
            return None

        return Customer(
            id=customer_db.id,
            auth_uid=customer_db.auth_uid,
            ruc=customer_db.ruc,
            company_name=customer_db.company_name,
            email=customer_db.email,
            username=customer_db.username,
            phone=customer_db.phone,
            cellphone_number=customer_db.cellphone_number,
            cellphone_country_code=customer_db.cellphone_country_code,
            address_id=customer_db.address_id,
            is_active=customer_db.is_active
        )

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        username: Optional[str] = None,
        company_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        ruc: Optional[str] = None,
        address_id: Optional[UUID] = None
    ) -> List[Customer]:
        """Obtener todos los customers con filtros opcionales"""
        query = select(CustomerDB)
        
        if username:
            query = query.where(CustomerDB.username.ilike(f"%{username}%"))
        
        if company_name:
            query = query.where(CustomerDB.company_name.ilike(f"%{company_name}%"))
            
        if is_active is not None:
            query = query.where(CustomerDB.is_active == is_active)
            
        if ruc:
            query = query.where(CustomerDB.ruc == ruc)
            
        if address_id:
            query = query.where(CustomerDB.address_id == address_id)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        customers_db = result.scalars().all()

        return [
            Customer(
                id=customer_db.id,
                auth_uid=customer_db.auth_uid,
                ruc=customer_db.ruc,
                company_name=customer_db.company_name,
                email=customer_db.email,
                username=customer_db.username,
                phone=customer_db.phone,
                cellphone_number=customer_db.cellphone_number,
                cellphone_country_code=customer_db.cellphone_country_code,
                address_id=customer_db.address_id,
                is_active=customer_db.is_active
            )
            for customer_db in customers_db
        ]

    async def update(self, customer_id: UUID, update_data: dict) -> Optional[Customer]:
        """Actualizar un customer"""
        existing_customer = await self.get_by_id(customer_id)
        if not existing_customer:
            return None
        
        update_values = {}
        for field, value in update_data.items():
            if hasattr(existing_customer, field) and value is not None:
                update_values[field] = value
        
        if not update_values:
            return existing_customer  # No hay cambios
        
        try:
            result = await self.session.execute(
                update(CustomerDB)
                .where(CustomerDB.id == customer_id)
                .values(**update_values)
            )
            await self.session.commit()

            if result.rowcount > 0:
                return await self.get_by_id(customer_id)
            return None
        except IntegrityError as e:
            await self.session.rollback()
            error_msg = str(e.orig).lower()
            
            if 'auth_uid' in error_msg or 'customers_auth_uid_key' in error_msg:
                raise CustomerAuthUidAlreadyExistsException(update_values.get('auth_uid', ''))
            elif 'ruc' in error_msg or 'customers_ruc_key' in error_msg:
                raise CustomerRucAlreadyExistsException(update_values.get('ruc', ''))
            elif 'email' in error_msg or 'customers_email_key' in error_msg:
                raise CustomerEmailAlreadyExistsException(update_values.get('email', ''))
            elif 'username' in error_msg or 'customers_username_key' in error_msg:
                raise CustomerUsernameAlreadyExistsException(update_values.get('username', ''))
            else:
                raise

    async def delete(self, customer_id: UUID) -> bool:
        """Eliminar un customer"""
        result = await self.session.execute(
            delete(CustomerDB).where(CustomerDB.id == customer_id)
        )
        await self.session.commit()

        return result.rowcount > 0 