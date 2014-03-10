# APNS Proxy Python Client

Client program of [APNs Proxy Server](https://github.com/genesix/apns-proxy-server)

## Installation

```
pip install -e git+git://github.com/genesix/apns-proxy-client-py.git#egg=apns-proxy-client
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

client = APNSProxyClient(host="localhost", port=5556, application_id="01")
with client:
    message = "This is notification message!!"
    expiry = int(time.time() + 60 * 60)  # 1 hour 
    for token in many_tokens:
        client.send(token, message, badge=1, sound='default', expiry=expiry)
```

OR use ```connect()``` and ```close()``` instead of ```with```

```python
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="01")
client.connect()

message = "This is notification message!!"
for token in many_tokens:
    client.send(token, message)

client.close()
```

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

