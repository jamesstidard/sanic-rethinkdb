import rethinkdb as r

import pytest

from enum import Enum

from sanic import Sanic
from sanic.response import json
from sanic_rethinkdb import RethinkDB


class InitType(Enum):
    EAGER = 0
    LAZY = 1


async def get_user(request, uuid: str):
    conn = await request.app.rdb.connection()
    user = await r.table('users').get(uuid).run(conn)
    return json(user)


@pytest.fixture(params=[InitType.EAGER, InitType.LAZY])
def app(request):
    app_ = Sanic(__name__)

    if request.param == InitType.EAGER:
        app_.rdb = RethinkDB(app_)
    elif request.param == InitType.LAZY:
        app_.rdb = RethinkDB()
        app_.rdb.init_app(app_)

    app_.add_route(get_user, '/users/<uuid>')

    return app_
