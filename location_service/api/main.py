"""
API principal del servicio de ubicaciones usando factory común
"""
import os
from dotenv import load_dotenv
from datetime import datetime

# ⭐ CARGAR .env AL INICIO
load_dotenv()

from commons.config import config
from commons.service_factory import create_service_factory, ServiceConfig, RouterConfig, run_service
from ..domain.exceptions import LocationDomainException
from ..domain.dto.responses import ErrorResponse
from .routes import country_router, state_router, city_router, local_router, branch_router
from ..infrastructure.models.base import Base


def create_location_service() -> ServiceConfig:
    """Crear configuración del Location Service"""
    return ServiceConfig(
        service_name="Location Service",
        service_version="1.0.0",
        service_port=config.LOCATION_SERVICE_PORT,
        cors_origins=["*"],
        database_url=config.DATABASE_URL,
        api_version=config.API_VERSION,
        api_prefix=config.API_PREFIX,
        title="Location Service API",
        description="API para gestión de ubicaciones, países, estados, ciudades, locales y sucursales",
        tags=["Locations", "Countries", "States", "Cities", "Locals", "Branches"]
    )


def create_location_app():
    """Crear aplicación Location Service usando factory común"""
    
    # Configuración del servicio
    service_config = create_location_service()
    
    # Manejadores de excepciones personalizados
    custom_exception_handlers = {
        LocationDomainException: lambda request, exc: ErrorResponse(
            message=exc.message,
            error_code=exc.error_code,
            timestamp=datetime.utcnow().isoformat(),
            path=request.url.path
        )
    }
    
    # Configurar routers con prefijos y tags personalizados
    routers = [
        RouterConfig(country_router, prefix="/countries", tags=["Countries"]),
        RouterConfig(state_router, prefix="/states", tags=["States"]),
        RouterConfig(city_router, prefix="/cities", tags=["Cities"]),
        RouterConfig(local_router, prefix="/locals", tags=["Locals"]),
        RouterConfig(branch_router, prefix="/branches", tags=["Branches"])
    ]
    
    # Crear aplicación usando factory común
    app = create_service_factory(
        service_config=service_config,
        base_model=Base,  # Para crear tablas automáticamente
        routers=routers,
        custom_exception_handlers=custom_exception_handlers,
        enable_auth=False,  # Deshabilitado temporalmente
        enable_auto_tables=True  # Habilitar creación automática de tablas
    )
    
    return app


# Crear la aplicación
app = create_location_app()


if __name__ == "__main__":
    service_config = create_location_service()
    run_service(app, service_config) 