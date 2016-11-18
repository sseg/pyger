from pyger.routers.http_methods import HTTPMethodRouter


def test_method_router_connect_resolve():
    router = HTTPMethodRouter()
    sentinel = object()
    router.connect(sentinel, method='FOO')
    match = router.match(method='FOO')
    assert match.target is sentinel


def test_method_router_custom_method_key():
    router = HTTPMethodRouter(method_key='the_method')
    sentinel = object()
    router.connect(sentinel, the_method='FOO')
    match = router.match(the_method='FOO')
    assert match.target is sentinel


def test_method_router_wildcard_match():
    router = HTTPMethodRouter()
    sentinel = object()
    router.connect(sentinel, method='*')
    match = router.match(method='FOO')
    assert match.target is sentinel


def test_method_router_custom_wildcard():
    router = HTTPMethodRouter(method_any='@#$')
    sentinel = object()
    router.connect(sentinel, method='@#$')
    match = router.match(method='FOO')
    assert match.target is sentinel


def test_method_router_available_keys():
    router = HTTPMethodRouter()
    router.connect(None, method='GET')
    router.connect(None, method='POST')
    assert set(router.keys()) == {'GET', 'POST'}


def test_method_router_invalid_method_key_passsed():
    router = HTTPMethodRouter(method_key='a')
    try:
        router.connect(None, b='BAZ')
    except TypeError as err:
        assert err.args[0] == "Expected keyword argument 'a' but received ['b']"
    except Exception as err:
        assert False, 'Expected TypeError; %s raised.' % err.__class__.__name__
    else:
        assert False, 'Expected TypeError; no error raised.'


def test_method_not_found():
    router = HTTPMethodRouter()
    assert router.map == {}
    try:
        router.match(method='PATCH')
    except Exception as err:
        assert err._pyger == {
            'router': router,
            'kwargs': {'method': 'PATCH'}
        }
    else:
        assert False, 'Expected MatchError; no error raised.'
