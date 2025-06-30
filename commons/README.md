# Módulo Commons - Base de Datos

Este módulo proporciona funcionalidades comunes para la conexión y gestión de base de datos que pueden ser utilizadas por todos los microservicios.

## Estructura

```
commons/
├── __init__.py          # Inicialización del módulo
├── config.py           # Configuración común
├── database.py         # Gestión de conexión a BD
├── examples.py         # Ejemplos de uso
└── README.md           # Esta documentación
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_bd
DATABASE_ECHO=false

# Configuración general
LOG_LEVEL=INFO
ENVIRONMENT=development
SERVICE_PORT=8000
CORS_ORIGINS=["http://localhost:3000"]
```

## Uso Básico

### 1. Importar el módulo común

```python
from commons.database import Base, db_manager, create_tables, get_db_session
```

### 2. Definir modelos

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from commons.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### 3. Inicializar base de datos

```python
async def initialize_database():
    # Crear tablas
    await create_tables()
    print("✅ Tablas creadas")
    
    # Probar conexión
    is_connected = await test_connection()
    print(f"✅ Conexión exitosa: {is_connected}")
```

### 4. Usar en FastAPI

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from commons.database import get_db_session

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db_session)):
    # Tu lógica aquí
    pass
```

## Configuración por Microservicio

### 1. Configuración específica

```python
# user_service/infrastructure/config.py
from pydantic import BaseSettings
from commons.config import Settings as BaseSettings

class UserServiceSettings(BaseSettings):
    SERVICE_NAME: str = "user-service"
    SERVICE_PORT: int = 8001
    USER_DEFAULT_ROLE: str = "user"
    
    class Config:
        env_file = ".env"

user_settings = UserServiceSettings()
```

### 2. Inicialización específica

```python
# user_service/infrastructure/connection.py
from commons.database import db_manager, Base

async def initialize_user_service_database():
    # Importar modelos específicos
    from .models import user, profile, role
    
    # Crear tablas
    await db_manager.create_tables(Base)
    print("✅ Base de datos del servicio de usuarios inicializada")
```

## Ventajas

1. **Reutilización**: Un solo módulo para todos los microservicios
2. **Consistencia**: Misma configuración y comportamiento en todos los servicios
3. **Mantenimiento**: Cambios centralizados en un solo lugar
4. **Flexibilidad**: Cada microservicio puede tener su propia configuración específica
5. **Compatibilidad**: Mantiene compatibilidad con código existente

## Funciones Disponibles

### DatabaseManager

- `create_tables(base)`: Crear tablas
- `drop_tables(base)`: Eliminar tablas
- `test_connection()`: Probar conexión
- `get_session()`: Obtener sesión
- `close()`: Cerrar conexión

### Funciones de Conveniencia

- `create_tables(base)`: Crear tablas
- `get_db_session()`: Dependency para FastAPI
- `test_connection()`: Probar conexión

## Ejemplos

Ver `examples.py` para ejemplos completos de uso.

# Commons - Componentes Compartidos

Este directorio contiene componentes reutilizables para todos los microservicios.

## Autenticación

### Uso del Cliente de Autenticación

El módulo `auth_client.py` proporciona dependencias de autenticación reutilizables que se comunican con el Auth Service.

#### Opción 1: Uso directo desde commons

```python
from commons.auth_client import require_auth, require_role

@router.get("/me")
async def get_current_user(current_user=Depends(require_auth)):
    return current_user

@router.post("/admin/users")
async def admin_action(current_user=Depends(require_role("admin"))):
    return {"message": "Acción administrativa"}
```

#### Opción 2: Uso con configuración personalizada

```python
from commons.auth_client import create_auth_dependencies

# Crear dependencias con configuración personalizada
require_auth, require_role = create_auth_dependencies(
    auth_service_url="http://custom-auth:8001",
    api_prefix="/api/v2"
)

@router.get("/me")
async def get_current_user(current_user=Depends(require_auth)):
    return current_user
```

#### Opción 3: Uso a través de middleware local (recomendado)

```python
# En user_service/api/middleware.py
from commons.auth_client import require_auth, require_role

auth_middleware = {
    "require_auth": require_auth,
    "require_role": require_role
}

# En las rutas
from ..middleware import auth_middleware

@router.get("/me")
async def get_current_user(current_user=Depends(auth_middleware["require_auth"])):
    return current_user
```

### Configuración

El cliente usa las siguientes variables de entorno:
- `AUTH_SERVICE_URL`: URL del Auth Service
- `API_VERSION`: Versión de la API (ej: "v1")

### Respuestas de Error

El cliente maneja automáticamente los siguientes errores:
- **401**: Token faltante o inválido
- **403**: Permisos insuficientes
- **503**: Auth Service no disponible

### Beneficios

1. **Reutilización**: Un solo cliente para todos los microservicios
2. **Consistencia**: Mismo manejo de errores en toda la aplicación
3. **Mantenibilidad**: Cambios centralizados en un solo lugar
4. **Flexibilidad**: Configuración personalizable por servicio 