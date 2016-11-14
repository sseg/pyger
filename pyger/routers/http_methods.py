from pyger.base import AbstractRouter


class HTTPMethodRouter(AbstractRouter):
    def __init__(self, method_key='method', method_any='*'):
        self.method_key = method_key
        self.method_any = method_any
        self.map = {}

    def connect(self, handler, **kwargs):
        method = self._get_method_arg(kwargs)
        self.map[method] = handler

    def resolve(self, match_info, **kwargs):
        sentinel = object()
        default = self.map.get(self.method_any, sentinel)
        if default is not sentinel:
            return default, {**match_info}
        method = self._get_method_arg(kwargs)
        return self.map[method], {**match_info}

    def _get_method_arg(self, kwarg_dict):
        method = kwarg_dict.get(self.method_key)
        if method is None:
            raise TypeError(
                'Expected keyword argument "{method_key}" but received {passed_args}'.format(
                    method_key=self.method_key, passed_args=list(kwarg_dict.keys())
                )
            )
        return method

    def keys(self):
        return self.map.keys()
