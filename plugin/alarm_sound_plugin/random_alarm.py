import threading
from time import sleep
from datetime import datetime
from random import random

from plugin.alarm_sound_plugin.alarm_data import AlarmData
from plugin.alarm_sound_plugin.alarm_handler import AlarmHandler
from plugin.alarm_sound_plugin.alarm_service import AlarmServiceInterface


class RandomAlarm(AlarmServiceInterface):
    def __init__(self, alarm_handler: AlarmHandler):
        super().__init__()
        self.alarm_handler = alarm_handler
        self.lock = threading.Lock()
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        while self.is_running:
            sleep(5)
            self.alarm_handler.update_alarm_data(AlarmData(random() > .5, timestamp=datetime.utcnow().timestamp()))

    def stop(self):
        with self.lock:
            self.is_running = False

    def get_data(self) -> AlarmData:
        with self.lock:
            return self.alarm_handler.get_alarm_data()
