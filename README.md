# PyGER
[![PyPI version](https://badge.fury.io/py/pyger.svg)](https://badge.fury.io/py/pyger)
[![Build status](https://travis-ci.org/sseg/pyger.svg?branch=master)](https://travis-ci.org/sseg/pyger)
[![Code coverage](https://codecov.io/gh/sseg/pyger/branch/master/graph/badge.svg)](https://codecov.io/gh/sseg/pyger)

**Py**thon **G**eneric **E**xtensible **R**outer

PyGER lets you build arbitrary route matchers and nested matching trees. It provides
a flexible and powerful routing layer that enables a clean separation between handling
request _types_ and request _content_.


## Features

**A composable request-matching interface:** PyGER lets you build a routing layer to dispatch
on _any_ facet of a request. This means you can model any state of the world and match it
to your request handler (e.g. HTTP headers, authentication state, the time of day, etc.).

**Powerful built-in URI path routing:** PyGER ships with a pre-made path router which supports
relative paths (`/resource/../actually_another_resource`), regex matched path segments
(`/fruits/{fruit_id:\d+}`), and remainder matching (`/root/{*the_rest_of_the_segments}`). It
supports valid [RFC3986](https://tools.ietf.org/html/rfc3986#section-3.3) paths and it aims
to be the fastest pure-Python router with its feature set.

**Routing and only routing:** By default, PyGER does not invoke any matched handlers, rather it
returns the matched handlers and information from the matching process. This is different
from the behavior you might expect from a controller where you can input a request and the
desired effects are performed. In contrast, PyGER lets you fully isolate choosing a function
from executing it resulting in applications that are easier to read, test, and reason about.

**Support for Python 3.4+:** Official support for Python 3.4 and up, with tests run against both
CPython and PyPy (PyPy3.3 until a newer version is stable).


## Installation

Installing PyGER is as simple as:
```
pip install pyger
```
Preferably inside a virtual environment.


## Basic Usage

Here is a simple example of how you would set up the path router:
```python
from pyger.routers import URIPathRouter

def foo_handler(): pass

def bar_handler(): pass

router = URIPathRouter()
router.connect(foo_handler, path="/foo/{foo_id}")
router.connect(bar_handler, path="/bar/{*path_to_specific_bar}")
```

And here is how you would evaluate paths against it:
```python
>>> router.match(path="/foo/blip")
RouteMatch(target=<function foo_handler>, match_info={'foo_id': 'fizzle'})

>>> router.match(path="/bar/baz/blip/bloop/")
RouteMatch(target=<function bar_handler>, match_info={'*path_to_specific_bar': ('baz', 'blip', 'bloop')})

>>> router.match(path="/unregistered_route")
pyger.base.MatchError
```

Check out the project [examples](https://github.com/sseg/pyger/tree/master/examples) to
see how to build nested routers, or how to integrate PyGER within a web framework.


## Contributing

PyGER is a young project and all contributions are welcome! Feel free to
[open an issue](https://github.com/sseg/pyger/issues)  or suggest a change in a pull request.

The project could particularly benefit from new example scripts integrating PyGER with
your favorite web frameworks, as well as new examples of using PyGER outside of the HTTP domain.


## License

BSD licensed. See the [LICENSE](https://github.com/sseg/pyger/blob/master/LICENSE) file for details.
