import threading
from datetime import datetime, timezone
from typing import Union, Dict

from flask import jsonify
from flask_restful import Api, Resource

from plugin.plugin_base import PluginBase
from plugin.ventilator_plugin.ventilator_communication import VentilatorData, VentilatorCommunication


class VentilatorPluginGetStatus(Resource):
    def __init__(self, **kwargs):
        self.plugin = kwargs['plugin']

    def get(self):
        current_data = self.plugin.get_data()
        if current_data:
            return jsonify(self.plugin.get_data())
        else:
            return jsonify({'ventilator': []})


class VentilatorPlugin(PluginBase):
    def __init__(self, serial_connection: VentilatorCommunication):
        self.lock = threading.Lock()
        self.serial_connection = serial_connection
        self.end_point = None
        self.is_running = False

    def start_plugin(self) -> None:
        with self.lock:
            if not self.is_running:
                self.serial_connection.start_connection()
                self.is_running = True

    def add_endpoints(self, api: Api) -> None:
        if self.end_point:
            api.add_resource(VentilatorPluginGetStatus, self.end_point, resource_class_kwargs={'plugin': self})

    def get_raw_data(self) -> VentilatorData:
        with self.lock:
            return self.serial_connection.get_data()

    def get_data(self) -> \
            Union[Dict[str, Union[str, Dict[str, Dict[str, Union[int, str]]]]], Dict[str, Union[str, dict]]]:
        current_data = self.get_raw_data()
        return {
            'timestamp': datetime.fromtimestamp(current_data.timestamp).isoformat(),
            'status': {
                'ieRatio': {
                    'value': current_data.ie_ratio,
                    'uom': 'ratio',
                },
                'peakInspiratoryPressure': {
                    'value': current_data.peak_inspiratory_pressure,
                    'uom': 'CMH20',
                },
                'peep': {
                    'value': current_data.peep,
                    'uom': 'CMH2O',
                },
                'respiratoryRate': {
                    'value': current_data.respiratory_rate,
                    'uom': 'breathsPerMinute',
                },
                'tidalVolume': {
                    'value': current_data.tidal_volume,
                    'uom': 'ml/kg',
                }
            }
        } if current_data else {
            'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            'status': {}
        }

    def stop_plugin(self) -> None:
        with self.lock:
            if self.is_running:
                self.serial_connection.stop_connection()
            self.is_running = False

    def enable_endpoint(self, end_point: str) -> None:
        self.end_point = end_point
