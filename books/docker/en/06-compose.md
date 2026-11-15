# 6. Docker Compose (several containers)

## What you will learn

- Describing several containers together in compose.yaml
- Commands such as up, down and logs
- Connecting containers to each other by name

## What is Compose?

When you combine several containers, like a web app and a database, typing `docker run` many times with long options is tiring. **Docker Compose** is a tool that lets you write all of that in one file, `compose.yaml`, and run everything together with one command.

## What we will make

We connect the Flask app from Chapter 4 to a database that counts (Redis). The number goes up every time you open the page.

```text
counter/
├── app.py
├── requirements.txt
├── Dockerfile          ← the same as Chapter 4
└── compose.yaml
```

`app.py`:

```python
import os
from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379)

@app.route("/")
def hello():
    n = r.incr("hits")          # add 1 and return the new number
    return f"This page has been viewed {n} times.\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:

```text
flask
redis
```

`compose.yaml`:

```yaml
services:
  web:                      # the service name (containers reach each other by this name)
    build: .                # build the image from the Dockerfile here
    ports:
      - "5000:5000"         # the same as docker run -p
    environment:
      - REDIS_HOST=redis    # connect to the service named "redis"
    depends_on:
      - redis               # start redis first
  redis:
    image: redis:7          # use the image from Docker Hub as is
    volumes:
      - redis-data:/data    # keep the count in a volume

volumes:
  redis-data:
```

- YAML shows grouping with indentation (spaces). Tabs cannot be used
- Services in the same compose.yaml join the same network and reach each other by **service name** (the name `redis` is itself the address of the other container)
- The `version: "3"` at the top in the old style is no longer needed

## Running it

```bash
docker compose up -d --build     # build, and run everything in the background
curl http://localhost:5000       # This page has been viewed 1 times.
curl http://localhost:5000       # This page has been viewed 2 times.
```

| Command | What it does |
| --- | --- |
| `docker compose up -d` | Run everything (`--build` rebuilds the images) |
| `docker compose ps` | List the running services |
| `docker compose logs -f web` | Keep watching web's logs (Ctrl + C to stop) |
| `docker compose exec redis redis-cli` | Type commands inside the redis container |
| `docker compose restart web` | Restart only web |
| `docker compose down` | Stop everything and remove the containers (volumes are kept) |
| `docker compose down -v` | Also remove the volumes (the data is removed too) |

In VS Code, you can also right-click `compose.yaml` → "Compose Up" or "Compose Down". Under CONTAINERS in the whale icon, they are grouped by project name (the folder name).

## During development, combine it with a bind mount

If rebuilding every time you change the code is a hassle, connect your local folder and use Flask's automatic reload.

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    volumes:
      - .:/app                                   # connect the local folder to /app
    command: flask --app app run --host 0.0.0.0 --port 5000 --debug   # reloads automatically when you edit
    depends_on:
      - redis
  redis:
    image: redis:7
```

`command` overrides the Dockerfile's `CMD`.

## Summary

- List containers under `services` in `compose.yaml`: `build` or `image`, plus `ports`, `environment` and `volumes`
- Containers reach each other by service name
- Run with `docker compose up -d --build` and clean up with `down` (`-v` also removes the data)
- During development, connect your local code with `volumes: - .:/app`

## Exercises

```quiz
Q: What is the file where Compose lists your containers called?
A: compose.yaml | compose.yml | docker-compose.yml
E: Containers go one by one under `services`.

Q: How do Compose containers find each other?
A: by service name | service name | name
E: A service called `db` is reached at the host name `db`.

Q: Which command rebuilds and starts Compose in the background?
A: docker compose up -d --build | up -d --build
E: Clean up with `docker compose down`.

Q: Which option for `docker compose down` also deletes volume data?
A: -v | --volumes
E: It cannot be undone, so use it with care.
```
