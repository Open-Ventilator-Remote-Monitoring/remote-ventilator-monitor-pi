class VentilatorData:
    def __init__(self, tidal_volume, respirator_rate, peak_inspiratory_pressure, ie_ratio, peep, alarms):
        self.tidal_volume = tidal_volume
        self.respirator_rate = respirator_rate
        self.peak_inspiratory_pressure = peak_inspiratory_pressure
        self.ie_ratio = ie_ratio
        self.peep = peep
        self.alarms = alarms

    def to_camelcase_dict(self) -> dict:
        return {
            'tidalVolume': self.tidal_volume,
            'respiratorRate': self.respirator_rate,
            'peakInspiratoryPressure': self.peak_inspiratory_pressure,
            'ieRatio': self.ie_ratio,
            'peep': self.peep,
            'alarms': self.alarms
        }


class VentilatorCommunication:
    def start_connection(self) -> None: pass

    def get_data(self) -> VentilatorData: pass
