import threading

from plugin.alarm_sound_plugin.alarm_data import AlarmData


class AlarmHandler(object):
    alarm_data: AlarmData = None

    def __init__(self):
        self.lock = threading.Lock()
        self.ready = False

    def update_ready(self, ready_status: bool) -> None:
        self.ready = ready_status

    def get_ready(self) -> bool:
        return self.ready

    def update_alarm_data(self, alarm_data: AlarmData):
        with self.lock:
            self.alarm_data = alarm_data

    def get_alarm_data(self) -> AlarmData:
        with self.lock:
            return self.alarm_data
