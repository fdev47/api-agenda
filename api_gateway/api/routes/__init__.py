"""
Rutas del API Gateway
"""
from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .admin_routes import router as admin_router

__all__ = [
    "auth_router",
    "user_router", 
    "admin_router"
] 