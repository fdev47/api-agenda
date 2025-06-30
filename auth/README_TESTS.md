# Tests del Servicio Auth

Este directorio contiene todos los tests y scripts de utilidad para el servicio de autenticación.

## 📁 Estructura

```
auth/
├── tests/
│   ├── __init__.py
│   ├── debug_routes.py          # Verificar rutas disponibles
│   ├── test_middleware_errors.py # Probar manejo de errores
│   ├── test_complete_flow.py    # Flujo completo de autenticación
│   └── test_with_real_token.py  # Pruebas con tokens reales
├── start_auth_service.py        # Script para iniciar el servicio
├── run_tests.py                 # Ejecutar todos los tests
└── README_TESTS.md              # Esta documentación
```

## 🚀 Cómo Usar

### 1. Iniciar el Servicio

```bash
# Desde el directorio auth/
python -m start_auth_service.py

# O desde la raíz del proyecto
python auth/start_auth_service.py
```

### 2. Ejecutar Tests Individuales

```bash
# Desde el directorio auth/
python tests/debug_routes.py
python tests/test_middleware_errors.py
python tests/test_complete_flow.py
python tests/test_with_real_token.py
```

### 3. Ejecutar Todos los Tests

```bash
# Desde el directorio auth/
python run_tests.py

# O desde la raíz del proyecto
python auth/run_tests.py
```

## 🧪 Descripción de los Tests

### `debug_routes.py`
- **Propósito**: Verificar que todas las rutas estén disponibles
- **Qué hace**: Consulta el OpenAPI spec y prueba rutas específicas
- **Uso**: Para verificar que el servicio se inició correctamente

### `test_middleware_errors.py`
- **Propósito**: Probar el manejo de errores del middleware
- **Qué hace**: Prueba tokens expirados, inválidos y sin token
- **Uso**: Para verificar que los errores usen nuestro formato personalizado

### `test_complete_flow.py`
- **Propósito**: Probar el flujo completo de autenticación
- **Qué hace**: Registro → Login → Acceso a rutas protegidas
- **Uso**: Para verificar que todo el flujo funcione correctamente

### `test_with_real_token.py`
- **Propósito**: Probar con tokens reales de Firebase
- **Qué hace**: Login con credenciales reales y validación de tokens
- **Uso**: Para pruebas de integración con Firebase

## ⚙️ Configuración

Los tests usan las variables de entorno del archivo `.env` en la raíz del proyecto:

```bash
# Configuración específica del servicio Auth
AUTH_SERVICE_PORT=8001
AUTH_SERVICE_NAME=auth-service
AUTH_SERVICE_VERSION=1.0.0
AUTH_CORS_ORIGINS=http://localhost:3000,http://localhost:8080,*

# Configuración compartida
FIREBASE_PROJECT_ID=fortis-fa43c
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
ENVIRONMENT=development
```

## 🔧 Troubleshooting

### Error de Importación
Si tienes errores de importación, asegúrate de ejecutar los tests desde el directorio correcto:

```bash
# ✅ Correcto - desde auth/
cd auth
python tests/debug_routes.py

# ❌ Incorrecto - desde la raíz
python auth/tests/debug_routes.py
```

### Servicio No Disponible
Si el servicio no está ejecutándose:

```bash
# Verificar si está corriendo
curl http://localhost:8001/health

# Iniciar el servicio
python start_auth_service.py
```

### Errores de Firebase
Si hay errores relacionados con Firebase:

1. Verificar que el archivo `.env` esté configurado
2. Verificar que las credenciales de Firebase sean válidas
3. Verificar que el proyecto de Firebase esté activo

## 📊 Interpretar Resultados

### Status Codes Esperados
- **200**: Operación exitosa
- **401**: No autenticado (token inválido/expirado)
- **403**: Prohibido (sin token)
- **404**: No encontrado
- **405**: Método no permitido (GET vs POST)
- **500**: Error interno del servidor

### Formato de Errores Personalizados
Los errores deben tener este formato:

```json
{
  "error": "auth_error",
  "message": "Token expirado",
  "error_code": "TOKEN_EXPIRED",
  "token_expired": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🎯 Próximos Pasos

1. **Agregar tests unitarios** para casos de uso individuales
2. **Agregar tests de integración** para Firebase
3. **Agregar tests de rendimiento** para el middleware
4. **Configurar CI/CD** para ejecutar tests automáticamente 