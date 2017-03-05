import asyncio

import rethinkdb as r

r.set_loop_type('asyncio')


class Settings:

    def __init__(self, host='localhost', port=28015, db='test', user='admin', password=None, auth_key=None, ssl=None):
        if not ssl:
            ssl = {}

        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.auth_key = auth_key
        self.ssl = ssl


class RethinkDB:

    def __init__(self, app=None, *, settings: Settings=None):
        self._connections = set()
        self._settings = settings

        if app is not None:
            self.init_app(app, settings=settings)

    def init_app(self, app, *, settings: Settings=None):
        if not settings:
            settings = Settings()

        settings.host = app.config.setdefault('RETHINKDB_HOST', settings.host)
        settings.port = app.config.setdefault('RETHINKDB_PORT', settings.port)
        settings.db   = app.config.setdefault('RETHINKDB_DB', settings.db)
        settings.user = app.config.setdefault('RETHINKDB_USER', settings.user)
        settings.password = app.config.setdefault('RETHINKDB_PASSWORD', settings.password)
        settings.auth_key = app.config.setdefault('RETHINKDB_AUTH', settings.auth_key)
        settings.ssl = app.config.setdefault('RETHINKDB_SSL', settings.ssl)

        self._settings = settings

        @app.listener('after_server_stop')
        async def teardown(*_):
            closers = [c.close for c in self._connections]
            await asyncio.wait(closers)

    async def connection(self):
        connection = await r.connect(
            host=self._settings.host,
            port=self._settings.port,
            db=self._settings.db,
            user=self._settings.user,
            password=self._settings.password,
            auth_key=self._settings.auth_key,
            ssl=self._settings.ssl)
        self._connections.add(connection)
        return connection

    async def drop_and_remake(self, model):
        connection = await self.connection()

        try:
            await r.db_drop(self._settings.db).run(connection)
        except r.errors.ReqlOpFailedError as e:
            pass

        await r.db_create(self._settings.db).run(connection)

        for table_name, options in model.items():
            await r.db(self._settings.db).table_create(table_name, **options).run(connection)
