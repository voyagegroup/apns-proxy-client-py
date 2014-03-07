# APNS-Proxy-Client-py

Client program of [APNsProxyServer](https://github.com/genesix/APNS-Proxy-Server)

## Installation

```
pip install -e git+git://github.com/genesix/APNS-Proxy-Client-py.git#egg=APNS-Proxy-Client
```

## Example

```
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="01")
with client:
    message = "This is notification message!!"
    for token in many_tokens:
        client.send(token, message, badge=1)
```

OR

```
from apns_proxy_client import APNSProxyClient

client = APNSProxyClient(host="localhost", port=5556, application_id="01")
client.connect()

message = "This is notification message!!"
for token in many_tokens:
    client.send(token, message, badge=1)

client.close()
```
