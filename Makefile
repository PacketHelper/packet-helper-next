all: format

build-local:
	rm -rf static
	mkdir -p static
	yarn build
	mv dist/static/* static/
	mv dist/index.html static/index.html

run-local:
	uvicorn --port 8080 ph.main:app 

clean:
	rm -rf phc

clean-local: clean
	rm -rf packet_helper_core

install-core: clean
	@echo "Updating core..."
	git clone https://github.com/PacketHelper/packet-helper-core.git phc
	cd phc && make all
	cd phc/dist && python3 -m pip install *.whl --force
	rm -rf phc
	@echo "Updating core... Done"

local-core: clean-local
	@echo "Getting core..."
	git clone https://github.com/PacketHelper/packet-helper-core.git phc
	mv phc/packet_helper_core ./packet_helper_core
	rm -rf phc
	@echo "Getting core... Done"

format-ui:
	prettier --write src/

format:
	@echo "Formatting..."
	python3 -m black -t py38 backend/ test/
	prettier --write src/
	@echo "Formatting... Done"

.PHONY: run-back
run-back:
	python3 manage.py runserver

test:
	mkdir -p static && touch static/index.html
	PYTHONPATH=${PWD} pytest

.PHONY: init
init:
	rm -rf node_modules/ yarn.lock
	yarn
