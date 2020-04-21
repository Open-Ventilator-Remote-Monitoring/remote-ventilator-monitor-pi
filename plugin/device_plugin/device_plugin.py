from datetime import datetime, timezone

from flask_restful import Api

from plugin.plugin_base import PluginBase


class DevicePlugin(PluginBase):
    def __init__(self, device_id: str, roles: dict):
        self.device_id = device_id
        self.roles = roles
        self.end_point = None

    def add_endpoints(self, api: Api) -> None: pass

    def start_plugin(self) -> None: pass

    def get_data(self):
        return self.get_raw_data()

    def get_raw_data(self):
        return {
            'currentTime': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            'id': self.device_id,
            'roles': self.roles,
        }

    def stop_plugin(self) -> None: pass

    def enable_endpoint(self, end_point: str) -> None:
        self.end_point = end_point
