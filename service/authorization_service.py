class AuthorizationService(object):
    def is_authorized(self, api_key: str) -> bool: pass


class ApiKeyAuthorizationService(AuthorizationService):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def is_authorized(self, api_key: str) -> bool:
        return api_key == self.api_key


class NoAuthorizationService(AuthorizationService):
    def is_authorized(self, api_key: str) -> bool:
        return True
