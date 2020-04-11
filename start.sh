#!/usr/bin/env sh
PORT="${FLASK_PORT:-8080}"
LISTEN="${FLASK_LISTEN:-0.0.0.0}"
echo listening on ${LISTEN}:${PORT}
gunicorn --bind ${LISTEN}:${PORT} 'wsgi:create_app()'
