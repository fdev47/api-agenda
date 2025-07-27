"""
Middleware de autenticación para Reservation Service
Usa las dependencias de autenticación desde commons
"""
from commons.auth_client import require_auth, require_role

# Re-exportar las dependencias para uso en las rutas
auth_middleware = {
    "require_auth": require_auth,
    "require_role": require_role
} 