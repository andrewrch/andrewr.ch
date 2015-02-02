SHELL=/bin/bash

CONTENT_DIR=content
BUILD_DIR=build
INSTALL_DIR=/var/www

proto: prep all

prep:
	if [ ! -d $(BUILD_DIR) ]; then mkdir -p $(BUILD_DIR); fi;

all:
	./build_content.py ${CONTENT_DIR} ${BUILD_DIR}

install:
	cp -r build/* ${INSTALL_DIR}

clean:
	rm -rf build
