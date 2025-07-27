"""
Script para poblar usuarios en user_service usando api_gateway
"""
import os
import sys
import asyncio
from commons.api_client import APIClient
from commons.config import config

async def get_profiles(api_client: APIClient):
    """
    Obtener perfiles disponibles para asignar a usuarios
    """
    try:
        response = await api_client.get(f"{config.API_PREFIX}/profiles/")
        if response:
            profiles = response.get('profiles', [])
            print(response)
            profile_map = {profile['name']: profile['id'] for profile in profiles}
            return profile_map
        return {}
    except Exception as e:
        print(f"⚠️  Error obteniendo perfiles: {e}")
        return {}

async def populate_user_data(dry_run: bool = False):
    """
    Poblar datos de usuarios usando el api_gateway
    """
    print("🙍 Poblando datos de usuarios...")
    
    # Configuración del API Gateway
    api_gateway_url = config.API_GATEWAY_URL
    access_token = os.getenv("ACCESS_TOKEN")
    
    if not access_token:
        print("❌ ERROR: ACCESS_TOKEN no configurado en variables de entorno")
        print("   Configura ACCESS_TOKEN en tu archivo .env")
        return {"users": 0}
    
    # Obtener perfiles disponibles
    async with APIClient(api_gateway_url, access_token) as api_client:
        profiles = await get_profiles(api_client)
        super_admin_id = profiles.get('SUPER_ADMIN')
        
        if not super_admin_id:
            print("⚠️  No se encontró el perfil SUPER_ADMIN")
            super_admin_id = None
    
    # Datos de usuarios a insertar (solo un usuario de prueba)
    users_data = [
        {
            "email": "test.username@example.com",
            "password": "123456",
            "username": "testuser",  # Nuevo campo
            "first_name": "Test",
            "last_name": "User",
            "phone": "555-1234",
            "cellphone_number": "991222333",
            "cellphone_country_code": "+595",
            "user_type": "admin",
            "profile_ids": [super_admin_id] if super_admin_id else [],  # Asignar SUPER_ADMIN
            "two_factor_enabled": False,
            "send_email_verification": False
        }
    ]
    
    if dry_run:
        print(f"🔍 Simulando inserción de {len(users_data)} usuarios...")
        for user in users_data:
            print(f"   - {user['email']}: {user['first_name']} {user['last_name']}")
            print(f"     Tipo: {user['user_type']}, Password: {user['password']}")
        return {"users": len(users_data)}
    
    inserted_count = 0
    
    try:
        async with APIClient(api_gateway_url, access_token) as api_client:
            for user_data in users_data:
                try:
                    print(f"   📝 Creando usuario: {user_data['email']}")
                    
                    # Crear usuario a través del API Gateway
                    response = await api_client.post(f"{config.API_PREFIX}/users/", data=user_data)
                    
                    if response:
                        print(f"   ✅ Usuario '{user_data['email']}' creado exitosamente")
                        print(f"      ID: {response.get('id', 'N/A')}")
                        print(f"      Auth UID: {response.get('auth_uid', 'N/A')}")
                        inserted_count += 1
                    else:
                        print(f"   ⚠️  Usuario '{user_data['email']}' no se pudo crear")
                    
                except Exception as e:
                    print(f"   ❌ Error creando usuario '{user_data['email']}': {e}")
                    continue
                    
    except Exception as e:
        print(f"❌ Error conectando con API Gateway: {e}")
        return {"users": 0}
    
    print(f"✅ Se insertaron {inserted_count} usuarios nuevos")
    return {"users": inserted_count}

if __name__ == "__main__":
    asyncio.run(populate_user_data()) 