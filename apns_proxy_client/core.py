# -*- coding: utf-8 -*-
"""
APNS Proxy Serverのクライアント
"""

import time

import zmq
import simplejson as json


READ_TIMEOUT = 1500  # msec
FLUSH_TIMEOUT = 5000  # msec

COMMAND_ASK_ADDRESS = b'\1'
COMMAND_SEND = b'\2'

DEVICE_TOKEN_LENGTH = 64


class APNSProxyClient(object):

    def __init__(self, host, port, application_id):
        """
        ZMQコンテキストとソケットの初期化
        """
        if host is None or not isinstance(host, str):
            raise ValueError("host must be string")
        if port is None or not isinstance(port, int):
            raise ValueError("host must be int type")
        self.host = host
        self.port = port

        self.context = zmq.Context()
        self.context.setsockopt(zmq.LINGER, FLUSH_TIMEOUT)

        self.communicator = self.context.socket(zmq.REQ)
        self.publisher = self.context.socket(zmq.PUSH)
        self.connected = False

        if not isinstance(application_id, str) or len(application_id) != 2:
            raise ValueError("application_id must be 2 length string")
        self.application_id = application_id

    def __enter__(self):
        self.connect()

    def connect(self):
        """リモートサーバーへ接続"""
        if self.connected is False:
            self.communicator.connect(self.build_address(self.port))
            push_port = self.get_push_port()
            self.publisher.connect(self.build_address(push_port))
            self.connected = True

    def build_address(self, port):
        return "tcp://%s:%s" % (self.host, port)

    def get_push_port(self):
        """
        PUSH-PULL接続用のポートを取得する
        """
        self.communicator.send(COMMAND_ASK_ADDRESS)
        poller = zmq.Poller()
        poller.register(self.communicator, zmq.POLLIN)
        if poller.poll(READ_TIMEOUT):
            return self.communicator.recv()
        else:
            self.close()
            raise IOError("Cannot connect to APNs Proxy Server. Timeout!!")

    def send(self, token, alert, sound='default', badge=None, expiry=None, test=False):
        """
        デバイストークンの送信
        """
        self._check_token(token)
        self.publisher.send(self._serialize(
            COMMAND_SEND, token, alert, sound, badge, expiry, test
        ))

    @staticmethod
    def _check_token(token):
        if len(token) != DEVICE_TOKEN_LENGTH:
            raise ValueError('Invalid token length %s' % token)

    def _serialize(self, command, token, alert, sound, badge, expiry, test):
        """
        送信データのフォーマット
        """
        aps = {
            'alert': alert,
            'sound': sound
        }
        if badge is not None:
            aps['badge'] = badge

        data = {
            'appid': self.application_id,
            'token': token,
            'aps': aps,
            'test': test
        }
        if expiry is not None:
            data['expiry'] = expiry
        return command + json.dumps(data, ensure_ascii=True)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._close()
            return False
        self.close()

    def close(self):
        start_time = time.time()
        self._close()
        end_time = time.time()
        if (end_time - start_time) > (FLUSH_TIMEOUT - 20)/1000.0:
            raise IOError('Timeout close operation. Some messages may not reached to server.')
        return True

    def _close(self):
        self.publisher.close()
        self.communicator.close()
        self.context.term()
