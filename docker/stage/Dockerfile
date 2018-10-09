FROM python:3.6-alpine as base
RUN apk --update --no-cache add git && \
    git clone https://github.com/architek/yggscr.git && rm -rf yggscr/.git
WORKDIR yggscr/
RUN pip install wheel && pip wheel . --wheel-dir=wheels


FROM python:3.6-alpine as uwsgi
COPY --from=base yggscr/ /opt/yggscr
WORKDIR /opt/yggscr
RUN pip install --no-index --find-links=/opt/yggscr/wheels -r requirements-dev.txt

RUN apk --update --no-cache add uwsgi uwsgi-python3 && \
    mkdir /run/ygg/ && chown -R uwsgi:uwsgi /run/ygg && \
    cp conf/ygg.ini src/yserver/

ENV PYTHONPATH /opt/yggscr/src

WORKDIR src/yserver
ENTRYPOINT ["/opt/yggscr/docker/stage/conf-setup.sh"]
CMD [ "uwsgi", "--ini", "ygg.ini", "--pythonpath", "/usr/local/lib/python3.6/site-packages", "--pythonpath", "/opt/yggscr/src"]

EXPOSE 8333
VOLUME /run/ygg/
