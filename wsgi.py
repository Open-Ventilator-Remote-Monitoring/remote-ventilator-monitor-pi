import argparse

from flask import Flask
from flask_cors import CORS

from serial_connection_factory import SerialConnectionFactory
from server import Server


def create_app(**kwargs):
    server_config = 'SERIAL'
    if 'config' in kwargs:
        server_config = kwargs.get('config')

    server_app = Flask(__name__)
    server_app.config.from_pyfile('config.py')
    CORS(server_app)
    connection_config = {'link': '/dev/ttyACM0', 'baud': 9600, 'timeout': 1}
    serial_connection = SerialConnectionFactory.create_serial_connection(server_config, connection_config)
    server = Server(app=server_app, serial_connection=serial_connection)
    server.setup()
    return server_app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev-serial',
                        help='enable running serial through command line',
                        action="store_true")
    args = parser.parse_args()

    config = 'SERIAL'
    if args.dev_serial:
        config = 'CONSOLE'
    app = create_app(**{'config': config})
    app.run()
