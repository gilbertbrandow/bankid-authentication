import io
import hmac
import qrcode
import hashlib
import requests
import datetime
from authentication.jwt_authentication import JWTAuthentication
from authentication.models import User
from requests.models import Response
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from authentication.models import BankIDAuthentication
from typing import Dict, Union
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import BankIDAuthentication


class BankIDService():
    RFA: dict[int, str] = {
        1: _("Please start the BankID app."),
        2: _("The BankID app is not installed. Please contact your bank."),
        3: _("Action cancelled. Please try again."),
        4: _("An identification or signing for this personal number is already started. Please try again."),
        5: _("Internal error. Please try again."),
        6: _("Action cancelled."),
        8: _("The BankID app is not responding. Please check that it’s started and that you have internet access. If you don’t have a valid BankID you can get one from your bank. Try again."),
        9: _("Enter your security code in the BankID app and select Identify or Sign."),
        13: _("Trying to start your BankID app."),
        15: _("Searching for BankID, it may take a little while … If a few seconds have passed and still no BankID has been found, you probably don’t have a BankID which can be used for this identification/signing on this device. If you don't have a BankID you can get one from your bank."),
        16: _("The BankID you are trying to use is blocked or too old. Please use another BankID or get a new one from your bank."),
        17: _("Failed to scan the QR code. Start the BankID app and scan the QR code. Check that the BankID app is up to date. If you don't have the BankID app, you need to install it and get a BankID from your bank. Install the app from your app store or https://install.bankid.com"),
        18: _("Start the BankID app."),
        19: _("Would you like to identify yourself or sign with a BankID on this computer, or with a Mobile BankID?"),
        21: _("Identification or signing in progress."),
        22: _("Unknown error. Please try again."),
        23: _("Process your machine-readable travel document using the BankID app.")
    }

    HINT_CODE_TO_RFA: dict[str, int] = {
        'outstandingTransaction': 1,
        'noClient': 1,
        'cancelled': 3,
        'userCancel': 6,
        'expiredTransaction': 8,
        'userSign': 9,
        'started': 15,
        'certificateErr': 16,
        'startFailed': 17,
        'userMrtd': 23,
        'userCallConfirm': 23,
    }

    DEFAULT_HINT_CODES: dict[str, int] = {
        'pending': 21,
        'failed': 22,
        'success': 21,
    }

    def __init__(self) -> None:
        self.bankid_url = settings.BANKID['endpoint']
        self.cert = (settings.BANKID['cert_path'],
                     settings.BANKID['cert_key_path'])
        self.verify = settings.BANKID['ca_cert_path']

    def _request(self, path: str, payload: Dict[str, Union[str, bool, object]]) -> Response:
        return requests.post(
            f'{self.bankid_url}{path}',
            json=payload,
            cert=self.cert,
            verify=self.verify
        )

    def get_rfa_message(self, index: int) -> str:
        return self.RFA[index]

    def get_default_rfa_message(self, status: str) -> str:
        return self.get_rfa_message(self.DEFAULT_HINT_CODES[status])

    def initiate_authentication(self, end_user_ip: str) -> str:
        try:
            response: Response = self._request(path='/rp/v6.0/auth', payload={
                'endUserIp': end_user_ip,
                'returnRisk': True,
                'requirement': {
                    'risk': 'low'
                },
            })

            response.raise_for_status()
            response_data = response.json()

            auth = BankIDAuthentication.objects.create(
                order_ref=response_data['orderRef'],
                auto_start_token=response_data['autoStartToken'],
                qr_start_token=response_data['qrStartToken'],
                qr_start_secret=response_data['qrStartSecret']
            )

            cache.set(auth.order_ref, auth, timeout=30)

            return auth.order_ref
        except requests.RequestException as e:
            raise
        except Exception as e:
            raise

    def generate_qr_code_data(self, order_ref: str) -> str:
        try:
            auth: BankIDAuthentication = cache.get(order_ref)

            if not auth:
                auth = BankIDAuthentication.objects.get(order_ref=order_ref)
                cache.set(auth.order_ref, auth, timeout=300)

            if (datetime.datetime.now(datetime.timezone.utc) - auth.created_at).total_seconds() > 30:
                auth.delete()
                raise ValueError(
                    _("The BankID authentication session has expired."))

            qr_start_token = auth.qr_start_token
            qr_start_secret = auth.qr_start_secret

            current_time = int((datetime.datetime.now(
                datetime.timezone.utc) - auth.created_at).total_seconds())
            qr_auth_code = hmac.new(
                key=qr_start_secret.encode(),
                msg=str(current_time).encode(),
                digestmod=hashlib.sha256
            ).hexdigest()

            return f"bankid.{qr_start_token}.{current_time}.{qr_auth_code}"
        except ObjectDoesNotExist:
            raise ValueError(_("Invalid order reference."))
        except Exception as e:
            raise

    def generate_qr_code_image(self, qr_data: str) -> bytes:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
        
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="transparent").convert("RGBA")
        
        with io.BytesIO() as buffer:
            img.save(buffer, format="PNG")
            return buffer.getvalue()

    def poll_authentication_status(self, order_ref: str) -> Dict[str, Union[str, object]]:
        try:
            response: Response = self._request(
                path='/rp/v6.0/collect', payload={'orderRef': order_ref})

            response.raise_for_status()
            response_data = response.json()

            status: str = response_data.get('status')
            hint_code: str = response_data.get('hintCode', '')

            if status == 'complete':
                completion_data = response_data.get('completionData', {})
                personal_number = completion_data.get(
                    'user', {}).get('personalNumber')
                if personal_number:
                    try:
                        user = User.objects.get(
                            personal_number=personal_number)
                        BankIDAuthentication.objects.get(
                            order_ref=order_ref).delete()

                        return {
                            'access_token': JWTAuthentication.generate_jwt(user),
                            'refresh_token': JWTAuthentication.generate_refresh_token(user).token
                        }
                    except User.DoesNotExist:
                        raise ValueError(
                            _('It does not seem you have an account associated with your personal number.'))
                else:
                    raise ValueError(
                        'Personal number not found in completion data')
            elif status == 'failed':
                BankIDAuthentication.objects.get(order_ref=order_ref).delete()
                raise ValueError(self.RFA[self.HINT_CODE_TO_RFA.get(hint_code, self.DEFAULT_HINT_CODES[status])])

            return {
                'status': status,
                'message': self.RFA[self.HINT_CODE_TO_RFA.get(
                    hint_code, self.DEFAULT_HINT_CODES[status])]
            }
        except requests.RequestException as e:
            raise
        except Exception as e:
            raise

    def cancel_authentication(self, order_ref: str) -> None:
        try:
            auth = BankIDAuthentication.objects.get(
                order_ref=order_ref)

            response: Response = self._request(path='/rp/v6.0/cancel', payload={
                'orderRef': order_ref
            })

            response.raise_for_status()

            auth.delete()
            cache.delete(order_ref)

            return None
        except ObjectDoesNotExist:
            raise ValueError(
                _("Invalid order reference or the authentication is not active."))
        except requests.RequestException as e:
            raise
        except Exception as e:
            raise
