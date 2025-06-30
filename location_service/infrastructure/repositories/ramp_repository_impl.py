"""
Implementación del repositorio para rampas
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ...domain.interfaces.ramp_repository import RampRepository
from ...domain.entities.ramp import Ramp
from ...domain.dto.requests.ramp_requests import RampFilterRequest
from ..models.ramp import Ramp as RampModel


class RampRepositoryImpl(RampRepository):
    """Implementación del repositorio para rampas"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, ramp: Ramp) -> Ramp:
        """Crear una nueva rampa"""
        ramp_model = RampModel(
            name=ramp.name,
            is_available=ramp.is_available,
            branch_id=ramp.branch_id
        )
        
        self.session.add(ramp_model)
        self.session.commit()
        self.session.refresh(ramp_model)
        
        return Ramp(
            id=ramp_model.id,
            name=ramp_model.name,
            is_available=ramp_model.is_available,
            branch_id=ramp_model.branch_id,
            created_at=ramp_model.created_at,
            updated_at=ramp_model.updated_at
        )
    
    async def get_by_id(self, ramp_id: int) -> Optional[Ramp]:
        """Obtener una rampa por ID"""
        ramp_model = self.session.query(RampModel).filter(RampModel.id == ramp_id).first()
        
        if not ramp_model:
            return None
        
        return Ramp(
            id=ramp_model.id,
            name=ramp_model.name,
            is_available=ramp_model.is_available,
            branch_id=ramp_model.branch_id,
            created_at=ramp_model.created_at,
            updated_at=ramp_model.updated_at
        )
    
    async def get_by_branch_id(self, branch_id: int) -> List[Ramp]:
        """Obtener todas las rampas de una sucursal"""
        ramp_models = self.session.query(RampModel).filter(
            RampModel.branch_id == branch_id
        ).order_by(RampModel.name).all()
        
        return [
            Ramp(
                id=ramp_model.id,
                name=ramp_model.name,
                is_available=ramp_model.is_available,
                branch_id=ramp_model.branch_id,
                created_at=ramp_model.created_at,
                updated_at=ramp_model.updated_at
            )
            for ramp_model in ramp_models
        ]
    
    async def list(self, filter_request: RampFilterRequest) -> tuple[List[Ramp], int]:
        """Listar rampas con filtros y paginación"""
        query = self.session.query(RampModel)
        
        # Aplicar filtros
        if filter_request.name:
            query = query.filter(RampModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.branch_id:
            query = query.filter(RampModel.branch_id == filter_request.branch_id)
        
        if filter_request.is_available is not None:
            query = query.filter(RampModel.is_available == filter_request.is_available)
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación
        query = query.offset(filter_request.offset).limit(filter_request.limit)
        
        # Ordenar por nombre
        query = query.order_by(RampModel.name)
        
        ramp_models = query.all()
        
        ramps = [
            Ramp(
                id=ramp_model.id,
                name=ramp_model.name,
                is_available=ramp_model.is_available,
                branch_id=ramp_model.branch_id,
                created_at=ramp_model.created_at,
                updated_at=ramp_model.updated_at
            )
            for ramp_model in ramp_models
        ]
        
        return ramps, total
    
    async def update(self, ramp: Ramp) -> Ramp:
        """Actualizar una rampa"""
        ramp_model = self.session.query(RampModel).filter(RampModel.id == ramp.id).first()
        
        if not ramp_model:
            raise ValueError(f"Rampa con ID {ramp.id} no encontrada")
        
        # Actualizar campos
        if ramp.name is not None:
            ramp_model.name = ramp.name
        if ramp.is_available is not None:
            ramp_model.is_available = ramp.is_available
        if ramp.branch_id is not None:
            ramp_model.branch_id = ramp.branch_id
        
        self.session.commit()
        self.session.refresh(ramp_model)
        
        return Ramp(
            id=ramp_model.id,
            name=ramp_model.name,
            is_available=ramp_model.is_available,
            branch_id=ramp_model.branch_id,
            created_at=ramp_model.created_at,
            updated_at=ramp_model.updated_at
        )
    
    async def delete(self, ramp_id: int) -> bool:
        """Eliminar una rampa"""
        ramp_model = self.session.query(RampModel).filter(RampModel.id == ramp_id).first()
        
        if not ramp_model:
            return False
        
        self.session.delete(ramp_model)
        self.session.commit()
        
        return True
    
    async def exists_by_name_and_branch(self, name: str, branch_id: int, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una rampa con el mismo nombre en la misma sucursal"""
        query = self.session.query(RampModel).filter(
            and_(
                RampModel.name == name,
                RampModel.branch_id == branch_id
            )
        )
        
        if exclude_id:
            query = query.filter(RampModel.id != exclude_id)
        
        return query.first() is not None 