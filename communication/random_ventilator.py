import random
from datetime import datetime

from plugin.ventilator_plugin.ventilator_communication import VentilatorCommunication, VentilatorData


class RandomVentilator(VentilatorCommunication):
    alarm_chance = 0.5
    ie_ratio_values = ["1:2", "1:3", "1:4", "2:1"]
    alarms = ["Failure to deliver pressurized air/oxygen", "Failure to deliver oxygen", "Inspiratory pressure too high",
              "Inspiratory pressure too low", "Inspiratory volume too high", "Inspiratory volume too low",
              "Breathing rate too high", "Breathing rate too low", "Cross-contamination", "Disconnect",
              "Component Malfunction", "Failure"]

    def get_data(self) -> VentilatorData:
        return VentilatorData(
            tidal_volume=random.randint(100, 1500),
            respiratory_rate=random.randint(10, 60),
            peak_inspiratory_pressure=random.randint(20, 120),
            ie_ratio=random.choice(RandomVentilator.ie_ratio_values),
            peep=random.randint(1, 3),
            alarms=self.randomize_alarms(),
            timestamp=datetime.utcnow().timestamp()
        )

    @staticmethod
    def randomize_alarms():
        if random.random() < RandomVentilator.alarm_chance:
            return {random.choice(RandomVentilator.alarms): True}
        else:
            return {}
