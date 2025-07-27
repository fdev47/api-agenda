"""
Script principal para ejecutar todos los módulos de población de datos
"""
import asyncio
import sys
import os
import argparse
from datetime import datetime

# Agregar el directorio raíz al path para poder importar commons
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from location_service.populate_data.location_data import populate_location_data
from location_service.populate_data.local_data import populate_local_data
from location_service.populate_data.sector_data import populate_sector_data
from location_service.populate_data.branch_data import populate_branch_data
from location_service.populate_data.ramp_data import populate_ramp_data


async def start_populate_location_data(dry_run: bool = False):
    """Poblar datos de ubicación (países, estados, ciudades)"""
    print("\n📍 POBLACIÓN DE DATOS DE UBICACIÓN")
    print("-" * 40)
    
    try:
        results = await populate_location_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de datos de ubicación completada")
        else:
            print(f"✅ Datos de ubicación poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando datos de ubicación: {e}")
        raise


async def start_populate_local_data(dry_run: bool = False):
    """Poblar datos de locales"""
    print("\n🏢 POBLACIÓN DE DATOS DE LOCALES")
    print("-" * 40)
    try:
        results = await populate_local_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de datos de locales completada")
        else:
            print(f"✅ Datos de locales poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando datos de locales: {e}")
        raise


async def start_populate_branch_data(dry_run: bool = False):
    """Poblar datos de sucursales y rampas"""
    print("\n🏢 POBLACIÓN DE DATOS DE SUCURSALES Y RAMPAS")
    print("-" * 40)
    try:
        results = await populate_branch_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de datos de sucursales y rampas completada")
        else:
            print(f"✅ Datos de sucursales y rampas poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando datos de sucursales y rampas: {e}")
        raise


async def start_populate_sector_data(dry_run: bool = False):
    """Poblar datos de sectores"""
    print("\n🏭 POBLACIÓN DE DATOS DE SECTORES")
    print("-" * 40)
    
    try:
        results = await populate_sector_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de datos de sectores completada")
        else:
            print(f"✅ Datos de sectores poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando datos de sectores: {e}")
        raise

async def start_populate_ramp_data(dry_run: bool = False):
    """Poblar rampas para cada sucursal"""
    print("\n🚚 POBLACIÓN DE RAMPAS")
    print("-" * 40)
    try:
        results = await populate_ramp_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de rampas completada")
        else:
            print(f"✅ Rampas pobladas exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando rampas: {e}")
        raise


def print_summary(results, dry_run: bool = False):
    """Imprimir resumen final de la población"""
    print("\n" + "=" * 50)
    if dry_run:
        print("🔍 ¡SIMULACIÓN COMPLETADA!")
    else:
        print("🎉 ¡POBLACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    
    # Mostrar resumen final
    print("\n📊 RESUMEN FINAL:")
    print("-" * 20)
    
    total_countries = 0
    total_states = 0
    total_cities = 0
    total_branches = 0
    total_sectors = 0
    total_measurement_units = 0
    total_sector_types = 0
    total_ramps = 0
    
    if "location" in results:
        location = results["location"]
        total_countries += location.get("countries", 0)
        total_states += location.get("states", 0)
        total_cities += location.get("cities", 0)
        print(f"📍 Ubicación: {location['countries']} países, {location['states']} estados, {location['cities']} ciudades")
    
    if "locals" in results:
        locals = results["locals"]
        total_branches += locals.get("locals", 0)
        print(f"🏢 Locales: {locals['locals']} locales")
    
    if "branches" in results:
        branches = results["branches"]
        if isinstance(branches, dict):
            total_branches += branches.get("branches", 0)
            print(f"🏢 Sucursales: {branches['branches']} sucursales")
        else:
            total_branches += branches
            print(f"🏢 Sucursales: {branches} sucursales")
    
    if "ramps" in results:
        ramps = results["ramps"]
        if isinstance(ramps, dict):
            total_ramps += ramps.get("ramps", 0)
            print(f"🚚 Rampas: {ramps['ramps']} rampas")
        else:
            total_ramps += ramps
            print(f"🚚 Rampas: {ramps} rampas")
    
    if "sectors" in results:
        sectors = results["sectors"]
        total_measurement_units += sectors.get("measurement_units", 0)
        total_sector_types += sectors.get("sector_types", 0)
        total_sectors += sectors.get("sectors", 0)
        print(f"🏭 Sectores: {sectors['measurement_units']} unidades, {sectors['sector_types']} tipos, {sectors['sectors']} sectores")
    
    print(f"\n📈 TOTALES:")
    print(f"   🌍 Países: {total_countries}")
    print(f"   🏛️ Estados: {total_states}")
    print(f"   🏙️ Ciudades: {total_cities}")
    print(f"   🏢 Sucursales: {total_branches}")
    print(f"   🚚 Rampas: {total_ramps}")
    print(f"   📏 Unidades de medida: {total_measurement_units}")
    print(f"   🏭 Tipos de sector: {total_sector_types}")
    print(f"   🛣️ Rampas: {total_ramps}")
    print(f"   🏭 Sectores: {total_sectors}")


async def main():
    """Función principal para ejecutar todos los scripts de población"""
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Script de población de datos")
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Ejecutar en modo simulación (no guardar en BD)"
    )
    args = parser.parse_args()
    
    dry_run = args.dry_run
    
    print("🚀 Iniciando población de datos...")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if dry_run:
        print("🔍 MODO SIMULACIÓN ACTIVADO")
    print("=" * 50)
    
    results = {}
    
    try:
        # Poblar datos de ubicación (países, estados, ciudades)
        location_results = await start_populate_location_data(dry_run)
        results["location"] = location_results

        # Poblar datos de locales
        local_results = await start_populate_local_data(dry_run)
        results["locals"] = local_results

        # Poblar datos de sucursales
        branch_results = await start_populate_branch_data(dry_run)
        results["branches"] = branch_results

        # Poblar rampas
        ramp_results = await start_populate_ramp_data(dry_run)
        results["ramps"] = ramp_results

        # Poblar datos de sectores
        sector_results = await start_populate_sector_data(dry_run)
        results["sectors"] = sector_results

        # Imprimir resumen final
        print_summary(results, dry_run)
        
    except Exception as e:
        print(f"\n❌ Error durante la población: {e}")
        print("🔍 Verifica los logs para más detalles")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 