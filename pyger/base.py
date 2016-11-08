from abc import ABCMeta, abstractmethod


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
            A matched handler.

        Raises:
            Any exception type.
        """

    def match(self, match_info, **kwargs):
        """
        Match arguments against the router.

        If the matched handler is itself a router node, that node's match method
        is invoked with the updated match_info dict and keyword arguments.

        Args:
            match_info (Dict[str, Any]): Collected data from resvolvers in the
            routing tree. Used to gather artifacts of routing.

            **kwargs: Any arguments used to resolve route.

        Returns:
            A matched handler.
        """
        matched = self.resolve(match_info, **kwargs)
        if isinstance(matched, AbstractRouter):
            return matched.match(match_info, **kwargs)
        return matched

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
