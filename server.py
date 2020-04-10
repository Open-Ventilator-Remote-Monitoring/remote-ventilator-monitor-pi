
from flask import Flask, jsonify
from flask_restful import Api, Resource

from ventilator_communication import VentilatorCommunication


class GetStatus(Resource):
    def __init__(self, **kwargs):
        self.serial_connection = kwargs['serial_connection']

    def get(self):
        return jsonify({'ventilator': [self.serial_connection.get_data().to_camelcase_dict()]})


class Server:
    def __init__(self, app: Flask,  serial_connection: VentilatorCommunication):
        self.app = app
        self.api = Api(self.app)
        self.serial_connection = serial_connection

    def setup_routing(self):
        self.api.add_resource(GetStatus, '/api/ventilator',
                              resource_class_kwargs={'serial_connection': self.serial_connection})

    def setup(self):
        self.serial_connection.start_connection()
        self.setup_routing()

    def shut_down(self):
        self.serial_connection.stop_connection()

