## ESTRUCTURA
auth-service/
├── auth_service/                    # Paquete principal
│   ├── __init__.py
│   ├── domain/                      # Capa de dominio
│   │   ├── __init__.py
│   │   ├── models.py                # Modelos de dominio
│   │   └── interfaces.py            # Interfaces/contratos
│   ├── infrastructure/              # Capa de infraestructura
│   │   ├── __init__.py
│   │   ├── firebase/
│   │   │   ├── __init__.py
│   │   │   ├── auth_provider.py
│   │   │   ├── token_validator.py
│   │   │   └── claims_manager.py
│   │   └── container.py             # Contenedor de DI
│   ├── use_cases/                   # Casos de uso
│   │   ├── __init__.py
│   │   └── auth_use_cases.py
│   └── api/                         # API REST
│       ├── __init__.py
│       ├── main.py
│       ├── middleware.py
│       └── schemas.py
├── requirements.txt
└── .env.example

## INSTALACIÓN Y CONFIGURACIÓN

1. Instalar dependencias:
   pip install -r requirements.txt

2. Configurar Firebase:
   - Crear proyecto en Firebase Console
   - Descargar archivo de credenciales JSON
   - Configurar variable de entorno FIREBASE_CREDENTIALS_PATH

3. Configurar variables de entorno:
   cp .env.example .env
   # Editar .env con tus valores

4. Ejecutar el servicio:
   uvicorn auth_service.api.main:create_app --factory --reload --host 0.0.0.0 --port 8000

## EJEMPLO DE USO

```python
from auth_service import AuthServiceContainer, UserRegistration

# Inicializar container
container = AuthServiceContainer("path/to/firebase-credentials.json")

# Crear usuario
registration = UserRegistration(
    email="user@example.com",
    password="securePassword123",
    display_name="Usuario Test"
)

try:
    # Crear usuario con rol inicial
    user = container.create_user_use_case.execute(registration, "customer")
    print(f"Usuario creado: {user.email}")
    
    # Validar token (normalmente viene del cliente)
    # validated_user = container.validate_token_use_case.execute(id_token)
    
    # Gestionar roles
    container.manage_roles_use_case.assign_permission(user.user_id, "create_reservation")
    roles = container.manage_roles_use_case.get_user_roles(user.user_id)
    print(f"Roles del usuario: {roles}")
    
except AuthError as e:
    print(f"Error de autenticación: {e}")
```

## ENDPOINTS DISPONIBLES

### Públicos
- POST /users - Crear usuario
- POST /validate-token - Validar token

### Autenticados
- GET /me - Información del usuario actual
- GET /users/{user_id} - Obtener usuario por ID

### Solo Admins
- POST /users/assign-role - Asignar rol
- POST /users/assign-permission - Asignar permiso
- DELETE /users/{user_id} - Eliminar usuario

## ESTRUCTURA DE RESPUESTAS

### Usuario
```json
{
  "user_id": "string",
  "email": "string",
  "display_name": "string",
  "phone_number": "string",
  "email_verified": true,
  "roles": ["user", "admin"],
  "permissions": ["read", "write"],
  "organization_id": "string",
  "created_at": "2023-01-01T00:00:00",
  "last_sign_in": "2023-01-01T00:00:00"
}
```

### Error
```json
{
  "error": "auth_error",
  "message": "Descripción del error",
  "error_code": "INVALID_TOKEN",
  "details": {}
}
```

### Éxito
```json
{
  "success": true,
  "message": "Operación completada",
  "data": {}
}
```

## CAMBIAR DE PROVEEDOR BaaS

Para cambiar de Firebase a otro proveedor (AWS Cognito, Auth0, etc.):

1. Crear nuevas implementaciones de las interfaces:
   - IAuthProvider
   - ITokenValidator  
   - IUserClaimsManager

2. Actualizar el container:
```python
class AuthServiceContainer:
    def __init__(self, config):
        # Cambiar implementaciones
        self._auth_provider = CognitoAuthProvider(config)  # En lugar de Firebase
        self._token_validator = CognitoTokenValidator()
        self._claims_manager = CognitoUserClaimsManager(self._auth_provider)
        
        # Los use cases permanecen iguales
        # ...
```

El resto del código no necesita cambios gracias a la arquitectura SOLID.