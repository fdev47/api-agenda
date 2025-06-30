"""
Script de prueba para verificar el manejo de errores del middleware
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

# URL base del servicio auth (usar puerto del .env)
SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT", "8001")
BASE_URL = f"http://localhost:{SERVICE_PORT}"

def test_expired_token():
    """Probar con un token expirado"""
    print("🧪 Probando token expirado...")
    
    # Token expirado de ejemplo (esto debería fallar)
    expired_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdCIsImF1ZCI6InRlc3QiLCJhdXRoX3RpbWUiOjE2NzI1MjgwMDAsInVzZXJfaWQiOiJ0ZXN0IiwiaWF0IjoxNjcyNTI4MDAwLCJleHAiOjE2NzI1MjgwMDB9.invalid_signature"
    
    headers = {
        "Authorization": f"Bearer {expired_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Verificar que devuelve nuestro formato de error
        if response.status_code == 401:
            data = response.json()
            if "error" in data and "error_code" in data:
                print("✅ Error manejado correctamente con formato personalizado")
            else:
                print("❌ Error no tiene formato personalizado")
        else:
            print(f"❌ Status code inesperado: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_missing_token():
    """Probar sin token"""
    print("\n🧪 Probando sin token...")
    
    try:
        response = requests.get(f"{BASE_URL}/users/me")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            data = response.json()
            if "error" in data and "error_code" in data:
                print("✅ Error manejado correctamente con formato personalizado")
            else:
                print("❌ Error no tiene formato personalizado")
        else:
            print(f"❌ Status code inesperado: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_invalid_token():
    """Probar con token inválido"""
    print("\n🧪 Probando token inválido...")
    
    invalid_token = "invalid_token_here"
    
    headers = {
        "Authorization": f"Bearer {invalid_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            data = response.json()
            if "error" in data and "error_code" in data:
                print("✅ Error manejado correctamente con formato personalizado")
            else:
                print("❌ Error no tiene formato personalizado")
        else:
            print(f"❌ Status code inesperado: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del middleware...")
    print(f"📡 URL base: {BASE_URL}")
    print(f"🔧 Puerto configurado: {SERVICE_PORT}")
    
    test_expired_token()
    test_missing_token()
    test_invalid_token()
    
    print("\n✅ Pruebas completadas") 