#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos
"""
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

async def test_database_connection():
    """Probar conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        # Importar módulo común
        from commons.database import test_connection, create_tables
        
        # Probar conexión
        is_connected = await test_connection()
        
        if is_connected:
            print("✅ Conexión exitosa a la base de datos!")
            
            # Intentar crear tablas (solo para probar)
            print("🔧 Probando creación de tablas...")
            await create_tables()
            print("✅ Tablas creadas/verificadas correctamente")
            
            return True
        else:
            print("❌ No se pudo conectar a la base de datos")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

async def test_user_service_connection():
    """Probar conexión específica del user_service"""
    print("\n🔍 Probando conexión del user_service...")
    
    try:
        from user_service.infrastructure.connection import test_connection, initialize_user_service_database
        
        # Probar conexión
        is_connected = await test_connection()
        
        if is_connected:
            print("✅ Conexión del user_service exitosa!")
            
            # Inicializar base de datos del servicio
            success = await initialize_user_service_database()
            if success:
                print("✅ Base de datos del user_service inicializada")
            else:
                print("⚠️ Error inicializando BD del user_service")
            
            return True
        else:
            print("❌ No se pudo conectar desde user_service")
            return False
            
    except Exception as e:
        print(f"❌ Error en user_service: {e}")
        return False

async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de conexión...")
    print(f"📄 Archivo .env encontrado: {os.path.exists('.env')}")
    print(f"🔧 DATABASE_URL: {os.getenv('DATABASE_URL', 'No configurado')}")
    print("-" * 50)
    
    # Probar conexión general
    general_success = await test_database_connection()
    
    # Probar conexión específica del user_service
    service_success = await test_user_service_connection()
    
    print("-" * 50)
    if general_success and service_success:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    asyncio.run(main()) 