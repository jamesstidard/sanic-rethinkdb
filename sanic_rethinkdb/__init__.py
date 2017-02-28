import os
import asyncio

from functools import partial

import rethinkdb as r

r.set_loop_type('asyncio')


class RethinkDB:

    def __init__(self, app=None):
        self._connection_maker = r.connect
        self._connections = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('RETHINKDB_HOST', 'localhost')
        app.config.setdefault('RETHINKDB_PORT', '28015')
        app.config.setdefault('RETHINKDB_AUTH', '')
        app.config.setdefault('RETHINKDB_DB', 'test')

        @app.listener('after_server_stop')
        async def teardown():
            closers = [c.close for c in self._connections]
            await asyncio.wait(closers)

        self._connection_maker = partial(r.connect,
                                         auth_key=app.config.RETHINKDB_AUTH,
                                         host=app.config.RETHINKDB_HOST,
                                         port=app.config.RETHINKDB_PORT,
                                         db=app.config.RETHINKDB_DB)

    async def connection(self):
        pid = os.getpid()
        if pid in self._connections:
            return self._connections[pid]
        else:
            connection = await self._connection_maker()
            return self._connections.setdefault(pid, connection)
