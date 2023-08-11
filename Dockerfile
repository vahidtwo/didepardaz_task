FROM tiangolo/uwsgi-nginx:python3.11

ENV NGINX_MAX_UPLOAD 16m
ENV LISTEN_PORT 8000
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 32
ENV NGINX_WORKER_PROCESSES 2
ENV UWSGI_INI /app/uwsgi.ini


# start setup varniosh
COPY install_varnish.sh /install_varnish.sh
RUN chmod +x /install_varnish.sh && /bin/bash /install_varnish.sh

RUN mkdir -p /etc/varnish/sites
COPY default.vcl /etc/varnish/default.vcl
# COPY ./varnish.supervisord.conf /etc/supervisor/conf.d/varnish.supervisord.conf
# end setup varnish


COPY custom-nginx.conf /etc/nginx/conf.d/custom.conf
WORKDIR /app


COPY requirements.txt /app/
COPY requirements /app/requirements
RUN pip install -r requirements.txt

COPY prestart.sh /app/prestart.sh
COPY uwsgi.ini /app/uwsgi.ini

COPY . /app
