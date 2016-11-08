try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


tests_require = [
    'flake8',
    'pytest',
    'pytest-cov'
]


setup(
    name="pyger",
    description="PyGER - Python Generic Extensible Router",
    long_description="""
        PyGER is a library for for building arbitrary routing trees.
    """,
    license="""BSD""",
    version="0.1",
    author="Steven Seguin",
    author_email="steven.seguin@gmail.com",
    maintainer="Steven Seguin",
    maintainer_email="steven.seguin@gmail.com",
    url="https://github.com/sseg/pyger",
    packages=['pyger'],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
