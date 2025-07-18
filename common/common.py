import random
import string
import requests

from django.conf import settings


key = settings.PAYSTACK_PUBLIC_KEY


def ref():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f'/transaction/verify/{ref}'

        headers = {
            'Authorization': f'Bearer {self.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        url = self.base_url + path

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']

        response_data = response.json()
        return response_data['status'], response_data['message']