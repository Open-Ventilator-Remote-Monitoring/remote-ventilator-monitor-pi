import serial

from ventilator_communication import VentilatorCommunication


class SerialConnection(VentilatorCommunication):
    connection: serial.Serial

    def __init__(self, link: str, baud: int, timeout: int) -> None:
        self.connection = serial.Serial(link, baud, timeout)

    def start_connection(self) -> None:
        self.connection.flush()

    def send_message(self, byte_string: bytes) -> None:
        self.connection.write(byte_string)

    def read_line(self) -> bytes:
        return self.connection.readline()

