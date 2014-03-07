# -*- coding: utf-8 -*-

from nose.tools import ok_


def test_import():
    from apns_proxy_client import APNSProxyClient
    ok_(APNSProxyClient)


def test_create_instance():
    from apns_proxy_client import APNSProxyClient
    client = APNSProxyClient('localhost', 9999, '10')
    ok_(client)
