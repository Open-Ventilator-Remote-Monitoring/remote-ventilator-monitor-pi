#!/usr/bin/env sh
sudo gunicorn --bind 0.0.0.0:80 wsgi:app
