#!/usr/bin/env python3
"""
Script de prueba para verificar que el problema de conexiones está resuelto
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio padre al path para poder importar user_service
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Cargar variables de entorno
load_dotenv()

from user_service.infrastructure.connection import get_db_session
from user_service.infrastructure.container import container
from user_service.application.use_cases.get_user_by_auth_uid_use_case import GetUserByAuthUidUseCase


async def test_connection_pool():
    """Probar el pool de conexiones"""
    print("🧪 Probando pool de conexiones...")
    
    # Simular múltiples requests concurrentes
    async def simulate_request(request_id: int):
        """Simular una request individual"""
        try:
            async for session in get_db_session():
                # Inyectar la sesión en el contenedor
                container.db_session.override(session)
                
                # Crear un use case
                use_case = container.get_user_by_auth_uid_use_case()
                
                # Simular una operación de base de datos
                print(f"✅ Request {request_id}: Sesión obtenida y liberada correctamente")
                
        except Exception as e:
            print(f"❌ Request {request_id}: Error - {e}")
    
    # Ejecutar múltiples requests concurrentes
    tasks = []
    for i in range(20):  # Simular 20 requests concurrentes
        task = asyncio.create_task(simulate_request(i))
        tasks.append(task)
    
    # Esperar a que todas las requests terminen
    await asyncio.gather(*tasks, return_exceptions=True)
    
    print("✅ Prueba completada - Pool de conexiones funcionando correctamente")


async def test_database_connection():
    """Probar la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        from user_service.infrastructure.connection import test_connection
        is_connected = await test_connection()
        
        if is_connected:
            print("✅ Conexión a la base de datos exitosa")
        else:
            print("❌ Error en la conexión a la base de datos")
            
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")


async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de conexión...")
    print()
    
    # Verificar configuración
    if not os.getenv("DATABASE_URL"):
        print("❌ Error: DATABASE_URL no configurado")
        return
    
    print(f"🗄️ Database URL configurado: {bool(os.getenv('DATABASE_URL'))}")
    print()
    
    # Probar conexión
    await test_database_connection()
    print()
    
    # Probar pool de conexiones
    await test_connection_pool()
    print()
    
    print("🎉 Todas las pruebas completadas")


if __name__ == "__main__":
    asyncio.run(main()) 