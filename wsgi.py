from flask import Flask
from flask_cors import CORS
import yaml
from signal import signal, SIGINT
from sys import exit

#from serial_connection_factory import SerialConnectionFactory
from server import Server


class ServerConfigurationException(Exception):
    def __init__(self, message):
        super().__init__(message)


def create_app():

    server_app = Flask(__name__)
    CORS(server_app)

    # We're not using a serial conncection in the MVP
    """
    config_file = "application-{}.yml".format(server_app.config["ENV"])
    try:
        with open(config_file) as file:
            yaml_config = yaml.load(file, Loader=yaml.Loader)
            print(f'Config loaded from {config_file}')
            if server_app.config["ENV"] == "development":
                print(yaml_config)
    except OSError:
        raise ServerConfigurationException(f'Error, could not load configuration {config_file}')

    serial_connection = SerialConnectionFactory.create_serial_connection(yaml_config['ventilator']['connection'])
    """

    #server = Server(app=server_app, serial_connection=serial_connection)
    server = Server(app=server_app)
    server.setup()

    def handler(signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        server.shut_down()
        exit(0)

    signal(SIGINT, handler)

    return server_app


if __name__ == "__main__":
    app = create_app()
    app.run()

