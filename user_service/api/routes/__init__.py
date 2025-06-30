"""
Rutas de la API
"""

from .user_routes import router as user_router
from .admin_routes import router as admin_router

__all__ = ["user_router", "admin_router"] 