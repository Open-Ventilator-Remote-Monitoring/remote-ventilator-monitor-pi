import serial

from serial_connection import SerialConnection


class SerialConnectionFactory:

    @staticmethod
    def create_serial_connection(link: str, baud: int, timeout: int) -> SerialConnection:
        return SerialConnection(serial.Serial(link, baud, timeout))
