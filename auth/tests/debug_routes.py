"""
Script para debuggear las rutas disponibles
"""
import requests
import json
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio raíz al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def check_routes():
    """Verificar todas las rutas disponibles"""
    # Obtener puerto del .env
    load_dotenv()
    
    service_port = os.getenv("AUTH_SERVICE_PORT", "8001")
    base_url = f"http://localhost:{service_port}"
    
    print("🔍 Verificando rutas disponibles...")
    
    # Obtener OpenAPI spec
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            data = response.json()
            
            print(f"📋 Servicio: {data.get('info', {}).get('title', 'Unknown')}")
            print(f"📋 Versión: {data.get('info', {}).get('version', 'Unknown')}")
            print("\n🚀 Rutas disponibles:")
            
            for path, methods in data['paths'].items():
                for method in methods.keys():
                    print(f"  {method.upper():<6} {path}")
                    
            print(f"\n📊 Total de rutas: {len(data['paths'])}")
            
        else:
            print(f"❌ Error obteniendo OpenAPI spec: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_specific_routes():
    """Probar rutas específicas"""
    # Obtener puerto del .env
    load_dotenv()
    
    service_port = os.getenv("AUTH_SERVICE_PORT", "8001")
    base_url = f"http://localhost:{service_port}"
    
    print("\n🧪 Probando rutas específicas...")
    
    routes_to_test = [
        "/health",
        "/auth/register",
        "/auth/login",
        "/auth/refresh",
        "/auth/validate",
        "/auth/validate-token",
        "/users/me",
        "/users/1"
    ]
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}")
            print(f"  {route:<20} - Status: {response.status_code}")
            
            if response.status_code == 404:
                print(f"    ❌ No encontrado")
            elif response.status_code == 405:
                print(f"    ⚠️  Método no permitido (probablemente POST)")
            elif response.status_code == 401:
                print(f"    🔐 Requiere autenticación")
            elif response.status_code == 403:
                print(f"    🚫 Prohibido")
            elif response.status_code == 200:
                print(f"    ✅ OK")
            else:
                print(f"    ❓ Status inesperado")
                
        except requests.exceptions.RequestException as e:
            print(f"  {route:<20} - Error: {e}")

if __name__ == "__main__":
    check_routes()
    test_specific_routes() 