import json

from flask import Flask
from flask_restful import Api, Resource

from ventilator_communication import VentilatorCommunication


class GetStatus(Resource):
    def __init__(self, **kwargs):
        self.serial_connection = kwargs['serial_connection']

    def get(self):
        line = self.serial_connection.request("getStats\n")
        print(line)
        json_line = json.loads(line)
        print(json_line)
        return json_line


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


""" `
ventilator = [
    {
        'tidalVolume' : u'500',
        'respiratoryRate' : u'25',
        'peakInspiratoryPressure' : u'70',
        'ieRatio' : u'1:3',
        'peep' : u'7'
    }
]
"""
