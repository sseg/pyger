from pyger.base import AbstractRouter


class UnitRouter(AbstractRouter):
    def __init__(self, handler):
        self.handler = handler

    def _resolve(self, match_info, **kwargs):
        return self.handler, dict(**match_info)

    def connect(self, handler, **kwargs):
        self.handler = handler
