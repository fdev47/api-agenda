"""
Módulo común para la conexión a la base de datos
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import ssl
from urllib.parse import quote_plus
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
        
        # Determinar si usar SSL basado en la URL y configuración
        use_ssl = self._should_use_ssl(database_url)
        connect_args = {}
        
        if use_ssl:
            ssl_context = self._create_ssl_context()
            if ssl_context:
                connect_args["ssl"] = ssl_context
        
        # Convertir URL de PostgreSQL a async
        if self.database_url.startswith('postgresql://'):
            self.database_url = self.database_url.replace('postgresql://', 'postgresql+asyncpg://')
        
        # Obtener configuración del pool
        pool_config = self.get_pool_config()
        
        self.engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            # Configuración del pool
            pool_size=pool_config["pool_size"],
            max_overflow=pool_config["max_overflow"],
            pool_timeout=pool_config["pool_timeout"],
            pool_recycle=pool_config["pool_recycle"],
            pool_pre_ping=pool_config["pool_pre_ping"],
            # SSL solo si es necesario
            connect_args=connect_args,
        )

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

    def get_pool_config(self) -> dict:
        """
        Obtener la configuración actual del pool de conexiones
        
        Returns:
            dict: Configuración del pool
        """
        return {
            "pool_size": int(os.getenv("DATABASE_POOL_SIZE", "5")),
            "max_overflow": int(os.getenv("DATABASE_MAX_OVERFLOW", "10")),
            "pool_timeout": int(os.getenv("DATABASE_POOL_TIMEOUT", "10")),
            "pool_recycle": int(os.getenv("DATABASE_POOL_RECYCLE", "1800")),
            "pool_pre_ping": os.getenv("DATABASE_POOL_PRE_PING", "true").lower() == "true"
        }

    def _should_use_ssl(self, database_url: str) -> bool:
        """
        Determina si se debe usar SSL basado en la URL de la base de datos.
        Por defecto, no se usa SSL en desarrollo local.
        """
        # Primero verificar si está explícitamente configurado
        use_ssl_env = os.getenv("DATABASE_USE_SSL", "").lower()
        if use_ssl_env == "true":
            return True
        elif use_ssl_env == "false":
            return False

    def _create_ssl_context(self) -> Optional[ssl.SSLContext]:
        """
        Crea un contexto SSL para la conexión a la base de datos.
        Solo se usa si se determina que se debe usar SSL.
        """
        ca_file_path = os.getenv("DATABASE_CA_FILE_PATH")
        if not ca_file_path:
            print("⚠️ DATABASE_CA_FILE_PATH no configurado. SSL no se puede habilitar.")
            return None

        try:
            ssl_context = ssl.create_default_context(cafile=ca_file_path)
            return ssl_context
        except FileNotFoundError:
            print(f"❌ Error: El archivo de certificado SSL no encontrado en {ca_file_path}")
            return None
        except Exception as e:
            print(f"❌ Error al crear contexto SSL: {e}")
            return None

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
    'test_connection',
    'get_pool_config'
]
