import io
import hmac
import time
import qrcode
import hashlib
import requests
import datetime
from requests.models import Response
from django.core.cache import cache
from django.conf import settings
from authentication.models import BankIDAuthentication
from typing import Dict, Union
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import BankIDAuthentication



class BankIDService():
    def __init__(self) -> None:
        self.bankid_url = settings.BANKID['endpoint']
        self.cert = (settings.BANKID['cert_path'], settings.BANKID['cert_key_path'])
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
            auth = BankIDAuthentication.objects.get(order_ref=order_ref, is_active=True)
            
            if (datetime.datetime.now(datetime.timezone.utc) - auth.created_at).total_seconds() > 30:
                auth.is_active = False
                auth.save()
                raise ValueError("The BankID authentication session has expired.")
            
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
            raise ValueError("Invalid order reference or the authentication is not active.")
        except Exception as e:
            raise

    def generate_qr_code_image(self, qr_data: str) -> bytes:
        qr_img = qrcode.make(qr_data)
        with io.BytesIO() as buffer:
            qr_img.save(buffer)
            return buffer.getvalue()