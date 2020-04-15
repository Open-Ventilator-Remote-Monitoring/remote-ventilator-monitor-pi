import threading

import json

from publisher import Publisher
from ventilator_communication import VentilatorData


class SerialMonitorHandler:
    current_data: VentilatorData = None
    lock: threading.Lock = threading.Lock()

    def __init__(self, publisher: Publisher):
        self.publisher = publisher

    def update(self, ventilator_data: VentilatorData):
        print('here')
        with self.lock:
            self.current_data = ventilator_data
        print('here1')
        self.publisher.dispatch('ventilator', json.dumps(
            {
                'type': 'ventilatorData',
                'data': {
                    'tidalVolume': ventilator_data.tidal_volume,
                    'respiratoryRate': ventilator_data.respiratory_rate,
                    'peakInspiratoryPressure': ventilator_data.peak_inspiratory_pressure,
                    'ieRatio': ventilator_data.ie_ratio,
                    'peep': ventilator_data.peep,
                    'alarms': ventilator_data.alarms,
                    'timestamp': ventilator_data.timestamp
                }
            }))

    def get_current_data(self) -> VentilatorData:
        with self.lock:
            return self.current_data
