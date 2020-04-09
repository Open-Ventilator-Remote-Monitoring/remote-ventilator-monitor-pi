from flask import Flask
from flask_cors import CORS
import yaml

from serial_connection_factory import SerialConnectionFactory
from server import Server


class ServerConfigurationException(Exception):
    def __init__(self, message):
        super().__init__(message)

def create_app(**kwargs):
    server_app = Flask(__name__)
    CORS(server_app)

    config_file = "application-{}.yml".format(server_app.config["ENV"])
    try:
        with open(config_file) as file:
            yaml_config = yaml.load(file, Loader=yaml.Loader)
            print(yaml_config)
            print(f'Config loaded from {config_file}')
    except OSError:
        raise ServerConfigurationException(f'Error, could not load configuration {config_file}')

    serial_connection = SerialConnectionFactory.create_serial_connection(yaml_config['ventilator']['connection'])
    serial_connection.start_connection()

    server = Server(app=server_app, serial_connection=serial_connection)
    server.setup()

    return server_app


if __name__ == "__main__":
    app = create_app()
    app.run()

