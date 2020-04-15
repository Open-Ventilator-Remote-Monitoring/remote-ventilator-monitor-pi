import ssl
from signal import signal, SIGINT
from sys import exit

import yaml
from flask import Flask
from flask_cors import CORS

from publisher import Publisher
from serial_connection_factory import SerialConnectionFactory
from server import Server
from socket_connection import SocketConnection


class ServerConfigurationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def create_app():

    server_app = Flask(__name__)
    CORS(server_app)

    config_file = "application-{}.yml".format(server_app.config["ENV"])
    try:
        with open(config_file) as file:
            yaml_config = yaml.load(file, Loader=yaml.Loader)
            print(f'Config loaded from {config_file}')
            if server_app.config["ENV"] == "development":
                print(yaml_config)
    except OSError:
        raise ServerConfigurationException(f'Error, could not load configuration {config_file}')
    publisher = Publisher(['ventilator'])

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations("./cert/ca-cert.pem")
    socket_server = SocketConnection('wss://127.0.0.1:1011/socket', cert_info=ssl_context)
    socket_server.start()
    print('here')
    publisher.register('ventilator', 'socket_server', socket_server.send_message)

    serial_connection = SerialConnectionFactory.create_serial_connection(yaml_config['ventilator']['connection'], publisher)

    server = Server(app=server_app, serial_connection=serial_connection)
    server.setup()

    def handler(signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        server.shut_down()
        exit(0)

    signal(SIGINT, handler)

    return server_app


if __name__ == "__main__":
    print('should not see this')
    app = create_app()
    app.run()

