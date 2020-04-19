from typing import Dict

from flask import jsonify
from flask_restful import Resource, Api

from plugin.plugin_base import PluginBase


class StatusPluginGetStatus(Resource):
    def __init__(self, **kwargs):
        self.plugin = kwargs['plugin']

    def get(self):
        current_data = self.plugin.get_data()
        return jsonify(current_data)


class StatusPlugin(PluginBase):
    def __init__(self, plugins: Dict[str, PluginBase]):
        self.plugins = plugins
        self.end_point = None

    def add_endpoints(self, api: Api) -> None:
        if self.end_point:
            api.add_resource(StatusPluginGetStatus, self.end_point, resource_class_kwargs={'plugin': self})

    def start_plugin(self) -> None:
        for plugin in self.plugins.values():
            plugin.start_plugin()

    def stop_plugin(self) -> None:
        for plugin in self.plugins.values():
            plugin.stop_plugin()

    def get_data(self):
        data = {}
        for key in self.plugins.keys():
            data[key] = self.plugins[key].get_data()
        return data

    def enable_endpoint(self, end_point: str) -> None:
        self.end_point = end_point
