try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="pyger",
    description="PyGER - Python Generic Extensible Router",
    long_description="""
        PyGER is a library for building arbitrary routing trees.
    """,
    license="""BSD""",
    version="0.1",
    author="Steven Seguin",
    author_email="steven.seguin+pyger@gmail.com",
    maintainer="Steven Seguin",
    maintainer_email="steven.seguin+pyger@gmail.com",
    url="https://github.com/sseg/pyger",
    packages=['pyger'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
