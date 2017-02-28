import pytest

from inspect import isawaitable
from rethinkdb import Connection


def test_connection_isawaitable(app):
    assert isawaitable(app.rdb.connection())


@pytest.mark.asyncio
async def test_connection_is_connection(app):
    connection = await app.rdb.connection()
    assert isinstance(connection, Connection)
