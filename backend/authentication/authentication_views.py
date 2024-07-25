import requests
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User
from .jwt_authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from authentication.services.bankid_service import BankIDService
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.translation import activate


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request: Request) -> Response:
    refresh_token_str = request.data.get('refresh_token')
    try:
        new_access_token = JWTAuthentication.refresh_access_token(
            refresh_token_str)
        return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)
    except exceptions.AuthenticationFailed as e:
        return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_password_login(request: Request) -> Response:
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.authenticate(email=email, password=password)

    if user is None:
        return Response({'detail': _('Invalid credentials')}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'access_token': JWTAuthentication.generate_jwt(user),
        'refresh_token': JWTAuthentication.generate_refresh_token(user).token
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def bankid_initiate_authentication(request: Request) -> Response:
    bankid_service = BankIDService()
    try:
        order_ref = bankid_service.initiate_authentication(
            end_user_ip=request.META.get('REMOTE_ADDR'))
        return Response({'orderRef': order_ref}, status=status.HTTP_200_OK)
    except requests.RequestException as e:
        return Response({'detail':  f"Failed to initiate BankID authentication: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def generate_qr_code(request: Request, order_ref: str) -> HttpResponse:
    bankid_service = BankIDService()
    try:
        qr_data = bankid_service.generate_qr_code_data(order_ref=order_ref)
        qr_image = bankid_service.generate_qr_code_image(qr_data=qr_data)
        return HttpResponse(qr_image, content_type="image/png")
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'detail': 'Authentication not found or inactive.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def poll_authentication_status(request: Request, order_ref: str) -> Response:
    bankid_service = BankIDService()
    try:
        auth = bankid_service.poll_authentication_status(order_ref)
        return Response(auth, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except requests.RequestException as e:
        error_message = f"Failed to poll BankID authentication status: {str(e)}"
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def cancel_authentication(request: Request, order_ref: str) -> Response:
    bankid_service = BankIDService()
    try:
        bankid_service.cancel_authentication(order_ref=order_ref)
        return Response({'success': 'BankID authentication cancelled.'}, status=status.HTTP_204_NO_CONTENT)
    except requests.RequestException as e:
        error_message = f"Failed to poll BankID authentication status: {str(e)}"
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def set_language(request: Request) -> Response:
    lang_code = request.data.get('language', settings.LANGUAGE_CODE)
    
    if lang_code and lang_code not in dict(settings.LANGUAGES).keys():
        return Response({'detail': 'Invalid language code'}, status=400)
    
    activate(lang_code)
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    request.session.save()
    return Response(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    user = request.user
    
    JWTAuthentication.revoke_all_refresh_tokens(user)
    request.session.flush()

    return Response({'detail': _('Successfully logged out.')}, status=status.HTTP_200_OK)
