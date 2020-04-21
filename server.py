from typing import Dict

from flask import Flask
from flask_restful import Api

from plugin.plugin_base import PluginBase


class Server:
    def __init__(self, app: Flask, plugins: Dict[str, PluginBase]):
        self.app = app
        self.api = Api(self.app)
        self.plugins = plugins

    def setup_routing(self):
        for key, plugin in self.plugins.items():
            plugin.add_endpoints(self.api)

    def setup(self):
        for key, plugin in self.plugins.items():
            plugin.start_plugin()
        self.setup_routing()

    def shut_down(self):
        for key, plugin in self.plugins.items():
            plugin.stop_plugin()
