from distutils.core import setup

setup(
    name='sanic_rethinkdb',
    version='0.1',
    packages=['sanic_rethinkdb'],
    url='https://github.com/jamesstidard/sanic-rethinkdb',
    license='MIT',
    author='James Stidard',
    author_email='jamesstidard@gmail.com',
    description='A simple RethinkDB extension for Sanic',
    keywords='sanic database rethinkdb extension',
    platforms=['any'],
    install_requires=[
        'rethinkdb',
        'sanic'])
