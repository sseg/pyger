"""
Example of a router for handling pub/sub messages.
"""

from pyger.base import AbstractRouter
from enum import Enum


class PubSubRouter(AbstractRouter):
    def __init__(self):
        self.map = {}

    def connect(self, handler, command=None):
        self.map[command] = handler

    def _resolve(self, match_info, **kwargs):
        command_type = kwargs['request']['command']
        found = self.map[command_type]
        return found, match_info


class MessageType(Enum):
    subscribe = 'subscribe'
    unsubscribe = 'unsubscribe'
    publish = 'publish'


def do_subscribe(request):
    resource_key = request['resource']
    print('Got subscribe request for resource "%s"' % resource_key)


def do_unsubscribe(request):
    resource_key = request['resource']
    print('Got unsubscribe request for resource "%s"' % resource_key)


def do_publish(request):
    resource_key = request['resource']
    message = request['message']
    print('Got publish request for resource "%s" with message: "%s"' % (resource_key, message))


def parse_request(message):
    command, resource, *message = message.split(maxsplit=2)
    return {
        'command': MessageType(command.lower()),
        'resource': resource,
        'message': message[0] if message else None
    }


def main():
    import traceback

    router = PubSubRouter()
    router.connect(do_subscribe, command=MessageType.subscribe)
    router.connect(do_unsubscribe, command=MessageType.unsubscribe)
    router.connect(do_publish, command=MessageType.publish)

    info = """
    Requests consist of two or three parts:

        COMMAND RESOURCE_KEY [MESSAGE]

    COMMAND can be any of: subscribe, unsubscribe, publish
    RESOURCE_KEY can be any string without whitespace
    MESSAGE is an optional string that is only used with the publish command.

    Example:
    >>> publish key_foo_bar special message for all listeners of "foo bar"
    """

    print(info)

    while True:
        try:
            raw_request = input('>>> ')
            request = parse_request(raw_request)
            handler, _ = router.match(request=request)
            handler(request)

        except Exception as err:
            traceback.print_exc()


if __name__ == '__main__':
    main()
