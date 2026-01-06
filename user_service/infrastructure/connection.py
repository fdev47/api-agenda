"""
Conexión a la base de datos para el microservicio de usuarios
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from commons.database import get_db_manager, Base

# Obtener el gestor de base de datos
db_manager = get_db_manager()

engine = db_manager.engine
AsyncSessionLocal = db_manager.AsyncSessionLocal

async def create_tables():
    """Crear todas las tablas de forma asíncrona"""
    await db_manager.create_tables(Base)

async def get_db_session() -> AsyncSession:
    """Dependency para FastAPI (async)"""
    async with db_manager.AsyncSessionLocal() as session:
        yield session

async def test_connection() -> bool:
    """Probar conexión a la BD de forma asíncrona"""
    return await db_manager.test_connection()

# Funciones adicionales específicas del servicio de usuarios
async def initialize_user_service_database():
    """Inicializar base de datos específicamente para el servicio de usuarios"""
    try:
        # Importar modelos específicos del servicio de usuarios
        from .models import user, profile, role
        
        # Crear tablas
        await create_tables()
        print("✅ Base de datos del servicio de usuarios inicializada")
        return True
    except Exception as e:
        print(f"❌ Error inicializando BD del servicio de usuarios: {e}")
        return False

async def health_check() -> dict:
    """Verificación de salud de la base de datos"""
    try:
        is_connected = await test_connection()
        return {
            "database": "healthy" if is_connected else "unhealthy",
            "service": "user-service",
            "status": "ok" if is_connected else "error"
        }
    except Exception as e:
        return {
            "database": "unhealthy",
            "service": "user-service", 
            "status": "error",
            "error": str(e)
        } 