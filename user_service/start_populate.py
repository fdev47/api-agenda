"""
Script principal para ejecutar todos los módulos de población de datos de user_service
"""
import asyncio
import sys
import os
import argparse
from datetime import datetime

# Agregar el directorio raíz al path para poder importar commons
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from populate_data.address_data import populate_address_data
from populate_data.role_data import populate_role_data
from populate_data.profile_data import populate_profile_data
from populate_data.user_data import populate_user_data
from populate_data.customer_data import populate_customer_data

async def start_populate_address_data(dry_run: bool = False):
    print("\n📍 POBLACIÓN DE DIRECCIONES (ADDRESS)")
    print("-" * 40)
    try:
        results = await populate_address_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de direcciones completada")
        else:
            print(f"✅ Direcciones pobladas exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando direcciones: {e}")
        raise

async def start_populate_role_data(dry_run: bool = False):
    print("\n🔑 POBLACIÓN DE ROLES")
    print("-" * 40)
    try:
        results = await populate_role_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de roles completada")
        else:
            print(f"✅ Roles poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando roles: {e}")
        raise

async def start_populate_profile_data(dry_run: bool = False):
    print("\n👤 POBLACIÓN DE PERFILES (PROFILE)")
    print("-" * 40)
    try:
        results = await populate_profile_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de perfiles completada")
        else:
            print(f"✅ Perfiles poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando perfiles: {e}")
        raise

async def start_populate_user_data(dry_run: bool = False):
    print("\n🙍 POBLACIÓN DE USUARIOS (USER)")
    print("-" * 40)
    try:
        results = await populate_user_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de usuarios completada")
        else:
            print(f"✅ Usuarios poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando usuarios: {e}")
        raise

async def start_populate_customer_data(dry_run: bool = False):
    print("\n🧑‍💼 POBLACIÓN DE CLIENTES (CUSTOMER)")
    print("-" * 40)
    try:
        results = await populate_customer_data(dry_run)
        if dry_run:
            print(f"✅ Simulación de clientes completada")
        else:
            print(f"✅ Clientes poblados exitosamente")
        return results
    except Exception as e:
        print(f"❌ Error poblando clientes: {e}")
        raise

def print_summary(results, dry_run: bool = False):
    print("\n" + "=" * 50)
    if dry_run:
        print("🔍 ¡SIMULACIÓN COMPLETADA!")
    else:
        print("🎉 ¡POBLACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("\n📊 RESUMEN FINAL:")
    print("-" * 20)
    total_addresses = 0
    total_roles = 0
    total_profiles = 0
    total_users = 0
    total_customers = 0
    if "addresses" in results:
        addresses = results["addresses"]
        total_addresses += addresses.get("addresses", 0)
        print(f"📍 Direcciones: {addresses['addresses']}")
    if "roles" in results:
        roles = results["roles"]
        total_roles += roles.get("roles", 0)
        print(f"🔑 Roles: {roles['roles']}")
    if "profiles" in results:
        profiles = results["profiles"]
        total_profiles += profiles.get("profiles", 0)
        print(f"👤 Perfiles: {profiles['profiles']}")
    if "users" in results:
        users = results["users"]
        total_users += users.get("users", 0)
        print(f"🙍 Usuarios: {users['users']}")
    if "customers" in results:
        customers = results["customers"]
        total_customers += customers.get("customers", 0)
        print(f"🧑‍💼 Clientes: {customers['customers']}")
    print(f"\n📈 TOTALES:")
    print(f"   📍 Direcciones: {total_addresses}")
    print(f"   🔑 Roles: {total_roles}")
    print(f"   👤 Perfiles: {total_profiles}")
    print(f"   🙍 Usuarios: {total_users}")
    print(f"   🧑‍💼 Clientes: {total_customers}")

async def main():
    parser = argparse.ArgumentParser(description="Script de población de datos de user_service")
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
        # address_results = await start_populate_address_data(dry_run)
        # results["addresses"] = address_results

        role_results = await start_populate_role_data(dry_run)
        results["roles"] = role_results

        profile_results = await start_populate_profile_data(dry_run)
        results["profiles"] = profile_results

        # user_results = await start_populate_user_data(dry_run)
        # results["users"] = user_results

        # customer_results = await start_populate_customer_data(dry_run)
        # results["customers"] = customer_results

        print_summary(results, dry_run)
    except Exception as e:
        print(f"\n❌ Error durante la población: {e}")
        print("🔍 Verifica los logs para más detalles")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 