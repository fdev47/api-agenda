"""
Script de prueba para verificar la población de usuarios
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(__file__))

from user_service.populate_data.user_data import populate_user_data

async def test_user_populate():
    """Probar la población de usuarios"""
    print("🧪 PROBANDO POBLACIÓN DE USUARIOS")
    print("=" * 50)
    
    # Verificar configuración
    access_token = os.getenv("ACCESS_TOKEN")
    api_gateway_url = os.getenv("API_GATEWAY_URL", "http://localhost:8000")
    
    print(f"🔧 Configuración:")
    print(f"   API Gateway URL: {api_gateway_url}")
    print(f"   Access Token: {'✅ Configurado' if access_token else '❌ No configurado'}")
    
    if not access_token:
        print("\n❌ ERROR: ACCESS_TOKEN no configurado")
        print("   Configura ACCESS_TOKEN en tu archivo .env")
        return
    
    # Probar en modo dry-run primero
    print("\n🔍 PROBANDO EN MODO DRY-RUN...")
    try:
        result = await populate_user_data(dry_run=True)
        print(f"✅ Dry-run exitoso: {result}")
    except Exception as e:
        print(f"❌ Error en dry-run: {e}")
        return
    
    # Preguntar si continuar con inserción real
    print("\n" + "=" * 50)
    response = input("¿Deseas continuar con la inserción real? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'sí', 'si']:
        print("\n🚀 INICIANDO INSERCIÓN REAL...")
        try:
            result = await populate_user_data(dry_run=False)
            print(f"✅ Inserción completada: {result}")
        except Exception as e:
            print(f"❌ Error en inserción: {e}")
    else:
        print("⏭️  Saltando inserción real")

if __name__ == "__main__":
    asyncio.run(test_user_populate()) 