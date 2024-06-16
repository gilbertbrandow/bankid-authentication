import requests
from requests.models import Response
from django.core.cache import cache
from django.conf import settings
from authentication.models import BankIDAuthentication
from typing import Dict, Union



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
