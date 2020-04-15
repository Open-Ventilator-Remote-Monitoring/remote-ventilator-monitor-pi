import serial

from open_ventilator_monitor_pi.serial_monitor.serial_monitor_handler import SerialMonitorHandler
from open_ventilator_monitor_pi.serial_monitor.serial_monitor_listener import SerialMonitorListener
from publisher import Publisher
from random_ventilator import RandomVentilator
from serial_connection import SerialConnection
from ventilator_communication import VentilatorCommunication


class UnknownConnectionType(Exception):
    def __init__(self, message):
        super().__init__(message)


class SerialConnectionFactory:

    @staticmethod
    def create_serial_connection(cnx_config, publisher: Publisher) -> VentilatorCommunication:
        cnx_type = cnx_config['type']
        if cnx_type == "serial":
            connection = serial.Serial(port=cnx_config['link'],
                                       baudrate=cnx_config['baud'],
                                       timeout=cnx_config['timeout'],
                                       stopbits=serial.STOPBITS_ONE,
                                       bytesize=serial.EIGHTBITS)
            serial_monitor_handler = SerialMonitorHandler(publisher)
            serial_monitor_listener = SerialMonitorListener(connection, serial_monitor_handler)
            return SerialConnection(connection=connection,
                                    serial_monitor_handler=serial_monitor_handler,
                                    serial_monitor_listener=serial_monitor_listener)
        elif cnx_type == "random":
            return RandomVentilator(publisher)
        else:
            raise UnknownConnectionType(f'Unknown connection type {type}')
