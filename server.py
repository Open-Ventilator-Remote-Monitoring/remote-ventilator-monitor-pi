
from flask import Flask, jsonify
from flask_cors import CORS
import yaml
from yaml import Loader
from flask_restful import Api, Resource

from serial_connection_factory import SerialConnectionFactory
from ventilator_communication import VentilatorCommunication


class GetStatus(Resource):
    def __init__(self, **kwargs):
        self.serial_connection = kwargs['serial_connection']

    def get(self):
        return jsonify({'ventilator': [self.serial_connection.get_data().__dict__]})



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

# @app.route("/")
# def hello():
#     return_string = "<h1>Ventilator Network Server</h1>"
#     return_string += "<p>Ventilator Stats:</p>"
#     return return_string
#
#
# @app.route("/api/ventilator", methods=['GET'])
# def get_status():
#     global serial_connection
#     data = serial_connection.read_line()
#     return jsonify({'ventilator': [data.__dict__]})

