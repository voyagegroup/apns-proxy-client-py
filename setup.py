import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = [
    'zmq',
    'simplejson'
    ]

setup(
    name="APNSProxyServerClient",
    version="0.0.1",
    author='Takashi Nishibayashi',
    author_email="takashi_nishibayashi@voyagegroup.com",
    description=("Client module for APNS Proxy"),
    license="MIT",
    platforms='any',
    keywords="apns",
    install_requires=requires,
    url='https://github.com/genesix/APNSProxyClient-py',
    packages=['apns_proxy_client', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
