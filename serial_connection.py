import serial


class SerialConnection:
    connection: serial.Serial

    def __init__(self, serial_connection: serial.Serial) -> None:
        self.connection = serial_connection

    def start_connection(self) -> None:
        self.connection.flush()

    def send_message(self, byte_string: bytes) -> None:
        self.connection.write(byte_string)

    def read_line(self) -> bytes:
        return self.connection.readline()

