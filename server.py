
from flask import Flask, jsonify
from flask_restful import Api, Resource

from ventilator_communication import VentilatorCommunication


class GetStatus(Resource):
    def get(self):
        return jsonify({'soundear': []})


class Server:
    # We're not using a serial connecting in the MVP
    #def __init__(self, app: Flask,  serial_connection: VentilatorCommunication):
    def __init__(self, app: Flask):
        self.app = app
        self.api = Api(self.app)
        # We're not using a serial connecting in the MVP
        #self.serial_connection = serial_connection

    def setup_routing(self):
        # We're not using a serial connecting in the MVP
        """
        self.api.add_resource(GetStatus, '/api/ventilator',
                              resource_class_kwargs={'serial_connection': self.serial_connection})
        """
        self.api.add_resource(GetStatus, '/api/v1/status' )

    def setup(self):
        # We're not using a serial connecting in the MVP
        #self.serial_connection.start_connection()
        self.setup_routing()

