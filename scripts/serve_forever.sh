#!/bin/sh

if [ -z "$GUNICORN_HTTPS" ]; then
  echo "Starting gunicorn over HTTP..."
  gunicorn -w "$GUNICORN_WORKERS" -b 0.0.0.0:8000 podcaststore_site.wsgi
else
  echo "Starting gunicorn over HTTPS..."
  gunicorn -w "$GUNICORN_WORKERS" -b 0.0.0.0:8000 --keyfile certs/privkey1.pem --certfile certs/fullchain1.pem podcaststore_site.wsgi
fi
