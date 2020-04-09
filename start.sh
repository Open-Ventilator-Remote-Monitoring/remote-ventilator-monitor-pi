#!/usr/bin/env sh
PORT="${FLASK_PORT:-default 8080}"
echo ${PORT}
gunicorn --bind 0.0.0.0:${PORT} 'wsgi:create_app()'
