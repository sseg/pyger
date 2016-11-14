from aiohttp import web, abc
from aiohttp.web_urldispatcher import MatchInfoError, UrlMappingMatchInfo, ResourceRoute
from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPNotFound
from pyger.routers import PathRouter, HTTPMethodRouter
from pyger.base import MatchError
import logging


log = logging.getLogger(__name__)


async def hello_v1(request):
    name = request.match_info['name']
    payload = 'Hello %s.' % name
    return web.Response(text=payload)


async def hello_v2(request):
    name = request.match_info['name']
    payload = 'Hi there, %s!' % name
    return web.Response(text=payload)


class PygerRouter(abc.AbstractRouter):
    def __init__(self):
        self.routes = PathRouter()

    def add_route(self, method, path, handler):
        method_router = HTTPMethodRouter()
        method_router.connect(handler, method=method)
        self.routes.connect(method_router, path=path)

    async def resolve(self, request):
        try:
            match = self.routes.match(path=request.path, method=request.method)
        except MatchError:
            log.exception('Not able to resolve request')
            return MatchInfoError(HTTPNotFound())
        route = ResourceRoute(request.method, match.target, match)
        return UrlMappingMatchInfo(match.match_info, route)


if __name__ == '__main__':
    app = web.Application(router=PygerRouter())
    app.router.add_route('GET', '/hello/{name}', hello_v1)
    app.router.add_route('GET', '/hi/{name}', hello_v2)
    web.run_app(app)
