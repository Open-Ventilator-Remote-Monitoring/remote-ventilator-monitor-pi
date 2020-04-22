#!/usr/bin/env sh
PORT="${FLASK_PORT:-8080}"
LISTEN="${FLASK_LISTEN:-0.0.0.0}"
echo environment ${FLASK_ENV}
echo listening on ${LISTEN}:${PORT}
gunicorn --certfile cert/server.crt --keyfile cert/server.key --bind ${LISTEN}:${PORT} 'wsgi:create_app()'
