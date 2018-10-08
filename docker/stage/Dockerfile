FROM python:3.6-alpine as base
WORKDIR /opt/yggscr/
RUN apk --update add tar
RUN wget -O latest.tgz `wget -q https://api.github.com/repos/architek/yggscr/releases/latest -O - | grep tarball_url | cut -d '"' -f 4` #"
RUN tar xf latest.tgz --strip-components=1 --wildcards '*/setup.py' '*/src' '*/docs/README.rst' '*/conf' '*/requirements-dev.txt'
RUN pip install wheel && pip wheel . --wheel-dir=wheels
VOLUME conf/

FROM python:3.6-alpine
COPY --from=base . .
RUN pip install --no-index --find-links=/opt/yggscr/wheels -r requirements-dev.txt
RUN apk --update --no-cache add uwsgi uwsgi-python3 && rm -rf /var/cache/apk/*
RUN mkdir /run/ygg/ && chown -R uwsgi:uwsgi /run/ygg
WORKDIR conf/
RUN sed 's/^;*\s*host\s*=\s*127.0.0.1/host = 0.0.0.0/' -i yserver.cfg
CMD [ "uwsgi", "--ini", "ygg.ini", "--pythonpath", "/usr/local/lib/python3.6/site-packages", "--pythonpath", "/opt/yggscr/src"]
VOLUME /run/ygg/
