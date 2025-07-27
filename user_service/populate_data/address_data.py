"""
Script para poblar direcciones (address) en user_service usando location_service
"""
import os
import sys
import asyncio
from commons.api_client import APIClient
from commons.config import config
from commons.database import db_manager
from user_service.domain.entities.address import Address
from user_service.data.repositories.address_repository_impl import AddressRepositoryImpl

# Datos de direcciones de Paraguay con códigos
direcciones_paraguay = [
    {
        "direccion": "CHILE C/PUERTO PINAZCO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "FLORIDA 9029 - LUQUE",
        "ciudad": "LUQ",
        "departamento": "CEN"
    },
    {
        "direccion": "AV. MONSENOR RODRIGUEZ KM 6 1/2",
        "ciudad": "LUQ",
        "departamento": "CEN"
    },
    {
        "direccion": "JAVIER BOGARIN C/ SPORTIVO LUQUEÑO",
        "ciudad": "LUQ",
        "departamento": "CEN"
    },
    {
        "direccion": "ALCIDES GONZALEZ E/OSVALDO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AVD MOLAS LOPEZ 301",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "RUTA INT Nº 7 KM 9",
        "ciudad": "CDE",
        "departamento": "ALP"
    },
    {
        "direccion": "ANDRES INSFRAN , 350",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "ZAVALAS CUE C/ YATAYTY",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AV. EUSEBIO AYAL CDE",
        "ciudad": "CDE",
        "departamento": "ALP"
    },
    {
        "direccion": "AV.NANAWA 136 C/ ADRIAN JARA",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "MAXIMA LUGO, 682",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "KM 318 CNEL BOGADO",
        "ciudad": "COB",
        "departamento": "ITA"
    },
    {
        "direccion": "LEON FRANGNAUG 768 E PACHECO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "MCAL. ESTIGARRIBIA N 1539 C/CURUPAY",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "ARTIGAS E/REPUBLICA DOMINICANA",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "SAMAKLAY C R.I. 3 CORRALES",
        "ciudad": "FER",
        "departamento": "CEN"
    },
    {
        "direccion": "GRAL.BRUGUEZ",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "HUMAITA DR.GASPAR R. DE FRANCIA",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AV.ACESO SUR N.1021 C/ABELINO MART",
        "ciudad": "FER",
        "departamento": "CEN"
    },
    {
        "direccion": "JUAN C.PATINO 1298 C/PADRE LUIS DE",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AVDA. CARLOS DOMINGUEZ 329",
        "ciudad": "SLO",
        "departamento": "CEN"
    },
    {
        "direccion": "LA PRADERA",
        "ciudad": "CAP",
        "departamento": "CEN"
    },
    {
        "direccion": 'CALLE "A" Nº 1909 C/SGTO.LOMBARDO',
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AVDA. KUBITSHEK 768",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "DR.CESAR L.MOREIRA1136 C/ NARCISO C",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AVDA. DEF. DEL CHACO Y PYCASU",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "PAPA JUAN N1570",
        "ciudad": "SLO",
        "departamento": "CEN"
    },
    {
        "direccion": "PEDRO GETTO Nº8966",
        "ciudad": "SLO",
        "departamento": "CEN"
    },
    {
        "direccion": "RUTA MARCIAL SAMANIEGO - ITAGUA",
        "ciudad": "ITG",
        "departamento": "CEN"
    },
    {
        "direccion": "ROSEDAL N 96 C/AVDA DEF DEL CHACO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "VENEZUELA 740 ESQ.FRAY LUIS DE LEO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "CABALLERO, 2644 C/15 PTDAS",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "JOSE PAPPALARDO C/TTE CACERES",
        "ciudad": "SLO",
        "departamento": "CEN"
    },
    {
        "direccion": "BELLA VISTA (ITAPUA)",
        "ciudad": "BEV",
        "departamento": "ITA"
    },
    {
        "direccion": "CARMEN GARCETE, 851",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "CELSA SPERATTI Y DE LA HONESTIDAD",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "DR. MANUEL PEREZ, 679 C/MISIONES",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "PETIROSSI 1133 C/PRES FRANCO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "AVDA.MOLAS LOPEZ 2125 C/SACRAMENT",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "TTE. DELGADO, 527 C/AVDA ESPAÑA",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "RUTA 7 KM 209 JUAN MANUEL FRUTOS",
        "ciudad": "DJM",
        "departamento": "CAG"
    },
    {
        "direccion": "ISRAEL 2843 C/CEFERINO RUIZ",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "NANAWA C/GONDRA - BARRIO CENTRAL",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "RUTA MCAL. ESTIGARRIBIA, 1282",
        "ciudad": "SLO",
        "departamento": "CEN"
    },
    {
        "direccion": "MERCADO CENRAL DE ABASTO",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "CHOFERES DEL CHACO Y LISTO VALOIS",
        "ciudad": "ASU",
        "departamento": "ASU"
    },
    {
        "direccion": "SANTA ROSA 259",
        "ciudad": "ASU",
        "departamento": "ASU"
    }
]

async def get_location_data(api_client: APIClient):
    """
    Obtener datos de location desde el API Gateway
    """
    try:
        # Obtener países
        countries_response = await api_client.get(f"{config.API_PREFIX}/location/countries/", params={"limit": 255})
        countries = countries_response.get('countries', []) if countries_response else []
        
        # Obtener estados (asumiendo Paraguay como país por defecto)
        paraguay_id = None
        if countries:
            paraguay = next((c for c in countries if c['name'] == 'Paraguay'), None)
            paraguay_id = paraguay['id'] if paraguay else None
        
        states_response = await api_client.get(
            f"{config.API_PREFIX}/location/states/",
            params={"country_id": paraguay_id, "limit": 255} if paraguay_id else {"limit": 255}
        )
        states = states_response.get('states', []) if states_response else []
        
        # Obtener ciudades (asumiendo Central como estado por defecto)
        central_id = None
        if states:
            central = next((s for s in states if s['name'] == 'Central'), None)
            central_id = central['id'] if central else None
        
        cities_response = await api_client.get(
            f"{config.API_PREFIX}/location/cities/",
            params={"state_id": central_id, "limit": 255} if central_id else {"limit": 255}
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

def find_location_ids_by_code(direccion_data, location_data):
    """
    Encontrar los IDs de ciudad y estado basándose en los códigos
    """
    ciudad_codigo = direccion_data['ciudad']
    departamento_codigo = direccion_data['departamento']
    
    # Buscar ciudad por código
    city_id = None
    state_id = None
    country_id = None
    
    for city in location_data['cities']:
        if city.get('code') == ciudad_codigo:
            city_id = city['id']
            state_id = city.get('state_id') or 0
            break
    
    # Si no encontramos la ciudad, buscar por estado
    if not city_id:
        for state in location_data['states']:
            if state.get('code') == departamento_codigo:
                state_id = state['id']
                # Buscar cualquier ciudad de ese estado
                for city in location_data['cities']:
                    if city.get('state_id') == state_id:
                        city_id = city['id']
                        break
                break
    
    # Buscar Paraguay como país
    for country in location_data['countries']:
        if country['name'] == 'Paraguay':
            country_id = country['id']
            break
    
    return city_id, state_id, country_id

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
                    print(f"   📍 Ejemplo estado: {location_data['states'][0]['name']} (código: {location_data['states'][0].get('code', 'N/A')})")
                if location_data['cities']:
                    print(f"   📍 Ejemplo ciudad: {location_data['cities'][0]['name']} (código: {location_data['cities'][0].get('code', 'N/A')})")
                
                # Procesar algunas direcciones de ejemplo
                processed_count = 0
                for direccion in direcciones_paraguay[:5]:  # Solo las primeras 5 para simulación
                    city_id, state_id, country_id = find_location_ids_by_code(direccion, location_data)
                    if city_id and state_id and country_id:
                        processed_count += 1
                        print(f"   ✅ Dirección procesada: {direccion['direccion']} -> Ciudad ID: {city_id}, Estado ID: {state_id}")
                    else:
                        print(f"   ❌ No se encontraron IDs para: {direccion['direccion']} (ciudad: {direccion['ciudad']}, depto: {direccion['departamento']})")
                
                print(f"   📍 Direcciones procesadas en simulación: {processed_count}")
                    
        except Exception as e:
            print(f"❌ Error obteniendo datos de location: {e}")
            
        return {"addresses": 0}
    
    # Lógica real de inserción
    try:
        # Obtener datos de location desde API Gateway
        async with APIClient(api_gateway_url, access_token) as api_client:
            location_data = await get_location_data(api_client)
            
            if not location_data['countries'] or not location_data['states'] or not location_data['cities']:
                print("❌ ERROR: No se pudieron obtener datos de location")
                return {"addresses": 0}
            
            print(f"✅ Datos de location obtenidos: {len(location_data['cities'])} ciudades, {len(location_data['states'])} estados")
            
            # Insertar direcciones directamente en la BD
            async with db_manager.AsyncSessionLocal() as session:
                address_repository = AddressRepositoryImpl(session)
                created_count = 0
                
                for direccion in direcciones_paraguay:
                    try:
                        city_id, state_id, country_id = find_location_ids_by_code(direccion, location_data)
                        
                        if not city_id or not state_id or not country_id:
                            print(f"⚠️  No se encontraron IDs para: {direccion['direccion']} (ciudad: {direccion['ciudad']}, depto: {direccion['departamento']})")
                            continue
                        
                        # Crear entidad Address
                        address = Address(
                            street=direccion['direccion'],
                            city_id=city_id,
                            state_id=state_id,
                            country_id=country_id,
                            postal_code=None,
                            additional_info=None
                        )
                        
                        # Guardar en BD
                        created_address = await address_repository.create(address)
                        created_count += 1
                        print(f"✅ Dirección creada: {direccion['direccion']} (ID: {created_address.id})")
                        
                    except Exception as e:
                        print(f"❌ Error procesando dirección {direccion['direccion']}: {e}")
                
                print(f"📍 Total de direcciones creadas: {created_count}")
                return {"addresses": created_count}
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        return {"addresses": 0} 