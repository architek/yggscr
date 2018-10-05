FROM debian:stretch-slim
ENV LANG C.UTF-8

# Apt setuptools & al
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-setuptools python3-pip \
    ca-certificates

# Install reqs
COPY requirements.txt /opt/app/
RUN pip3 install -r /opt/app/requirements.txt

# Copy and install
RUN mkdir -p /opt/app/src/yserver
RUN mkdir -p /opt/app/docs
COPY setup.py /opt/app/
COPY docs/README.rst /opt/app/docs/
COPY src/yserver/ /opt/app/src/yserver/
COPY src/yggscr/ /opt/app/src/yggscr/
WORKDIR /opt/app
RUN python3 setup.py install

# Copy static stuffs
COPY src/yserver/resources /opt/app/src/yserver/
COPY src/yserver/views /opt/app/src/yserver/

# Run daemon
WORKDIR /opt/app/src/yserver/
RUN sed 's/^\s*host\s*=\s*127.0.0.1/host = 0.0.0.0/' -i yserver.cfg
ENTRYPOINT ["yserver"]
EXPOSE 8333
