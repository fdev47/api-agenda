"""
Ejemplo de cómo usar el middleware de autenticación en otros servicios
"""
from fastapi import FastAPI, Depends
from auth.api.external_middleware import create_auth_middleware

# Crear la aplicación
app = FastAPI(title="Servicio Ejemplo", version="1.0.0")

# Crear middleware de autenticación (usará automáticamente el puerto del .env)
auth_middleware = create_auth_middleware()


@app.get("/public")
async def public_endpoint():
    """Endpoint público - no requiere autenticación"""
    return {"message": "Este endpoint es público"}


@app.get("/protected")
async def protected_endpoint(current_user=Depends(auth_middleware.require_auth)):
    """Endpoint protegido - requiere autenticación"""
    return {
        "message": "Este endpoint está protegido",
        "user": current_user
    }


@app.get("/admin-only")
async def admin_endpoint(current_user=Depends(auth_middleware.require_role("admin"))):
    """Endpoint solo para administradores"""
    return {
        "message": "Este endpoint es solo para administradores",
        "user": current_user
    }


@app.get("/user-profile")
async def user_profile(current_user=Depends(auth_middleware.get_current_user)):
    """Endpoint que puede ser usado con o sin autenticación"""
    if current_user:
        return {
            "message": "Usuario autenticado",
            "user": current_user
        }
    else:
        return {
            "message": "Usuario no autenticado",
            "user": None
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 