from random_ventilator import RandomVentilator
from serial_connection import SerialConnection
from ventilator_communication import VentilatorCommunication


class UnknownConnectionType(Exception):
    def __init__(self, message):
        super().__init__(message)


class SerialConnectionFactory:

    @staticmethod
    def create_serial_connection(cnx_config) -> VentilatorCommunication:
        cnx_type = cnx_config['type']
        if cnx_type == "serial":
            return SerialConnection(cnx_config['link'], cnx_config['baud'], cnx_config['timeout'])
        elif cnx_type == "random":
            return RandomVentilator(cnx_config['link'], cnx_config['baud'], cnx_config['timeout'])
        else:
            raise UnknownConnectionType(f'Unknown connection type {type}')
