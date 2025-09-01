"""
Rutas para notificaciones en el API Gateway

Este módulo contiene todas las rutas necesarias para la gestión de notificaciones
a través del API Gateway.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Optional
import logging

from api_gateway.application.notification.use_cases.send_message_whatsapp_use_case import SendMessageWhatsappUseCase
from api_gateway.application.notification.use_cases.send_remember_message_whatsapp_use_case import SendRememberMessageWhatsappUseCase
from api_gateway.domain.notification.dto.requests.notification_requests import SendMessageWhatsappRequest, SendRememberMessageWhatsappRequest
from api_gateway.domain.notification.dto.responses.notification_responses import NotificationResponse
from api_gateway.api.middleware import auth_middleware

# Configurar logger
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/send-whatsapp", response_model=NotificationResponse, status_code=status.HTTP_200_OK)
async def send_message_whatsapp(
    request: SendMessageWhatsappRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Enviar mensaje de WhatsApp
    
    Args:
        request: Datos del mensaje (to_number, from_number, text)
        current_user: Usuario autenticado
        authorization: Token de autorización
        
    Returns:
        NotificationResponse: Respuesta con el resultado de la operación
    """
    try:
        logger.info("🚀 Endpoint send_message_whatsapp llamado")
        logger.info(f"📝 Datos del mensaje: to_number={request.to_number}, from_number={request.from_number}, text_length={len(request.text)}")
        
        # Obtener use case
        logger.info("📝 Obteniendo use case...")
        use_case = SendMessageWhatsappUseCase()
        logger.info("✅ Use case obtenido correctamente")
        
        # Ejecutar envío
        logger.info("🔄 Ejecutando envío de mensaje...")
        result = await use_case.execute(request, authorization)
        logger.info("✅ Envío completado exitosamente")
        
        # Log del resultado
        logger.info(f"📊 Resultado: success={result.success}, message={result.message}")
        
        if result.success:
            logger.info("✅ Mensaje enviado exitosamente")
            return result
        else:
            logger.warning(f"⚠️ Error enviando mensaje: {result.message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": result.message}
            )
            
    except HTTPException:
        # Re-lanzar HTTPExceptions
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado en send_message_whatsapp: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Error interno del servidor: {str(e)}"}
        )


@router.post("/send-remember-whatsapp", response_model=NotificationResponse, status_code=status.HTTP_200_OK)
async def send_remember_message_whatsapp(
    request: SendRememberMessageWhatsappRequest,
    current_user=Depends(auth_middleware["require_auth"]),
    authorization: Optional[str] = Header(None)
):
    """
    Enviar mensaje recordatorio de WhatsApp
    
    Args:
        request: Datos del recordatorio (currentDate)
        current_user: Usuario autenticado
        authorization: Token de autorización
        
    Returns:
        NotificationResponse: Respuesta con el resultado de la operación
    """
    try:
        logger.info("🚀 Endpoint send_remember_message_whatsapp llamado")
        logger.info(f"📝 Fecha para recordatorios: {request.currentDate}")
        
        # Obtener use case
        logger.info("📝 Obteniendo use case...")
        use_case = SendRememberMessageWhatsappUseCase()
        logger.info("✅ Use case obtenido correctamente")
        
        # Ejecutar envío
        logger.info("🔄 Ejecutando envío de mensaje recordatorio...")
        result = await use_case.execute(request, authorization)
        logger.info("✅ Envío completado exitosamente")
        
        # Log del resultado
        logger.info(f"📊 Resultado: success={result.success}, message={result.message}")
        
        if result.success:
            logger.info("✅ Mensaje recordatorio enviado exitosamente")
            return result
        else:
            logger.warning(f"⚠️ Error enviando mensaje recordatorio: {result.message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": result.message}
            )
            
    except HTTPException:
        # Re-lanzar HTTPExceptions
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado en send_remember_message_whatsapp: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Error interno del servidor: {str(e)}"}
        )
