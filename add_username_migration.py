#!/usr/bin/env python3
"""
Script simple para agregar columna username a la tabla users
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from commons.config import config

async def add_username_column():
    """Agregar columna username a la tabla users"""
    
    print("🔧 Agregando columna username a la tabla users...")
    
    # Crear engine de conexión
    engine = create_async_engine(config.DATABASE_URL)
    
    try:
        async with engine.begin() as conn:
            # Verificar si la columna username ya existe
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'username'
            """)
            
            result = await conn.execute(check_query)
            has_username = result.fetchone() is not None
            
            if not has_username:
                print("📝 Agregando columna username...")
                add_username = text("""
                    ALTER TABLE users 
                    ADD COLUMN username VARCHAR(50) UNIQUE
                """)
                await conn.execute(add_username)
                print("   ✅ Columna username agregada")
            else:
                print("   ℹ️  Columna username ya existe")
                
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise
    finally:
        await engine.dispose()
    
    print("🎉 Migración completada!")

if __name__ == "__main__":
    asyncio.run(add_username_column()) 