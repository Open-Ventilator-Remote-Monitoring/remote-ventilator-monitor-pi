import threading
from datetime import datetime
from threading import Thread

from gpiozero import Button

from plugin.alarm_sound_plugin.alarm_data import AlarmData
from plugin.alarm_sound_plugin.alarm_handler import AlarmHandler


class AlarmServiceInterface(Thread):
    def get_data(self) -> AlarmData: pass


class AlarmService(AlarmServiceInterface):
    def __init__(self, alarm_handler: AlarmHandler, trigger: Button):
        super().__init__()
        self.alarm_handler = alarm_handler
        self.trigger = trigger
        self.lock = threading.Lock()
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        with self.lock:
            self.alarm_handler.update_alarm_data(AlarmData(True, timestamp=datetime.utcnow().timestamp()))
            self.trigger.wait_for_active()
        while self.is_running:
            self.trigger.wait_for_inactive()
            with self.lock:
                self.alarm_handler.update_alarm_data(AlarmData(True, timestamp=datetime.utcnow().timestamp()))
            self.trigger.wait_for_active()
            with self.lock:
                self.alarm_handler.update_alarm_data(AlarmData(False, timestamp=datetime.utcnow().timestamp()))

    def stop(self):
        with self.lock:
            self.is_running = False

    def get_data(self) -> AlarmData:
        with self.lock:
            return self.alarm_handler.get_alarm_data()




