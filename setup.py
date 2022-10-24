#!/usr/bin/env python

from distutils.core import setup

setup(
    name='mailgun-api-sdk',
    version='0.0.5',
    description='Python Interface to the Mailgun API',
    author='reveni',
    author_email='dev@reveni.io',
    packages=['mailgun_api_sdk'],
    url='https://github.com/reveni-io/mailgun-api-sdk',
    license='BSD 3-clause "New" or "Revised License"',
    install_requires=['requests>=2.27.1'],
    dependency_links=[
        'https://github.com/kennethreitz/requests',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='python mailgun rest api sdk',
    python_requires='>=3',
)
