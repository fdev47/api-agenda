"""
Implementación del repositorio de Address
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from ...domain.interfaces.address_repository import AddressRepository
from ...domain.entities.address import Address
from ...infrastructure.models.address import AddressDB


class AddressRepositoryImpl(AddressRepository):
    """Implementación del repositorio de Address"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, address: Address) -> Address:
        """Crear una nueva dirección"""
        address_db = AddressDB(
            street=address.street,
            city_id=address.city_id,
            state_id=address.state_id,
            country_id=address.country_id,
            postal_code=address.postal_code,
            additional_info=address.additional_info
        )
        
        self.session.add(address_db)
        await self.session.commit()
        await self.session.refresh(address_db)
        
        return Address(
            id=address_db.id,
            street=address_db.street,
            city_id=address_db.city_id,
            state_id=address_db.state_id,
            country_id=address_db.country_id,
            postal_code=address_db.postal_code,
            additional_info=address_db.additional_info
        )
    
    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        """Obtener una dirección por ID"""
        result = await self.session.execute(
            select(AddressDB).where(AddressDB.id == address_id)
        )
        address_db = result.scalar_one_or_none()
        
        if not address_db:
            return None
        
        return Address(
            id=address_db.id,
            street=address_db.street,
            city_id=address_db.city_id,
            state_id=address_db.state_id,
            country_id=address_db.country_id,
            postal_code=address_db.postal_code,
            additional_info=address_db.additional_info
        )
    
    async def get_all(self) -> List[Address]:
        """Obtener todas las direcciones"""
        result = await self.session.execute(select(AddressDB))
        addresses_db = result.scalars().all()
        
        return [
            Address(
                id=address_db.id,
                street=address_db.street,
                city_id=address_db.city_id,
                state_id=address_db.state_id,
                country_id=address_db.country_id,
                postal_code=address_db.postal_code,
                additional_info=address_db.additional_info
            )
            for address_db in addresses_db
        ]
    
    async def update(self, address_id: UUID, address: Address) -> Optional[Address]:
        """Actualizar una dirección"""
        result = await self.session.execute(
            update(AddressDB)
            .where(AddressDB.id == address_id)
            .values(
                street=address.street,
                city_id=address.city_id,
                state_id=address.state_id,
                country_id=address.country_id,
                postal_code=address.postal_code,
                additional_info=address.additional_info
            )
        )
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(address_id)
        return None
    
    async def delete(self, address_id: UUID) -> bool:
        """Eliminar una dirección"""
        result = await self.session.execute(
            delete(AddressDB).where(AddressDB.id == address_id)
        )
        await self.session.commit()
        
        return result.rowcount > 0 