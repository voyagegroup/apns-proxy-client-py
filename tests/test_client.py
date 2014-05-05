# -*- coding: utf-8 -*-

import time
import json

import mock
from nose.tools import ok_, eq_, raises

from apns_proxy_client import APNSProxyClient, COMMAND_SEND

TEST_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@raises(ValueError)
def test_invalid_application_id():
    APNSProxyClient('localhost', 9999, 10)


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


def test_serialize_with_content_available():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', content_available=True)

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_(True, body['aps']['content_available'])


def test_serialize_with_content_available_False():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', content_available=False)

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    ok_(not 'content_available' in body)


def test_serialize_silent_message():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, None, None, content_available=True)

    send_data = client.publisher.send.call_args[0][0]
    eq_(COMMAND_SEND, send_data[:1])
    eq_({
        'token': TEST_TOKEN,
        'appid': '10',
        'test': False,
        'aps': {
            'content_available': True
        }
        }, json.loads(send_data[1:]))


def test_serialize_with_custom_field():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, 'Hey Hey', custom={
        'APP_CUSTOM1': 200,
        'APP_CUSTOM2': {
            'foo': 'bar',
            'boo': False
        }
    })

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_({
        'APP_CUSTOM1': 200,
        'APP_CUSTOM2': {
            'foo': 'bar',
            'boo': False
        }
        }, body['aps']['custom'])


@raises(ValueError)
def test_serialize_with_invalid_custom_filed():
    client = APNSProxyClient('localhost', 9999, '10')
    client.send(TEST_TOKEN, 'Go Go', custom='Boooooo')


def test_serialize_with_json_alert():
    client = APNSProxyClient('localhost', 9999, '10')
    client.publisher.send = mock.Mock()
    client.send(TEST_TOKEN, {
        'body': 'JSON ALERT',
        'action_loc_key': None,
        'loc_key': None,
        'loc_args': ['one', 'two'],
        'launch_image': 'image1'
    })

    send_data = client.publisher.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_({
        'body': 'JSON ALERT',
        'action_loc_key': None,
        'loc_key': None,
        'loc_args': ['one', 'two'],
        'launch_image': 'image1'
        }, body['aps']['alert'])


@raises(ValueError)
def test_serialize_with_invalid_json_alert1():
    client = APNSProxyClient('localhost', 9999, '10')
    client.send(TEST_TOKEN, {
        'body': 'JSON ALERT',
        'action-loc-key': None,
        'loc-key': None,
        'loc-args': ['one', 'two'],
        'launch-image': 'image1'
    })


def test_get_feeedback():
    client = APNSProxyClient('localhost', 9999, '10')
    client.communicator.send = mock.Mock()
    client.communicator.recv = mock.Mock()
    client.communicator.recv.return_value = '{}'

    client.get_feedback()

    send_data = client.communicator.send.call_args[0][0]
    body = json.loads(send_data[1:])
    eq_({'appid': '10'}, body)
