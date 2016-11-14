from pyger.routers.path import PathMap, PathRouter, make_regex_tuple
from pyger.base import MatchError
import re


def test_path_map():
    mapping = PathMap()
    sentinel = object()
    mapping['abcd'] = sentinel
    assert mapping['abcd'][0] is sentinel


def test_path_map_named():
    mapping = PathMap()
    sentinel = object()
    mapping['{id}'] = sentinel
    assert mapping['abcd'][0] is sentinel
    assert mapping['3521'][1] == 'id'


def test_path_map_regex():
    mapping = PathMap()
    sentinel = object()
    mapping['{id:\d+}'] = sentinel
    match = mapping['1234']
    assert match[0] is sentinel
    assert match[1] == 'id'


def test_path_map_plain_lookup_error():
    mapping = PathMap()
    mapping['abc'] = object()
    try:
        mapping['bcd']
    except KeyError:
        pass
    else:
        assert False, 'Expected KeyError'


def test_path_map_regex_lookup_error():
    mapping = PathMap()
    mapping['{category:[123]*}'] = object()
    try:
        mapping['456']
    except KeyError:
        pass
    else:
        assert False, 'Expected KeyError'


def test_path_map_multiple_keys():
    mapping = PathMap()
    hello = object()
    mapping['hello'] = hello
    howdy = object()
    mapping['howdy'] = howdy
    generic_greeting = object()
    mapping['{generic_greeting}'] = generic_greeting

    assert mapping['hello'][0] is hello
    assert mapping['howdy'][0] is howdy
    assert mapping['other123_()$!@3'][0] is generic_greeting


def test_nested_path_maps():
    inner = PathMap()
    outer = PathMap()
    sentinel = object()
    path = '/outer/inner'
    segments = path.strip('/').split('/')
    outer[segments[0]] = inner
    inner[segments[1]] = sentinel

    first_match = outer[segments[0]]
    second_match = first_match[0][segments[1]]
    assert second_match[0] is sentinel


def test_path_router_connect_resolve():
    router = PathRouter()
    sentinel = object()
    router.connect(sentinel, path='/outer/inner')
    match = router.match(path='/outer/inner')
    assert match.target is sentinel


def test_path_router_regex_connect_resolve():
    router = PathRouter()
    sentinel = object()
    router.connect(sentinel, path='/objects/{id}')
    object_id = '123abcdef'
    match = router.match(path='/objects/' + object_id)
    assert match.target is sentinel
    assert match.match_info['id'] == object_id


def test_path_router_root():
    router = PathRouter()
    sentinel = object()
    router.connect(sentinel, path='/')
    assert router.match(path='/').target is sentinel


def test_path_router_trailing_slash():
    router = PathRouter()
    sentinel = object()
    router.connect(sentinel, path='/trailing/')
    router.connect(sentinel, path='/not-trailing')

    assert router.match(path='/trailing/').target is sentinel
    assert router.match(path='/trailing').target is sentinel
    assert router.match(path='/not-trailing').target is sentinel
    assert router.match(path='/not-trailing/').target is sentinel


def test_path_router_no_match_found():
    router = PathRouter()
    router.connect(object(), path='/some/path')
    try:
        router.match(path='/some/other/path')
    except MatchError:
        pass
    except Exception as err:
        assert False, 'Expected MatchError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected MatchError; no error raised.'


def test_path_router_missing_arg():
    router = PathRouter()
    try:
        router.match(patch='/some/path')
    except TypeError:
        pass
    except Exception as err:
        assert False, 'Expected TypeError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected TypeError; no error raised.'


def test_path_map_alternate_arg_key():
    router = PathRouter(path_key='foo')
    sentinel = object()
    router.connect(sentinel, foo='/index')
    assert router.match(foo='/index').target is sentinel


def test_path_router_traversal_did_not_lead_to_leaf():
    router = PathRouter()
    router.connect(object(), path='/some/long/path')
    try:
        router.match(path='/some/long')
    except MatchError:
        pass
    except Exception as err:
        assert False, 'Expected MatchError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected MatchError; no error raised.'


def test_make_regex_tuple():
    name_pattern = '{command:(?:he)(?:lp|llo)}'
    pair = make_regex_tuple(name_pattern)
    name, compiled = pair[0], pair[1]
    assert name == 'command'
    assert compiled == re.compile('(?:he)(?:lp|llo)')
