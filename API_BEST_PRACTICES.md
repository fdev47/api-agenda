# 🏗️ Mejores Prácticas para Rutas API

## 📋 **Estructura de Rutas Implementada**

### **1. Versionado de API**
```
/api/v1/auth/login
/api/v1/users/me
/api/v2/auth/login  # Futura versión
```

**Configuración:**
```bash
# En .env
API_VERSION=v1
```

### **2. Estructura Jerárquica por Recurso**
```
/api/v1/auth/          # Autenticación
├── /register         # POST - Registrar usuario
├── /login            # POST - Iniciar sesión
├── /refresh          # POST - Refrescar token
├── /validate         # POST - Validar token
└── /validate-token   # GET - Validar desde header

/api/v1/users/         # Gestión de usuarios
├── /me               # GET - Usuario actual
└── /{user_id}        # GET - Usuario por ID

/api/v1/admin/         # Funciones administrativas
└── /users/
    ├── /assign-role      # POST - Asignar rol
    ├── /assign-permission # POST - Asignar permiso
    ├── /{user_id}/roles  # GET - Obtener roles
    └── /{user_id}        # DELETE - Eliminar usuario
```

### **3. Headers Estándar Implementados**

#### **Headers de Respuesta Automáticos:**
```
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
X-API-Version: v1
X-Service-Name: auth-service
X-Service-Version: 1.0.0
```

#### **Headers de Request Esperados:**
```
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
```

## 🎯 **Convenciones de Nomenclatura**

### **Rutas RESTful:**
- **GET** `/api/v1/users` - Listar usuarios
- **GET** `/api/v1/users/{id}` - Obtener usuario específico
- **POST** `/api/v1/users` - Crear usuario
- **PUT** `/api/v1/users/{id}` - Actualizar usuario completo
- **PATCH** `/api/v1/users/{id}` - Actualizar usuario parcialmente
- **DELETE** `/api/v1/users/{id}` - Eliminar usuario

### **Rutas de Acción:**
- **POST** `/api/v1/auth/login` - Acción de login
- **POST** `/api/v1/auth/refresh` - Acción de refresh
- **POST** `/api/v1/admin/users/assign-role` - Acción administrativa

## 📊 **Códigos de Estado HTTP**

### **Éxito:**
- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado
- `204 No Content` - Operación exitosa sin contenido

### **Cliente:**
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `409 Conflict` - Conflicto (ej: email duplicado)

### **Servidor:**
- `500 Internal Server Error` - Error interno
- `502 Bad Gateway` - Error de servicio externo
- `503 Service Unavailable` - Servicio no disponible

## 🔐 **Autenticación y Autorización**

### **Tokens JWT:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### **Validación de Roles:**
```python
# En las rutas
@router.post("/admin/users/assign-role")
async def assign_role(
    current_user=Depends(auth_middleware.require_role("admin"))
):
    # Solo usuarios con rol "admin" pueden acceder
```

## 📝 **Formato de Respuestas**

### **Respuesta de Éxito:**
```json
{
  "user_id": "abc123",
  "email": "user@example.com",
  "display_name": "John Doe",
  "email_verified": true,
  "custom_claims": {
    "role": "user",
    "permissions": ["read", "write"]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "last_sign_in": "2024-01-15T14:20:00Z"
}
```

### **Respuesta de Error:**
```json
{
  "error": "auth_error",
  "message": "Token expirado",
  "error_code": "TOKEN_EXPIRED",
  "token_expired": true,
  "timestamp": "2024-01-15T14:20:00Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## 🧪 **Testing de Endpoints**

### **Ejemplos de Testing:**
```bash
# Health check
curl http://localhost:8001/health

# Login
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Obtener usuario actual
curl http://localhost:8001/api/v1/users/me \
  -H "Authorization: Bearer <token>"

# Validar token
curl http://localhost:8001/api/v1/auth/validate-token \
  -H "Authorization: Bearer <token>"
```

## 📚 **Documentación Automática**

### **Swagger UI:**
```
http://localhost:8001/docs
http://localhost:8001/api/docs  # Redirige a /docs
```

### **ReDoc:**
```
http://localhost:8001/redoc
http://localhost:8001/api/redoc  # Redirige a /redoc
```

### **OpenAPI JSON:**
```
http://localhost:8001/openapi.json
http://localhost:8001/api/openapi.json  # Redirige a /openapi.json
```

## 🔄 **Migración de Versiones**

### **Estrategia de Versionado:**
1. **URL Path Versioning** (implementado): `/api/v1/`, `/api/v2/`
2. **Header Versioning**: `X-API-Version: v1`
3. **Query Parameter**: `?version=v1`

### **Plan de Migración:**
1. Mantener versión anterior por 6-12 meses
2. Documentar cambios entre versiones
3. Proporcionar migración automática cuando sea posible
4. Notificar deprecación con anticipación

## 🚀 **Monitoreo y Logging**

### **Request ID Tracking:**
Cada request tiene un ID único para tracking:
```json
{
  "X-Request-ID": "550e8400-e29b-41d4-a716-446655440000"
}
```

### **Logs Estructurados:**
```json
{
  "timestamp": "2024-01-15T14:20:00Z",
  "level": "INFO",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "service": "auth-service",
  "endpoint": "/api/v1/auth/login",
  "method": "POST",
  "status_code": 200,
  "response_time_ms": 150
}
```

## 📋 **Checklist de Implementación**

- [x] Versionado de API en URL
- [x] Headers estándar automáticos
- [x] Request ID único por request
- [x] Estructura jerárquica de rutas
- [x] Códigos de estado HTTP apropiados
- [x] Formato de respuesta consistente
- [x] Documentación automática (Swagger/ReDoc)
- [x] Manejo de errores estandarizado
- [x] Autenticación y autorización
- [x] CORS configurado
- [x] Health check endpoint
- [x] Logging estructurado
- [x] Variables de entorno organizadas 