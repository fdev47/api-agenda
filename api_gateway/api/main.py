"""
API principal del API Gateway usando factory común
"""
import os
from dotenv import load_dotenv

# ⭐ CARGAR .env AL INICIO
load_dotenv()

from commons.config import config
from commons.service_factory import create_service_factory, ServiceConfig, RouterConfig, run_service
from .routes import user_router, profile_router


def create_api_gateway_service() -> ServiceConfig:
    """Crear configuración del API Gateway"""
    return ServiceConfig(
        service_name="API Gateway",
        service_version="1.0.0",
        service_port=config.API_GATEWAY_PORT,
        cors_origins=["*"],
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
        RouterConfig(profile_router, prefix="/profiles", tags=["Profiles"])
    ]
    
    # Crear aplicación usando factory común
    app = create_service_factory(
        service_config=service_config,
        routers=routers,
        enable_auth=False,  # Deshabilitado para usar dependencias
        enable_auto_tables=False  # API Gateway no tiene BD
    )
    
    return app


# Crear la aplicación
app = create_api_gateway_app()


if __name__ == "__main__":
    service_config = create_api_gateway_service()
    run_service(app, service_config) 