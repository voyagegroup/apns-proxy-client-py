# Commands for developer

setup:
	virtualenv .
	./bin/pip install -r requirements.txt

lint:
	./bin/flake8 apns_proxy_client tests

test:
	./bin/nosetests

pypi:
	pandoc -f markdown_github -t rst -o README.rst Readme.md
	python setup.py register
	python setup.py sdist
	python setup.py sdist upload
