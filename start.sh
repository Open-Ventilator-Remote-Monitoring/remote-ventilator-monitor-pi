# wsgi:create_app(config="CONSOLE") if you want to run on desktop
gunicorn --bind 0.0.0.0:8080 'wsgi:create_app()'
