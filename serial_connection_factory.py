from console_connection import ConsoleConnection
from serial_connection import SerialConnection
from ventilator_communication import VentilatorCommunication


class SerialConnectionFactory:

    @staticmethod
    def create_serial_connection(connection_type: str, config) -> VentilatorCommunication:
        if connection_type == "SERIAL":
            return SerialConnection(config['link'], config['baud'], config['timeout'])
        elif connection_type == "DEBUG":
            return ConsoleConnection(config['link'], config['baud'], config['timeout'])
