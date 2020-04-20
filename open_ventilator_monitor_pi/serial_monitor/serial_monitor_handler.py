import threading

from plugin.ventilator_plugin.ventilator_communication import VentilatorData


class SerialMonitorHandler:
    current_data: VentilatorData = None

    def __init__(self):
        self.ready = False
        self.lock: threading.Lock = threading.Lock()

    def update(self, ventilator_data: VentilatorData):
        with self.lock:
            self.current_data = ventilator_data

    def get_current_data(self) -> VentilatorData:
        with self.lock:
            return self.current_data

    def update_ready(self, ready: bool) -> None:
        self.ready = ready

    def get_ready(self):
        return self.ready
