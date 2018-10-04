FROM debian:stretch-slim
ENV LANG C.UTF-8

# Apt upgrade
RUN apt-get update -y
RUN apt-get upgrade -y

# Py Setuptools
RUN apt-get -y install python3-setuptools python3-pip
RUN apt-get -y install ca-certificates

# Install reqs
COPY requirements.txt /opt/app/
RUN pip3 install -r /opt/app/requirements.txt

# Install code
ADD ./.dock/code.tar /opt/app/
WORKDIR /opt/app
RUN python3 setup.py install

# Copy remaining stuffs
COPY . /opt/app/

# Run daemon
WORKDIR /opt/app/src/yserver/
ENTRYPOINT ["yserver"]
# EXPOSE 8333:8333
