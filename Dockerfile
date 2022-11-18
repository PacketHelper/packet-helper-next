# build stage (frontend)
FROM node:lts-alpine@sha256:2175727cef5cad4020cb77c8c101d56ed41d44fbe9b1157c54f820e3d345eab1 as build-stage
WORKDIR /app
COPY package.json yarn.lock ./

RUN yarn -g install
COPY . .
RUN yarn build

# build stage (backend & package)
FROM python:3.11-buster@sha256:43db725cf6c954611ffe4938e330e8d18b48627ad19e4f1ed62196baf5a3ca58

# Install tshark/wireshark dependecies
RUN echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -y install wireshark

RUN apt-get update && apt-get install -y --allow-change-held-packages --force-yes tshark


# Install Python stuff
RUN pip install cython
ADD ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -q -r /tmp/requirements.txt


# Copy files
ADD . /opt/packet_server/
RUN mkdir -p /opt/packet_server/tmp
RUN mkdir -p /opt/packet_server/static

WORKDIR /opt/packet_server
COPY --from=build-stage /app/dist/static static
COPY --from=build-stage /app/dist/index.html static

# Set ENV's
ARG PH_REV
ENV PH_REVISION=${PH_REV}

ARG PH_VER
ENV PH_VERSION=${PH_VER}

# $PORT is set by Heroku
CMD uvicorn --host 0.0.0.0 --port $PORT ph.main:app
