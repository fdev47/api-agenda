"""
API principal del User Service usando factory común
"""
import os
from dotenv import load_dotenv
from datetime import datetime

# ⭐ CARGAR .env AL INICIO
load_dotenv()

from commons.config import config
from commons.service_factory import create_service_factory, ServiceConfig, RouterConfig, run_service
from ..domain.exceptions import UserError
from .routes import user_router, admin_router, profile_router, role_router, address_router, customer_router
from ..infrastructure.models.base import Base


def create_user_service() -> ServiceConfig:
    """Crear configuración del User Service"""
    return ServiceConfig(
        service_name="User Service",
        service_version="1.0.0",
        service_port=config.USER_SERVICE_PORT,
        cors_origins=config.USER_CORS_ORIGINS,
        database_url=config.DATABASE_URL,
        api_version=config.API_VERSION,
        api_prefix=config.API_PREFIX,
        title="User Service API",
        description="Servicio de gestión de usuarios",
        tags=["Users", "Administration", "Profiles", "Roles"],
        additional_settings={
            "auth_service_url": config.AUTH_SERVICE_URL
        }
    )


def create_user_app():
    """Crear aplicación User Service usando factory común"""
    
    # Configuración del servicio
    service_config = create_user_service()
    
    # Manejadores de excepciones personalizados (vacío para usar el estándar)
    custom_exception_handlers = {}
    
    # Configurar routers con prefijos personalizados
    routers = [
        RouterConfig(user_router, prefix="/users", tags=["Users"]),
        RouterConfig(admin_router, prefix="/admin", tags=["Administration"]),
        RouterConfig(profile_router, prefix="/profiles", tags=["Profiles"]),
        RouterConfig(role_router, prefix="/roles", tags=["Roles"]),
        RouterConfig(address_router, prefix="/addresses", tags=["Addresses"]),
        RouterConfig(customer_router, prefix="/customers", tags=["Customers"])
    ]
    
    # Crear aplicación usando factory común
    app = create_service_factory(
        service_config=service_config,
        base_model=Base,  # ✅ Habilitar ORM con modelos de User Service
        routers=routers,
        custom_exception_handlers=custom_exception_handlers,
        enable_auth=False,  # Deshabilitado para usar dependencias
        enable_auto_tables=True  # ✅ Habilitar creación automática de tablas
    )
    
    return app


# Crear la aplicación
app = create_user_app()


if __name__ == "__main__":
    service_config = create_user_service()
    run_service(app, service_config) 