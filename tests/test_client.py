# -*- coding: utf-8 -*-

import time
import json

import mock
from nose.tools import ok_, eq_, raises

from apns_proxy_client import APNSProxyClient, COMMAND_SEND

TEST_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@raises(ValueError)
def test_invalid_application_id():
    APNSProxyClient('localhost', 9999, 'my_app')


@raises(ValueError)
def test_invalid_port():
    APNSProxyClient('localhost', 'abc', 'my_app')


@raises(ValueError)
def test_invalid_host():
    APNSProxyClient(None, 8000, 'my_app')


def test_send_method_called():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey')
    ok_(client.publisher.send.called)


@raises(ValueError)
def test_invalid_token():
    client = APNSProxyClient('localhost', 9999, '10')
    client.send('Invalid Token', 'Hey Hey')


def test_serialize_message_only():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey')

    send_data = client.publisher.send.call_args[0][0]
    eq_(COMMAND_SEND, send_data[:1])
    eq_({
        'token': TEST_TOKEN,
        'appid': '10',
        'test': False,
        'aps': {
            'alert': 'Hey Hey',
            'sound': 'default'
        }
        }, json.loads(send_data[1:]))


def test_serialize_with_sound():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', sound='xxxx')

    send_data = client.publisher.send.call_args[0][0]
    eq_(COMMAND_SEND, send_data[:1])
    eq_({
        'token': TEST_TOKEN,
        'appid': '10',
        'test': False,
        'aps': {
            'alert': 'Hey Hey',
            'sound': 'xxxx'
        }
        }, json.loads(send_data[1:]))


def test_serialize_with_expiry():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    one_hour = int(time.time()) + (60 * 60)
    client.send(TEST_TOKEN, 'Hey Hey', expiry=one_hour)

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_(one_hour, body['expiry'])


def test_serialize_with_test():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', badge=123, test=True)

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_(True, body['test'])


def test_serialize_with_badge():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', badge=123)

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_(123, body['aps']['badge'])


def test_serialize_with_priority():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', priority=5)

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_(5, body['priority'])
