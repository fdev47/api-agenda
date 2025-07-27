"""
Script para poblar perfiles (profile) en user_service
"""
from commons.database import db_manager
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_profile_data(dry_run: bool = False):
    """
    Poblar datos de perfiles con sus roles asociados
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
    
    # Importar dependencias necesarias
    from domain.entities.profile import Profile
    from data.repositories.profile_repository_impl import ProfileRepositoryImpl
    from data.repositories.role_repository_impl import RoleRepositoryImpl
    from infrastructure.models.profile import ProfileDB
    
    inserted_count = 0
    
    async with db_manager.get_session() as session:
        profile_repo = ProfileRepositoryImpl(session)
        role_repo = RoleRepositoryImpl(session)
        
        for profile_data in profiles_data:
            try:
                # Verificar si el perfil ya existe
                existing_profile = await profile_repo.get_by_name(profile_data["name"])
                
                if existing_profile:
                    print(f"   ⚠️  Perfil '{profile_data['name']}' ya existe, saltando...")
                    continue
                
                # Obtener los roles asociados
                profile_roles = []
                for role_name in profile_data["roles"]:
                    role = await role_repo.get_by_name(role_name)
                    if role:
                        profile_roles.append(role)
                    else:
                        print(f"   ⚠️  Rol '{role_name}' no encontrado para perfil '{profile_data['name']}'")
                
                # Crear nueva entidad Profile
                new_profile = Profile(
                    name=profile_data["name"],
                    description=profile_data["description"],
                    roles=profile_roles
                )
                
                # Crear el perfil en la BD
                profile_db = ProfileDB(
                    name=new_profile.name,
                    description=new_profile.description
                )
                
                # Asignar roles al perfil
                for role in profile_roles:
                    # Obtener el RoleDB correspondiente
                    role_db = await role_repo.get_by_name(role.name)
                    if role_db:
                        profile_db.roles.append(role_db)
                
                session.add(profile_db)
                await session.commit()
                await session.refresh(profile_db)
                
                print(f"   ✅ Perfil '{profile_data['name']}' creado exitosamente")
                print(f"      Roles asignados: {', '.join([r.name for r in profile_roles])}")
                inserted_count += 1
                
            except Exception as e:
                print(f"   ❌ Error creando perfil '{profile_data['name']}': {e}")
                continue
    
    print(f"✅ Se insertaron {inserted_count} perfiles nuevos")
    return {"profiles": inserted_count} 