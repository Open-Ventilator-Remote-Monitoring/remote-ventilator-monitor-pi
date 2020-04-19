import threading

from plugin.alarm_sound_plugin.alarm_data import AlarmData


class AlarmHandler(object):
    alarm_data: AlarmData = None

    def __init__(self):
        self.lock = threading.Lock()

    def update_alarm_data(self, alarm_data: AlarmData):
        with self.lock:
            self.alarm_data = alarm_data

    def get_alarm_data(self) -> AlarmData:
        with self.lock:
            return self.alarm_data
