# API Gateway

El API Gateway es el orquestador principal de todos los microservicios de la aplicación. Actúa como punto de entrada único para todas las operaciones y redirige las peticiones a los servicios correspondientes.

## 🏗️ Arquitectura

```
┌─────────────────┐
│   API Gateway   │ ← Punto de entrada único
│   (Puerto 8000) │
└─────────────────┘
         │
         ├── Auth Service (Puerto 8001)
         ├── User Service (Puerto 8002)
         ├── Location Service (Puerto 8003)
         └── Reservation Service (Puerto 8004)
```

## 🔐 Autenticación y Autorización

### Validación de Tokens

El API Gateway valida automáticamente todos los tokens de Firebase a través del Auth Service. Todas las rutas (excepto `/health`) requieren autenticación.

### Formato de Errores de Autenticación

```json
{
  "error": "auth_error",
  "message": "Token inválido o expirado",
  "error_code": "INVALID_TOKEN",
  "timestamp": "2024-01-01T12:00:00",
  "request_id": "uuid-request-id"
}
```

### Códigos de Error

- `MISSING_TOKEN`: Token no proporcionado
- `INVALID_TOKEN`: Token inválido o expirado
- `INSUFFICIENT_PERMISSIONS`: Rol requerido no disponible

## 🚀 Configuración

### Variables de Entorno

El API Gateway utiliza las siguientes variables de entorno (definidas en `.env` en la raíz del proyecto):

```bash
# Configuración del API Gateway
GATEWAY_SERVICE_NAME=api-gateway
GATEWAY_SERVICE_VERSION=1.0.0
GATEWAY_SERVICE_PORT=8000
GATEWAY_CORS_ORIGINS=http://localhost:3000,http://localhost:8080,*

# URLs de servicios
AUTH_SERVICE_URL=http://localhost:8001
USER_SERVICE_URL=http://localhost:8002
LOCATION_SERVICE_URL=http://localhost:8003
RESERVATION_SERVICE_URL=http://localhost:8004

# Configuración global
API_VERSION=v1
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Estructura de Rutas

El API Gateway expone las siguientes rutas con el prefijo `/api/v1`:

#### Autenticación (`/api/v1/auth`) 🔐
- `GET /validate-token` - Validar token de Firebase (requiere token)
- `GET /user-info` - Obtener información del usuario (requiere token)
- `GET /login` - Redirigir al login
- `GET /refresh-token` - Redirigir al refresh token

#### Usuarios (`/api/v1/users`) 👥
- `GET /` - Listar usuarios (requiere token)
- `POST /` - Crear usuario (requiere token)
- `GET /{user_id}` - Obtener usuario por ID (requiere token)
- `PUT /{user_id}` - Actualizar usuario (requiere token)
- `DELETE /{user_id}` - Eliminar usuario (requiere token)
- `GET /profile/{user_id}` - Obtener perfil de usuario (requiere token)
- `GET /customers/{customer_id}` - Obtener cliente por ID (requiere token)

#### Administración (`/api/v1/admin`) ⚙️
- `GET /users` - Listar usuarios (requiere rol admin)
- `POST /users/assign-role` - Asignar rol a usuario (requiere rol admin)
- `DELETE /users/{user_id}` - Eliminar usuario (requiere rol admin)
- `GET /roles` - Listar roles (requiere rol admin)
- `POST /roles` - Crear rol (requiere rol admin)
- `GET /auth/users` - Listar usuarios de autenticación (requiere rol admin)

## 🛠️ Ejecución

### Opción 1: Desde la raíz del proyecto (Recomendado)
```bash
# Desde la raíz del proyecto
python run_api_gateway.py
```

### Opción 2: Script interno del API Gateway
```bash
cd api_gateway
python run_gateway.py
```

### Opción 3: Directamente con uvicorn
```bash
# Desde la raíz del proyecto
uvicorn api_gateway.main:app --host 0.0.0.0 --port 8000 --reload

# O desde el directorio api_gateway
cd api_gateway
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Solución de Problemas

### Error de Importación Relativa

Si encuentras el error:
```
ImportError: attempted relative import with no known parent package
```

**Solución**: Usa la **Opción 1** (desde la raíz del proyecto) que es la más confiable.

### Verificación de Configuración

Para verificar que todo esté configurado correctamente:

```bash
# Verificar que el archivo .env existe
ls -la .env

# Verificar las variables de entorno
grep -E "GATEWAY_|AUTH_|USER_" .env
```

### Pruebas de Autenticación

```bash
# Probar sin token
curl http://localhost:8000/api/v1/auth/validate-token

# Probar con token inválido
curl -H "Authorization: Bearer invalid_token" http://localhost:8000/api/v1/auth/validate-token

# Probar health check (no requiere token)
curl http://localhost:8000/health
```

## 📚 Documentación

Una vez ejecutado, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## 🔧 Características

### Middleware de Headers
El API Gateway agrega automáticamente los siguientes headers a todas las respuestas:
- `X-Request-ID`: ID único de la petición
- `X-API-Version`: Versión de la API
- `X-Service-Name`: Nombre del servicio
- `X-Service-Version`: Versión del servicio

### Middleware de Autenticación
- ✅ Validación automática de tokens Firebase
- ✅ Comunicación con Auth Service
- ✅ Manejo de errores consistente
- ✅ Soporte para roles y permisos
- ✅ Request ID en errores de autenticación

### Manejo de Errores
- Manejo centralizado de excepciones HTTP
- Manejo de errores del Gateway
- Manejo de errores generales
- Inclusión de Request ID en errores
- **Nuevo**: Manejo específico de errores de autenticación

### CORS
Configuración automática de CORS basada en `GATEWAY_CORS_ORIGINS`

### Validación de Configuración
El API Gateway valida que las URLs de los servicios estén configuradas antes de iniciar.

## 🔄 Flujo de Peticiones

1. **Cliente** → API Gateway (Puerto 8000)
2. **API Gateway** → Valida token con Auth Service
3. **API Gateway** → Servicio específico según la ruta
4. **Servicio** → Respuesta al API Gateway
5. **API Gateway** → Cliente

## 📝 Logs

El API Gateway registra:
- Inicio y cierre del servicio
- URLs de servicios configurados
- Errores de configuración
- Request IDs para trazabilidad
- **Nuevo**: Errores de validación de tokens
- **Nuevo**: Timeouts de comunicación con Auth Service

## 🔍 Debug

Para verificar la configuración:
```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "version": "1.0.0",
  "api_version": "v1",
  "auth_service_url": "http://localhost:8001",
  "user_service_url": "http://localhost:8002",
  "location_service_url": "http://localhost:8003",
  "timestamp": "2024-01-01T00:00:00",
  "debug": {
    "env_file_exists": true,
    "current_directory": "/path/to/project",
    "has_auth_service": true,
    "has_user_service": true,
    "has_location_service": true
  }
}
```

## 📁 Estructura de Archivos

```
api_gateway/
├── main.py              # Aplicación principal FastAPI
├── config.py            # Configuración específica del Gateway
├── middleware.py        # 🔐 Middleware de autenticación
├── run_gateway.py       # Script de ejecución interno
├── README.md            # Este archivo
├── __init__.py          # Hace que api_gateway sea un paquete
├── api/
│   └── routes/          # Rutas del API Gateway
│       ├── auth_routes.py
│       ├── user_routes.py
│       └── admin_routes.py
├── domain/              # Dominio del Gateway
│   ├── exceptions.py    # Excepciones personalizadas
│   └── dto/            # Data Transfer Objects
├── application/         # Casos de uso
└── infrastructure/      # Infraestructura y clientes
    ├── container.py     # Contenedor de dependencias
    ├── auth_service_client.py
    └── user_service_client.py
```

## 🚀 Scripts de Ejecución

### run_api_gateway.py (Raíz del proyecto)
- ✅ Recomendado
- ✅ Sin problemas de importación
- ✅ Carga automática de .env
- ✅ Validaciones completas

### run_gateway.py (Directorio api_gateway)
- ⚠️ Puede tener problemas de importación
- ✅ Ejecución desde el directorio del servicio
- ✅ Carga automática de .env desde la raíz

## 🧪 Pruebas

### Script de Pruebas
```bash
python test_gateway_auth.py
```

Este script prueba:
- ✅ Rutas sin token
- ✅ Tokens inválidos
- ✅ Formatos incorrectos
- ✅ Rutas protegidas
- ✅ Rutas de administración
- ✅ Health check (sin autenticación) 