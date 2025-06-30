"""
Script completo para probar el flujo de autenticación
"""
import requests
import json
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio raíz al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Cargar variables de entorno
load_dotenv()

# URL base del servicio auth
SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT", "8001")
BASE_URL = f"http://localhost:{SERVICE_PORT}"

def test_complete_flow():
    """Probar el flujo completo: registro -> login -> acceso protegido"""
    print("🚀 Iniciando prueba del flujo completo...")
    print(f"📡 URL base: {BASE_URL}")
    
    # Paso 1: Registrar un usuario
    print("\n📝 Paso 1: Registrando usuario...")
    register_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "display_name": "Test User"
    }
    
    try:
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Registro Status: {register_response.status_code}")
        
        if register_response.status_code == 200:
            print("✅ Usuario registrado exitosamente")
            user_data = register_response.json()
            print(f"Usuario: {json.dumps(user_data, indent=2)}")
        else:
            print(f"❌ Error en registro: {register_response.json()}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión en registro: {e}")
        return
    
    # Paso 2: Login del usuario
    print("\n🔐 Paso 2: Haciendo login...")
    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ Login exitoso")
            auth_data = login_response.json()
            token = auth_data.get("token", {}).get("access_token")
            
            if token:
                print(f"Token obtenido: {token[:50]}...")
                
                # Paso 3: Probar acceso a ruta protegida /users/me
                print("\n👤 Paso 3: Probando /users/me...")
                headers = {"Authorization": f"Bearer {token}"}
                
                me_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
                print(f"/users/me Status: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    print("✅ /users/me exitoso")
                    me_data = me_response.json()
                    print(f"Usuario actual: {json.dumps(me_data, indent=2)}")
                    
                    # Paso 4: Probar acceso a ruta protegida /users/{user_id}
                    print(f"\n🔍 Paso 4: Probando /users/{me_data['user_id']}...")
                    
                    user_response = requests.get(f"{BASE_URL}/users/{me_data['user_id']}", headers=headers)
                    print(f"/users/{me_data['user_id']} Status: {user_response.status_code}")
                    
                    if user_response.status_code == 200:
                        print("✅ /users/{user_id} exitoso")
                        user_data = user_response.json()
                        print(f"Usuario por ID: {json.dumps(user_data, indent=2)}")
                    else:
                        print(f"❌ Error en /users/{me_data['user_id']}: {user_response.json()}")
                        
                else:
                    print(f"❌ Error en /users/me: {me_response.json()}")
                    
            else:
                print("❌ No se obtuvo token del login")
        else:
            print(f"❌ Error en login: {login_response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión en login: {e}")

def test_without_token():
    """Probar acceso sin token"""
    print("\n🚫 Probando acceso sin token...")
    
    try:
        # Probar /users/me sin token
        response = requests.get(f"{BASE_URL}/users/me")
        print(f"/users/me sin token - Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Probar /users/1 sin token
        response2 = requests.get(f"{BASE_URL}/users/1")
        print(f"/users/1 sin token - Status: {response2.status_code}")
        print(f"Response: {json.dumps(response2.json(), indent=2)}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_invalid_token():
    """Probar con token inválido"""
    print("\n🚫 Probando con token inválido...")
    
    invalid_token = "invalid_token_here"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"/users/me con token inválido - Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🧪 Iniciando pruebas del flujo de autenticación...")
    print(f"🔧 Puerto configurado: {SERVICE_PORT}")
    
    # Probar flujo completo
    test_complete_flow()
    
    # Probar casos de error
    test_without_token()
    test_invalid_token()
    
    print("\n✅ Pruebas completadas") 