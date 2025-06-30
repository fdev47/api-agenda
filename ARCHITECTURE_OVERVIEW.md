# 🏗️ Arquitectura del Sistema - Microservicios

## 📋 **Resumen de la Arquitectura**

El sistema está diseñado siguiendo **Clean Architecture** y **SOLID principles** con una separación clara entre microservicios:

### **Auth Service** (Puerto 8001)
- **Responsabilidad**: Autenticación y autorización con Firebase
- **Base de datos**: Firebase Authentication
- **Endpoints**: Solo autenticación y validación de tokens

### **User Service** (Puerto 8002)
- **Responsabilidad**: Gestión completa de usuarios
- **Base de datos**: PostgreSQL
- **Endpoints**: CRUD de usuarios, perfiles, roles, administración

---

## 🔄 **Flujo de Creación de Usuario**

### **1. Cliente llama a User Service**
```http
POST /api/v1/users
{
  "email": "user@example.com",
  "password": "password123",
  "display_name": "John Doe"
}
```

### **2. User Service orquesta la creación**
```python
# CreateUserUseCase.execute()
1. Llama a Auth Service para crear en Firebase
2. Si Firebase es exitoso, crea en PostgreSQL
3. Si Firebase falla, NO toca PostgreSQL
```

### **3. Comunicación entre servicios**
```python
# AuthServiceClient.create_user()
POST http://localhost:8001/api/v1/auth/create-user
{
  "email": "user@example.com",
  "password": "password123",
  "display_name": "John Doe"
}
```

---

## 🏛️ **Clean Architecture Implementada**

### **User Service - Capas**

#### **1. Domain Layer** (Core Business Logic)
```
user_service/domain/
├── entities/          # Entidades de negocio
├── dto/              # Data Transfer Objects
├── exceptions/       # Excepciones de dominio
└── interfaces/       # Contratos/Protocolos
```

#### **2. Application Layer** (Use Cases)
```
user_service/application/use_cases/
├── create_user_use_case.py    # Orquesta creación
├── get_user_use_case.py       # Obtener usuario
├── update_user_use_case.py    # Actualizar usuario
└── delete_user_use_case.py    # Eliminar usuario
```

#### **3. Infrastructure Layer** (External Concerns)
```
user_service/infrastructure/
├── auth_service_client.py     # Cliente HTTP para Auth
├── container.py              # Inyección de dependencias
├── connection.py             # Base de datos
└── models/                   # Modelos SQLAlchemy
```

#### **4. API Layer** (Controllers)
```
user_service/api/
├── main.py                   # Aplicación FastAPI
├── routes/                   # Controladores
└── middleware.py             # Autenticación
```

---

## 🔧 **Principios SOLID Aplicados**

### **S - Single Responsibility Principle**
- ✅ `AuthServiceClient`: Solo comunicación con Auth Service
- ✅ `CreateUserUseCase`: Solo orquestación de creación
- ✅ `UserRepository`: Solo operaciones de base de datos

### **O - Open/Closed Principle**
- ✅ Uso de Protocols para interfaces
- ✅ Fácil extensión sin modificar código existente

### **L - Liskov Substitution Principle**
- ✅ Implementaciones siguen contratos de interfaces
- ✅ Repositorios intercambiables

### **I - Interface Segregation Principle**
- ✅ Interfaces específicas para cada responsabilidad
- ✅ No hay interfaces "gordas"

### **D - Dependency Inversion Principle**
- ✅ Use Cases dependen de abstracciones (Protocols)
- ✅ Inyección de dependencias en container

---

## 🚀 **Patrones de Diseño Utilizados**

### **1. Repository Pattern**
```python
class UserRepository(Protocol):
    async def create_user(self, user_data: dict) -> User: ...

class UserRepositoryImpl(UserRepository):
    async def create_user(self, user_data: dict) -> User:
        # Implementación con SQLAlchemy
```

### **2. Use Case Pattern**
```python
class CreateUserUseCase:
    def __init__(self, user_repository, auth_service_client):
        self.user_repository = user_repository
        self.auth_service_client = auth_service_client
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        # Orquestación del flujo de negocio
```

### **3. Dependency Injection**
```python
class UserServiceContainer(containers.DeclarativeContainer):
    auth_service_client = providers.Singleton(AuthServiceClient)
    user_repository = providers.Singleton(UserRepositoryImpl)
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        auth_service_client=auth_service_client
    )
```

### **4. Client-Server Pattern**
```python
class AuthServiceClient:
    async def create_user(self, request: CreateUserRequest) -> dict:
        # HTTP call a Auth Service
```

---

## 🔐 **Seguridad y Autenticación**

### **1. Validación de Tokens**
```python
# User Service middleware
async def require_auth(self, authorization: str) -> dict:
    # Llama a Auth Service para validar token
    user = await self._validate_token(token)
    return user
```

### **2. Control de Acceso**
```python
# Rutas protegidas
@router.get("/me")
async def get_current_user(current_user=Depends(auth_middleware.require_auth)):
    # Solo usuarios autenticados
```

### **3. Roles y Permisos**
```python
# Rutas administrativas
@router.post("/admin/users/assign-role")
async def assign_role(current_user=Depends(auth_middleware.require_role("admin"))):
    # Solo usuarios con rol admin
```

---

## 📊 **Manejo de Errores**

### **1. Errores de Dominio**
```python
class UserError(Exception):
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
```

### **2. Transaccionalidad**
```python
# Si Firebase falla, no tocar PostgreSQL
try:
    firebase_user = await self.auth_service_client.create_user(request)
    user = await self.user_repository.create_user(user_data)
except UserError:
    # Rollback automático - no se creó en PostgreSQL
    raise
```

### **3. Timeouts y Resiliencia**
```python
class AuthServiceClient:
    def __init__(self, base_url: str):
        self.timeout = 10.0  # 10 segundos timeout
```

---

## 🧪 **Testing Strategy**

### **1. Unit Tests**
- Use Cases con mocks
- Repositorios con base de datos en memoria
- Cliente HTTP con respuestas mock

### **2. Integration Tests**
- Comunicación entre servicios
- Base de datos real
- Auth Service real

### **3. End-to-End Tests**
- Flujo completo de creación de usuario
- Validación de tokens
- Control de acceso

---

## 🚀 **Despliegue y Escalabilidad**

### **1. Variables de Entorno**
```bash
# Auth Service
AUTH_SERVICE_PORT=8001
FIREBASE_PROJECT_ID=fortis-fa43c

# User Service
USER_SERVICE_PORT=8002
DATABASE_URL=postgresql://...
AUTH_SERVICE_URL=http://localhost:8001
```

### **2. Health Checks**
```http
GET /health
{
  "status": "healthy",
  "service": "user-service",
  "database_configured": true,
  "auth_service_url": "http://localhost:8001"
}
```

### **3. Monitoreo**
- Request ID único por request
- Headers estándar en todas las respuestas
- Logs estructurados
- Métricas de performance

---

## 📈 **Próximos Pasos**

### **1. Implementar**
- [x] Auth Service con Firebase
- [x] User Service con PostgreSQL
- [x] Comunicación entre servicios
- [x] Clean Architecture
- [ ] Tests automatizados
- [ ] Documentación de API

### **2. Mejorar**
- [ ] Circuit Breaker para llamadas HTTP
- [ ] Caché de tokens
- [ ] Rate limiting
- [ ] Logging centralizado
- [ ] Métricas y alertas

### **3. Escalar**
- [ ] Load balancer
- [ ] Base de datos replicada
- [ ] Microservicios independientes
- [ ] API Gateway
- [ ] Service Mesh 