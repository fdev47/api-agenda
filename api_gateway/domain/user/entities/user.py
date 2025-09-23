"""
Entidad User del dominio - API Gateway
"""
from typing import Literal

# Definir el tipo como variable para mejor mantenibilidad
UserType = Literal['root', 'admin', 'user', 'recepcionista', 'recepcionista_rampa', 'recepcionista_rampa_frio']
