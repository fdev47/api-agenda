#!/usr/bin/env python3
"""
Script de prueba para las operaciones CRUD del Auth Service
"""
import asyncio
import aiohttp
import json
from commons.config import config

AUTH_SERVICE_URL = config.AUTH_SERVICE_URL
API_PREFIX = config.API_PREFIX

async def test_auth_crud():
    """Probar operaciones CRUD del Auth Service"""
    
    print("🧪 Probando operaciones CRUD del Auth Service...")
    print(f"📍 URL: {AUTH_SERVICE_URL}")
    print("=" * 60)
    
    # Datos de prueba
    test_user = {
        "email": "test.crud@example.com",
        "password": "password123",
        "display_name": "Usuario Test CRUD",
        "phone_number": "+1234567890",
        "two_factor_enabled": False,
        "send_email_verification": False
    }
    
    created_user_id = None
    
    try:
        async with aiohttp.ClientSession() as session:
            
            # 1. CREAR USUARIO
            print("📝 1. Creando usuario...")
            async with session.post(
                f"{AUTH_SERVICE_URL}{API_PREFIX}/auth/register",
                json=test_user
            ) as response:
                if response.status == 200:
                    user_data = await response.json()
                    created_user_id = user_data.get("user_id")
                    print(f"   ✅ Usuario creado: {created_user_id}")
                    print(f"   📧 Email: {user_data.get('email')}")
                    print(f"   👤 Nombre: {user_data.get('display_name')}")
                else:
                    error_data = await response.json()
                    print(f"   ❌ Error creando usuario: {error_data}")
                    return
            
            if not created_user_id:
                print("   ❌ No se pudo obtener el ID del usuario creado")
                return
            
            # 2. ACTUALIZAR USUARIO
            print("\n📝 2. Actualizando usuario...")
            update_data = {
                "display_name": "Usuario Test CRUD Actualizado",
                "phone_number": "+0987654321",
                "email_verified": True
            }
            
            async with session.put(
                f"{AUTH_SERVICE_URL}{API_PREFIX}/auth/users/{created_user_id}",
                json=update_data
            ) as response:
                if response.status == 200:
                    updated_user = await response.json()
                    print(f"   ✅ Usuario actualizado")
                    print(f"   👤 Nuevo nombre: {updated_user.get('display_name')}")
                    print(f"   📱 Nuevo teléfono: {updated_user.get('phone_number')}")
                    print(f"   ✅ Email verificado: {updated_user.get('email_verified')}")
                else:
                    error_data = await response.json()
                    print(f"   ❌ Error actualizando usuario: {error_data}")
            
            # 3. ELIMINAR USUARIO
            print("\n📝 3. Eliminando usuario...")
            async with session.delete(
                f"{AUTH_SERVICE_URL}{API_PREFIX}/auth/users/{created_user_id}"
            ) as response:
                if response.status == 200:
                    delete_result = await response.json()
                    print(f"   ✅ Usuario eliminado: {delete_result.get('message')}")
                else:
                    error_data = await response.json()
                    print(f"   ❌ Error eliminando usuario: {error_data}")
            
            # 4. VERIFICAR QUE EL USUARIO FUE ELIMINADO
            print("\n📝 4. Verificando que el usuario fue eliminado...")
            async with session.get(
                f"{AUTH_SERVICE_URL}{API_PREFIX}/auth/users/{created_user_id}"
            ) as response:
                if response.status == 404:
                    print("   ✅ Usuario no encontrado (eliminado correctamente)")
                else:
                    print(f"   ⚠️ Usuario aún existe: {response.status}")
            
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")

if __name__ == "__main__":
    asyncio.run(test_auth_crud()) 