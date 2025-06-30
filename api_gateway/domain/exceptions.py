"""Excepciones de dominio para API Gateway"""

class GatewayError(Exception):
    """Excepción base para errores del API Gateway"""
    
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)


class ServiceUnavailableError(GatewayError):
    """Error cuando un servicio no está disponible"""
    
    def __init__(self, service_name: str, message: str = None):
        self.service_name = service_name
        super().__init__(
            error_code="SERVICE_UNAVAILABLE",
            message=message or f"Servicio {service_name} no está disponible"
        )


class ServiceTimeoutError(GatewayError):
    """Error cuando un servicio no responde en tiempo"""
    
    def __init__(self, service_name: str, timeout: float):
        self.service_name = service_name
        self.timeout = timeout
        super().__init__(
            error_code="SERVICE_TIMEOUT",
            message=f"Servicio {service_name} no respondió en {timeout} segundos"
        )


class ServiceCommunicationError(GatewayError):
    """Error de comunicación con un servicio"""
    
    def __init__(self, service_name: str, error: str):
        self.service_name = service_name
        self.original_error = error
        super().__init__(
            error_code="SERVICE_COMMUNICATION_ERROR",
            message=f"Error de comunicación con {service_name}: {error}"
        )


class OrchestrationError(GatewayError):
    """Error durante la orquestación de servicios"""
    
    def __init__(self, operation: str, message: str):
        self.operation = operation
        super().__init__(
            error_code="ORCHESTRATION_ERROR",
            message=f"Error en {operation}: {message}"
        ) 