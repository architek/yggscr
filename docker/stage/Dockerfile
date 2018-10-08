FROM python:3.6-alpine as base
WORKDIR /opt/yggscr/
# This is a non reproducable step... /!\ #
#RUN apk --update add tar
#RUN wget -O latest.tgz `wget -q https://api.github.com/repos/architek/yggscr/releases/latest -O - | grep tarball_url | cut -d '"' -f 4` #" Vim display bug
#RUN tar xf latest.tgz --strip-components=1 --wildcards '*/setup.py' '*/src/' '*/docs/README.rst' '*/conf/' '*/requirements-dev.txt' && rm latest.tgz
COPY setup.py requirements-dev.txt ./
COPY src src
COPY docs docs
COPY conf conf
RUN pip install wheel && pip wheel . --wheel-dir=wheels

FROM python:3.6-alpine as uwsgi
COPY --from=base /opt/yggscr /opt/yggscr
WORKDIR /opt/yggscr
RUN pip install --no-index --find-links=/opt/yggscr/wheels -r requirements-dev.txt

RUN apk --update --no-cache add uwsgi uwsgi-python3 && rm -rf /var/cache/apk/*
RUN mkdir /run/ygg/ && chown -R uwsgi:uwsgi /run/ygg
RUN sed 's/^;*\s*host\s*=\s*127.0.0.1/host = 0.0.0.0/' -i conf/yserver.cfg
RUN mv conf/yserver.cfg src/yserver/
RUN mv conf/ygg.ini src/yserver/
ENV PYTHONPATH /opt/yggscr/src
WORKDIR src/yserver
CMD [ "uwsgi", "--ini", "ygg.ini", "--pythonpath", "/usr/local/lib/python3.6/site-packages", "--pythonpath", "/opt/yggscr/src"]

EXPOSE 8333
VOLUME /run/ygg/
