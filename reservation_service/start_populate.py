"""
Script principal para ejecutar todos los módulos de población de datos de reservation_service
"""
import asyncio
import sys
import os
import argparse
from datetime import datetime

# Agregar el directorio raíz al path para poder importar commons
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from populate_data.branch_schedule_data import populate_branch_schedule_data

async def start_populate_branch_schedule_data(dry_run: bool = False):
    print("\n🏢 POBLACIÓN DE HORARIOS DE SUCURSALES (BRANCH SCHEDULE)")
    print("-" * 60)
    try:
        results = await populate_branch_schedule_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de horarios completada")
        else:
            print(f"✅ Horarios de sucursales poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando horarios: {e}")
        raise

def print_summary(results, dry_run: bool = False):
    print("\n" + "=" * 60)
    if dry_run:
        print("🔍 ¡SIMULACIÓN COMPLETADA!")
    else:
        print("🎉 ¡POBLACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("\n📊 RESUMEN FINAL:")
    print("-" * 20)
    total_schedules = results.get('schedules', 0)
    
    print(f"🏢 Horarios de sucursales: {total_schedules}")
    
    print("\n" + "=" * 60)
    if dry_run:
        print("🔍 SIMULACIÓN: No se realizaron cambios en la base de datos")
        print("   Para ejecutar la población real, usa: python start_populate.py")
    else:
        print("✅ POBLACIÓN REAL: Los datos han sido insertados en la base de datos")
    print("=" * 60)

async def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Poblar datos en reservation_service")
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Ejecutar en modo simulación (no insertar datos)"
    )
    
    args = parser.parse_args()
    dry_run = args.dry_run
    
    print("🚀 INICIANDO POBLACIÓN DE DATOS - RESERVATION SERVICE")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Modo: {'Simulación' if dry_run else 'Población real'}")
    print("=" * 60)
    
    try:
        # Ejecutar población de horarios de sucursales
        schedule_results = await start_populate_branch_schedule_data(dry_run)
        
        # Resumen final
        all_results = {
            **schedule_results
        }
        
        print_summary(all_results, dry_run)
        
    except KeyboardInterrupt:
        print("\n⚠️  Población interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante la población: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 