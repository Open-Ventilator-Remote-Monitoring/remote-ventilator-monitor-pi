import serial


class SerialService:

    connection: serial

    def __init__(self, link: str, baud: int, timeout: int):
        self.link = link
        self.baud = baud
        self.timeout = timeout

    def start_connection(self):
        self.connection = serial.Serial(self.link, self.baud, self.timeout)
        self.connection.flush()

    def send_message(self, byte_string: bytes):
        self.connection.write(byte_string)

    def read_line(self) -> bytes:
        return self.connection.readline()

