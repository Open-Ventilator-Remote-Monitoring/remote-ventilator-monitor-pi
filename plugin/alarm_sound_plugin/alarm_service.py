import threading
from datetime import datetime
from threading import Thread
from time import sleep

from gpiozero import Button

from plugin.alarm_sound_plugin.alarm_data import AlarmData
from plugin.alarm_sound_plugin.alarm_handler import AlarmHandler


class AlarmServiceInterface(Thread):
    def get_data(self) -> AlarmData: pass
    def is_ready(self) -> bool: pass
    def stop(self) -> None: pass


class AlarmService(AlarmServiceInterface):
    def __init__(self, alarm_handler: AlarmHandler, trigger: Button):
        super().__init__()
        self.alarm_handler = alarm_handler
        self.trigger = trigger
        self.lock = threading.Lock()
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        while self.is_running:
            sleep(.01)
            self.alarm_handler.update_ready(True)
            if self.trigger.is_active:
                self.alarm_handler.update_alarm_data(AlarmData(True, timestamp=datetime.utcnow().timestamp()))
            else:
                self.alarm_handler.update_alarm_data(AlarmData(False, timestamp=datetime.utcnow().timestamp()))

    def stop(self) -> None:
        with self.lock:
            self.is_running = False

    def get_data(self) -> AlarmData:
        with self.lock:
            return self.alarm_handler.get_alarm_data()

    def is_ready(self) -> bool:
        return self.alarm_handler.get_ready()




