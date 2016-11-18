from pyger.routers.unit import UnitRouter


def test_resolve():
    sentinel = object()
    router = UnitRouter(sentinel)

    value, match_info = router._resolve({})
    assert value is sentinel


def test_nested_match():
    sentinel = object()
    inner_router = UnitRouter(sentinel)
    outer_router = UnitRouter(inner_router)

    value = outer_router.match(_match_info={})
    assert value.target is sentinel


def test_connect():
    router = UnitRouter(None)
    assert router.handler is None

    sentinel = object()
    router.connect(sentinel)
    assert router.handler is sentinel
