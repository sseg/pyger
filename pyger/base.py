from abc import ABCMeta, abstractmethod
from collections import namedtuple


RouteMatch = namedtuple('RouteMatch', ['target', 'match_info'])


class MatchError(LookupError):
    pass


class AbstractRouter(metaclass=ABCMeta):
    """
    A router implementation exposes a public API consisting of at least the methods
    `connect` and `match`.
    """
    def __init__(self, raises=MatchError):
        self.exc_class = raises

    @abstractmethod
    def connect(self, handler, **kwargs):
        """
        A method that registers new handlers to routes.

        Args:
            handler (Any): The value resolved by a match.

            **kwargs: All arguments necessary to update the router's state. These
            are the same keyword arguments that will be used to later match a route.

        Returns:
            Anything.
        """

    def match(self, _match_info=None, **kwargs):
        """
        Match arguments against the router.

        If the matched handler is itself a router node, that node's match method
        is invoked with the updated match_info dict and keyword arguments.

        Args:
            match_info (Dict[str, Any]): Collected data from resvolvers in the
            routing tree. Used to gather artifacts of routing.

            **kwargs: Any arguments used to resolve route.

        Returns:
            RouteMatch

        Raises:
            yes
        """
        match_info = {} if _match_info is None else _match_info
        handler, updated_match_info = self._resolve(match_info, **kwargs)
        if isinstance(handler, AbstractRouter):
            return handler.match(_match_info=updated_match_info, **kwargs)
        return RouteMatch(target=handler, match_info=updated_match_info)

    @abstractmethod
    def _resolve(self, match_info, **kwargs):
        """
        A method that finds a registered route handler.

        Args:
            match_info (Dict[str, Any]): Collected data from resvolvers in the
            routing tree. Used to gather artifacts of routing.

            **kwargs: Any arguments used to resolve a route.

        Returns:
            A tuple of a matched handler and an updated match_info dict.

        Raises:
            Any exception type.
        """

    def _build_exception(self, **extra):
        exc = self.exc_class()
        exc._pyger = extra
        exc._pyger.update(router=self)
        return exc
