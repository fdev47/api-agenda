"""
API principal del Reservation Service usando factory común
"""
import os
from dotenv import load_dotenv
from datetime import datetime

# ⭐ CARGAR .env AL INICIO
load_dotenv()

from commons.config import config
from commons.service_factory import create_service_factory, ServiceConfig, RouterConfig, run_service
from .routes import schedule_routes, schedule_validation_routes, reservation_routes
from ..infrastructure.models.base import Base


def create_reservation_service() -> ServiceConfig:
    """Crear configuración del Reservation Service"""
    return ServiceConfig(
        service_name="Reservation Service",
        service_version="1.0.0",
        service_port=8004,  # Puerto por defecto para reservation service
        cors_origins=["*"],
        database_url=config.DATABASE_URL,
        api_version=config.API_VERSION,
        api_prefix=config.API_PREFIX,
        title="Reservation Service API",
        description="API para gestión de reservas y horarios de sucursales",
        tags=["Reservations", "Schedules", "Validation"]
    )


def create_reservation_app():
    """Crear aplicación Reservation Service usando factory común"""
    
    # Configuración del servicio
    service_config = create_reservation_service()
    
    # Configurar routers con prefijos y tags personalizados
    routers = [
        RouterConfig(schedule_routes.router, prefix="/schedules", tags=["Schedules"]),
        RouterConfig(schedule_validation_routes.router, prefix="/schedule-validation", tags=["Schedule Validation"]),
        RouterConfig(reservation_routes.router, prefix="/reservations", tags=["Reservations"])
    ]
    
    # Crear aplicación usando factory común
    app = create_service_factory(
        service_config=service_config,
        base_model=Base,  # ✅ Habilitar ORM con modelos de Reservation Service
        routers=routers,
        enable_auth=False,  # Deshabilitado para usar dependencias
        enable_auto_tables=True  # ✅ Habilitar creación automática de tablas
    )
    
    return app


# Crear la aplicación
app = create_reservation_app()


if __name__ == "__main__":
    service_config = create_reservation_service()
    run_service(app, service_config) 