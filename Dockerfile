# build stage (frontend)
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./

RUN yarn -g install
COPY . .
RUN yarn build

# build stage (backend & package)
FROM python:3.8-buster

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

WORKDIR /opt/packet_server
COPY --from=build-stage /app/dist dist

# Set ENV's
ARG PH_REV
ENV PH_REVISION=${PH_REV}
ARG PAT_TOKEN
ENV PAT_TOKEN=${PAT_TOKEN}

ENV DJANGO_SETTINGS_MODULE="backend.settings.prod"
# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn backend.wsgi --log-file -
