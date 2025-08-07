#!/usr/bin/env python3
"""
Script para iniciar el API Gateway
"""
import uvicorn
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_gateway.api.main import app
from commons.config import config

if __name__ == "__main__":
    print("🚀 Iniciando API Gateway...")
    print(f"📍 Puerto: {config.API_GATEWAY_PORT}")
    print(f"🔗 URL: http://localhost:{config.API_GATEWAY_PORT}")
    print(f"📚 Docs: http://localhost:{config.API_GATEWAY_PORT}/docs")
    
    uvicorn.run(
        "api_gateway.api.main:app",
        host="0.0.0.0",
        port=config.API_GATEWAY_PORT,
        reload=True,
        log_level="info"
    ) 