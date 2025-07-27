"""
Módulo común para funcionalidades compartidas entre microservicios
"""

from .service_factory import create_service_factory, ServiceConfig, RouterConfig, run_service, ErrorResponse

__all__ = [
    'create_service_factory',
    'ServiceConfig', 
    'RouterConfig',
    'run_service',
    'ErrorResponse'
] 