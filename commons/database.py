"""
Módulo común para la conexión a la base de datos
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from typing import Optional
import os

# Base declarativa común para todos los modelos
Base = declarative_base()

class DatabaseManager:
    """Gestor de conexión a la base de datos"""
    
    def __init__(self, database_url: Optional[str] = None, echo: Optional[bool] = None):
        """
        Inicializar el gestor de base de datos
        
        Args:
            database_url: URL de conexión a la BD (opcional, usa la configuración por defecto)
            echo: Habilitar logs de SQL (opcional, usa la configuración por defecto)
        """
        # Si no se proporciona URL, intentar detectar automáticamente según el servicio
        if database_url is None:
            # Detectar el servicio basado en las variables de entorno disponibles
            if os.getenv("USER_DATABASE_URL"):
                database_url = os.getenv("USER_DATABASE_URL")
            elif os.getenv("LOCATION_DATABASE_URL"):
                database_url = os.getenv("LOCATION_DATABASE_URL")
            elif os.getenv("RESERVATION_DATABASE_URL"):
                database_url = os.getenv("RESERVATION_DATABASE_URL")
            else:
                # Fallback a DATABASE_URL genérica
                database_url = os.getenv("DATABASE_URL", "")
        
        self.database_url = database_url
        self.echo = echo if echo is not None else (os.getenv("DATABASE_ECHO", "false").lower() == "true")
        
        # Convertir URL de PostgreSQL a async
        if self.database_url.startswith('postgresql://'):
            self.database_url = self.database_url.replace('postgresql://', 'postgresql+asyncpg://')
        
        # Crear engine con configuración de pool optimizada
        self.engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            # Configuración del pool de conexiones
            pool_size=10,  # Número de conexiones en el pool
            max_overflow=20,  # Conexiones adicionales que se pueden crear
            pool_timeout=30,  # Tiempo de espera para obtener una conexión
            pool_recycle=3600,  # Reciclar conexiones cada hora
            pool_pre_ping=True,  # Verificar conexión antes de usar
        )
        
        # Crear session factory
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def create_tables(self, base: Optional[declarative_base] = None) -> None:
        """
        Crear todas las tablas de forma asíncrona
        
        Args:
            base: Base declarativa con los modelos (opcional, usa Base por defecto)
        """
        base_to_use = base or Base
        async with self.engine.begin() as conn:
            await conn.run_sync(base_to_use.metadata.create_all)
    
    async def drop_tables(self, base: Optional[declarative_base] = None) -> None:
        """
        Eliminar todas las tablas de forma asíncrona
        
        Args:
            base: Base declarativa con los modelos (opcional, usa Base por defecto)
        """
        base_to_use = base or Base
        async with self.engine.begin() as conn:
            await conn.run_sync(base_to_use.metadata.drop_all)
    
    async def test_connection(self) -> bool:
        """
        Probar conexión a la BD de forma asíncrona
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                row = result.fetchone()
                return bool(row)
        except Exception as e:
            print(f"❌ Error conexión BD: {e}")
            return False
    
    async def get_session(self) -> AsyncSession:
        """
        Obtener una sesión de base de datos
        
        Returns:
            AsyncSession: Sesión de base de datos
        """
        return self.AsyncSessionLocal()
    
    async def close(self) -> None:
        """Cerrar la conexión a la base de datos"""
        await self.engine.dispose()

# Instancia global del gestor de base de datos (se inicializará cuando se necesite)
db_manager = None

def get_db_manager(database_url: Optional[str] = None) -> DatabaseManager:
    """Obtener una instancia del gestor de base de datos"""
    global db_manager
    
    if db_manager is None:
        db_manager = DatabaseManager(database_url)
    return db_manager

# Funciones de conveniencia para compatibilidad con el código existente
async def create_tables(base: Optional[declarative_base] = None, database_url: Optional[str] = None) -> None:
    """Crear todas las tablas de forma asíncrona"""
    manager = get_db_manager(database_url)
    await manager.create_tables(base)

async def get_db_session(database_url: Optional[str] = None) -> AsyncSession:
    """Dependency para FastAPI (async)"""
    manager = get_db_manager(database_url)
    async with manager.AsyncSessionLocal() as session:
        yield session

async def test_connection(database_url: Optional[str] = None) -> bool:
    """Probar conexión a la BD de forma asíncrona"""
    manager = get_db_manager(database_url)
    return await manager.test_connection()

# Exportar componentes principales
__all__ = [
    'Base',
    'DatabaseManager',
    'db_manager',
    'get_db_manager',
    'create_tables',
    'get_db_session',
    'test_connection'
] 