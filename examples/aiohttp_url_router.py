from aiohttp import web, abc
from aiohttp.web_urldispatcher import MatchInfoError, UrlMappingMatchInfo, ResourceRoute
from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPNotFound
from pyger.routers import URIPathRouter, HTTPMethodRouter
from pyger.base import MatchError


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
        self.routes = URIPathRouter(raises=HTTPNotFound)

    def add_route(self, method, path, handler):  # TODO use API version as path segments in subrouter
        method_router = HTTPMethodRouter()  # raises default MatchError
        method_router.connect(handler, method=method)
        self.routes.connect(method_router, path=path)

    async def resolve(self, request):
        try:
            match = self.routes.match(path=request.path, method=request.method)
        except Exception as err:
            if isinstance(err, MatchError):  # the HTTPMethodRouter raised an error
                method_key = err._pyger['router'].method_key
                method = err._pyger['kwargs'][method_key]
                allowed_methods = err._pyger['router'].keys()
                err = HTTPMethodNotAllowed(method, allowed_methods)
            return MatchInfoError(err)
        route = ResourceRoute(request.method, match.target, match)
        return UrlMappingMatchInfo(match.match_info, route)


if __name__ == '__main__':
    app = web.Application(router=PygerRouter())
    app.router.add_route('GET', '/hello/{name}', hello_v1)
    app.router.add_route('GET', '/hi/{name}', hello_v2)
    web.run_app(app)
