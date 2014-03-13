# APNS Proxy Python Client

Client program of [APNs Proxy Server](https://github.com/genesix/apns-proxy-server)

[![Build Status](https://travis-ci.org/genesix/apns-proxy-client-py.png?branch=master)](https://travis-ci.org/genesix/apns-proxy-client-py)

## Installation

```
pip install git+git://github.com/genesix/apns-proxy-client-py.git
```

or

```
git clone git@github.com:genesix/apns-proxy-client-py.git
python apns-proxy-client/setup.py install
```

## How to Use

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
with client:
    for token in many_tokens:
        client.send(token, 'Hello', badge=1)
```

OR use ```connect()``` and ```close()``` instead of ```with```

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
client.connect()
for token in many_tokens:
    client.send(token, 'Hello')
client.close()
```

Set host and port for your server running on. application_id is specified in settings.py on apns-proxy-server.

### send() method synopsis

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
with client:
    # Simple
    client.send(token, 'Hello')

    # Custom sound (default = 'default')
    client.send(token, 'Alert with custom sound', sound='custom')

    # Silent
    client.send(token, 'I am silent', sound=None)

    # Badge
    client.send(token, 'Alert with badge', badge=2)

    # Set expiry (default = 1hour)
    four_hours_later = int(time.time()) + (60 * 60 * 4)
    client.send(token, 'I am long life', expiry=four_hours_later)

    # Set priority (default = 10)
    client.send(token, 'I am low priority', priority=5)

    # For background fetch
    client.send(token, None, sound=None, content_available=True)

    # With custom field.
    client.send(token, 'With custom field', custom={
        'foo': True,
        'bar': [200, 300],
        'boo': "Hello"
    })
    # Finally following payload will send to APNs
    # {
    #     "aps": {
    #         "alert": "With custom field",
    #         "sound": "default",
    #      },
    #      "foo": True,
    #      "bar": [200, 300]
    #}

    # Use JSON Payload
    client.send(token, {
        'body': 'This is JSON alert',
        'action_loc_key': None,
        'loc_key': 'loc key',
        'loc_args': ['one', 'two'],
        'launch_image': 'aa.png'
    })

    # All
    client.send(token, 'Many opts', sound='foo', badge=2, content_available=True,
                custom={"bar": "boo"}, expiry=four_hour_later, priority=5)

    # Test. APNsProxyServer don't send to APNs
    client.send(token, 'This message never send to device', test=True)
```

Parameters of send method

Name | Type | Required | Default Value
--- | --- | --- | ---
token | string | yes | None
alert | string, unicode or dict | yes | None
sound | string | no | 'default'
badge | number | no | None
content_available | bool | no | False
custom | dict | no | None
expiry | date | no | 1 hour
priority | number | no | 10

## For contributor

Make file provides some useful commands.

--- | ---
make setup | Setup work directory
make lint | Code check using flake8
make test | Run tests

## License

BSD

