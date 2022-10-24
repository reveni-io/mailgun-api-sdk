#!/usr/bin/env python

__version__ = '0.0.3'

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

    def _request(self, url, method, **kwargs):
        response = requests.request(
            method, url,
            auth=("api", self.api_key),
            **kwargs)

        if not (200 <= response.status_code < 300):
            raise MailgunError(response)

        return response

    def _endpoint(self, endpoint, method, **kwargs):
        return self._request(
            f"{self.base_url}/v{self.version}/{self.domain}/{endpoint}", method, **kwargs)

    def _get(self, endpoint, params=None, **kwargs):
        kwargs.update(params or {})
        return self._endpoint(endpoint, 'GET', params=kwargs)

    def _post(self, endpoint, data=None):
        return self._endpoint(endpoint, 'POST', data=data)

    def _put(self, endpoint, data=None):
        return self._endpoint(endpoint, 'PUT', data=data)

    def _delete(self, endpoint, **kwargs):
        return self._endpoint(endpoint, 'DELETE', **kwargs)

    # Templates

    def list_templates(self, params=None, **kwargs):
        return self._get("templates", params=params, **kwargs)

    def get_template(self, name):
        return self._get(f"templates/{name}")

    def create_template(self, name, description, content=None, tag=None, engine=None, comment=None):
        data = {
            "name": name,
            "description": description
        }
        if content:
            data.update({"template": content})
        if tag:
            data.update({"tag": tag})
        if engine:
            data.update({"engine": engine})
        if comment:
            data.update({"comment": comment})

        return self._post("templates", data=data)

    def update_template(self, name, description):
        data = {
            "description": description
        }
        return self._put(f"templates/{name}", data=data)

    def delete_template(self, name):
        return self._delete(f"templates/{name}")

    def delete_all_templates(self):
        return self._delete("templates")

    # Template versions

    def list_template_versions(self, name, params=None, **kwargs):
        return self._get(f"templates/{name}/versions", params=params, **kwargs)

    def get_template_version(self, name, tag):
        return self._get(f"templates/{name}/versions/{tag}")

    def create_template_version(self, name, content, tag, comment=None, active=None):
        data = {
            "template": content,
            "tag": tag
        }
        if comment:
            data.update({"comment": comment})
        if active:
            data.update({"active": active})

        return self._post(f"templates/{name}/versions", data=data)

    def update_template_version(self, name, tag, content=None, comment=None, active=None):
        data = {}
        if content:
            data.update({"template": content})
        if comment:
            data.update({"comment": comment})
        if active:
            data.update({"active": active})

        return self._put(f"templates/{name}/versions/{tag}", data=data)

    def delete_template_version(self, name, tag):
        return self._delete(f"templates/{name}/versions/{tag}")

    def send_email(self, to, subject, template, variables):
        return self._post("messages", {
            "from": "Mailgun Sandbox <postmaster@mail.reveni.dev>",
            "to": to,
            "subject": subject,
            "template": template,
            "t:variables": json.dumps(variables)
        })