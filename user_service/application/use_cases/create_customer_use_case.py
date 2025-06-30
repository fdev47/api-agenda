"""
Use case para crear clientes
"""
from typing import Protocol
from ...domain.interfaces.customer_repository import CustomerRepository
from ...domain.dto.requests.customer_requests import CreateCustomerRequest
from ...domain.dto.responses.customer_responses import CustomerResponse
from ...domain.entities.customer import Customer
from ...domain.exceptions.user_exceptions import UserException


class AuthServiceClient(Protocol):
    """Protocolo para el cliente de Auth Service"""
    async def create_user(self, email: str, password: str, display_name: str = None) -> dict:
        """Crear usuario en el proveedor de autenticación"""
        ...


class CreateCustomerUseCase:
    """
    Use Case para crear clientes
    
    Responsabilidades:
    - Orquestar la creación de cliente en el proveedor de auth y PostgreSQL
    - Manejar errores y rollback si es necesario
    - Garantizar consistencia de datos
    """
    
    def __init__(self, customer_repository: CustomerRepository, auth_service_client: AuthServiceClient):
        """
        Inicializar el use case
        
        Args:
            customer_repository: Repositorio para operaciones de base de datos
            auth_service_client: Cliente para comunicarse con Auth Service
        """
        self.customer_repository = customer_repository
        self.auth_service_client = auth_service_client
    
    async def execute(self, request: CreateCustomerRequest) -> CustomerResponse:
        """
        Ejecutar la creación de cliente
        
        Flujo:
        1. Crear usuario en el proveedor de auth (Auth Service)
        2. Si es exitoso, crear cliente en PostgreSQL
        3. Si el auth falla, no tocar la base de datos
        
        Args:
            request: Datos del cliente a crear
            
        Returns:
            CustomerResponse: Cliente creado exitosamente
            
        Raises:
            UserException: Si falla la creación en el auth o PostgreSQL
        """
        try:
            # Paso 1: Crear usuario en el proveedor de auth (Auth Service)
            auth_user = await self._create_customer_in_auth(request)
            
            # Paso 2: Crear cliente en PostgreSQL
            customer = await self._create_customer_in_database(request, auth_user)
            
            # Paso 3: Retornar respuesta
            return CustomerResponse.model_validate(customer)
            
        except UserException:
            # Re-lanzar errores de dominio
            raise
        except Exception as e:
            # Convertir errores inesperados en errores de dominio
            raise UserException(
                f"Error inesperado al crear cliente: {str(e)}"
            )
    
    async def _create_customer_in_auth(self, request: CreateCustomerRequest) -> dict:
        """
        Crear usuario en el proveedor de auth a través de Auth Service
        
        Args:
            request: Datos del cliente
            
        Returns:
            dict: Datos del usuario creado en el auth
            
        Raises:
            UserException: Si falla la creación en el auth
        """
        try:
            # Generar password temporal (el cliente lo cambiará después)
            temp_password = f"Temp{request.ruc}!"
            
            return await self.auth_service_client.create_user(
                email=request.email,
                password=temp_password,
                display_name=request.company_name
            )
        except Exception as e:
            # Log del error para debugging
            print(f"❌ Error al crear cliente en auth: {str(e)}")
            raise UserException(
                f"Error al crear cliente en auth: {str(e)}"
            )
    
    async def _create_customer_in_database(self, request: CreateCustomerRequest, auth_user: dict) -> Customer:
        """
        Crear cliente en la base de datos PostgreSQL
        
        Args:
            request: Datos del cliente
            auth_user: Datos del usuario creado en el auth
            
        Returns:
            Customer: Cliente creado en la base de datos
            
        Raises:
            UserException: Si falla la creación en la base de datos
        """
        try:
            # Actualizar el auth_uid con el ID del proveedor de auth
            request.auth_uid = auth_user.get("user_id")
            
            return await self.customer_repository.create(request)
            
        except Exception as e:
            # Log del error para debugging
            print(f"❌ Error al crear cliente en base de datos: {str(e)}")
            raise UserException(
                f"Error al crear cliente en base de datos: {str(e)}"
            ) 