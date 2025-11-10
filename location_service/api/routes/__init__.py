"""
Rutas del location_service
"""
from .country_routes import router as country_router
from .state_routes import router as state_router
from .city_routes import router as city_router
from .local_routes import router as local_router
from .branch_routes import router as branch_router
from .sector_routes import router as sector_router
from .sector_type_routes import router as sector_type_router
from .measurement_unit_routes import router as measurement_unit_router
from .ramp_routes import router as ramp_router
from .ramp_schedule_routes import router as ramp_schedule_router

__all__ = [
    "country_router",
    "state_router", 
    "city_router",
    "local_router",
    "branch_router",
    "sector_router",
    "sector_type_router",
    "measurement_unit_router",
    "ramp_router",
    "ramp_schedule_router"
] 