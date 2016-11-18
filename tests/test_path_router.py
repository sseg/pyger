from pyger.routers.path import PathMap, URIPathRouter, make_regex_tuple
from pyger.base import MatchError
import re


# PathMap tests

def test_path_map():
    mapping = PathMap()
    sentinel = object()
    mapping.set('abcd', sentinel)
    assert mapping.get('abcd')[0] is sentinel


def test_path_map_named():
    mapping = PathMap()
    sentinel = object()
    mapping.set('{id}', sentinel)
    assert mapping.get('abcd')[0] is sentinel
    assert mapping.get('3521')[1] == 'id'


def test_path_map_regex():
    mapping = PathMap()
    sentinel = object()
    mapping.set('{id:\d+}', sentinel)
    match = mapping.get('1234')
    assert match[0] is sentinel
    assert match[1] == 'id'


def test_path_map_regex_partial_match():
    mapping = PathMap()
    sentinel = object()
    mapping.set('{name:fred}', sentinel)
    try:
        mapping.get('freddie')
    except KeyError:
        pass
    else:
        assert False, 'Expected KeyError'


def test_path_map_plain_lookup_error():
    mapping = PathMap()
    mapping.set('abc', object())
    try:
        mapping.get('bcd')
    except KeyError:
        pass
    else:
        assert False, 'Expected KeyError'


def test_path_map_regex_lookup_error():
    mapping = PathMap()
    mapping.set('{category:[123]*}', object())
    try:
        mapping.get('456')
    except KeyError:
        pass
    else:
        assert False, 'Expected KeyError'


def test_path_map_multiple_keys():
    mapping = PathMap()
    hello = object()
    mapping.set('hello', hello)
    howdy = object()
    mapping.set('howdy', howdy)
    generic_greeting = object()
    mapping.set('{generic_greeting}', generic_greeting)

    assert mapping.get('hello')[0] is hello
    assert mapping.get('howdy')[0] is howdy
    assert mapping.get('other123_()$!@3')[0] is generic_greeting


def test_nested_path_maps():
    inner = PathMap()
    outer = PathMap()
    sentinel = object()
    path = '/outer/inner'
    segments = path.strip('/').split('/')
    outer.set(segments[0], inner)
    inner.set(segments[1], sentinel)

    first_match = outer.get(segments[0])
    second_match = first_match[0].get(segments[1])
    assert second_match[0] is sentinel


# URIPathRouter tests

def test_path_router_connect_resolve():
    router = URIPathRouter()
    sentinel = object()
    router.connect(sentinel, path='/outer/inner')
    match = router.match(path='/outer/inner')
    assert match.target is sentinel


def test_path_router_regex_connect_resolve():
    router = URIPathRouter()
    sentinel = object()
    router.connect(sentinel, path='/objects/{id}')
    object_id = '123abcdef'
    match = router.match(path='/objects/' + object_id)
    assert match.target is sentinel
    assert match.match_info['id'] == object_id


def test_path_router_root():
    router = URIPathRouter()
    sentinel = object()
    router.connect(sentinel, path='/')
    assert router.match(path='/').target is sentinel


def test_path_router_trailing_slash():
    router = URIPathRouter()
    sentinel = object()
    router.connect(sentinel, path='/trailing/')
    router.connect(sentinel, path='/not-trailing')

    assert router.match(path='/trailing/').target is sentinel
    assert router.match(path='/trailing').target is sentinel
    assert router.match(path='/not-trailing').target is sentinel
    assert router.match(path='/not-trailing/').target is sentinel


def test_path_router_no_match_found():
    router = URIPathRouter()
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
    router = URIPathRouter()
    try:
        router.match(patch='/some/path')
    except TypeError:
        pass
    except Exception as err:
        assert False, 'Expected TypeError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected TypeError; no error raised.'


def test_path_map_alternate_arg_key():
    router = URIPathRouter(path_key='foo')
    sentinel = object()
    router.connect(sentinel, foo='/index')
    assert router.match(foo='/index').target is sentinel


def test_path_router_traversal_did_not_lead_to_leaf():
    router = URIPathRouter()
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
    name, compiled = make_regex_tuple(name_pattern)
    assert name == 'command'
    assert compiled == re.compile('(?:he)(?:lp|llo)')


def test_make_regex_tuple_no_regex_provided():
    name_pattern = '{name}'
    default_pattern = '[^/]+'
    name, compiled = make_regex_tuple(name_pattern)
    assert name == 'name'
    assert compiled == re.compile(default_pattern)


def test_path_router_glob_remainder():
    router = URIPathRouter()
    sentinel = object()
    router.connect(sentinel, path='/foo/{*fizz}')
    match = router.match(path='/foo/bar/baz.txt')
    assert match.target is sentinel
    assert match.match_info['*fizz'] == ('bar', 'baz.txt')


def test_path_router_glob_remainder_in_middle():
    router = URIPathRouter()
    sentinel = object()
    try:
        router.connect(sentinel, path='/foo/{*bar}/baz/{*fizz}')
    except ValueError:
        pass
    except Exception as err:
        assert False, 'Expected ValueError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected ValueError; no error raised.'


def test_path_router_too_many_segments():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/bar')
    try:
        router.match(path='/foo/bar/baz')
    except MatchError:
        pass
    except Exception as err:
        assert False, 'Expected MatchError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected MatchError; no error raised.'


def test_path_router_extraneous_path_separators():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/bar')
    match = router.match(path='/foo//bar')
    assert match.target is sentinel


def test_path_router_extraneous_path_separators_with_variable():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/bar/{baz:\d+}/{*pop}')
    match = router.match(path='////foo/bar/2342///abc///def///g')
    assert match.target is sentinel
    assert match.match_info['baz'] == '2342'
    assert match.match_info['*pop'] == ('abc', 'def', 'g')


def test_path_router_single_dot_segments():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/bar/baz')
    match = router.match(path='/foo/./././bar/./baz')
    assert match.target is sentinel


def test_path_router_double_dot_segments():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/bar/baz')
    match = router.match(path='/foo/../foo/bar/../../foo/bar/baz')
    assert match.target is sentinel


def test_path_router_double_dot_segments_limits_at_root():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='')
    match = router.match(path='/foo/bar/../../../../../')
    assert match.target is sentinel


def test_path_router_double_dot_segments_limits_at_root_and_resource():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/bar')
    match = router.match(path='/foo/bar/../../../../../bar')
    assert match.target is sentinel


def test_path_router_dots_as_part_of_path_segments():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/.bar/baz')
    match = router.match(path='/foo/.bar/baz')
    assert match.target is sentinel


def test_path_router_double_dots_as_part_of_path_segments():
    router = URIPathRouter()
    sentinel = object()

    router.connect(sentinel, path='/foo/..bar/baz')
    match = router.match(path='/foo/..bar/baz')
    assert match.target is sentinel
