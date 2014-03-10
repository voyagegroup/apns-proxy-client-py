# Commands for developer

setup:
	virtualenv .
	./bin/pip install -r requirements.txt

lint:
	./bin/flake8 apns_proxy_client tests

test:
	./bin/nosetests
