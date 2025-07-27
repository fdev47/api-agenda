"""
Script para poblar usuarios en user_service usando api_gateway
"""
import os
from commons.api_client import create_api_client

async def populate_user_data(dry_run: bool = False):
    """
    Poblar datos de usuarios usando el api_gateway
    """
    print("🙍 Poblando datos de usuarios...")
    
    # Configuración del API Gateway
    api_gateway_url = os.getenv("API_GATEWAY_URL", "http://localhost:8000")
    access_token = os.getenv("ACCESS_TOKEN")
    
    if not access_token:
        print("❌ ERROR: ACCESS_TOKEN no configurado en variables de entorno")
        print("   Configura ACCESS_TOKEN en tu archivo .env")
        return {"users": 0}
    
    # Datos de usuarios a insertar
    users_data = [
        {
            "auth_uid": "user_recepcionista_001",
            "email": "recepcionista@fortis.com",
            "first_name": "María",
            "last_name": "González",
            "phone": "555-1234",
            "cellphone_number": "5512345678",
            "cellphone_country_code": "+52",
            "user_type": "user",
            "is_active": True
        }
        # {
        #     "auth_uid": "user_recepcionista_frio_001", 
        #     "email": "recepcionista.frio@fortis.com",
        #     "first_name": "Carlos",
        #     "last_name": "Rodríguez",
        #     "phone": "555-5678",
        #     "cellphone_number": "5587654321",
        #     "cellphone_country_code": "+52",
        #     "user_type": "user",
        #     "is_active": True
        # },
        # {
        #     "auth_uid": "user_agendamiento_001",
        #     "email": "agendamiento@fortis.com", 
        #     "first_name": "Ana",
        #     "last_name": "Martínez",
        #     "phone": "555-9012",
        #     "cellphone_number": "5598765432",
        #     "cellphone_country_code": "+52",
        #     "user_type": "user",
        #     "is_active": True
        # },
        # {
        #     "auth_uid": "user_admin_001",
        #     "email": "admin@fortis.com",
        #     "first_name": "Luis",
        #     "last_name": "Pérez",
        #     "phone": "555-3456",
        #     "cellphone_number": "5567890123",
        #     "cellphone_country_code": "+52", 
        #     "user_type": "admin",
        #     "is_active": True
        # }
    ]
    
    if dry_run:
        print(f"🔍 Simulando inserción de {len(users_data)} usuarios...")
        for user in users_data:
            print(f"   - {user['email']}: {user['first_name']} {user['last_name']}")
            print(f"     Tipo: {user['user_type']}, Activo: {user['is_active']}")
        return {"users": len(users_data)}
    
    inserted_count = 0
    
    async with create_api_client(api_gateway_url, access_token) as api_client:
        for user_data in users_data:
            try:
                print(f"   📝 Creando usuario: {user_data['email']}")
                
                # Crear usuario a través del API Gateway
                response = await api_client.post("/users/", user_data)
                
                if response:
                    print(f"   ✅ Usuario '{user_data['email']}' creado exitosamente")
                    print(f"      ID: {response.get('id', 'N/A')}")
                    inserted_count += 1
                else:
                    print(f"   ⚠️  Usuario '{user_data['email']}' no se pudo crear")
                
            except Exception as e:
                print(f"   ❌ Error creando usuario '{user_data['email']}': {e}")
                continue
    
    print(f"✅ Se insertaron {inserted_count} usuarios nuevos")
    return {"users": inserted_count} 