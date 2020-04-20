from werkzeug.datastructures import EnvironHeaders


class AuthorizationService(object):
    def is_authorized(self, authorization: str) -> bool: pass


class ApiKeyAuthorizationService(AuthorizationService):
    def __init__(self, authorization: str):
        self.authorization = authorization

    def is_authorized(self, headers: EnvironHeaders) -> bool:
        return self.authorization == headers.get('Authorization')


class NoAuthorizationService(AuthorizationService):
    def is_authorized(self, authorization: str) -> bool:
        return True
