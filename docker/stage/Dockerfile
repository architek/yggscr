FROM python:3.6-alpine as base

ARG BUILD_DATE
ARG VCS_REF
LABEL org.label-schema.schema-version=1.0 \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name=architek/yggscr \
      org.label-schema.description="YggTorrent scrapper" \
      org.label-schema.vcs-url="https://github.com/architek/yggscr" \
      org.label-schema.vcs-ref=$VCS_REF
LABEL maintainer="Laurent Kislaire <teebeenator@gmail.com>"

RUN apk --update --no-cache add git && \
    git clone https://github.com/architek/yggscr.git && rm -rf yggscr/.git && \
    apk del git
WORKDIR yggscr/
RUN pip install wheel && pip wheel . --wheel-dir=wheels


FROM python:3.6-alpine as uwsgi
ARG BUILD_DATE

COPY --from=base yggscr/ /opt/yggscr
WORKDIR /opt/yggscr
RUN echo "__builddate__ = '$BUILD_DATE'" > src/yggscr/__build__.py
RUN apk --update --no-cache add uwsgi uwsgi-python3 && \
    mkdir /run/ygg/ && chown -R uwsgi:uwsgi /run/ygg
RUN pip install --no-index --find-links=/opt/yggscr/wheels -r requirements-dev.txt

ENV PYTHONPATH /opt/yggscr/src
ENV DEF_GUID=1001

WORKDIR src/yserver
ENTRYPOINT ["/opt/yggscr/docker/stage/conf-setup.sh"]

ARG def_wsgi_ini=ygg.ini
ENV WSGI_INI=$def_wsgi_ini
CMD uwsgi --ini $WSGI_INI --pythonpath /usr/local/lib/python3.6/site-packages --pythonpath /opt/yggscr/src


EXPOSE 8333
VOLUME /run/ygg/
