FROM nginx
RUN mkdir -p /opt/yggscr/conf /opt/yggscr/docker/nginx
RUN set -x && \
    apt update && apt install --no-install-recommends -y wget ca-certificates && \
    wget https://raw.githubusercontent.com/architek/yggscr/master/conf/ygg.conf -O /opt/yggscr/conf/ygg.conf && \
    wget https://raw.githubusercontent.com/architek/yggscr/master/docker/nginx/conf-setup.sh -O /opt/yggscr/docker/nginx/conf-setup.sh && \
    chmod +x /opt/yggscr/docker/nginx/conf-setup.sh && \
    apt purge -y wget ca-certificates && apt autoremove -y && rm -rf /var/lib/apt/lists/*
CMD ["nginx", "-g", "daemon off;"]
ENTRYPOINT ["/opt/yggscr/docker/nginx/conf-setup.sh"]
EXPOSE 80
