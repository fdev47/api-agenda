"""
Módulo común para la conexión a la base de datos
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from typing import Optional
from .config import db_settings

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
        self.database_url = database_url or db_settings.DATABASE_URL
        self.echo = echo if echo is not None else db_settings.DATABASE_ECHO
        
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

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

# Funciones de conveniencia para compatibilidad con el código existente
async def create_tables(base: Optional[declarative_base] = None) -> None:
    """Crear todas las tablas de forma asíncrona"""
    await db_manager.create_tables(base)

async def get_db_session() -> AsyncSession:
    """Dependency para FastAPI (async)"""
    async with db_manager.AsyncSessionLocal() as session:
        yield session

async def test_connection() -> bool:
    """Probar conexión a la BD de forma asíncrona"""
    return await db_manager.test_connection()

# Exportar componentes principales
__all__ = [
    'Base',
    'DatabaseManager',
    'db_manager',
    'create_tables',
    'get_db_session',
    'test_connection'
] 