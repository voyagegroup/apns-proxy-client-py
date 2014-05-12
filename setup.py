import os
from setuptools import setup

version = '0.1.0'
name = 'apns-proxy-client'
short_description = 'Client library for APNs Proxy Server.'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = [
    'pyzmq',
    'simplejson'
    ]

setup(
    name=name,
    version=version,
    author='Takashi Nishibayashi',
    author_email="takashi_nishibayashi@voyagegroup.com",
    description=short_description,
    long_description=read('README.rst'),
    license="BSD",
    platforms='any',
    keywords="apns",
    install_requires=requires,
    url='https://github.com/voyagegroup/apns-proxy-client-py',
    packages=['apns_proxy_client', 'tests'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
