class VentilatorData:
    def __init__(self,
                 tidal_volume: int,
                 respiratory_rate: int,
                 peak_inspiratory_pressure: int,
                 ie_ratio: int,
                 peep: int,
                 alarms: dict,
                 timestamp: float):
        self.tidal_volume = tidal_volume
        self.respiratory_rate = respiratory_rate
        self.peak_inspiratory_pressure = peak_inspiratory_pressure
        self.ie_ratio = ie_ratio
        self.peep = peep
        self.alarms = alarms
        self.timestamp = timestamp


class VentilatorCommunication:
    def start_connection(self) -> None: pass

    def get_data(self) -> VentilatorData: pass

    def stop_connection(self) -> None: pass
