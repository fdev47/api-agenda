#!/usr/bin/env python3
"""
Test script to validate Firebase tokens with proper Authorization header
"""

import requests
import json
import os

# Configuration
AUTH_SERVICE_URL = "http://localhost:8001"
USER_SERVICE_URL = "http://localhost:8002"
API_PREFIX = "/api/v1"

def print_step(step, description):
    print(f"\n{step} {description}")
    print("=" * 50)

def print_result(status, data=None, error=None):
    print(f"Status: {status}")
    if data:
        print(f"Response: {json.dumps(data, indent=2)}")
    if error:
        print(f"Error: {error}")
    print()

def test_token_validation(token):
    """Test token validation with Auth Service"""
    print_step("1️⃣", "Validando token con Auth Service")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}{API_PREFIX}/auth/validate-token",
            headers=headers
        )
        
        print_result(response.status_code, response.json())
        return response.status_code == 200 and response.json().get("valid", False)
        
    except Exception as e:
        print_result("ERROR", None, f"Error de conexión: {str(e)}")
        return False

def test_user_service_with_token(token):
    """Test User Service with the token"""
    print_step("2️⃣", "Probando User Service con token")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{USER_SERVICE_URL}{API_PREFIX}/users/me",
            headers=headers
        )
        
        print_result(response.status_code, response.json())
        return response.status_code == 200
        
    except Exception as e:
        print_result("ERROR", None, f"Error de conexión: {str(e)}")
        return False

def main():
    print("🔐 Test de validación de token de Firebase")
    print("=" * 60)
    
    # Get token from user input
    print("💡 Pega aquí tu token de Firebase (sin 'Bearer '):")
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ3YWU0OWM0YzlkM2ViODVhNTI1NDA3MmMzMGQyZThlNzY2MWVmZTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiZmFiaWFuIHZlcmEiLCJyb2xlcyI6WyJ1c2VyIl0sInBlcm1pc3Npb25zIjpbXSwib3JnYW5pemF0aW9uX2lkIjpudWxsLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZm9ydGlzLWZhNDNjIiwiYXVkIjoiZm9ydGlzLWZhNDNjIiwiYXV0aF90aW1lIjoxNzUyNDc0MDUzLCJ1c2VyX2lkIjoiSkpoMFBWYWhKeVFpZ0pVd1EyVmlpd1BJVTQ0MiIsInN1YiI6IkpKaDBQVmFoSnlRaWdKVXdRMlZpaXdQSVU0NDIiLCJpYXQiOjE3NTI0NzQwNTMsImV4cCI6MTc1MjQ3NzY1MywiZW1haWwiOiJmYWJpYW52ZXJhLmRldkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfbnVtYmVyIjoiKzU5NTk4MTEyMzQ1NiIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZmFiaWFudmVyYS5kZXZAZ21haWwuY29tIl0sInBob25lIjpbIis1OTU5ODExMjM0NTYiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.rwtW231bOzaHpSf236tMcoX2v5YpSC1foxTLHqOgudAKW-EWi3JqwyJYRoxFYPmxm6eU6MhSfj2K3xZO82AGKrNRVq4qD7wjngooT-fHoiev4PNH3BFyQAcjQCh56OlkONezIc716wMEWM6iisHq6-aRtvmXhUzxPfykvEOy100mIiqXfjiyO-NV8FlUEc9nb9YINChM5B41gkKbOkG98uuQSX0E-v36gRuAKo7QeEPjlgS0-Kw9HY3ajM7C19dgBgntw8eLVeahzOx92oC-dgKBZ8qDjqbeChH_h1i72CEslQbDv-Cvjb4kCs315Gp6eqorCnGPr3UKiot5gdP6Ug"
    
    if not token:
        print("❌ No se proporcionó token")
        return
    
    print(f"🔑 Token recibido (primeros 20 chars): {token[:20]}...")
    
    # Test token validation
    is_valid = test_token_validation(token)
    
    if is_valid:
        print("✅ Token válido en Auth Service")
        
        # Test User Service
        user_service_works = test_user_service_with_token(token)
        
        if user_service_works:
            print("✅ User Service acepta el token")
            print("\n🎉 Todo funciona correctamente!")
        else:
            print("❌ User Service rechaza el token")
    else:
        print("❌ Token inválido en Auth Service")
        print("💡 Verifica que el token sea válido y no haya expirado")

if __name__ == "__main__":
    main() 