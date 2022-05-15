import json

from django.conf import settings
from requests import request

ERROR_CODES = {
    'invalid_request_key': 'API1025',
    'missing_request_key': 'API1004'
}


class CallAPI():
    base_url = 'https://api.sikkasoft.com/v4'
    office_id = None
    secret_key = None
    request_key = None
    refresh_key = None

    def __init__(self):
        if not self.office_id and not self.secret_key:
            self.get_authorized_practices()

    def call_api(self, method, url, base_headers={}, data={}, loop=False):
        headers = {
            "User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00",
            **base_headers
        }
        proxies = None
        u = self.base_url + url
        response = request(method, u, proxies=proxies,
                           headers=headers, data=data)
        if response.status_code == 400 and not loop:
            res_json = response.json()
            error_code = res_json.get('error_code')
            if error_code == ERROR_CODES.get('invalid_request_key'):
                self.get_request_key(loop=True)
                return error_code
        return response

    def get_authorized_practices(self, office_id=None):
        method = 'GET'
        url = '/authorized_practices'
        headers = {
            'app-id': settings.SIKKA_APP_ID,
            'app-key': settings.SIKKA_APP_SECRET_KEY
        }
        payload = {}
        response = self.call_api(method=method, url=url,
                                 base_headers=headers, data=payload)
        if response and response.status_code == 200:
            response = response.json()
            practices = response.get('items', [None])
            practice = practices[0]

            if office_id:
                practice = next(
                    filter(lambda practice: practice['office_id'] == office_id, practices), practice)

            if practice:
                self.secret_key = practice.get('secret_key')
                self.office_id = practice.get('office_id')

                if self.secret_key and self.office_id:
                    self.get_request_key()
        return response

    def delete_request_key(self):
        url = '/request_key'
        method = 'DELETE'
        headers = {
            'Content-Type': 'application/json',
            'Request-Key': self.request_key
        }
        response = self.call_api(method=method, url=url, base_headers=headers)
        return response

    def get_request_key(self, loop=False):
        url = '/request_key'
        method = 'POST'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "grant_type": "request_key",
            "office_id": self.office_id,
            "secret_key": self.secret_key,
            "app_id": settings.SIKKA_APP_ID,
            "app_key": settings.SIKKA_APP_SECRET_KEY,
        })
        response = self.call_api(
            method=method, url=url, base_headers=headers, data=payload, loop=loop)
        if response and response.status_code == 200:
            response_json = response.json()
            self.request_key = response_json.get('request_key')
            self.refresh_key = response_json.get('refresh_key')
        return response

    def get_appointments(self, loop=False):
        url = '/appointments'
        method = 'GET'
        payload = {}
        headers = {
            'Request-Key': self.request_key
        }
        response = self.call_api(method=method, url=url,
                                 base_headers=headers, data=payload)
        if response == ERROR_CODES.get('invalid_request_key') and not loop:
            return self.get_appointments(loop=True)
        return response.json()


apis = CallAPI()
