#!/bin/bash

mkdir -p /data/log/nginx/
pip install celery redis


cp /src/docker/nginx.conf /etc/nginx/nginx.conf
cp /src/docker/default.conf /etc/nginx/conf.d/default.conf
service nginx stop
nginx -g "daemon off;" &
echo "started nginx"

if [ "$#" -ne 0 ]; then
    exec "$@"
fi