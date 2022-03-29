#!/usr/bin/env python

__version__ = '0.0.1'

import json
import requests


class MailgunError(Exception):

    """
    Exception Handling
    """

    def __init__(self, response=None):
        self.response = response
        self.code = response.status_code

        try:
            error = json.loads(response.content)
        except ValueError:
            self.message = "Unknown error"
        else:
            self.message = error.get("message", "Unknown error")


class Client(object):

    """
    A client for Mailgun API.
    See https://documentation.mailgun.com/en/latest/api_reference.html
    for complete API documentation.
    """

    user_agent = 'MailgunSDK/api-rest-sdk:' + __version__

    def __init__(self, api_key, domain, version=3, base_url=None):

        self.api_key = api_key
        self.version = version
        self.base_url = base_url or "https://api.eu.mailgun.net"
        self.domain = domain

    def request(self, url, method, **kwargs):
        response = requests.request(
            method, url,
            auth=("api", self.api_key),
            **kwargs)

        if not (200 <= response.status_code < 300):
            raise MailgunError(response)

        return response

    def _endpoint(self, endpoint, method, **kwargs):
        return self.request(
            f"{self.base_url}/v{self.version}/{self.domain}/{endpoint}", method, **kwargs)

    def get(self, endpoint, params=None, **kwargs):
        kwargs.update(params or {})
        return self._endpoint(endpoint, 'GET', params=kwargs)

    def post(self, endpoint, data=None):
        return self._endpoint(endpoint, 'POST', data=data)

    def put(self, endpoint, data=None):
        return self._endpoint(endpoint, 'PUT', data=data)

    def delete(self, endpoint, **kwargs):
        return self._endpoint(endpoint, 'DELETE', **kwargs)

    # Templates

    def list_templates(self, params=None, **kwargs):
        return self.get("templates", params=params, **kwargs)

    def get_template(self, name):
        return self.get(f"templates/{name}")

    def create_template(self, name, description, template=None, tag=None, engine=None, comment=None):
        data = {
            "name": name,
            "description": description
        }
        if template:
            data.update({"template": template})
        if tag:
            data.update({"tag": tag})
        if engine:
            data.update({"engine": engine})
        if comment:
            data.update({"comment": comment})

        return self.post("templates", data=data)

    def update_template(self, name, description):
        data = {
            "description": description
        }
        return self.put(f"templates/{name}", data=data)

    def delete_template(self, name):
        return self.get(f"templates/{name}", **kwargs)

    # Template versions

    def create_version(self, name, template, tag, comment=None, active=None):
        data = {
            "template": template,
            "tag": tag
        }
        if comment:
            data.update({"comment": comment})
        if active:
            data.update({"active": active})

        return self.post(f"templates/{name}/versions", data=data)
