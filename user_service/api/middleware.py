"""
Middleware de autenticación para User Service
Usa las dependencias de autenticación desde commons
"""
from commons.auth_client import require_auth, require_role, auth_dependencies

# Re-exportar las dependencias para uso en las rutas
auth_middleware = {
    "require_auth": require_auth,                    # Validación rápida (por defecto)
    "require_auth_full": auth_dependencies["require_auth_full"],  # Validación completa
    "require_role": require_role                     # Validación completa + rol
} 