"""
Script para probar con un token real de Firebase
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

def test_login_and_validate():
    """Probar login y luego validar el token"""
    print("🧪 Probando login y validación de token...")
    
    # Datos de prueba (ajusta según tu configuración)
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        # Intentar login
        print("📝 Intentando login...")
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("token", {}).get("access_token")
            
            if token:
                print("✅ Login exitoso, probando token...")
                
                # Probar el token
                headers = {"Authorization": f"Bearer {token}"}
                user_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
                
                print(f"Token validation Status: {user_response.status_code}")
                print(f"Response: {json.dumps(user_response.json(), indent=2)}")
                
                if user_response.status_code == 200:
                    print("✅ Token válido")
                else:
                    print("❌ Token inválido")
            else:
                print("❌ No se obtuvo token del login")
        else:
            print(f"❌ Login falló: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_register_and_login():
    """Probar registro y login"""
    print("\n🧪 Probando registro y login...")
    
    # Datos de registro
    register_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "display_name": "Test User"
    }
    
    try:
        # Intentar registro
        print("📝 Intentando registro...")
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Register Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Registro exitoso")
            
            # Intentar login con el usuario registrado
            login_data = {
                "email": register_data["email"],
                "password": register_data["password"]
            }
            
            print("📝 Intentando login...")
            login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            print(f"Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                data = login_response.json()
                token = data.get("token", {}).get("access_token")
                
                if token:
                    print("✅ Login exitoso")
                    print(f"Token: {token[:50]}...")
                    
                    # Probar el token
                    headers = {"Authorization": f"Bearer {token}"}
                    user_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
                    
                    print(f"Token validation Status: {user_response.status_code}")
                    if user_response.status_code == 200:
                        print("✅ Token válido")
                        print(f"User: {json.dumps(user_response.json(), indent=2)}")
                    else:
                        print(f"❌ Token inválido: {user_response.json()}")
                else:
                    print("❌ No se obtuvo token del login")
            else:
                print(f"❌ Login falló: {login_response.json()}")
        else:
            print(f"❌ Registro falló: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas con tokens reales...")
    print(f"📡 URL base: {BASE_URL}")
    print(f"🔧 Puerto configurado: {SERVICE_PORT}")
    
    test_register_and_login()
    # test_login_and_validate()
    
    print("\n✅ Pruebas completadas") 