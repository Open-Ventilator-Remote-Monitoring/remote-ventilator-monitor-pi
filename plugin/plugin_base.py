from flask_restful import Api


class PluginBase(object):
    def add_endpoints(self, api: Api) -> None: pass

    def start_plugin(self) -> None: pass

    def get_data(self): pass

    def get_raw_data(self): pass

    def stop_plugin(self) -> None: pass

    def enable_endpoint(self, end_point: str) -> None: pass
