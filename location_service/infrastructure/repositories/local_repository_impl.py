"""
Implementación del repositorio para locales
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ...domain.interfaces.local_repository import LocalRepository
from ...domain.entities.local import Local
from ...domain.dto.requests.local_requests import LocalFilterRequest
from ..models.local import Local as LocalModel


class LocalRepositoryImpl(LocalRepository):
    """Implementación del repositorio para locales"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, local: Local) -> Local:
        """Crear un nuevo local"""
        local_model = LocalModel(
            name=local.name,
            code=local.code,
            description=local.description,
            phone=local.phone,
            email=local.email,
            is_active=local.is_active
        )
        
        self.session.add(local_model)
        self.session.commit()
        self.session.refresh(local_model)
        
        return Local(
            id=local_model.id,
            name=local_model.name,
            code=local_model.code,
            description=local_model.description,
            phone=local_model.phone,
            email=local_model.email,
            is_active=local_model.is_active,
            created_at=local_model.created_at,
            updated_at=local_model.updated_at
        )
    
    async def get_by_id(self, local_id: int) -> Optional[Local]:
        """Obtener un local por ID"""
        local_model = self.session.query(LocalModel).filter(LocalModel.id == local_id).first()
        
        if not local_model:
            return None
        
        return Local(
            id=local_model.id,
            name=local_model.name,
            code=local_model.code,
            description=local_model.description,
            phone=local_model.phone,
            email=local_model.email,
            is_active=local_model.is_active,
            created_at=local_model.created_at,
            updated_at=local_model.updated_at
        )
    
    async def get_by_code(self, code: str) -> Optional[Local]:
        """Obtener un local por código"""
        local_model = self.session.query(LocalModel).filter(LocalModel.code == code).first()
        
        if not local_model:
            return None
        
        return Local(
            id=local_model.id,
            name=local_model.name,
            code=local_model.code,
            description=local_model.description,
            phone=local_model.phone,
            email=local_model.email,
            is_active=local_model.is_active,
            created_at=local_model.created_at,
            updated_at=local_model.updated_at
        )
    
    async def list_all(self, filter_request: LocalFilterRequest) -> Tuple[List[Local], int]:
        """Listar todos los locales con filtros"""
        query = self.session.query(LocalModel)
        
        # Aplicar filtros
        if filter_request.name:
            query = query.filter(LocalModel.name.ilike(f"%{filter_request.name}%"))
        
        if filter_request.code:
            query = query.filter(LocalModel.code.ilike(f"%{filter_request.code}%"))
        
        if filter_request.is_active is not None:
            query = query.filter(LocalModel.is_active == filter_request.is_active)
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación
        query = query.offset(filter_request.offset).limit(filter_request.limit)
        
        # Ordenar por nombre
        query = query.order_by(LocalModel.name)
        
        local_models = query.all()
        
        locals = [
            Local(
                id=local_model.id,
                name=local_model.name,
                code=local_model.code,
                description=local_model.description,
                phone=local_model.phone,
                email=local_model.email,
                is_active=local_model.is_active,
                created_at=local_model.created_at,
                updated_at=local_model.updated_at
            )
            for local_model in local_models
        ]
        
        return locals, total
    
    async def update(self, local_id: int, local: Local) -> Optional[Local]:
        """Actualizar un local"""
        local_model = self.session.query(LocalModel).filter(LocalModel.id == local_id).first()
        
        if not local_model:
            return None
        
        # Actualizar campos
        if local.name is not None:
            local_model.name = local.name
        if local.code is not None:
            local_model.code = local.code
        if local.description is not None:
            local_model.description = local.description
        if local.phone is not None:
            local_model.phone = local.phone
        if local.email is not None:
            local_model.email = local.email
        if local.is_active is not None:
            local_model.is_active = local.is_active
        
        self.session.commit()
        self.session.refresh(local_model)
        
        return Local(
            id=local_model.id,
            name=local_model.name,
            code=local_model.code,
            description=local_model.description,
            phone=local_model.phone,
            email=local_model.email,
            is_active=local_model.is_active,
            created_at=local_model.created_at,
            updated_at=local_model.updated_at
        )
    
    async def delete(self, local_id: int) -> bool:
        """Eliminar un local"""
        local_model = self.session.query(LocalModel).filter(LocalModel.id == local_id).first()
        
        if not local_model:
            return False
        
        self.session.delete(local_model)
        self.session.commit()
        
        return True
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un local con el código dado"""
        query = self.session.query(LocalModel).filter(LocalModel.code == code)
        
        if exclude_id:
            query = query.filter(LocalModel.id != exclude_id)
        
        return query.first() is not None 