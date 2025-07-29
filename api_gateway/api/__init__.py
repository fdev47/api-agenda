"""
Rutas del API Gateway
"""
from .user.routes import router as user_router
from .profile.routes import router as profile_router
from .location.routes import router as location_router
from .customer.routes import router as customer_router

__all__ = ["user_router", "profile_router", "location_router", "customer_router"] 