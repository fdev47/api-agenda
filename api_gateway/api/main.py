"""
API principal del API Gateway usando factory común
"""
import os
from dotenv import load_dotenv

# ⭐ CARGAR .env AL INICIO
load_dotenv()

from commons.config import config
from commons.service_factory import create_service_factory, ServiceConfig, RouterConfig, run_service
from commons.api_client import HTTPError
from commons.error_codes import ErrorCode
from . import user_router, profile_router, location_router, customer_router
from .schedule.schedule_routes import router as schedule_router
from .reservation.reservation_routes import router as reservation_router
from .branch.routes import router as branch_router
from .measurement_unit.routes import router as measurement_unit_router
from .local.routes import router as local_router
from .sector_type.routes import router as sector_type_router
from .sector.routes import router as sector_router
from .ramp.ramp_routes import router as ramp_router


def create_api_gateway_service() -> ServiceConfig:
    """Crear configuración del API Gateway"""
    return ServiceConfig(
        service_name=config.API_GATEWAY_NAME,
        service_version=config.API_GATEWAY_VERSION,
        service_port=config.API_GATEWAY_PORT,
        cors_origins=config.API_GATEWAY_CORS_ORIGINS,
        database_url=None,  # API Gateway no tiene BD
        api_version=config.API_VERSION,
        api_prefix=config.API_PREFIX,
        title="API Gateway",
        description="API Gateway para orquestar servicios",
        tags=["Gateway", "Orchestration"]
    )


def create_api_gateway_app():
    """Crear aplicación API Gateway usando factory común"""
    
    # Configuración del servicio
    service_config = create_api_gateway_service()
    
    # Configurar routers
    routers = [
        RouterConfig(user_router, prefix="/users", tags=["Users"]),
        RouterConfig(profile_router, prefix="/profiles", tags=["Profiles"]),
        RouterConfig(location_router, prefix="/location", tags=["Location"]),
        RouterConfig(customer_router, prefix="/customers", tags=["Customers"]),
        RouterConfig(schedule_router, prefix="/schedules", tags=["Schedules"]),
        RouterConfig(reservation_router, prefix="/reservations", tags=["Reservations"]),
        RouterConfig(branch_router, prefix="/branches", tags=["Branches"]),
        RouterConfig(measurement_unit_router, prefix="/measurement-units", tags=["Measurement Units"]),
        RouterConfig(local_router, prefix="/locals", tags=["Locals"]),
        RouterConfig(sector_type_router, prefix="/sector-types", tags=["Sector Types"]),
        RouterConfig(sector_router, prefix="/sectors", tags=["Sectors"]),
        RouterConfig(ramp_router, prefix="/ramps", tags=["Ramps"])
    ]
    
    # Crear aplicación usando factory común
    app = create_service_factory(
        service_config=service_config,
        routers=routers,
        enable_auth=False,  # Deshabilitado para usar dependencias
        enable_auto_tables=False  # API Gateway no tiene BD
    )
    
    # Handler personalizado para HTTPError del APIClient
    @app.exception_handler(HTTPError)
    async def http_error_handler(request, exc: HTTPError):
        from fastapi.responses import JSONResponse
        from datetime import datetime
        
        # Mapear códigos de estado HTTP a códigos de error
        if exc.status_code == 409:
            error_code = ErrorCode.PHONE_NUMBER_EXISTS.value
            message = "El número de teléfono ya existe en el sistema. Intente con otro número."
        elif exc.status_code == 400:
            error_code = ErrorCode.VALIDATION_ERROR.value
            message = "Datos de usuario inválidos"
        else:
            error_code = ErrorCode.INTERNAL_SERVER_ERROR.value
            message = "Error del servicio de autenticación"
        
        error_response = {
            "error": True,
            "message": message,
            "error_code": error_code,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
            "request_id": getattr(request.state, 'request_id', None)
        }
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    
    return app


# Crear la aplicación
app = create_api_gateway_app()


if __name__ == "__main__":
    service_config = create_api_gateway_service()
    run_service(app, service_config) 