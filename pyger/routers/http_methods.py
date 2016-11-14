from pyger.base import AbstractRouter, MatchError


class HTTPMethodRouter(AbstractRouter):
    def __init__(self, method_key='method', method_any='*', raises=MatchError):
        self.method_key = method_key
        self.method_any = method_any
        self.map = {}
        self.exc_class = raises

    def connect(self, handler, **kwargs):
        method = self._get_method_arg(kwargs)
        self.map[method] = handler

    def _resolve(self, match_info, **kwargs):
        sentinel = object()
        default = self.map.get(self.method_any, sentinel)
        if default is not sentinel:
            return default, {**match_info}
        method = self._get_method_arg(kwargs)
        try:
            return self.map[method], {**match_info}
        except LookupError as err:
            raise self._build_exception(kwargs=kwargs) from err

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
