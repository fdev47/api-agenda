"""
Rutas del API Gateway
"""
from .user_routes import router as user_router
from .profile_routes import router as profile_router
from .location_routes import router as location_router

__all__ = ["user_router", "profile_router", "location_router"] 