from pyger.base import AbstractRouter, MatchError
from collections.abc import MutableMapping
import re


class PathRouter(AbstractRouter):
    """
    A router which connects based on path hierarchies.

    Args:
        path_key (str): the name of the keyword argument to be used when matching
        routes.

    >>> router = PathRouter()
    >>> router.connect(index_handler, path='/index')
    >>> router.connect(article_handler, path='/articles/{category}/{id:[0-9]+}')
    >>> router.match('/index')
    RouteMatch(target=index_handler, match_info={})
    >>> router.match('/articles/books/123')
    RouteMatch(target=article_handler, match_info={'category': 'books', 'id': '123'})
    >>> router.match('/not/valid')
    MatchError
    """

    def __init__(self, path_key='path', raises=MatchError):
        self.path_key = path_key
        self.map = PathMap()
        self.exc_class = raises

    def connect(self, handler, **kwargs):
        path = self._get_path_arg(kwargs)
        segments = path.strip('/').split('/')
        node = self.map
        for segment in segments[:-1]:
            node[segment] = PathMap()
            node = node[segment][0]
        node[segments[-1]] = handler

    def _resolve(self, match_info, **kwargs):
        path = self._get_path_arg(kwargs)
        segments = path.strip('/').split('/')
        try:
            found, dispatch_matches = self._traverse_map(segments)
        except LookupError as err:
            raise self._build_exception(kwargs=kwargs)
        if isinstance(found, PathMap):
            # traversal did not lead to a leaf node
            raise self._build_exception(kwargs=kwargs)
        return found, {**match_info, **dispatch_matches}

    def _get_path_arg(self, kwarg_dict):
        path = kwarg_dict.get(self.path_key)
        if path is None:
            raise TypeError(
                'Expected keyword argument "{path_key}" but received {passed_args}'.format(
                    path_key=self.path_key, passed_args=list(kwarg_dict.keys())
                )
            )
        return path

    def _traverse_map(self, path_segments):
        node = self.map
        dispatch_matches = {}
        for segment in path_segments:
            node, segment_name = node[segment]
            if segment_name is not None:
                dispatch_matches[segment_name] = segment
        return node, dispatch_matches


class PathMap:
    def __init__(self):
        self.plain_segments = {}
        self.regex_segments = {}

    def __getitem__(self, name):
        try:
            return self.plain_segments[name], None
        except KeyError:
            for (segment_name, re_pattern), value in self.regex_segments.items():
                if re_pattern.fullmatch(name):
                    return value, segment_name
            raise

    def __setitem__(self, name, value):
        if name and name[0] == '{':
            regex_tuple = make_regex_tuple(name)
            self.regex_segments[regex_tuple] = value
        else:
            self.plain_segments[name] = value


def make_regex_tuple(name_pattern, default='[^/]+'):
    pattern_pair = name_pattern.strip('{}').split(':')
    name = pattern_pair[0]
    if len(pattern_pair) == 1:
        pattern = default
    else:
        pattern = pattern_pair[1]
    return name, re.compile(pattern)
