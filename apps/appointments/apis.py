import json

from django.conf import settings
from requests import request


class CallAPI():
    base_url = 'https://api.sikkasoft.com/v4'
    office_id = None
    secret_key = None
    request_key = None
    refresh_key = None

    def __init__(self):
        if not self.office_id and not self.secret_key:
            self.get_authorized_practices()
            self.get_request_key()

    def call_api(self, method, url, base_headers={}, data={}):
        response = request(method, self.base_url+url,
                           headers=base_headers, data=data)
        if response.status_code == 400:
            pass
        return response

    def get_authorized_practices(self):
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
            practice = response.get('items', [None])[0]
            if practice:
                self.secret_key = practice.get('secret_key')
                self.office_id = practice.get('office_id')
        return response

    def get_request_key(self):
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
            method=method, url=url, base_headers=headers, data=payload)
        if response and response.status_code == 200:
            response = response.json()
            self.request_key = response.get('request_key')
            self.refresh_key = response.get('refresh_key')
        return response

    def get_appointments(self):
        url = '/appointments'
        method = 'GET'
        payload = {}
        headers = {
            'Request-Key': self.request_key
        }
        response = self.call_api(method=method, url=url,
                                 base_headers=headers, data=payload)
        return response
