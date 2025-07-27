#!/bin/bash

# Script para probar autenticación rápidamente
# Reemplaza estas variables con tus valores reales

BASE_URL="http://localhost:8003"
API_PREFIX="/api/v1"
TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6IjZkZTQwZjA0ODgxYzZhMDE2MTFlYjI4NGE0Yzk1YTI1MWU5MTEyNTAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiZmFiaWFuIHZlcmEiLCJyb2xlcyI6WyJ1c2VyIl0sInBlcm1pc3Npb25zIjpbXSwib3JnYW5pemF0aW9uX2lkIjpudWxsLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZm9ydGlzLWZhNDNjIiwiYXVkIjoiZm9ydGlzLWZhNDNjIiwiYXV0aF90aW1lIjoxNzUzNTY5NTk0LCJ1c2VyX2lkIjoiSkpoMFBWYWhKeVFpZ0pVd1EyVmlpd1BJVTQ0MiIsInN1YiI6IkpKaDBQVmFoSnlRaWdKVXdRMlZpaXdQSVU0NDIiLCJpYXQiOjE3NTM1Njk1OTQsImV4cCI6MTc1MzU3MzE5NCwiZW1haWwiOiJmYWJpYW52ZXJhLmRldkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfbnVtYmVyIjoiKzU5NTk4MTEyMzQ1NiIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZmFiaWFudmVyYS5kZXZAZ21haWwuY29tIl0sInBob25lIjpbIis1OTU5ODExMjM0NTYiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.LdKDhMBVw5BU2Pra_udQR9V-mXHy3ks2zsloy4U0sEZx9WknXR9DCTOrKQgsnBazaAE9ZSFqs3TahZ2DAKOvCMDrU7oXYqr6gBtIsGE8J1D8wJDmBhpvEEMQ-Y9U1qmrk8o6QWWIvCaeNesBj7uishAmo5PJcNmZ7rkZZ-T--UQNQLSF-NnbWkcEthNlVjg_t_DnD1PeqGVo8bSh4EB-kNXIENlQQqbfs8xPAiLTcPgFrxy0fjebMluZlAihNQgwZdtrlPWSjUMCGSv3gpyDRMt4Oad3y9eOECLVAQPPi9J4-UMGqzIuoIQ9FvLjc8r4d4GB83WvMHXxrdOMaepuIw"

echo "=== TESTING AUTENTICACIÓN ==="
echo "Base URL: $BASE_URL"
echo "Token (primeros 20 chars): ${TOKEN:0:20}..."
echo

# 1. Probar endpoint público
echo "1. Probando endpoint público /health..."
curl -s -w "Status: %{http_code}\n" "$BASE_URL/health" | head -5
echo

# 2. Probar debug/openapi (ahora debe funcionar)
echo "2. Probando /debug/openapi..."
curl -s -w "Status: %{http_code}\n" "$BASE_URL/debug/openapi" | head -10
echo

# 3. Probar endpoint protegido SIN token
echo "3. Probando endpoint protegido SIN token..."
curl -s -w "Status: %{http_code}\n" "$BASE_URL$API_PREFIX/states/states/" | jq .
echo

# 4. Probar endpoint protegido CON token
echo "4. Probando endpoint protegido CON token..."
curl -s -H "Authorization: Bearer $TOKEN" -w "Status: %{http_code}\n" "$BASE_URL$API_PREFIX/states/states/" | jq .
echo

echo "=== FIN DEL TEST ==="