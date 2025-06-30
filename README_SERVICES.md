# 🚀 Servicios de la API

## 📋 **Estructura de Servicios**

### **API Gateway** (Puerto 8000)
- **Responsabilidad**: Orquestador principal de microservicios
- **Script**: `run_gateway.py`
- **Documentación**: `/docs` en http://localhost:8000

### **Auth Service** (Puerto 8001)
- **Responsabilidad**: Validación de tokens de Firebase Auth
- **Script**: `run_auth_service.py` (raíz) o `auth/start_auth_service.py`
- **Documentación**: `/docs` en http://localhost:8001

### **User Service** (Puerto 8002)
- **Responsabilidad**: Gestión de usuarios en PostgreSQL
- **Script**: `run_user_service.py` (raíz) o `user_service/start_user_service.py`
- **Documentación**: `/docs` en http://localhost:8002

---

## 🔥 **Flujo de Autenticación con Firebase**

### **1. Autenticación del Cliente**
```javascript
// En tu aplicación web/móvil
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const auth = getAuth();
const userCredential = await signInWithEmailAndPassword(auth, email, password);
const idToken = await userCredential.user.getIdToken();
```

### **2. Validación en tu API**
```javascript
// Enviar token a tu API
const response = await fetch('/api/v1/auth/validate-token', {
  headers: {
    'Authorization': `Bearer ${idToken}`
  }
});
```

### **3. Crear Usuario en tu Base de Datos**
```javascript
// Después de validar el token, crear usuario en PostgreSQL
const response = await fetch('/api/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${idToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    firebase_uid: userCredential.user.uid,
    email: userCredential.user.email,
    display_name: userCredential.user.displayName
  })
});
```

---

## 🏃‍♂️ **Ejecutar Servicios**

### **Desde la Raíz del Proyecto**

```bash
# API Gateway (orquestador principal)
python run_gateway.py

# Auth Service (validación de tokens)
python run_auth_service.py

# User Service (gestión de usuarios)
python run_user_service.py
```

### **Desde el Directorio del Servicio**

```bash
# Auth Service
cd auth
python start_auth_service.py

# User Service
cd user_service
python start_user_service.py
```

---

## 🔧 **Configuración**

### **Variables de Entorno Requeridas**

```bash
# Archivo .env en la raíz del proyecto

# Configuración Global
ENVIRONMENT=development
LOG_LEVEL=INFO
API_VERSION=v1

# Firebase (compartido)
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
FIREBASE_PROJECT_ID=your-project-id

# Base de Datos (compartido)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# API Gateway
GATEWAY_SERVICE_PORT=8000
GATEWAY_CORS_ORIGINS=http://localhost:3000,*

# Auth Service
AUTH_SERVICE_PORT=8001
AUTH_CORS_ORIGINS=http://localhost:3000,*

# User Service
USER_SERVICE_PORT=8002
USER_CORS_ORIGINS=http://localhost:3000,*

# Comunicación entre servicios
AUTH_SERVICE_URL=http://localhost:8001
USER_SERVICE_URL=http://localhost:8002
```

---

## 🌐 **Endpoints Disponibles**

### **API Gateway (http://localhost:8000)**
```
/api/v1/auth/validate-token    # Validar token de Firebase
/api/v1/auth/user-info         # Obtener info del usuario
/api/v1/users/                 # CRUD de usuarios
/api/v1/admin/users/           # Funciones administrativas
```

### **Auth Service (http://localhost:8001)**
```
/api/v1/auth/validate-token    # Validar token de Firebase
/api/v1/auth/user-info         # Obtener info del usuario
/api/v1/auth/create-user       # Crear usuario en Firebase (interno)
```

### **User Service (http://localhost:8002)**
```
/api/v1/users/                 # CRUD de usuarios
/api/v1/users/me               # Usuario actual
/api/v1/admin/users/           # Funciones administrativas
```

---

## 🧪 **Testing**

### **Ejecutar Tests del Auth Service**
```bash
cd auth
python run_tests.py
```

### **Health Checks**
```bash
# API Gateway
curl http://localhost:8000/health

# Auth Service
curl http://localhost:8001/health

# User Service
curl http://localhost:8002/health
```

---

## 📚 **Documentación**

### **Swagger UI**
- **API Gateway**: http://localhost:8000/docs
- **Auth Service**: http://localhost:8001/docs
- **User Service**: http://localhost:8002/docs

### **ReDoc**
- **API Gateway**: http://localhost:8000/redoc
- **Auth Service**: http://localhost:8001/redoc
- **User Service**: http://localhost:8002/redoc

---

## 🔄 **Flujo de Comunicación**

```
Cliente (Firebase Auth) → API Gateway → Auth Service (Validar Token)
                                    ↓
                                User Service (PostgreSQL)
```

### **Ejemplo: Crear Usuario**
1. Cliente se autentica con Firebase y obtiene ID Token
2. Cliente llama a `POST /api/v1/users` en API Gateway con el token
3. API Gateway valida el token con Auth Service
4. Si es válido, API Gateway llama a User Service para crear en PostgreSQL
5. API Gateway retorna respuesta unificada al cliente

---

## 🚨 **Solución de Problemas**

### **Error: Puerto ya en uso**
```bash
# Verificar puertos en uso
lsof -i :8000
lsof -i :8001
lsof -i :8002

# Matar proceso si es necesario
kill -9 <PID>
```

### **Error: Variables de entorno no encontradas**
```bash
# Verificar archivo .env
ls -la .env

# Verificar variables cargadas
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('AUTH_SERVICE_URL:', os.getenv('AUTH_SERVICE_URL'))"
```

### **Error: Servicio no responde**
```bash
# Verificar logs del servicio
# Verificar configuración de Firebase/Database
# Verificar conectividad entre servicios
```

---

## 🔐 **Autenticación en Swagger UI**

Para probar endpoints protegidos en Swagger UI:

1. **Obtener token de Firebase** desde tu aplicación
2. **Hacer clic en "Authorize"** en Swagger UI
3. **Ingresar**: `Bearer <tu-firebase-id-token>`
4. **Probar endpoints** que requieren autenticación 