import jwt
from datetime import datetime
from django.conf import settings
from rest_framework.request import Request
from rest_framework import authentication, exceptions
from .models import User

class CustomJWTAuthentication(authentication.BaseAuthentication):
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

        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
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
    def authenticate_header(request: Request) -> str:
        """
        Return the authentication header.

        @param request: The HTTP request object.
        @return: The authentication header string.
        """
        return 'Bearer'

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
