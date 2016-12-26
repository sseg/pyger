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
    version="0.2",
    author="Steven Seguin",
    author_email="steven.seguin+pyger@gmail.com",
    maintainer="Steven Seguin",
    maintainer_email="steven.seguin+pyger@gmail.com",
    url="https://github.com/sseg/pyger",
    packages=['pyger'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Internet'
    ]
)
