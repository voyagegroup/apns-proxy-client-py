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

## Example

```python
import time
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
with client:
    message = "This is notification message!!"
    expiry = int(time.time() + 60 * 60)  # 1 hour 
    for token in many_tokens:
        client.send(token, message, badge=1, sound='default', expiry=expiry)
```

OR use ```connect()``` and ```close()``` instead of ```with```

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="myapp")
client.connect()

message = "This is notification message!!"
for token in many_tokens:
    client.send(token, message)

client.close()
```

Set host and port for your server running on. application_id is specified in settings.py on apns-proxy-server.

## For contributor

Setup work directory
```
make setup
```

Code check
```
make lint
```

Test
```
make test
```

