"""
Rutas de la API
"""

from .user_routes import router as user_router
from .admin_routes import router as admin_router
from .profile_routes import router as profile_router
from .role_routes import router as role_router
from .address_routes import router as address_router
from .customer_routes import router as customer_router

__all__ = ["user_router", "admin_router", "profile_router", "role_router", "address_router", "customer_router"] 