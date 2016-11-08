from pyger.base import AbstractRouter


class SimpleRouter(AbstractRouter):
    def __init__(self, handler):
        self.handler = handler

    def resolve(self, match_info, **kwargs):
        return self.handler

    def connect(self, handler, **kwargs):
        self.handler = handler
