"""
Script para poblar perfiles (profile) en user_service usando use cases
"""
import asyncio
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from commons.database import db_manager
from user_service.infrastructure.container import container
from user_service.domain.dto.requests.profile_requests import CreateProfileRequest
from user_service.domain.exceptions.user_exceptions import ProfileAlreadyExistsException

async def populate_profile_data(dry_run: bool = False):
    """
    Poblar datos de perfiles con sus roles asociados usando use cases
    """
    print("👤 Poblando datos de perfiles...")
    
    # Datos de perfiles a insertar
    profiles_data = [
        {
            "name": "RECEPCIONISTA",
            "description": "Recepcionista",
            "roles": ["RECEPCIONISTA"]
        },
        {
            "name": "RECEPCIONISTA_FRIO",
            "description": "Recepcionista de rampa frio",
            "roles": ["RECEPCIONISTA_RAMPA_FRIO"]
        },
        {
            "name": "AGENDAMIENTO",
            "description": "Realiza agendamientos",
            "roles": ["AGENDAMIENTO"]
        },
        {
            "name": "SUPER_ADMIN",
            "description": "Administrador con todos los permisos",
            "roles": ["RECEPCIONISTA", "RECEPCIONISTA_RAMPA_FRIO", "AGENDAMIENTO"]
        }
    ]
    
    if dry_run:
        print(f"🔍 Simulando inserción de {len(profiles_data)} perfiles...")
        for profile in profiles_data:
            print(f"   - {profile['name']}: {profile['description']}")
            print(f"     Roles: {', '.join(profile['roles'])}")
        return {"profiles": len(profiles_data)}
    
    inserted_count = 0
    
    # Usar el contexto de sesión de base de datos
    async with db_manager.AsyncSessionLocal() as session:
        # Configurar el container para usar esta sesión
        container.db_session.override(session)
        
        try:
            # Obtener los use cases del container
            create_profile_use_case = container.create_profile_use_case()
            list_roles_use_case = container.list_roles_use_case()
            
            # Obtener todos los roles disponibles
            all_roles = await list_roles_use_case.execute()
            roles_by_name = {role.name: role for role in all_roles}
            
            for profile_data in profiles_data:
                try:
                    # Crear request DTO para crear perfil
                    create_request = CreateProfileRequest(
                        name=profile_data["name"],
                        description=profile_data["description"],
                        role_ids=[]  # Sin roles inicialmente
                    )
                    
                    # Crear perfil
                    created_profile = await create_profile_use_case.execute(create_request)
                    print(f"   ✅ Perfil '{created_profile.name}' creado exitosamente")
                    
                    # Obtener los roles asociados
                    profile_roles = []
                    for role_name in profile_data["roles"]:
                        if role_name in roles_by_name:
                            profile_roles.append(roles_by_name[role_name])
                        else:
                            print(f"   ⚠️  Rol '{role_name}' no encontrado para perfil '{profile_data['name']}'")
                    
                    # Asignar roles al perfil usando el repositorio directamente
                    if profile_roles:
                        from user_service.data.repositories.profile_repository_impl import ProfileRepositoryImpl
                        from user_service.data.repositories.role_repository_impl import RoleRepositoryImpl
                        
                        profile_repo = ProfileRepositoryImpl(session)
                        role_ids = [role.id for role in profile_roles]
                        updated_profile = await profile_repo.assign_roles(created_profile.id, role_ids)
                        print(f"      Roles asignados: {', '.join([r.name for r in profile_roles])}")
                    
                    inserted_count += 1
                    
                except ProfileAlreadyExistsException:
                    print(f"   ⚠️  Perfil '{profile_data['name']}' ya existe, saltando...")
                    continue
                except Exception as e:
                    print(f"   ❌ Error creando perfil '{profile_data['name']}': {e}")
                    continue
        finally:
            # Restaurar el provider original
            container.db_session.reset_override()
    
    print(f"✅ Se insertaron {inserted_count} perfiles nuevos")
    return {"profiles": inserted_count} 