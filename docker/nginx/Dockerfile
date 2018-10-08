FROM nginx
RUN set -x && \
    apt update && apt install -y wget && rm -rf /var/lib/apt/lists/* && \
    wget https://raw.githubusercontent.com/architek/yggscr/master/conf/ygg.conf -O /etc/nginx/conf.d/default.conf
EXPOSE 80
