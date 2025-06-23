"""Domain layer - Core business logic and models"""

from .models import (
    AuthToken,
    UserCredentials,
    UserRegistration,
    AuthenticatedUser,
    CustomClaims,
    AuthError,
    AuthErrorCode
)

from .interfaces import (
    IAuthProvider,
    ITokenValidator,
    IUserClaimsManager
)

__all__ = [
    "AuthToken", "UserCredentials", "UserRegistration", "AuthenticatedUser",
    "CustomClaims", "AuthError", "AuthErrorCode", "IAuthProvider",
    "ITokenValidator", "IUserClaimsManager"
] 