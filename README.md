# sanic-rethinkdb
A simple RethinkDB extension for Sanic.

Warning: very much a work-in-progress. Not nailed down how I'd want this to work yet. Also be aware the connection isn't threadsafe if you are using multiple workers.

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
