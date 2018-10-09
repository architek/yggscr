FROM nginx
RUN set -x && \
    apt update && apt install --no-install-recommends -y wget ca-certificates && \
    wget https://raw.githubusercontent.com/architek/yggscr/master/conf/ygg.conf -O /etc/nginx/conf.d/default.conf && \
    apt purge -y wget ca-certificates && rm -rf /var/lib/apt/lists/*
EXPOSE 80
VOLUME /run/ygg
