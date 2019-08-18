#!/bin/sh

if [ -z "$NEW_RELIC_CONFIG_FILE" ]; then
  if [ -z "$GUNICORN_HTTPS" ]; then
    echo "Starting gunicorn over HTTP..."
    gunicorn -w "$GUNICORN_WORKERS" -b 0.0.0.0:8000 cadastro_site.wsgi
  else
    echo "Starting gunicorn over HTTPS..."
    gunicorn -w "$GUNICORN_WORKERS" -b 0.0.0.0:8000 --keyfile certs/privkey1.pem --certfile certs/fullchain1.pem cadastro_site.wsgi
  fi
else
  if [ -z "$GUNICORN_HTTPS" ]; then
    echo "Starting gunicorn with relic over HTTP..."
    newrelic-admin run-program gunicorn -w "$GUNICORN_WORKERS" -b 0.0.0.0:8000 cadastro_site.wsgi
  else
    echo "Starting gunicorn with relic over HTTPS..."
    newrelic-admin run-program gunicorn -w "$GUNICORN_WORKERS" -b 0.0.0.0:8000 --keyfile certs/privkey1.pem --certfile certs/fullchain1.pem cadastro_site.wsgi
  fi
fi
