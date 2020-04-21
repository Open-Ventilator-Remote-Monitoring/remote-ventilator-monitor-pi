from serial import Serial

from open_ventilator_monitor_pi.serial_monitor.serial_monitor_handler import SerialMonitorHandler
from open_ventilator_monitor_pi.serial_monitor.serial_monitor_listener import SerialMonitorListener
from plugin.ventilator_plugin.ventilator_communication import VentilatorCommunication, VentilatorData


class SerialConnection(VentilatorCommunication):
    connection: Serial
    serial_monitor_handler: SerialMonitorHandler

    def __init__(self,
                 connection: Serial,
                 serial_monitor_handler: SerialMonitorHandler,
                 serial_monitor_listener: SerialMonitorListener
                 ) -> None:
        self.connection = connection
        self.serial_monitor_handler = serial_monitor_handler
        self.serial_monitor_listener = serial_monitor_listener

    def start_connection(self) -> None:
        self.connection.flush()
        self.serial_monitor_listener.start()

    def stop_connection(self) -> None:
        self.serial_monitor_listener.stop()
        self.serial_monitor_listener.join()

    def get_data(self) -> VentilatorData:
        return self.serial_monitor_handler.get_current_data()

    def is_ready(self) -> bool:
        return self.serial_monitor_handler.get_ready()
