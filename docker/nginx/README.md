# Nginx reverse proxy
[![](https://images.microbadger.com/badges/image/architek/nginx.svg)](https://microbadger.com/images/architek/nginx "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/architek/nginx.svg)](https://microbadger.com/images/architek/nginx "Get your own version badge on microbadger.com")
Settings:

* No server_name
* Listens on 0.0.0.0:80 only
* Redirects anything under / to proxy pass
* Communicates with uwsgi through /run/ygg/ygg.sock
* Default debian user: nginx
* uWsgi read/send timeouts to 20s
