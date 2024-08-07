import jwt
import secrets
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework.request import Request
from rest_framework import authentication, exceptions
from .models import User, RefreshToken

class JWTAuthentication(authentication.BaseAuthentication):
    BEARER_PREFIX = 'Bearer '
    
    """
    Custom JWT Authentication class.
    """
    @staticmethod
    def authenticate(request: Request) -> tuple[User, str] | None:
        """
        Authenticate the request using JWT token.

        @param request: The HTTP request object.
        @return: A tuple containing the user and the token if authentication is successful, or None if no auth header is provided.
        @exception: Raises AuthenticationFailed if the token is invalid, expired, or if the user does not exist.
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith(JWTAuthentication.BEARER_PREFIX):
            return None

        token = auth_header.replace(JWTAuthentication.BEARER_PREFIX, '', 1)

        if not token:
            return None

        try:
            payload = jwt.decode(jwt=token, key=settings.JWT_AUTH['JWT_SECRET_KEY'], algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']])
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Error decoding token')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, token)

    @staticmethod
    def generate_jwt(user: User) -> str:
        """
        Generate a JWT token for the given user.

        @param user: The user for whom the JWT token is being generated.
        @return: A JWT token as a string.
        """
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
            'iat': datetime.utcnow()
        }
        token = jwt.encode(
            payload=payload, key=settings.JWT_AUTH['JWT_SECRET_KEY'], algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
        )
        return token

    @staticmethod
    def generate_refresh_token(user: User) -> RefreshToken:
        """
        Generate a refresh token for the given user.

        @param user: The user for whom the refresh token is being generated.
        @return: A RefreshToken object.
        """
        refresh_token = RefreshToken.objects.create(
            user=user,
            token=secrets.token_urlsafe(64),
            expires_at=timezone.now() + settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
        )
        return refresh_token

    @staticmethod
    def refresh_access_token(refresh_token_str: str) -> str:
        """
        Refresh the access token using the provided refresh token.

        @param refresh_token_str: The refresh token string.
        @return: A new JWT access token.
        @exception: Raises AuthenticationFailed if the refresh token is invalid or expired.
        """
        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_str)
            if refresh_token.is_expired():
                raise exceptions.AuthenticationFailed('Refresh token has expired')
            
            # Generate new access token
            access_token = JWTAuthentication.generate_jwt(refresh_token.user)
            return access_token
        except RefreshToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid refresh token')

    @staticmethod
    def revoke_refresh_token(refresh_token_str: str) -> None:
        """
        Revoke the refresh token by deleting it from the database.

        @param refresh_token_str: The refresh token string.
        """
        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_str)
            refresh_token.delete()
        except RefreshToken.DoesNotExist:
            pass  # If the token does not exist, it's already revoked

    @staticmethod
    def revoke_all_refresh_tokens(user: User) -> None:
        """
        Revoke all refresh tokens for the given user by deleting them from the database.

        @param user: The user for whom the refresh tokens are being revoked.
        """
        RefreshToken.objects.filter(user=user).delete()