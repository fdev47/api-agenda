#!/usr/bin/env python3
"""
Script para verificar y recrear las tablas del User Service
"""
import asyncio
import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commons.database import db_manager
from sqlalchemy import text

async def check_tables():
    """Verificar la estructura de las tablas"""
    print("🔍 Verificando estructura de tablas...")
    
    try:
        async with db_manager.AsyncSessionLocal() as session:
            # Verificar si la tabla users existe
            result = await session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            
            if not columns:
                print("❌ La tabla 'users' no existe")
                return False
            
            print("📋 Columnas encontradas en la tabla 'users':")
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
            
            # Verificar si existe la columna auth_uid
            auth_uid_exists = any(col[0] == 'auth_uid' for col in columns)
            
            if not auth_uid_exists:
                print("❌ La columna 'auth_uid' no existe")
                return False
            
            print("✅ Estructura de tabla correcta")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

async def recreate_tables():
    """Recrear las tablas"""
    print("🔄 Recreando tablas...")
    
    try:
        # Importar modelos para asegurar que se registren
        from user_service.infrastructure.models import user, profile, role
        
        # Eliminar tablas existentes
        async with db_manager.engine.begin() as conn:
            await conn.execute(text("DROP TABLE IF EXISTS user_profiles CASCADE"))
            await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            await conn.execute(text("DROP TABLE IF EXISTS profiles CASCADE"))
            await conn.execute(text("DROP TABLE IF EXISTS roles CASCADE"))
            print("✅ Tablas eliminadas")
        
        # Crear tablas nuevamente
        from user_service.infrastructure.connection import initialize_user_service_database
        success = await initialize_user_service_database()
        
        if success:
            print("✅ Tablas recreadas correctamente")
            return True
        else:
            print("❌ Error recreando tablas")
            return False
            
    except Exception as e:
        print(f"❌ Error recreando tablas: {e}")
        return False

async def main():
    """Función principal"""
    print("🔧 Verificando y reparando tablas del User Service...")
    
    # Verificar estructura actual
    tables_ok = await check_tables()
    
    if not tables_ok:
        print("\n🔄 Recreando tablas...")
        success = await recreate_tables()
        
        if success:
            # Verificar nuevamente
            tables_ok = await check_tables()
            if tables_ok:
                print("✅ Tablas reparadas correctamente")
            else:
                print("❌ Error después de recrear tablas")
                sys.exit(1)
        else:
            print("❌ No se pudieron recrear las tablas")
            sys.exit(1)
    else:
        print("✅ Las tablas están correctas")

if __name__ == "__main__":
    asyncio.run(main()) 