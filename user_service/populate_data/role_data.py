"""
Script para poblar roles en user_service
"""
from commons.database import db_manager
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_role_data(dry_run: bool = False):
    """
    Poblar datos de roles
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
    
    # Importar dependencias necesarias
    from domain.entities.role import Role
    from data.repositories.role_repository_impl import RoleRepositoryImpl
    
    inserted_count = 0
    
    async with db_manager.get_session() as session:
        role_repo = RoleRepositoryImpl(session)
        
        for role_data in roles_data:
            try:
                # Verificar si el rol ya existe
                existing_role = await role_repo.get_by_name(role_data["name"])
                
                if existing_role:
                    print(f"   ⚠️  Rol '{role_data['name']}' ya existe, saltando...")
                    continue
                
                # Crear nueva entidad Role
                new_role = Role(
                    name=role_data["name"],
                    description=role_data["description"]
                )
                
                # Insertar en la base de datos
                created_role = await role_repo.create(new_role)
                print(f"   ✅ Rol '{created_role.name}' creado exitosamente")
                inserted_count += 1
                
            except Exception as e:
                print(f"   ❌ Error creando rol '{role_data['name']}': {e}")
                continue
    
    print(f"✅ Se insertaron {inserted_count} roles nuevos")
    return {"roles": inserted_count} 