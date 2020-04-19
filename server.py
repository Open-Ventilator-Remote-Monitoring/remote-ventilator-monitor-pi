
from flask import Flask, jsonify
from flask_restful import Api, Resource

from ventilator_communication import VentilatorCommunication

from gpiozero import Button

input_from_soundear = Button(4, pull_up = False)

class GetStatus(Resource):
    def get(self):

        if input_from_soundear.is_pressed:
            soundear_alarm = False
        else:
            soundear_alarm = True

        return jsonify({  "device": {
            "id": "ventilator-1",
            "currentTime": "2020-04-17T11:58:00Z",
            "roles": {
              "ventilatorAlarmSoundMonitor": "true",
              "ventilatorDataMonitor": "false"
            }
          },
          "ventilatorAlarmSoundMonitor":
          {
            "timestamp": "2020-04-17T11:58:00Z",
            "status": {
            },
            "alerts": {
              "audioAlarm": soundear_alarm
            }
          }
        })


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

