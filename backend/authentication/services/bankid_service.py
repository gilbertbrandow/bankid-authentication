import io
import hmac
import time
import qrcode
import hashlib
import requests
import datetime
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
        13: _("Trying to start your BankID app."),
        15: _("Searching for BankID, it may take a little while … If a few seconds have passed and still no BankID has been found, you probably don’t have a BankID which can be used for this identification/signing on this device. If you don't have a BankID you can get one from your bank."),
        19: _("Would you like to identify yourself or sign with a BankID on this computer, or with a Mobile BankID?"),
        21: _("An unknown error occurred. Please try again."),
    }

    HINT_CODE_TO_RFA: dict[str, int] = {
        'outstandingTransaction': 1,
        'noClient': 1,
        'started': 15,
        'userSign': 9,
        'userMrtd': 23,
        'userCallConfirm': 23,
        'unknown': 21
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
                qr_start_secret=response_data['qrStartSecret'],
                is_active=True
            )
            return auth.order_ref
        except requests.RequestException as e:
            raise
        except Exception as e:
            raise

    def generate_qr_code_data(self, order_ref: str) -> str:
        try:
            auth = BankIDAuthentication.objects.get(
                order_ref=order_ref, is_active=True)

            if (datetime.datetime.now(datetime.timezone.utc) - auth.created_at).total_seconds() > 30:
                auth.is_active = False
                auth.save()
                raise ValueError(
                    "The BankID authentication session has expired.")

            qr_start_token = auth.qr_start_token
            qr_start_secret = auth.qr_start_secret

            current_time = int(time.time() // 1)
            qr_auth_code = hmac.new(
                key=qr_start_secret.encode(),
                msg=str(current_time).encode(),
                digestmod=hashlib.sha256
            ).hexdigest()

            qr_data = f"{qr_start_token}.{current_time}.{qr_auth_code}"
            return qr_data
        except ObjectDoesNotExist:
            raise ValueError(
                "Invalid order reference or the authentication is not active.")
        except Exception as e:
            raise

    def generate_qr_code_image(self, qr_data: str) -> bytes:
        qr_img = qrcode.make(qr_data)
        with io.BytesIO() as buffer:
            qr_img.save(buffer)
            return buffer.getvalue()

    def poll_authentication_status(self, order_ref: str) -> Dict[str, Union[str, bool]]:
        try:
            response: Response = self._request(path='/rp/v6.0/collect', payload={
                'orderRef': order_ref
            })

            response.raise_for_status()
            response_data = response.json()

            status: str = response_data.get('status')
            hint_code: str = response_data.get('hintCode')
            message: str = self.RFA[self.HINT_CODE_TO_RFA.get(hint_code, 21)]
            
            if status == 'complete' or status == 'failed':
                BankIDAuthentication.objects.filter(order_ref=order_ref).update(is_active=False)

            return {
                'status': status,
                'message': message
            }
        except requests.RequestException as e:
            raise
        except Exception as e:
            raise

    def cancel_authentication(self, order_ref: str) -> None:
        try:
            response: Response = self._request(path='/rp/v6.0/cancel', payload={
                'orderRef': order_ref
            })
            response.raise_for_status()
            return None
        except requests.RequestException as e:
            raise
        except Exception as e:
            raise
