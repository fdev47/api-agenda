#!/usr/bin/env python3
"""
Script para limpiar y recrear la base de datos
"""
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

async def clean_and_recreate_database():
    """Limpiar y recrear la base de datos"""
    print("🧹 Limpiando base de datos...")
    
    try:
        from commons.database import db_manager, Base
        
        # Eliminar todas las tablas existentes
        await db_manager.drop_tables(Base)
        print("✅ Tablas eliminadas")
        
        # Crear tablas nuevamente
        await db_manager.create_tables(Base)
        print("✅ Tablas recreadas")
        
        # Probar conexión
        is_connected = await db_manager.test_connection()
        if is_connected:
            print("✅ Conexión verificada después de limpieza")
            return True
        else:
            print("❌ Error en conexión después de limpieza")
            return False
            
    except Exception as e:
        print(f"❌ Error durante limpieza: {e}")
        return False

async def clean_user_service_database():
    """Limpiar específicamente las tablas del user_service"""
    print("\n🧹 Limpiando tablas del user_service...")
    
    try:
        from user_service.infrastructure.connection import db_manager, Base
        
        # Eliminar tablas del user_service
        await db_manager.drop_tables(Base)
        print("✅ Tablas del user_service eliminadas")
        
        # Recrear tablas
        await db_manager.create_tables(Base)
        print("✅ Tablas del user_service recreadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error limpiando user_service: {e}")
        return False

async def main():
    """Función principal"""
    print("🚀 Iniciando limpieza de base de datos...")
    print(f"📄 Archivo .env encontrado: {os.path.exists('.env')}")
    print(f"🔧 DATABASE_URL: {os.getenv('DATABASE_URL', 'No configurado')}")
    print("-" * 50)
    
    # Limpiar base de datos general
    general_success = await clean_and_recreate_database()
    
    # Limpiar específicamente user_service
    service_success = await clean_user_service_database()
    
    print("-" * 50)
    if general_success and service_success:
        print("🎉 ¡Limpieza completada exitosamente!")
        print("💡 Ahora puedes ejecutar test_connection.py nuevamente")
    else:
        print("⚠️ Algunos problemas durante la limpieza.")

if __name__ == "__main__":
    asyncio.run(main()) 