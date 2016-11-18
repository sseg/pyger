from pyger.base import AbstractRouter


class MockRouter(AbstractRouter):
    def connect(self, handler, **kwargs):
        pass

    def _resolve(self, match_info, **kwargs):
        pass


def test_base_router_exception_builder():
    default_exc_router = MockRouter(raises=Exception)
    exc = default_exc_router._build_exception(foo='bar', baz=2)
    assert exc._pyger == {
        'router': default_exc_router,
        'foo': 'bar',
        'baz': 2
    }
