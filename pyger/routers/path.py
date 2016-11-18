from pyger.base import AbstractRouter, MatchError
import re


def get_path_segments(path):
    base_segments = [x for x in path.split('/') if x and x != '.']
    output_buffer = []
    for s in base_segments:
        if s == '..':
            output_buffer = output_buffer[:-1]
        else:
            output_buffer.append(s)
    return output_buffer


class URIPathRouter(AbstractRouter):
    """
    A router which dispatches based on path hierarchies.

    Args:
        path_key (str, optional): the name of the keyword argument to be used
        when matching routes. Defaults to "path".

        raises (Exception, optional): an exception class to be raised when no
        match is found. Defaults to `pyger.base.MatchError`.

    Usage:
        >>> router = URIPathRouter()
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
        self._root_marker = ''

    def connect(self, handler, **kwargs):
        path = self._get_path_arg(kwargs)
        segments = get_path_segments(path)
        node = self.map

        for segment in segments[:-1]:
            if segment.startswith('{*'):
                raise ValueError(
                    'Globbing path segments (`*foo`) can only be '
                    'used as the last segment in a path'
                )
            next_node = PathMap()
            node.set(segment, next_node)
            node = next_node

        last_segment = segments[-1] if segments else self._root_marker
        node.set(last_segment, handler)

    def _resolve(self, match_info, **kwargs):
        path = self._get_path_arg(kwargs)
        segments = get_path_segments(path)
        try:
            found, dispatch_matches = self.traverse_map(segments)
        except LookupError as err:
            raise self._build_exception(kwargs=kwargs) from err
        if isinstance(found, PathMap):
            # traversal did not lead to a leaf node
            raise self._build_exception(kwargs=kwargs)
        updated_match = match_info.copy()
        updated_match.update(dispatch_matches)
        return found, updated_match

    def _get_path_arg(self, kwarg_dict):
        path = kwarg_dict.get(self.path_key)
        if path is None:
            raise TypeError(
                'Expected keyword argument "{path_key}" but received {passed_args}'.format(
                    path_key=self.path_key, passed_args=list(kwarg_dict.keys())
                )
            )
        return path

    def traverse_map(self, path_segments):
        if not path_segments:
            target, _ = self.map.get(self._root_marker)
            return target, {}
        return self._traverse_map(path_segments)

    def _traverse_map(self, path_segments):
        # initial node and match state
        node = self.map
        dispatch_matches = {}

        for i, segment in enumerate(path_segments):
            if not isinstance(node, PathMap):
                # we have more segments to process but we ran out of nodes
                raise KeyError

            # get the next node
            node, segment_name = node.get(segment)

            if segment_name is not None:
                # build match dict
                if segment_name.startswith('*'):
                    # this node collects following path segments
                    dispatch_matches[segment_name] = tuple(
                        segment for segment in path_segments[i:]
                    )
                    break  # globbing variables only allowed as last segment
                else:
                    dispatch_matches[segment_name] = segment

        return node, dispatch_matches


class PathMap:
    def __init__(self):
        self.plain_segments = {}
        self.regex_segments = {}

    def get(self, name):
        try:
            return self.plain_segments[name], None
        except KeyError:
            for (segment_name, re_pattern), value in self.regex_segments.items():
                match = re_pattern.match(name)
                if match and match.group(0) == name:
                    return value, segment_name
            raise

    def set(self, name, value):
        if name.startswith('{'):
            regex_tuple = make_regex_tuple(name)
            self.regex_segments[regex_tuple] = value
        else:
            self.plain_segments[name] = value


def make_regex_tuple(name_pattern, default='[^/]+'):
    pattern_pair = name_pattern.strip('{}').split(':', maxsplit=1)
    name = pattern_pair[0]
    if len(pattern_pair) == 1:
        pattern = default
    else:
        pattern = pattern_pair[1]
    return name, re.compile(pattern)
