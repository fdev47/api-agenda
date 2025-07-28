"""
Implementación del repositorio para unidades de medida
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, func
from ...domain.interfaces.measurement_unit_repository import MeasurementUnitRepository
from ...domain.entities.measurement_unit_entity import MeasurementUnit
from ...domain.dto.requests.measurement_unit_requests import MeasurementUnitFilterRequest
from ..models.measurement_unit import MeasurementUnit as MeasurementUnitModel
from commons.database import get_db_session


class MeasurementUnitRepositoryImpl(MeasurementUnitRepository):
    """Implementación del repositorio para unidades de medida"""
    
    async def create(self, measurement_unit: MeasurementUnit) -> MeasurementUnit:
        """Crear una nueva unidad de medida"""
        async for session in get_db_session():
            # Verificar si ya existe una unidad con el mismo código
            if await self.exists_by_code(measurement_unit.code):
                raise ValueError(f"Ya existe una unidad de medida con el código '{measurement_unit.code}'")
            
            # Crear el modelo
            measurement_unit_model = MeasurementUnitModel(
                name=measurement_unit.name,
                code=measurement_unit.code,
                description=measurement_unit.description,
                is_active=measurement_unit.is_active
            )
            
            session.add(measurement_unit_model)
            await session.commit()
            await session.refresh(measurement_unit_model)
            
            # Retornar entidad del dominio
            return MeasurementUnit(
                id=measurement_unit_model.id,
                name=measurement_unit_model.name,
                code=measurement_unit_model.code,
                description=measurement_unit_model.description,
                is_active=measurement_unit_model.is_active,
                created_at=measurement_unit_model.created_at,
                updated_at=measurement_unit_model.updated_at
            )
    
    async def get_by_id(self, measurement_unit_id: int) -> Optional[MeasurementUnit]:
        """Obtener una unidad de medida por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(MeasurementUnitModel).where(MeasurementUnitModel.id == measurement_unit_id)
            )
            measurement_unit_model = result.scalar_one_or_none()
            
            if not measurement_unit_model:
                return None
            
            return MeasurementUnit(
                id=measurement_unit_model.id,
                name=measurement_unit_model.name,
                code=measurement_unit_model.code,
                description=measurement_unit_model.description,
                is_active=measurement_unit_model.is_active,
                created_at=measurement_unit_model.created_at,
                updated_at=measurement_unit_model.updated_at
            )
    
    async def get_by_code(self, code: str) -> Optional[MeasurementUnit]:
        """Obtener una unidad de medida por código"""
        async for session in get_db_session():
            result = await session.execute(
                select(MeasurementUnitModel).where(MeasurementUnitModel.code == code)
            )
            measurement_unit_model = result.scalar_one_or_none()
            
            if not measurement_unit_model:
                return None
            
            return MeasurementUnit(
                id=measurement_unit_model.id,
                name=measurement_unit_model.name,
                code=measurement_unit_model.code,
                description=measurement_unit_model.description,
                is_active=measurement_unit_model.is_active,
                created_at=measurement_unit_model.created_at,
                updated_at=measurement_unit_model.updated_at
            )
    
    async def list_all(self, filter_request: MeasurementUnitFilterRequest) -> Tuple[List[MeasurementUnit], int]:
        """Listar todas las unidades de medida con filtros"""
        async for session in get_db_session():
            query = select(MeasurementUnitModel)
            
            # Aplicar filtros
            if filter_request.name:
                query = query.where(MeasurementUnitModel.name.ilike(f"%{filter_request.name}%"))
            
            if filter_request.code:
                query = query.where(MeasurementUnitModel.code.ilike(f"%{filter_request.code}%"))
            
            if filter_request.is_active is not None:
                query = query.where(MeasurementUnitModel.is_active == filter_request.is_active)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación y ordenamiento
            query = query.offset(filter_request.offset).limit(filter_request.limit).order_by(MeasurementUnitModel.name)
            
            result = await session.execute(query)
            measurement_unit_models = result.scalars().all()
            
            # Convertir a entidades del dominio
            measurement_units = [
                MeasurementUnit(
                    id=model.id,
                    name=model.name,
                    code=model.code,
                    description=model.description,
                    is_active=model.is_active,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in measurement_unit_models
            ]
            
            return measurement_units, total
    
    async def update(self, measurement_unit_id: int, measurement_unit: MeasurementUnit) -> Optional[MeasurementUnit]:
        """Actualizar una unidad de medida"""
        async for session in get_db_session():
            result = await session.execute(
                select(MeasurementUnitModel).where(MeasurementUnitModel.id == measurement_unit_id)
            )
            measurement_unit_model = result.scalar_one_or_none()
            
            if not measurement_unit_model:
                return None
            
            # Verificar si ya existe otra unidad con el mismo código
            if await self.exists_by_code(measurement_unit.code, exclude_id=measurement_unit_id):
                raise ValueError(f"Ya existe una unidad de medida con el código '{measurement_unit.code}'")
            
            # Actualizar campos
            if measurement_unit.name is not None:
                measurement_unit_model.name = measurement_unit.name
            if measurement_unit.code is not None:
                measurement_unit_model.code = measurement_unit.code
            if measurement_unit.description is not None:
                measurement_unit_model.description = measurement_unit.description
            if measurement_unit.is_active is not None:
                measurement_unit_model.is_active = measurement_unit.is_active
            
            await session.commit()
            await session.refresh(measurement_unit_model)
            
            return MeasurementUnit(
                id=measurement_unit_model.id,
                name=measurement_unit_model.name,
                code=measurement_unit_model.code,
                description=measurement_unit_model.description,
                is_active=measurement_unit_model.is_active,
                created_at=measurement_unit_model.created_at,
                updated_at=measurement_unit_model.updated_at
            )
    
    async def delete(self, measurement_unit_id: int) -> bool:
        """Eliminar una unidad de medida"""
        async for session in get_db_session():
            result = await session.execute(
                select(MeasurementUnitModel).where(MeasurementUnitModel.id == measurement_unit_id)
            )
            measurement_unit_model = result.scalar_one_or_none()
            
            if not measurement_unit_model:
                return False
            
            await session.delete(measurement_unit_model)
            await session.commit()
            
            return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una unidad de medida con el código dado"""
        async for session in get_db_session():
            query = select(MeasurementUnitModel).where(MeasurementUnitModel.code == code)
            
            if exclude_id:
                query = query.where(MeasurementUnitModel.id != exclude_id)
            
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None
    
    async def exists_by_id(self, measurement_unit_id: int) -> bool:
        """Verificar si existe una unidad de medida con el ID dado"""
        async for session in get_db_session():
            result = await session.execute(
                select(MeasurementUnitModel).where(MeasurementUnitModel.id == measurement_unit_id)
            )
            return result.scalar_one_or_none() is not None 