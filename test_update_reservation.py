#!/usr/bin/env python3
"""
Script para probar la actualización granular de reservas
"""
import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:8001"
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjE2YjQ5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5YzM5In0.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZm9ydGlzLWFnZW5kYSIsImF1ZCI6ImZvcnRpcy1hZ2VuZGEiLCJhdXRoX3RpbWUiOjE3MzQ5NjgwMDAsInVzZXJfaWQiOiJ0ZXN0LXVzZXItaWQiLCJpYXQiOjE3MzQ5NjgwMDAsImV4cCI6MTczNDk3MTYwMCwicGhvbmVfbnVtYmVyIjoiKzU5MzEyMzQ1Njc4IiwidXNlcl9uYW1lIjoidGVzdC11c2VyIiwidXNlcl9lbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNfYWN0aXZlIjp0cnVlfQ.test-signature"

def test_update_reservation():
    """Probar actualización granular de una reserva"""
    
    # Headers con autenticación
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 1. Primero, obtener una reserva existente
    print("🔍 Obteniendo lista de reservas...")
    response = requests.get(f"{BASE_URL}/reservations", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error al obtener reservas: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    reservations = response.json()
    if not reservations.get("items"):
        print("❌ No hay reservas disponibles para actualizar")
        return
    
    reservation_id = reservations["items"][0]["id"]
    print(f"✅ Reserva encontrada con ID: {reservation_id}")
    
    # 2. Mostrar el estado actual de la reserva
    print("\n📋 Estado actual de la reserva:")
    current_reservation = reservations["items"][0]
    print(f"  - Notes: {current_reservation.get('notes', 'No definido')}")
    print(f"  - Sector description: {current_reservation.get('sector_data', {}).get('description', 'No definido')}")
    
    # 3. Realizar actualización granular
    update_data = {
        "notes": "actualizado",
        "sector_data": {
            "description": "Sector para cargas y descargas"
        }
    }
    
    print(f"\n🔄 Actualizando reserva con datos: {json.dumps(update_data, indent=2)}")
    
    response = requests.put(
        f"{BASE_URL}/reservations/{reservation_id}",
        headers=headers,
        json=update_data
    )
    
    if response.status_code != 200:
        print(f"❌ Error al actualizar reserva: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    updated_reservation = response.json()
    print("✅ Reserva actualizada exitosamente")
    
    # 4. Verificar que solo se actualizaron los campos específicos
    print("\n📋 Estado después de la actualización:")
    print(f"  - Notes: {updated_reservation.get('notes')}")
    print(f"  - Sector description: {updated_reservation.get('sector_data', {}).get('description')}")
    print(f"  - Sector name: {updated_reservation.get('sector_data', {}).get('name')} (debería mantenerse igual)")
    print(f"  - Sector capacity: {updated_reservation.get('sector_data', {}).get('capacity')} (debería mantenerse igual)")
    
    # 5. Verificar que otros campos no se modificaron
    print("\n🔍 Verificando que otros campos se mantuvieron igual:")
    
    # Comparar campos que NO deberían cambiar
    original_sector = current_reservation.get('sector_data', {})
    updated_sector = updated_reservation.get('sector_data', {})
    
    fields_to_check = ['name', 'capacity', 'sector_type_id', 'measurement_unit_id']
    for field in fields_to_check:
        original_value = original_sector.get(field)
        updated_value = updated_sector.get(field)
        if original_value == updated_value:
            print(f"  ✅ {field}: se mantuvo igual ({original_value})")
        else:
            print(f"  ❌ {field}: cambió de {original_value} a {updated_value}")

if __name__ == "__main__":
    test_update_reservation() 