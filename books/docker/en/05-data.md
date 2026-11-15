# 5. Data and settings (volumes and environment variables)

## Two ways to keep data

Files inside a container disappear when you remove the container (Chapter 3). Keep what you want to keep outside the container.

| Method | How to write it | Where it is stored | Good for |
| --- | --- | --- | --- |
| **Volume** | `-v name:/place/in/container` | A place managed by Docker | Data the container uses, such as database data |
| **Bind mount** | `-v /place/on/computer:/place/in/container` | The folder on your computer itself | Code under development, data to read, results to write out |

If the left side of `:` is a **name**, it is a volume; if it is a **path** starting with `/` or `./`, it is a bind mount.

## Volumes

```bash
docker volume create pgdata
docker run -d --name db -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
docker rm -f db                                      # even if you remove the container
docker run -d --name db -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
# the earlier data is still there
```

- List them with `docker volume ls`, and remove one with `docker volume rm name` (the data inside is removed too)
- In VS Code, they appear under VOLUMES in the whale icon

## Bind mounts

This makes a folder on your computer visible from inside the container. A change on one side shows up on the other side right away.

```bash
cd ~/apps/docker-study
echo 'print("running a local file with the Python in the container")' > hello.py
docker run --rm -v "$(pwd)":/work -w /work python:3.12-slim python hello.py
```

- `$(pwd)` is the folder you are in. Surrounding it with `"` makes it work even for paths with spaces
- `-w /work` is the working folder inside the container
- If you edit `hello.py` in VS Code and run it again, the change shows up right away (no need to rebuild the image)

### Watch out for file ownership

Containers often run as root (the administrator), so files written by the container belong to root on your computer, and sometimes you cannot delete them normally. Running as your own user prevents this.

```bash
docker run --rm -v "$(pwd)":/work -w /work --user "$(id -u):$(id -g)" python:3.12-slim \
  python -c "open('out.txt', 'w').write('ok')"
ls -l out.txt          # it belongs to you
```

## Passing settings with environment variables

Settings that change depending on where you run — passwords, what to connect to, the time zone and so on — are not built into the image but passed as **environment variables**.

```bash
docker run --rm -e TZ=Asia/Tokyo -e GREETING=hello python:3.12-slim \
  python -c "import os; print(os.environ['GREETING'])"
```

Inside the app, in Python, read them with `os.environ.get("NAME", "value if missing")`.

### The .env file

When there are many, put them together in a file.

`.env`:

```text
POSTGRES_PASSWORD=secret
TZ=Asia/Tokyo
```

```bash
docker run --rm --env-file .env postgres:16 env | grep TZ
```

> Add a `.env` with passwords in it to `.gitignore` and `.dockerignore` so that it does not end up on GitHub or in an image.

## Summary

- Put data you cannot afford to lose in a volume (`-v name:/place`) or a bind mount (`-v "$(pwd)":/place`)
- With a bind mount, you can edit local code and try it in the container right away. Match the owner with `--user "$(id -u):$(id -g)"`
- Pass settings with `-e` or `--env-file .env`. Do not upload `.env` to GitHub

## Exercises

```quiz
Q: What is the named storage managed by Docker for keeping data called?
A: volume | volumes
E: Attach it with `-v name:/path`.

Q: What do we call connecting a folder on your PC directly into a container?
A: bind mount | bind mounts
E: You can edit code on your PC and test it in the container right away.

Q: Which `docker run` option passes one environment variable?
A: -e | --env
E: For many, use `--env-file .env`.

Q: Which file holds passwords and must not be uploaded to GitHub?
A: .env | env
E: Add it to `.gitignore`.
```
