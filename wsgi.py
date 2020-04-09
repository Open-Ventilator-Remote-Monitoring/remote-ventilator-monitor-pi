import argparse

from flask import Flask
from flask_cors import CORS

from serial_connection_factory import SerialConnectionFactory
from server import Server

config = 'SERIAL'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    CORS(app)
    connection_config = {'link': '/dev/ttyACM0', 'baud': 9600, 'timeout': 1}
    serial_connection = SerialConnectionFactory.create_serial_connection(config, connection_config)
    print(args)
    server = Server(app=app, serial_connection=serial_connection)
    server.setup()
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev-serial',
                        help='enable running serial through command line',
                        action="store_true")
    args = parser.parse_args()

    if args.dev_serial:
        config = 'CONSOLE'
    app = create_app()
    app.run()
