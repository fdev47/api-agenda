"""
Entidades del dominio de usuarios
"""
from .user import User
from .customer import Customer
from .address import Address
from .profile import Profile
from .role import Role

__all__ = ['User', 'Customer', 'Address', 'Profile', 'Role'] 