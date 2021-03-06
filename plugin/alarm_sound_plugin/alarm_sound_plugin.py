import threading
from datetime import datetime, timezone

from flask_restful import Api

from plugin.alarm_sound_plugin.alarm_data import AlarmData
from plugin.alarm_sound_plugin.alarm_service import AlarmServiceInterface
from plugin.plugin_base import PluginBase


class AlarmSoundPlugin(PluginBase):
    def __init__(self, alarm_service: AlarmServiceInterface):
        self.end_point = None
        self.is_running = False
        self.lock = threading.Lock()
        self.alarm_service = alarm_service

    def add_endpoints(self, api: Api) -> None: pass

    def start_plugin(self) -> None:
        with self.lock:
            if not self.is_running:
                self.alarm_service.start()
                self.is_running = True

    def get_data(self):
        data = self.get_raw_data()
        return {
            'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            'status': {
                'ready': self.alarm_service.is_ready(),
                'running': self.is_running,
            },
            'alerts': {
                'audioAlarm': data.status,
                'triggered': datetime.fromtimestamp(data.timestamp).isoformat()
            }
        } if data else {
            'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            'status': {
                'ready': self.alarm_service.is_ready(),
                'running': self.is_running,
            },
        }

    def get_raw_data(self) -> AlarmData:
        with self.lock:
            return self.alarm_service.get_data()

    def stop_plugin(self) -> None:
        with self.lock:
            if self.is_running:
                self.alarm_service.stop()
                self.is_running = False

    def enable_endpoint(self, end_point: str) -> None:
        self.end_point = end_point
