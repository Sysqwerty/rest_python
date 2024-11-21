# rest_python

Make sure you have [Docker Engine](https://docs.docker.com/engine/install/) installed first

```shell
docker run --name rest_python_jwt -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
```

```shell
alembic upgrade head
```

```shell
fastapi dev main.py
```

Open in browser SWAGGER doc: [link](http://127.0.0.1:8000/docs#/)