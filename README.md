# sanic-rethinkdb
A simple RethinkDB extension for Sanic.

## Installation
```bash
$ pip install sanic_rethinkdb
```

## Usage
```python
import rethinkdb as r

from sanic import Sanic
from sanic.response import json
from sanic_rethinkdb import RethinkDB


app = Sanic(__name__)
rdb = RethinkDB(app)

@app.get("/users/<uuid:str>")
async def hello(request, uuid: str):
    conn = await rdb.connection()
    user = await r.table('users').get(uuid).run(conn)
    return json(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```