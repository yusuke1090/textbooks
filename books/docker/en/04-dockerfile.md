# 4. Building images with a Dockerfile

## What you will learn

- How to write a Dockerfile (FROM, WORKDIR, COPY, RUN, CMD)
- Building an image (build) and running it
- Layers and the cache, and .dockerignore
- Putting an image on Docker Hub

## What we will make

We will turn a small Python web app (Flask) into an image. In VS Code, create these files.

```text
myapp/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

`app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Docker!\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:

```text
flask
```

> `host="0.0.0.0"` is important. If you leave it as `127.0.0.1` (Flask's default), it can only be reached from **inside** the container, and your computer's browser cannot see it.

## Dockerfile

The file name is `Dockerfile` (no extension). VS Code's Container Tools shows completions and explanations as you write.

```dockerfile
# the image to start from
FROM python:3.12-slim

# the working folder inside the container (created if it does not exist)
WORKDIR /app

# copy only the list of libraries first and install them (for the cache; explained later)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the app's files
COPY . .

# the port this container uses (for documentation; docker run -p does the actual connection)
EXPOSE 5000

# the command to run when the container starts
CMD ["python", "app.py"]
```

| Instruction | Meaning |
| --- | --- |
| `FROM` | The image to start from. Write one at the beginning |
| `WORKDIR` | The working folder. The following instructions run here |
| `COPY source destination` | Copy files from your computer into the image |
| `RUN` | Run a command while building the image (to install libraries, for example) |
| `ENV NAME=value` | Set an environment variable |
| `EXPOSE` | Note the port that is used |
| `CMD` | The command when the container runs. One, at the end |

`RUN` runs **when the image is built**, and `CMD` runs **when the container is started**.

## Building and running the image

Run these in the `myapp` folder.

```bash
docker build -t myapp .                          # build from the Dockerfile in ., with the name myapp
docker images                                    # myapp is there
docker run -d --name myapp -p 5000:5000 myapp    # run it
curl http://localhost:5000                       # Hello from Docker!
```

- Name it with `-t name:tag` (if you leave out the tag, it is `latest`). It is good to add a version, as in `-t myapp:1.0`
- The final `.` is the folder that has the Dockerfile (the files here are what COPY can reach)
- In VS Code, you can also right-click `Dockerfile` → "Build Image..."

### When you change the code

The image stays as it was when you built it. If you change `app.py`, rebuild it and recreate the container too.

```bash
docker rm -f myapp
docker build -t myapp .
docker run -d --name myapp -p 5000:5000 myapp
```

Doing this every time is a hassle, so during development use Compose (Chapter 6) or Dev Containers (Chapter 7).

## Layers and the cache

An image is made of a stack of **layers**, one for each instruction. When you rebuild, layers for instructions that have not changed reuse the previous ones (the **cache**), so it is faster. When an instruction changes, **everything after it** is rebuilt.

| Order | Bad way to write it | Good way to write it |
| --- | --- | --- |
| 1 | `COPY . .` | `COPY requirements.txt .` |
| 2 | `RUN pip install -r requirements.txt` | `RUN pip install -r requirements.txt` |
| 3 | | `COPY . .` |
| When you change `app.py` | `COPY . .` changes, so pip install runs again too (slow) | pip install uses the cache, and only `COPY . .` runs again (fast) |

Put things that rarely change first, and things that change often later.

## .dockerignore

So that `COPY . .` does not put unneeded things into the image, list them in `.dockerignore` (written the same way as `.gitignore`).

```text
.venv/
__pycache__/
*.pyc
.git/
.env
```

It is also important not to put `.env` (passwords and so on; Chapter 5) into the image.

## Putting the image somewhere (Docker Hub)

To use the image on other computers or a Raspberry Pi, you can put it in a registry.

```bash
docker login                                 # log in with your Docker Hub account
docker tag myapp:latest username/myapp:1.0   # give it a name for where it goes
docker push username/myapp:1.0
# on another computer
docker pull username/myapp:1.0
```

You can also use GitHub's Container Registry (`ghcr.io`). For things you do not want to publish, use a private repository.

## Summary

- A Dockerfile goes `FROM` → `WORKDIR` → `COPY` → `RUN` → `CMD`
- Build with `docker build -t name .` and run with `docker run`. Rebuild when you change the code
- Make the app listen on `0.0.0.0`
- Writing things that rarely change (libraries) first makes builds faster thanks to the cache. Put unneeded things in `.dockerignore`
