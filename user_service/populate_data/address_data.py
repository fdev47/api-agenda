"""
Script para poblar direcciones (address) en user_service usando location_service
"""
import os
import sys
import asyncio
from commons.api_client import APIClient
from commons.config import config

async def get_location_data(api_client: APIClient):
    """
    Obtener datos de location desde el API Gateway
    """
    try:
        # Obtener países
        countries_response = await api_client.get(f"{config.API_PREFIX}/location/countries/")
        countries = countries_response.get('countries', []) if countries_response else []
        
        # Obtener estados (asumiendo Paraguay como país por defecto)
        paraguay_id = None
        if countries:
            paraguay = next((c for c in countries if c['name'] == 'Paraguay'), None)
            paraguay_id = paraguay['id'] if paraguay else None
        
        states_response = await api_client.get(
            f"{config.API_PREFIX}/location/states/",
            params={"country_id": paraguay_id} if paraguay_id else {}
        )
        states = states_response.get('states', []) if states_response else []
        
        # Obtener ciudades (asumiendo Central como estado por defecto)
        central_id = None
        if states:
            central = next((s for s in states if s['name'] == 'Central'), None)
            central_id = central['id'] if central else None
        
        cities_response = await api_client.get(
            f"{config.API_PREFIX}/location/cities/",
            params={"state_id": central_id} if central_id else {}
        )
        cities = cities_response.get('cities', []) if cities_response else []
        
        return {
            'countries': countries,
            'states': states,
            'cities': cities
        }
        
    except Exception as e:
        print(f"⚠️  Error obteniendo datos de location: {e}")
        return {'countries': [], 'states': [], 'cities': []}

async def populate_address_data(dry_run: bool = False):
    """
    Poblar datos de direcciones usando location_service
    """
    print("📍 Poblando direcciones (address)...")
    
    # Configuración del API Gateway
    api_gateway_url = config.API_GATEWAY_URL
    access_token = os.getenv("ACCESS_TOKEN")
    
    if not access_token:
        print("❌ ERROR: ACCESS_TOKEN no configurado en variables de entorno")
        print("   Configura ACCESS_TOKEN en tu archivo .env")
        return {"addresses": 0}
    
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")
        
        try:
            async with APIClient(api_gateway_url, access_token) as api_client:
                location_data = await get_location_data(api_client)
                
                print(f"   📍 Países disponibles: {len(location_data['countries'])}")
                print(f"   📍 Estados disponibles: {len(location_data['states'])}")
                print(f"   📍 Ciudades disponibles: {len(location_data['cities'])}")
                
                # Mostrar algunos ejemplos
                if location_data['countries']:
                    print(f"   📍 Ejemplo país: {location_data['countries'][0]['name']}")
                if location_data['states']:
                    print(f"   📍 Ejemplo estado: {location_data['states'][0]['name']}")
                if location_data['cities']:
                    print(f"   📍 Ejemplo ciudad: {location_data['cities'][0]['name']}")
                    
        except Exception as e:
            print(f"❌ Error obteniendo datos de location: {e}")
            
        return {"addresses": 0}
    
    # Aquí irá la lógica de inserción real
    return {"addresses": 0} 