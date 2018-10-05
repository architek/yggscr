FROM nginx
COPY conf/ygg.conf /etc/nginx/conf.d/default.conf
RUN adduser nginx www-data && usermod -g www-data nginx
EXPOSE 8333:80
