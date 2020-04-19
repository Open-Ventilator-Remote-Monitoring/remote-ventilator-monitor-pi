from signal import signal, SIGINT
from sys import exit

import yaml
from flask import Flask
from flask_cors import CORS
from gpiozero import Button

from communication.serial_connection_factory import SerialConnectionFactory
from plugin.alarm_sound_plugin.alarm_handler import AlarmHandler
from plugin.alarm_sound_plugin.alarm_service import AlarmService
from plugin.alarm_sound_plugin.alarm_sound_plugin import AlarmSoundPlugin
from plugin.alarm_sound_plugin.random_alarm import RandomAlarm
from plugin.device_plugin.device_plugin import DevicePlugin
from plugin.status_plugin.status_plugin import StatusPlugin
from plugin.ventilator_plugin.ventilator_plugin import VentilatorPlugin
from server import Server
from service.authorization_service import ApiKeyAuthorizationService, NoAuthorizationService


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

    if yaml_config['ventilator']['api_key']:
        authorization_service = ApiKeyAuthorizationService(yaml_config['ventilator']['api_key'])
    else:
        authorization_service = NoAuthorizationService()

    device_config = yaml_config['ventilator']['device']

    device_plugin = DevicePlugin(device_config['id'], device_config['roles'])
    plugins = {
        'device': device_plugin
    }
    additional_plugins = {}
    if device_config['roles']:
        if device_config['roles']['ventilatorDataMonitor']:
            serial_connection = SerialConnectionFactory.create_serial_connection(
                yaml_config['ventilator']['connection'])
            ventilator_plugin = VentilatorPlugin(
                serial_connection=serial_connection,
                authorization_service=authorization_service
            )
            ventilator_plugin.enable_endpoint('/api/v1/ventilatorDataMonitor')
            additional_plugins['ventilatorDataMonitor'] = ventilator_plugin
        if device_config['roles']['ventilatorAlarmSoundMonitor']:
            alarm_handler = AlarmHandler()
            if yaml_config['ventilator']['alarm']['pin'] == -1:
                alarm_service = RandomAlarm(alarm_handler)
            else:
                alarm_service = AlarmService(
                    alarm_handler=alarm_handler,
                    trigger=Button(yaml_config['ventilator']['alarm']['pin'], True)
                )
            alarm_plugin = AlarmSoundPlugin(alarm_service=alarm_service)
            alarm_plugin.enable_endpoint('/api/v1/ventilatorAlarmSoundMonitor')
            additional_plugins['ventilatorAlarmSoundMonitor'] = alarm_plugin

    plugins.update(additional_plugins)
    status_plugin = StatusPlugin(plugins=plugins, authorization_service=authorization_service)
    status_plugin.enable_endpoint('/api/v1/status')

    visible_plugin = {
        'status': status_plugin
    }
    visible_plugin.update(additional_plugins)
    server = Server(app=server_app, plugins=visible_plugin)
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
