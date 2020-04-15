import json
import time
from threading import Timer

from ventilator_communication import VentilatorCommunication, VentilatorData
import random


class RandomVentilator(VentilatorCommunication):

    alarm_chance = 0.5
    ie_ratio_values = ["1:2", "1:3", "1:4", "2:1"]
    alarms = ["Failure to deliver pressurized air/oxygen", "Failure to deliver oxygen", "Inspiratory pressure too high",
              "Inspiratory pressure too low", "Inspiratory volume too high", "Inspiratory volume too low",
              "Breathing rate too high", "Breathing rate too low", "Cross-contamination", "Disconnect",
              "Component Malfunction", "Failure"]

    def __init__(self, publisher):
        self.publisher = publisher

    def send_data(self):
        ventilator_data = self.get_data()
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
        Timer(5, self.send_data).start()

    def start_connection(self) -> None:
        Timer(5, self.send_data).start()

    def get_data(self) -> VentilatorData:
        return VentilatorData(
            tidal_volume=random.randint(100, 1500),
            respiratory_rate=random.randint(10, 60),
            peak_inspiratory_pressure=random.randint(20, 120),
            ie_ratio=random.choice(RandomVentilator.ie_ratio_values),
            peep=random.randint(1, 3),
            alarms=self.randomize_alarms(),
            timestamp=time.time()
        )

    @staticmethod
    def randomize_alarms():
        if random.random() < RandomVentilator.alarm_chance:
            return {random.choice(RandomVentilator.alarms): True}
        else:
            return {}
