# APNs Proxy Python Client

Client program of [APNs Proxy Server](https://github.com/voyagegroup/apns-proxy-server)

[![Build Status](https://travis-ci.org/voyagegroup/apns-proxy-client-py.png?branch=master)](https://travis-ci.org/voyagegroup/apns-proxy-client-py)

## Installation

```
pip install git+git://github.com/voyagegroup/apns-proxy-client-py.git@v0.1
```

or

```
git clone git@github.com:voyagegroup/apns-proxy-client-py.git
python apns-proxy-client/setup.py install
```

## How to Use

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
with client:
    # send "Hello" alerts to many tokens
    for token in many_tokens:
        client.send(token, 'Hello', badge=1)

    # get disabled device tokens from feedback service
    feedback = client.get_feedback()
```

OR use ```connect()``` and ```close()``` instead of ```with```

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
client.connect()
# send "Hello" alerts to many tokens
for token in many_tokens:
    client.send(token, 'Hello')

# get disabled device tokens from feedback service
feedback = client.get_feedback()
client.close()
```

Set host and port for your server running on. application_id is specified in settings.py on apns-proxy-server.

### send() method synopsis

```python
token = "YOUR_VALID_DEVICE_TOKEN"

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
with client:
    # Simple
    client.send(token, 'Hello')

    # Custom sound (default = 'default')
    client.send(token, 'Alert with custom sound', sound='custom')

    # Message without sound
    client.send(token, 'I am silent', sound=None)

    # Badge
    client.send(token, 'Alert with badge', badge=2)

    # Change badge silently
    client.send(token, None, sound=None, badge=9999)

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
    #      "bar": [200, 300],
    #      "boo": "Hello"
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

Name | Type | Required | Default Value (Set on server)
--- | --- | --- | ---
token | string | yes | -
alert | string, unicode or dict | yes | -
sound | string | no | 'default'
badge | number | no | None
content_available | bool | no | False
custom | dict | no | None
expiry | date | no | 1 hour
priority | number | no | 10
test | bool | no | False

### get_feedback() method synopsis

This client library provides a way to get disabled device tokens from APNs feedback service; just call `get_feedback()` without any parameters.

`get_feedback()` returns the dict that is a pair of "device_token" and "timestamp".

Name | Type | Description
--- | --- | ---
device_token | string | The device token string which cannot be received push notifications
timestamp | float | The seconds since 00:00 on January 1, 1970 UTC. This value means a timestamp which APNs judged the device token should be disabled.

```python
client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
with client:
    feedback = client.get_feedback()
    # a value of feedback likes the following dict:
    #   {
    #       "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef": 1399442843.0,  # device_token : unix timestamp
    #       "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789": 1399442892.0,
    #   }
```

## For contributor

Makefile provides some useful commands.

Command | Description
--- | ---
make setup | Setup work directory
make lint | Code check using flake8
make test | Run tests

## License

BSD

