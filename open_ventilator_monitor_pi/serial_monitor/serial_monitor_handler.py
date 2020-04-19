import threading

from plugin.ventilator_plugin.ventilator_communication import VentilatorData


class SerialMonitorHandler:
    current_data: VentilatorData = None
    lock: threading.Lock = threading.Lock()

    def update(self, ventilator_data: VentilatorData):
        with self.lock:
            self.current_data = ventilator_data

    def get_current_data(self) -> VentilatorData:
        with self.lock:
            return self.current_data
