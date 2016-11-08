from pyger.routers import SimpleRouter


def test_resolve():
    sentinel = object()
    router = SimpleRouter(sentinel)

    value = router.resolve({})
    assert value is sentinel


def test_nested_match():
    sentinel = object()
    inner_router = SimpleRouter(sentinel)
    outer_router = SimpleRouter(inner_router)

    value = outer_router.match({})
    assert value is sentinel


def test_connect():
    router = SimpleRouter(None)
    assert router.handler is None

    sentinel = object()
    router.connect(sentinel)
    assert router.handler is sentinel
