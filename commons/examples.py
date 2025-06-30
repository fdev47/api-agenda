"""
Ejemplos de uso del módulo común de base de datos
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base, db_manager, create_tables, get_db_session, test_connection

# Ejemplo de modelo que puede usar cualquier microservicio
class ExampleModel(Base):
    """Modelo de ejemplo para demostrar el uso"""
    __tablename__ = "example_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

async def example_usage():
    """Ejemplo de uso del módulo común"""
    
    # 1. Probar conexión
    is_connected = await test_connection()
    print(f"✅ Conexión exitosa: {is_connected}")
    
    # 2. Crear tablas
    await create_tables()
    print("✅ Tablas creadas")
    
    # 3. Usar sesión de base de datos
    async with db_manager.AsyncSessionLocal() as session:
        # Crear un registro de ejemplo
        example = ExampleModel(
            name="Ejemplo",
            description="Descripción de ejemplo"
        )
        session.add(example)
        await session.commit()
        print("✅ Registro creado")
        
        # Consultar registros
        result = await session.execute(
            "SELECT * FROM example_table"
        )
        rows = result.fetchall()
        print(f"✅ Registros encontrados: {len(rows)}")

# Ejemplo de cómo configurar un microservicio específico
class MicroserviceConfig:
    """Configuración específica para un microservicio"""
    
    def __init__(self, service_name: str, service_port: int = 8000):
        self.service_name = service_name
        self.service_port = service_port
    
    async def initialize_database(self):
        """Inicializar base de datos para este microservicio"""
        # Aquí puedes importar tus modelos específicos
        # from your_models import YourModel1, YourModel2
        
        # Crear tablas específicas de este microservicio
        # await create_tables()  # Esto creará todas las tablas registradas
        
        print(f"✅ Base de datos inicializada para {self.service_name}")

# Ejemplo de uso en un microservicio
async def setup_microservice():
    """Configurar un microservicio usando el módulo común"""
    
    # Configurar el microservicio
    config = MicroserviceConfig("user-service", 8001)
    
    # Inicializar base de datos
    await config.initialize_database()
    
    # Probar conexión
    await test_connection()
    
    print("✅ Microservicio configurado correctamente") 