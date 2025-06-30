"""
Rutas del location_service
"""
from .country_routes import router as country_router
from .state_routes import router as state_router
from .city_routes import router as city_router
from .local_routes import router as local_router
from .branch_routes import router as branch_router

__all__ = [
    "country_router",
    "state_router", 
    "city_router",
    "local_router",
    "branch_router"
] 