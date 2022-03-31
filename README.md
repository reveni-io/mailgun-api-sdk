# Mailgun API SDK

[Mailgun API SDK](https://github.com/reveni-io/mailgun-api-sdk) integrates the Mailgun API, specifically the [Templates API](https://documentation.mailgun.com/en/latest/api-templates.html#templates).

## Installation

    $ pip install git+https://github.com/reveni-io/mailgun-api-sdk.git

## Usage

.. code:: python

    >>> import mailgun_api_sdk
    >>> client = mailgun_api_sdk.Client('api_key', 'domain')
    >>> r = client.get_templates()
    >>> r.json()
    [
      ...
    ]
    >>> r.status_code
    200

## Documentation

Mailgun API documentation is availabe at https://documentation.mailgun.com/en/latest/index.html

## License

This package is licensed under [BSD 3-Clause "New" or "Revised" License](https://github.com/reveni-io/mailgun-api-sdk/blob/main/LICENSE).
