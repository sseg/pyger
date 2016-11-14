from abc import ABCMeta, abstractmethod
from collections import namedtuple


RouteMatch = namedtuple('RouteMatch', ['target', 'match_info'])


class MatchError(LookupError):
    pass


class AbstractRouter(metaclass=ABCMeta):
    @abstractmethod
    def resolve(self, match_info, **kwargs):
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
        """
        match_info = {} if _match_info is None else _match_info
        try:
            handler, updated_match_info = self.resolve(match_info, **kwargs)
        except Exception as err:
            raise MatchError from err
        if isinstance(handler, AbstractRouter):
            return handler.match(_match_info=updated_match_info, **kwargs)
        return RouteMatch(target=handler, match_info=updated_match_info)

    @abstractmethod
    def connect(self, handler, **kwargs):
        """
        A method which registers new handlers to routes.

        Args:
            handler (Any): The value resolved by a match.

            **kwargs: All arguments necessary to update the router's state.

        Returns:
            Anything.
        """
