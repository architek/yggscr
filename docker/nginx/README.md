Nginx reverse proxy with:

* No server_name
* Listens on 0.0.0.0:80 only
* Redirects anything under / to proxy pass
* Communicates with uwsgi through /run/ygg/ygg.sock
* Default debian user: nginx
* uWsgi read/send timeouts to 20s
