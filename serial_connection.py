import serial

from ventilator_communication import VentilatorCommunication, VentilatorData


class SerialConnection(VentilatorCommunication):
    connection: serial.Serial

    def __init__(self, link: str, baud: int, timeout: int) -> None:
        self.connection = serial.Serial(link, baud, timeout)

    def start_connection(self) -> None:
        self.connection.flush()

    def get_data(self) -> VentilatorData:
        return self.convert(self.connection.readline())

    @staticmethod
    def convert(bytes) -> VentilatorData:
        # TODO need to get this from the cached data coming off the serial port
        return VentilatorData(
            tidal_volume=500,
            respiratory_rate=25,
            peak_inspiratory_pressure=70,
            ie_ratio="1:3",
            peep=7,
            alarms={}
        )
