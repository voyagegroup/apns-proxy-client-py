import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = [
    'pyzmq',
    'simplejson'
    ]

setup(
    name="APNsProxyClient",
    version="0.1.0",
    author='Takashi Nishibayashi',
    author_email="takashi_nishibayashi@voyagegroup.com",
    description=("Client module for APNs Proxy"),
    license="BSD",
    platforms='any',
    keywords="apns",
    install_requires=requires,
    url='https://github.com/voyagegroup/apns-proxy-client-py',
    packages=['apns_proxy_client', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
