all: format

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

format:
	@echo "Formatting..."
	python -m black -t py38 packet_server/ tests/
	@echo "Formatting... Done"