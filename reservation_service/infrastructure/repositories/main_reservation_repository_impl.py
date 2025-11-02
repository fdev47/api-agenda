"""
Implementación del repositorio de main_reservations
"""
from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
import logging

from ...domain.entities.main_reservation import MainReservation
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from ...infrastructure.models.main_reservation import MainReservationModel
from commons.database import get_db_session

# Configurar logging
logger = logging.getLogger(__name__)


class MainReservationRepositoryImpl(MainReservationRepository):
    """Implementación del repositorio para main_reservations"""
    
    def __init__(self):
        pass
    
    async def create(self, main_reservation: MainReservation) -> MainReservation:
        """Crear una nueva main_reservation"""
        logger.info("💾 MainReservationRepositoryImpl.create() iniciado")
        
        async for session in get_db_session():
            logger.info(f"🔍 Session obtenida: {session}")
            if session is None:
                logger.error("❌ Session es None!")
                raise Exception("No se pudo obtener una sesión de base de datos")
            
            try:
                # Convertir entidad de dominio a modelo de BD
                main_reservation_model = MainReservationModel.from_domain(main_reservation)
                logger.info("✅ MainReservationModel creado correctamente")
                
                session.add(main_reservation_model)
                logger.info("✅ MainReservationModel agregado a la sesión")
                await session.commit()
                logger.info("✅ Commit realizado")
                await session.refresh(main_reservation_model)
                logger.info("✅ Refresh realizado")
                
                logger.info(f"✅ MainReservation creada en BD con ID: {main_reservation_model.id}")
                return main_reservation_model.to_domain()
                
            except Exception as e:
                logger.error(f"❌ Error en MainReservationRepositoryImpl.create(): {str(e)}", exc_info=True)
                await session.rollback()
                raise
    
    async def get_by_id(self, main_reservation_id: int) -> Optional[MainReservation]:
        """Obtener una main_reservation por ID"""
        async for session in get_db_session():
            result = await session.execute(
                select(MainReservationModel).where(MainReservationModel.id == main_reservation_id)
            )
            main_reservation_model = result.scalar_one_or_none()
            
            if not main_reservation_model:
                return None
            
            return main_reservation_model.to_domain()
    
    async def list(
        self,
        sector_id: Optional[int] = None,
        reservation_id: Optional[int] = None,
        reservation_date: Optional[datetime] = None,
        start_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[MainReservation], int]:
        """
        Listar main_reservations con filtros
        
        Args:
            sector_id: Filtrar por sector_id
            reservation_id: Filtrar por reservation_id
            reservation_date: Filtrar por fecha de reserva
            start_time: Filtrar por hora de inicio
            skip: Número de registros a saltar (paginación)
            limit: Número máximo de registros a retornar
            
        Returns:
            Tuple[List[MainReservation], int]: Lista de reservas y total de registros
        """
        async for session in get_db_session():
            # Construir la consulta base
            query = select(MainReservationModel)
            count_query = select(func.count()).select_from(MainReservationModel)
            
            # Aplicar filtros
            conditions = []
            
            if sector_id:
                conditions.append(MainReservationModel.sector_id == sector_id)
            
            if reservation_id:
                conditions.append(MainReservationModel.reservation_id == reservation_id)
            
            if reservation_date:
                # Filtrar por fecha completa (ignorando hora)
                conditions.append(
                    func.date(MainReservationModel.reservation_date) == func.date(reservation_date)
                )
            
            if start_time:
                # Filtrar por hora de inicio exacta
                conditions.append(MainReservationModel.start_time == start_time)
            
            # Aplicar condiciones si existen
            if conditions:
                query = query.where(and_(*conditions))
                count_query = count_query.where(and_(*conditions))
            
            # Contar total de registros
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginación
            query = query.offset(skip).limit(limit)
            
            # Ordenar por fecha de reserva descendente
            query = query.order_by(MainReservationModel.reservation_date.desc())
            
            # Ejecutar consulta
            result = await session.execute(query)
            main_reservation_models = result.scalars().all()
            
            # Convertir a entidades de dominio
            main_reservations = [
                main_reservation_model.to_domain() 
                for main_reservation_model in main_reservation_models
            ]
            
            logger.info(f"📋 MainReservationRepositoryImpl.list(): {len(main_reservations)} registros encontrados de {total} totales")
            
            return main_reservations, total
    
    async def update(self, main_reservation: MainReservation) -> MainReservation:
        """Actualizar una main_reservation"""
        logger.info(f"🔄 MainReservationRepositoryImpl.update() iniciado para ID: {main_reservation.id}")
        
        async for session in get_db_session():
            try:
                # Buscar el modelo existente
                result = await session.execute(
                    select(MainReservationModel).where(MainReservationModel.id == main_reservation.id)
                )
                main_reservation_model = result.scalar_one_or_none()
                
                if not main_reservation_model:
                    logger.error(f"❌ MainReservation con ID {main_reservation.id} no encontrada")
                    raise Exception(f"MainReservation con ID {main_reservation.id} no encontrada")
                
                # Convertir entidad de dominio a modelo de BD
                updated_model = MainReservationModel.from_domain(main_reservation)
                
                # Actualizar campos
                main_reservation_model.sector_id = updated_model.sector_id
                main_reservation_model.reservation_id = updated_model.reservation_id
                main_reservation_model.ramp_id = updated_model.ramp_id
                main_reservation_model.sector_data = updated_model.sector_data
                main_reservation_model.reservation_date = updated_model.reservation_date
                main_reservation_model.start_time = updated_model.start_time
                main_reservation_model.end_time = updated_model.end_time
                main_reservation_model.updated_at = datetime.utcnow()
                
                logger.info("✅ Campos actualizados correctamente")
                
                await session.commit()
                logger.info("✅ Commit realizado")
                await session.refresh(main_reservation_model)
                logger.info("✅ Refresh realizado")
                
                logger.info(f"✅ MainReservation actualizada correctamente con ID: {main_reservation_model.id}")
                return main_reservation_model.to_domain()
                
            except Exception as e:
                logger.error(f"❌ Error en MainReservationRepositoryImpl.update(): {str(e)}", exc_info=True)
                await session.rollback()
                raise
    
    async def delete(self, main_reservation_id: int) -> bool:
        """
        Eliminar una main_reservation por ID
        
        Args:
            main_reservation_id: ID de la main_reservation a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        logger.info(f"🗑️ MainReservationRepositoryImpl.delete() iniciado para ID: {main_reservation_id}")
        
        async for session in get_db_session():
            try:
                # Buscar el modelo existente
                result = await session.execute(
                    select(MainReservationModel).where(MainReservationModel.id == main_reservation_id)
                )
                main_reservation_model = result.scalar_one_or_none()
                
                if not main_reservation_model:
                    logger.warning(f"⚠️ MainReservation con ID {main_reservation_id} no encontrada")
                    return False
                
                await session.delete(main_reservation_model)
                await session.commit()
                
                logger.info(f"✅ MainReservation eliminada correctamente con ID: {main_reservation_id}")
                return True
                
            except Exception as e:
                logger.error(f"❌ Error en MainReservationRepositoryImpl.delete(): {str(e)}", exc_info=True)
                await session.rollback()
                raise

