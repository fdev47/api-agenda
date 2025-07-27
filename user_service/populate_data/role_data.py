"""
Script para poblar roles en user_service usando use cases
"""
import asyncio
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from commons.database import db_manager
from user_service.infrastructure.container import container
from user_service.domain.dto.requests.role_requests import CreateRoleRequest
from user_service.domain.exceptions.user_exceptions import RoleAlreadyExistsException

async def populate_role_data(dry_run: bool = False):
    """
    Poblar datos de roles usando create_role_use_case
    """
    print("🔑 Poblando datos de roles...")
    
    # Datos de roles a insertar
    roles_data = [
        {
            "name": "RECEPCIONISTA",
            "description": "Recepcionista"
        },
        {
            "name": "RECEPCIONISTA_RAMPA_FRIO", 
            "description": "Recepcionista de rampa frio"
        },
        {
            "name": "AGENDAMIENTO",
            "description": "Realiza agendamientos"
        }
    ]
    
    if dry_run:
        print(f"🔍 Simulando inserción de {len(roles_data)} roles...")
        for role in roles_data:
            print(f"   - {role['name']}: {role['description']}")
        return {"roles": len(roles_data)}
    
    inserted_count = 0
    
    # Usar el contexto de sesión de base de datos
    async with db_manager.AsyncSessionLocal() as session:
        # Configurar el container para usar esta sesión
        container.db_session.override(session)
        
        try:
            # Obtener el use case del container
            create_role_use_case = container.create_role_use_case()
            
            for role_data in roles_data:
                try:
                    # Crear request DTO
                    create_request = CreateRoleRequest(
                        name=role_data["name"],
                        description=role_data["description"]
                    )
                    
                    # Ejecutar use case
                    created_role = await create_role_use_case.execute(create_request)
                    print(f"   ✅ Rol '{created_role.name}' creado exitosamente")
                    inserted_count += 1
                    
                except RoleAlreadyExistsException:
                    print(f"   ⚠️  Rol '{role_data['name']}' ya existe, saltando...")
                    continue
                except Exception as e:
                    print(f"   ❌ Error creando rol '{role_data['name']}': {e}")
                    continue
        finally:
            # Restaurar el provider original
            container.db_session.reset_override()
    
    print(f"✅ Se insertaron {inserted_count} roles nuevos")
    return {"roles": inserted_count} 