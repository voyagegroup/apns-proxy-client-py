# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_, raises
import json

from apns_proxy_client import APNSProxyClient, COMMAND_SEND


@raises(ValueError)
def test_invalid_application_id():
    client = APNSProxyClient('localhost', 9999, '100')


@raises(ValueError)
def test_invalid_port():
    client = APNSProxyClient('localhost', 'abc', '10')


@raises(ValueError)
def test_invalid_host():
    client = APNSProxyClient(None, 8000, '10')


def test_serialize():
    client = APNSProxyClient('localhost', 9999, '10')

    token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    data = client._serialize(COMMAND_SEND, token, 'Hey Hey', 'default', 1, None, False)

    eq_(COMMAND_SEND, data[:1])

    native = json.loads(data[1:])
    eq_(native['token'], token)
    eq_(native['appid'], '10')
    eq_(native['test'], False)
    eq_(native['aps']['alert'], 'Hey Hey')
    eq_(native['aps']['sound'], 'default')
    eq_(native['aps']['badge'], 1)
    eq_(native['aps']['expiry'], None)
    eq_(len(native.keys()), 4)


def test_serialize_test_is_true():
    client = APNSProxyClient('localhost', 9999, '10')

    token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    data = client._serialize(COMMAND_SEND, token, 'Hey Hey', 'default', 1, None, True)

    eq_(COMMAND_SEND, data[:1])

    native = json.loads(data[1:])
    eq_(native['token'], token)
    eq_(native['appid'], '10')
    eq_(native['test'], True)
    eq_(native['aps']['alert'], 'Hey Hey')
    eq_(native['aps']['sound'], 'default')
    eq_(native['aps']['badge'], 1)
    eq_(native['aps']['expiry'], None)
    eq_(len(native.keys()), 4)


def test_serialize_test_is_true():
    client = APNSProxyClient('localhost', 9999, '10')

    token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    data = client._serialize(COMMAND_SEND, token, u'メッセージ', 'default', 1, None, True)

    eq_(COMMAND_SEND, data[:1])

    native = json.loads(data[1:])
    eq_(native['token'], token)
    eq_(native['appid'], '10')
    eq_(native['test'], True)
    eq_(native['aps']['alert'], u'メッセージ')
    eq_(native['aps']['sound'], 'default')
    eq_(native['aps']['badge'], 1)
    eq_(native['aps']['expiry'], None)
    eq_(len(native.keys()), 4)


@raises(ValueError)
def test_token_length_check():
    token = "xxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    client = APNSProxyClient('localhost', 9999, '10')
    client.send(token, 'Booooom')
