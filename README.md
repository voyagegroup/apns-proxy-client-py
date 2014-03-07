# APNS-Proxy-Client-py

Client program of [APNsProxyServer](https://github.com/genesix/APNS-Proxy-Server)

## Installation

```
pip install -e git+git://github.com/genesix/APNS-Proxy-Client-py.git#egg=APNS-Proxy-Client
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

