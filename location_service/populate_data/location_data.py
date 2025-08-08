"""
Script para poblar la base de datos del location_service con datos de Paraguay
"""
import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path para poder importar commons
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commons.database import db_manager
from commons.config import config
from infrastructure.models.country import Country as CountryModel
from infrastructure.models.state import State as StateModel
from infrastructure.models.city import City as CityModel
from sqlalchemy.ext.asyncio import AsyncSession
from commons.database import get_db_manager
from commons.config import config


async def populate_countries(session: AsyncSession, dry_run: bool = False):
    """Poblar países"""
    print("🌍 Poblando países...")
    
    # Solo Paraguay
    paraguay = CountryModel(
        name="Paraguay",
        code="PY",
        phone_code="595",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    if not dry_run:
        session.add(paraguay)
        await session.commit()
        await session.refresh(paraguay)
    
    print(f"✅ País creado: {paraguay.name} (ID: {paraguay.id})")
    return paraguay


async def populate_states(session: AsyncSession, paraguay_id: int, dry_run: bool = False):
    """Poblar estados/departamentos de Paraguay"""
    print("🏛️ Poblando estados/departamentos...")
    
    states_data = [
        {"name": "Asunción", "code": "ASU"},
        {"name": "Central", "code": "CEN"},
        {"name": "Caazapá", "code": "CAA"},
        {"name": "Caaguazú", "code": "CAG"},
        {"name": "Canindeyú", "code": "CAN"},
        {"name": "Concepción", "code": "CON"},
        {"name": "Cordillera", "code": "COR"},
        {"name": "Guairá", "code": "GUA"},
        {"name": "Itapúa", "code": "ITA"},
        {"name": "Misiones", "code": "MIS"},
        {"name": "Ñeembucú", "code": "NEE"},
        {"name": "Paraguarí", "code": "PAR"},
        {"name": "Presidente Hayes", "code": "PRE"},
        {"name": "San Pedro", "code": "SAN"},
        {"name": "Alto Paraguay", "code": "ALT"},
        {"name": "Alto Paraná", "code": "ALP"},
        {"name": "Amambay", "code": "AMA"},
        {"name": "Boquerón", "code": "BOQ"}
    ]

    
    states = []
    for state_data in states_data:
        state = StateModel(
            name=state_data["name"],
            code=state_data["code"],
            country_id=paraguay_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        states.append(state)
        if not dry_run:
            session.add(state)
    
    if not dry_run:
        await session.commit()
    
    # Refrescar para obtener los IDs
    for state in states:
        if not dry_run:
            await session.refresh(state)
        print(f"✅ Estado creado: {state.name} (ID: {state.id})")
    
    return states


async def populate_cities(session: AsyncSession, states, dry_run: bool = False):
    """Poblar ciudades de Paraguay"""
    print("🏙️ Poblando ciudades...")
    
    # Crear un diccionario para mapear nombres de estados a objetos
    states_dict = {state.name: state for state in states}
    
    cities_data = [
        # Asunción
        {"name": "Asunción", "state_name": "Asunción", "code": "ASU"},
        
        # Central
        {"name": "San Lorenzo", "state_name": "Central", "code": "SLO"},
        {"name": "Luque", "state_name": "Central", "code": "LUQ"},
        {"name": "Capiatá", "state_name": "Central", "code": "CAP"},
        {"name": "Lambaré", "state_name": "Central", "code": "LAM"},
        {"name": "Fernando de la Mora", "state_name": "Central", "code": "FER"},
        {"name": "Limpio", "state_name": "Central", "code": "LIM"},
        {"name": "Ñemby", "state_name": "Central", "code": "NEM"},
        {"name": "Itauguá", "state_name": "Central", "code": "ITG"},
        {"name": "Mariano Roque Alonso", "state_name": "Central", "code": "MAR"},
        {"name": "San Antonio", "state_name": "Central", "code": "SAN"},
        {"name": "Villa Elisa", "state_name": "Central", "code": "VIL"},
        {"name": "Villeta", "state_name": "Central", "code": "VIL"},
        {"name": "Guarambaré", "state_name": "Central", "code": "GUA"},
        {"name": "Itá", "state_name": "Central", "code": "ITA"},
        {"name": "J. Augusto Saldívar", "state_name": "Central", "code": "JAS"},
        {"name": "Nueva Italia", "state_name": "Central", "code": "NUE"},
        {"name": "San José", "state_name": "Central", "code": "SJO"},
        {"name": "Tobatí", "state_name": "Central", "code": "TOB"},
        {"name": "Ypacaraí", "state_name": "Central", "code": "YPA"},
        {"name": "Areguá", "state_name": "Central", "code": "ARE"},
        {"name": "Capiibary", "state_name": "Central", "code": "CPI"},
        {"name": "Eusebio Ayala", "state_name": "Central", "code": "EUS"},
        {"name": "Isla Pucú", "state_name": "Central", "code": "ISL"},
        {"name": "Itacurubí de la Cordillera", "state_name": "Central", "code": "ITC"},
        {"name": "Piribebuy", "state_name": "Central", "code": "PIR"},
        {"name": "San Bernardino", "state_name": "Central", "code": "SBE"},
        {"name": "Santa Elena", "state_name": "Central", "code": "STE"},
        {"name": "Tobatí", "state_name": "Central", "code": "TOB"},
        {"name": "Valenzuela", "state_name": "Central", "code": "VAL"},
        
        # Caazapá
        {"name": "Caazapá", "state_name": "Caazapá", "code": "CAA"},
        {"name": "Abaí", "state_name": "Caazapá", "code": "ABA"},
        {"name": "Buena Vista", "state_name": "Caazapá", "code": "BUE"},
        {"name": "Dr. Moisés S. Bertoni", "state_name": "Caazapá", "code": "DMS"},
        {"name": "Fulgencio Yegros", "state_name": "Caazapá", "code": "FUL"},
        {"name": "General Higinio Morínigo", "state_name": "Caazapá", "code": "GHM"},
        {"name": "Maciel", "state_name": "Caazapá", "code": "MAC"},
        {"name": "San Juan Nepomuceno", "state_name": "Caazapá", "code": "SJN"},
        {"name": "Tavaí", "state_name": "Caazapá", "code": "TAV"},
        {"name": "Yuty", "state_name": "Caazapá", "code": "YUT"},
        
        # Caaguazú
        {"name": "Coronel Oviedo", "state_name": "Caaguazú", "code": "COV"},
        {"name": "Caaguazú", "state_name": "Caaguazú", "code": "CAG"},
        {"name": "Carayaó", "state_name": "Caaguazú", "code": "CAR"},
        {"name": "Cecilio Báez", "state_name": "Caaguazú", "code": "CEB"},
        {"name": "Dr. J. Eulogio Estigarribia", "state_name": "Caaguazú", "code": "DJE"},
        {"name": "Dr. Juan Manuel Frutos", "state_name": "Caaguazú", "code": "DJM"},
        {"name": "José Domingo Ocampos", "state_name": "Caaguazú", "code": "JDO"},
        {"name": "La Pastora", "state_name": "Caaguazú", "code": "LAP"},
        {"name": "Mcal. Francisco S. López", "state_name": "Caaguazú", "code": "MFS"},
        {"name": "Nueva Londres", "state_name": "Caaguazú", "code": "NUE"},
        {"name": "R.I. 3 Corrales", "state_name": "Caaguazú", "code": "RIC"},
        {"name": "Repatriación", "state_name": "Caaguazú", "code": "REP"},
        {"name": "R. I. 1 Yhú", "state_name": "Caaguazú", "code": "RIY"},
        {"name": "San Joaquín", "state_name": "Caaguazú", "code": "SJO"},
        {"name": "San José de los Arroyos", "state_name": "Caaguazú", "code": "SJA"},
        {"name": "Santa Rosa del Mbutuy", "state_name": "Caaguazú", "code": "SRM"},
        {"name": "Simón Bolívar", "state_name": "Caaguazú", "code": "SIB"},
        {"name": "Tembiaporá", "state_name": "Caaguazú", "code": "TEM"},
        {"name": "Tres de Febrero", "state_name": "Caaguazú", "code": "TDF"},
        {"name": "Vaquería", "state_name": "Caaguazú", "code": "VAQ"},
        {"name": "Yhú", "state_name": "Caaguazú", "code": "YHU"},
        
        # Canindeyú
        {"name": "Salto del Guairá", "state_name": "Canindeyú", "code": "SDG"},
        {"name": "Corpus Christi", "state_name": "Canindeyú", "code": "COR"},
        {"name": "Curuguaty", "state_name": "Canindeyú", "code": "CUR"},
        {"name": "General Francisco Caballero Alvarez", "state_name": "Canindeyú", "code": "GFC"},
        {"name": "Itanará", "state_name": "Canindeyú", "code": "ITA"},
        {"name": "Katueté", "state_name": "Canindeyú", "code": "KAT"},
        {"name": "La Paloma", "state_name": "Canindeyú", "code": "LAP"},
        {"name": "Nueva Esperanza", "state_name": "Canindeyú", "code": "NUE"},
        {"name": "Yasy Cañy", "state_name": "Canindeyú", "code": "YAS"},
        {"name": "Ybyrarovaná", "state_name": "Canindeyú", "code": "YBY"},
        {"name": "Ypehú", "state_name": "Canindeyú", "code": "YPE"},
        
        # Concepción
        {"name": "Concepción", "state_name": "Concepción", "code": "CON"},
        {"name": "Belén", "state_name": "Concepción", "code": "BEL"},
        {"name": "Horqueta", "state_name": "Concepción", "code": "HOR"},
        {"name": "Loreto", "state_name": "Concepción", "code": "LOR"},
        {"name": "San Carlos del Apa", "state_name": "Concepción", "code": "SCA"},
        {"name": "San Lázaro", "state_name": "Concepción", "code": "SLA"},
        {"name": "Yby Yaú", "state_name": "Concepción", "code": "YBY"},
        {"name": "Azotey", "state_name": "Concepción", "code": "AZO"},
        
        # Cordillera
        {"name": "Caacupé", "state_name": "Cordillera", "code": "CAA"},
        {"name": "Altos", "state_name": "Cordillera", "code": "ALT"},
        {"name": "Arroyos y Esteros", "state_name": "Cordillera", "code": "ARY"},
        {"name": "Atyrá", "state_name": "Cordillera", "code": "ATY"},
        {"name": "Caraguatay", "state_name": "Cordillera", "code": "CAR"},
        {"name": "Emboscada", "state_name": "Cordillera", "code": "EMB"},
        {"name": "Eusebio Ayala", "state_name": "Cordillera", "code": "EUS"},
        {"name": "Isla Pucú", "state_name": "Cordillera", "code": "ISL"},
        {"name": "Itacurubí de la Cordillera", "state_name": "Cordillera", "code": "ITC"},
        {"name": "Juan de Mena", "state_name": "Cordillera", "code": "JDM"},
        {"name": "Loma Grande", "state_name": "Cordillera", "code": "LOM"},
        {"name": "Mbocayaty del Yhaguy", "state_name": "Cordillera", "code": "MBY"},
        {"name": "Nueva Colombia", "state_name": "Cordillera", "code": "NUE"},
        {"name": "Piribebuy", "state_name": "Cordillera", "code": "PIR"},
        {"name": "Primero de Marzo", "state_name": "Cordillera", "code": "PDM"},
        {"name": "San Bernardino", "state_name": "Cordillera", "code": "SBE"},
        {"name": "San José Obrero", "state_name": "Cordillera", "code": "SJO"},
        {"name": "Santa Elena", "state_name": "Cordillera", "code": "STE"},
        {"name": "Tobatí", "state_name": "Cordillera", "code": "TOB"},
        {"name": "Valenzuela", "state_name": "Cordillera", "code": "VAL"},
        
        # Guairá
        {"name": "Villarrica", "state_name": "Guairá", "code": "VIL"},
        {"name": "Borja", "state_name": "Guairá", "code": "BOR"},
        {"name": "Colonia Independencia", "state_name": "Guairá", "code": "COI"},
        {"name": "Coronel Martínez", "state_name": "Guairá", "code": "COM"},
        {"name": "Dr. Bottrell", "state_name": "Guairá", "code": "DRB"},
        {"name": "Fassardi", "state_name": "Guairá", "code": "FAS"},
        {"name": "Félix Pérez Cardozo", "state_name": "Guairá", "code": "FPC"},
        {"name": "Garay", "state_name": "Guairá", "code": "GAR"},
        {"name": "Itapé", "state_name": "Guairá", "code": "ITA"},
        {"name": "Iturbe", "state_name": "Guairá", "code": "ITU"},
        {"name": "José A. Fassardi", "state_name": "Guairá", "code": "JAF"},
        {"name": "Mbocayaty", "state_name": "Guairá", "code": "MBO"},
        {"name": "Natalicio Talavera", "state_name": "Guairá", "code": "NAT"},
        {"name": "Ñumí", "state_name": "Guairá", "code": "NUM"},
        {"name": "Paso Yobái", "state_name": "Guairá", "code": "PAY"},
        {"name": "San Salvador", "state_name": "Guairá", "code": "SSA"},
        {"name": "Tebicuary", "state_name": "Guairá", "code": "TEB"},
        {"name": "Troche", "state_name": "Guairá", "code": "TRO"},
        {"name": "Yataity", "state_name": "Guairá", "code": "YAT"},
        
        # Itapúa
        {"name": "Encarnación", "state_name": "Itapúa", "code": "ENC"},
        {"name": "Alto Verá", "state_name": "Itapúa", "code": "ALV"},
        {"name": "Bella Vista", "state_name": "Itapúa", "code": "BEV"},
        {"name": "Cambyretá", "state_name": "Itapúa", "code": "CAM"},
        {"name": "Capitán Meza", "state_name": "Itapúa", "code": "CPM"},
        {"name": "Capitán Miranda", "state_name": "Itapúa", "code": "CPM"},
        {"name": "Carlos Antonio López", "state_name": "Itapúa", "code": "CAL"},
        {"name": "Carmen del Paraná", "state_name": "Itapúa", "code": "CDP"},
        {"name": "Coronel Bogado", "state_name": "Itapúa", "code": "COB"},
        {"name": "Edelira", "state_name": "Itapúa", "code": "EDE"},
        {"name": "Fram", "state_name": "Itapúa", "code": "FRA"},
        {"name": "General Artigas", "state_name": "Itapúa", "code": "GEA"},
        {"name": "General Delgado", "state_name": "Itapúa", "code": "GED"},
        {"name": "Hohenau", "state_name": "Itapúa", "code": "HOH"},
        {"name": "Itapúa", "state_name": "Itapúa", "code": "ITA"},
        {"name": "Jesús", "state_name": "Itapúa", "code": "JES"},
        {"name": "José Leandro Oviedo", "state_name": "Itapúa", "code": "JLO"},
        {"name": "La Paz", "state_name": "Itapúa", "code": "LAP"},
        {"name": "Mayor Julio D. Otaño", "state_name": "Itapúa", "code": "MJD"},
        {"name": "Natalio", "state_name": "Itapúa", "code": "NAT"},
        {"name": "Nueva Alborada", "state_name": "Itapúa", "code": "NUE"},
        {"name": "Obligado", "state_name": "Itapúa", "code": "OBL"},
        {"name": "Pirapó", "state_name": "Itapúa", "code": "PIR"},
        {"name": "San Cosme y Damián", "state_name": "Itapúa", "code": "SCD"},
        {"name": "San Juan del Paraná", "state_name": "Itapúa", "code": "SJP"},
        {"name": "San Pedro del Paraná", "state_name": "Itapúa", "code": "SPP"},
        {"name": "San Rafael del Paraná", "state_name": "Itapúa", "code": "SRP"},
        {"name": "Tomás Romero Pereira", "state_name": "Itapúa", "code": "TRP"},
        {"name": "Trinidad", "state_name": "Itapúa", "code": "TRI"},
        {"name": "Yatytay", "state_name": "Itapúa", "code": "YAT"},
        
        # Misiones
        {"name": "San Juan Bautista", "state_name": "Misiones", "code": "SJB"},
        {"name": "Ayolas", "state_name": "Misiones", "code": "AYO"},
        {"name": "San Ignacio", "state_name": "Misiones", "code": "SIG"},
        {"name": "San Miguel", "state_name": "Misiones", "code": "SMI"},
        {"name": "San Patricio", "state_name": "Misiones", "code": "SPA"},
        {"name": "Santa María", "state_name": "Misiones", "code": "STM"},
        {"name": "Santa Rosa", "state_name": "Misiones", "code": "STR"},
        {"name": "Santiago", "state_name": "Misiones", "code": "SAN"},
        {"name": "Villa Florida", "state_name": "Misiones", "code": "VFL"},
        {"name": "Yabebyry", "state_name": "Misiones", "code": "YAB"},
        
        # Ñeembucú
        {"name": "Pilar", "state_name": "Ñeembucú", "code": "PIL"},
        {"name": "Alberdi", "state_name": "Ñeembucú", "code": "ALB"},
        {"name": "Cerrito", "state_name": "Ñeembucú", "code": "CER"},
        {"name": "Desmochados", "state_name": "Ñeembucú", "code": "DES"},
        {"name": "General José Eduvigis Díaz", "state_name": "Ñeembucú", "code": "GJD"},
        {"name": "Guazú Cuá", "state_name": "Ñeembucú", "code": "GUC"},
        {"name": "Humaitá", "state_name": "Ñeembucú", "code": "HUM"},
        {"name": "Isla Umbú", "state_name": "Ñeembucú", "code": "ISU"},
        {"name": "Laureles", "state_name": "Ñeembucú", "code": "LAU"},
        {"name": "Mayor José J. Martínez", "state_name": "Ñeembucú", "code": "MJJ"},
        {"name": "Paso de Patria", "state_name": "Ñeembucú", "code": "PDP"},
        {"name": "San Juan Bautista del Ñeembucú", "state_name": "Ñeembucú", "code": "SJB"},
        {"name": "Tacuaras", "state_name": "Ñeembucú", "code": "TAC"},
        {"name": "Villa Franca", "state_name": "Ñeembucú", "code": "VFR"},
        {"name": "Villa Oliva", "state_name": "Ñeembucú", "code": "VOL"},
        {"name": "Villalbín", "state_name": "Ñeembucú", "code": "VIL"},
        
        # Paraguarí
        {"name": "Paraguarí", "state_name": "Paraguarí", "code": "PAR"},
        {"name": "Acahay", "state_name": "Paraguarí", "code": "ACA"},
        {"name": "Caapucú", "state_name": "Paraguarí", "code": "CAA"},
        {"name": "Carapeguá", "state_name": "Paraguarí", "code": "CAR"},
        {"name": "Escobar", "state_name": "Paraguarí", "code": "ESC"},
        {"name": "General Bernardino Caballero", "state_name": "Paraguarí", "code": "GBC"},
        {"name": "La Colmena", "state_name": "Paraguarí", "code": "LAC"},
        {"name": "Mbuyapey", "state_name": "Paraguarí", "code": "MBU"},
        {"name": "Pirayú", "state_name": "Paraguarí", "code": "PIR"},
        {"name": "Quiindy", "state_name": "Paraguarí", "code": "QUI"},
        {"name": "Quyquyhó", "state_name": "Paraguarí", "code": "QUY"},
        {"name": "San Roque González de Santa Cruz", "state_name": "Paraguarí", "code": "SRG"},
        {"name": "Sapucai", "state_name": "Paraguarí", "code": "SAP"},
        {"name": "Tebicuarymí", "state_name": "Paraguarí", "code": "TEB"},
        {"name": "Yaguarón", "state_name": "Paraguarí", "code": "YAG"},
        {"name": "Ybycuí", "state_name": "Paraguarí", "code": "YBY"},
        
        # Presidente Hayes
        {"name": "Villa Hayes", "state_name": "Presidente Hayes", "code": "VHA"},
        {"name": "Benjamín Aceval", "state_name": "Presidente Hayes", "code": "BEA"},
        {"name": "Chaco-i", "state_name": "Presidente Hayes", "code": "CHI"},
        {"name": "Colonia Falcón", "state_name": "Presidente Hayes", "code": "COF"},
        {"name": "Dr. José Falcón", "state_name": "Presidente Hayes", "code": "DJF"},
        {"name": "General José María Bruguez", "state_name": "Presidente Hayes", "code": "GJM"},
        {"name": "Nanawa", "state_name": "Presidente Hayes", "code": "NAN"},
        {"name": "Pozo Colorado", "state_name": "Presidente Hayes", "code": "POC"},
        {"name": "Puerto Pinasco", "state_name": "Presidente Hayes", "code": "PUP"},
        {"name": "Tte. 1ro Manuel Irala Fernández", "state_name": "Presidente Hayes", "code": "TMI"},
        
        # San Pedro
        {"name": "San Pedro", "state_name": "San Pedro", "code": "SPE"},
        {"name": "Antequera", "state_name": "San Pedro", "code": "ANT"},
        {"name": "Capiibary", "state_name": "San Pedro", "code": "CPI"},
        {"name": "Choré", "state_name": "San Pedro", "code": "CHO"},
        {"name": "General Elizardo Aquino", "state_name": "San Pedro", "code": "GEA"},
        {"name": "General Isidoro Resquín", "state_name": "San Pedro", "code": "GIR"},
        {"name": "Guayaibí", "state_name": "San Pedro", "code": "GUA"},
        {"name": "Itacurubí del Rosario", "state_name": "San Pedro", "code": "IDR"},
        {"name": "Lima", "state_name": "San Pedro", "code": "LIM"},
        {"name": "Nueva Germania", "state_name": "San Pedro", "code": "NUG"},
        {"name": "San Estanislao", "state_name": "San Pedro", "code": "SES"},
        {"name": "San Pablo", "state_name": "San Pedro", "code": "SPA"},
        {"name": "Tacuatí", "state_name": "San Pedro", "code": "TAC"},
        {"name": "Unión", "state_name": "San Pedro", "code": "UNI"},
        {"name": "Veinticinco de Diciembre", "state_name": "San Pedro", "code": "VDC"},
        {"name": "Villa del Rosario", "state_name": "San Pedro", "code": "VDR"},
        {"name": "Yataity del Norte", "state_name": "San Pedro", "code": "YDN"},
        {"name": "Yrybucuá", "state_name": "San Pedro", "code": "YRY"},
        
        # Alto Paraguay
        {"name": "Fuerte Olimpo", "state_name": "Alto Paraguay", "code": "FOL"},
        {"name": "Bahía Negra", "state_name": "Alto Paraguay", "code": "BAN"},
        {"name": "Capitán Carmelo Peralta", "state_name": "Alto Paraguay", "code": "CCP"},
        {"name": "Puerto Casado", "state_name": "Alto Paraguay", "code": "PUC"},
        
        # Alto Paraná
        {"name": "Ciudad del Este", "state_name": "Alto Paraná", "code": "CDE"},
        {"name": "Hernandarias", "state_name": "Alto Paraná", "code": "HER"},
        {"name": "Minga Guazú", "state_name": "Alto Paraná", "code": "MIG"},
        {"name": "Presidente Franco", "state_name": "Alto Paraná", "code": "PFR"},
        {"name": "San Alberto", "state_name": "Alto Paraná", "code": "SAL"},
        {"name": "Domingo Martínez de Irala", "state_name": "Alto Paraná", "code": "DMI"},
        {"name": "Dr. Juan León Mallorquín", "state_name": "Alto Paraná", "code": "DJL"},
        {"name": "Dr. Raúl Peña", "state_name": "Alto Paraná", "code": "DRP"},
        {"name": "Itakyry", "state_name": "Alto Paraná", "code": "ITA"},
        {"name": "Juan Emilio O'Leary", "state_name": "Alto Paraná", "code": "JEO"},
        {"name": "Los Cedrales", "state_name": "Alto Paraná", "code": "LCE"},
        {"name": "Mbaracayú", "state_name": "Alto Paraná", "code": "MBA"},
        {"name": "Minga Porá", "state_name": "Alto Paraná", "code": "MIP"},
        {"name": "Naranjal", "state_name": "Alto Paraná", "code": "NAR"},
        {"name": "Ñacunday", "state_name": "Alto Paraná", "code": "NAC"},
        {"name": "Santa Rita", "state_name": "Alto Paraná", "code": "SRI"},
        {"name": "Santa Rosa del Monday", "state_name": "Alto Paraná", "code": "SRM"},
        {"name": "Tavapy", "state_name": "Alto Paraná", "code": "TAV"},
        {"name": "Yguazú", "state_name": "Alto Paraná", "code": "YGU"},
        
        # Amambay
        {"name": "Pedro Juan Caballero", "state_name": "Amambay", "code": "PJC"},
        {"name": "Bella Vista Norte", "state_name": "Amambay", "code": "BVN"},
        {"name": "Capitán Bado", "state_name": "Amambay", "code": "CAB"},
        {"name": "Karapaí", "state_name": "Amambay", "code": "KAR"},
        {"name": "Paso de Otero", "state_name": "Amambay", "code": "PDO"},
        {"name": "Zanja Pytá", "state_name": "Amambay", "code": "ZAP"},
        
        # Boquerón
        {"name": "Filadelfia", "state_name": "Boquerón", "code": "FIL"},
        {"name": "Loma Plata", "state_name": "Boquerón", "code": "LOP"},
        {"name": "Mariscal Estigarribia", "state_name": "Boquerón", "code": "MAE"},
        {"name": "Neuland", "state_name": "Boquerón", "code": "NEU"},
        {"name": "Dr. Pedro P. Peña", "state_name": "Boquerón", "code": "DPP"},
        {"name": "Gral. Eugenio A. Garay", "state_name": "Boquerón", "code": "GEA"},
        {"name": "Teniente Irala Fernández", "state_name": "Boquerón", "code": "TIF"}
    ]
    
    cities = []
    for city_data in cities_data:
        state = states_dict.get(city_data["state_name"])
        if state:
            city = CityModel(
                name=city_data["name"],
                code=city_data["code"],
                state_id=state.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            cities.append(city)
            if not dry_run:
                session.add(city)
    
    if not dry_run:
        await session.commit()
    
    # Refrescar para obtener los IDs
    for city in cities:
        if not dry_run:
            await session.refresh(city)
        print(f"✅ Ciudad creada: {city.name} (ID: {city.id})")
    
    return cities


async def populate_location_data(dry_run: bool = False):
    """Función principal para poblar la base de datos"""
    print("🚀 Iniciando población de datos de Paraguay...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")
    
    # Obtener la URL de la base de datos de location
    location_db_url = config.LOCATION_DATABASE_URL
    if not location_db_url:
        raise ValueError("LOCATION_DATABASE_URL no está configurada")
    
    # Obtener el gestor de base de datos para location
    db_manager = get_db_manager(location_db_url)
    session = await db_manager.get_session()
    
    try:
        # Poblar países
        paraguay = await populate_countries(session, dry_run)
        
        # Poblar estados
        states = await populate_states(session, paraguay.id, dry_run)
        
        # Poblar ciudades
        cities = await populate_cities(session, states, dry_run)
        
        if dry_run:
            print(f"\n🔍 SIMULACIÓN COMPLETADA - No se guardaron datos")
        else:
            print(f"\n🎉 ¡Población completada exitosamente!")
        
        print(f"📊 Resumen:")
        print(f"   🌍 Países: 1")
        print(f"   🏛️ Estados: {len(states)}")
        print(f"   🏙️ Ciudades: {len(cities)}")
        
        return {
            "countries": 1,
            "states": len(states),
            "cities": len(cities)
        }
        
    except Exception as e:
        print(f"❌ Error durante la población: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close() 