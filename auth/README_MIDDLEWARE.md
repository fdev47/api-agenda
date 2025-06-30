# Middleware de Autenticación

Este documento explica cómo usar el middleware de autenticación tanto dentro del servicio `auth` como en otros servicios.

## Estructura del Middleware

### 1. **Middleware Interno** (`auth/api/middleware.py`)
- **Propósito**: Uso interno del servicio `auth`
- **Características**: 
  - Acceso directo a los casos de uso
  - Validación local de tokens
  - Respuestas de error personalizadas

### 2. **Middleware Externo** (`auth/api/external_middleware.py`)
- **Propósito**: Uso en otros servicios
- **Características**:
  - Validación de tokens via HTTP al servicio `auth`
  - Fácil integración en otros servicios
  - Manejo de errores consistente

## Uso en el Servicio Auth

### Rutas Protegidas
```python
from auth.api.middleware import auth_middleware

@app.get("/protected")
async def protected_endpoint(current_user=Depends(auth_middleware.require_auth)):
    return {"user": current_user}
```

### Rutas con Roles Específicos
```python
@app.get("/admin-only")
async def admin_endpoint(current_user=Depends(auth_middleware.require_role("admin"))):
    return {"user": current_user}
```

### Rutas Opcionales
```python
@app.get("/optional-auth")
async def optional_endpoint(current_user=Depends(auth_middleware.get_current_user)):
    if current_user:
        return {"authenticated": True, "user": current_user}
    return {"authenticated": False}
```

## Uso en Otros Servicios

### 1. Instalar Dependencias
```bash
pip install httpx
```

### 2. Importar y Configurar
```python
from auth.api.external_middleware import create_auth_middleware

# Crear middleware apuntando al servicio auth
auth_middleware = create_auth_middleware("http://localhost:8000")
```

### 3. Usar en Rutas
```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/protected")
async def protected_endpoint(current_user=Depends(auth_middleware.require_auth)):
    return {"message": "Protegido", "user": current_user}

@app.get("/admin")
async def admin_endpoint(current_user=Depends(auth_middleware.require_role("admin"))):
    return {"message": "Solo admin", "user": current_user}
```

## Endpoints de Validación

### Endpoint para Otros Servicios
- **URL**: `GET /auth/validate-token`
- **Headers**: `Authorization: Bearer <token>`
- **Respuesta**:
```json
{
    "valid": true,
    "message": "Token válido",
    "user": {
        "user_id": "user123",
        "email": "user@example.com",
        "display_name": "John Doe",
        "email_verified": true,
        "custom_claims": {
            "roles": ["user", "admin"]
        },
        "created_at": "2024-01-01T00:00:00",
        "last_sign_in": "2024-01-01T12:00:00"
    }
}
```

## Manejo de Errores

### Errores de Autenticación
```json
{
    "error": "auth_error",
    "message": "Token inválido o expirado",
    "error_code": "INVALID_TOKEN",
    "token_expired": true,
    "timestamp": "2024-01-01T12:00:00"
}
```

### Errores de Permisos
```json
{
    "error": "auth_error",
    "message": "Se requiere rol: admin",
    "error_code": "INSUFFICIENT_PERMISSIONS",
    "timestamp": "2024-01-01T12:00:00"
}
```

## Ejemplo Completo

Ver `auth/examples/external_service_example.py` para un ejemplo completo de cómo integrar el middleware en otro servicio.

## Configuración

### Variables de Entorno
```bash
# URL del servicio de autenticación
AUTH_SERVICE_URL=http://localhost:8000
```

### Configuración en Código
```python
# Para desarrollo
auth_middleware = create_auth_middleware("http://localhost:8000")

# Para producción
auth_middleware = create_auth_middleware("https://auth-service.production.com")
```

## Ventajas

1. **Separación de Responsabilidades**: El servicio `auth` maneja toda la lógica de autenticación
2. **Reutilización**: Otros servicios pueden usar el mismo middleware
3. **Consistencia**: Manejo uniforme de errores y respuestas
4. **Flexibilidad**: Soporte para autenticación opcional y obligatoria
5. **Escalabilidad**: Fácil de extender con nuevos roles y permisos 