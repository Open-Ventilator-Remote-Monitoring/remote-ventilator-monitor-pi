from datetime import datetime, timezone
from random import random

from flask_restful import Api

from plugin.plugin_base import PluginBase


class AlarmSoundPlugin(PluginBase):
    def __init__(self):
        self.end_point = None

    def add_endpoints(self, api: Api) -> None: pass

    def start_plugin(self) -> None: pass

    def get_data(self):
        return self.get_raw_data()

    def get_raw_data(self):
        data = {
            'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        }
        if random() > .5:
            data['alerts'] = {
                "audioAlarm": True
            }
        return data

    def stop_plugin(self) -> None: pass

    def enable_endpoint(self, end_point: str) -> None:
        self.end_point = end_point
