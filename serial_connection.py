import serial

from open_ventilator_monitor_pi.serial_monitor.serial_monitor_handler import SerialMonitorHandler
from open_ventilator_monitor_pi.serial_monitor.serial_monitor_listener import SerialMonitorListener
from ventilator_communication import VentilatorCommunication, VentilatorData


class SerialConnection(VentilatorCommunication):
    connection: serial.Serial
    serial_monitor_handler: SerialMonitorHandler

    def __init__(self, link: str, baud: int, timeout: int) -> None:
        self.connection = serial.Serial(port=link,
                                        baudrate=baud,
                                        timeout=timeout,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS)
        self.serial_monitor_handler = SerialMonitorHandler()
        self.serial_monitor_listener = SerialMonitorListener(self, self.connection, self.serial_monitor_handler)

    def start_connection(self) -> None:
        self.connection.flush()
        self.serial_monitor_listener.start()

    def stop_connection(self) -> None:
        self.serial_monitor_listener.stop()
        self.serial_monitor_listener.join()

    def get_data(self) -> VentilatorData:
        return self.serial_monitor_handler.get_current_data()
