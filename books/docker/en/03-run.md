# 3. Running containers

## What you will learn

- Getting an image (pull) and running a container (run)
- Listing, stopping and removing containers, viewing logs and going inside
- Common options of `docker run` (ports, names, running in the background)

## Run Python just once

```bash
docker run --rm python:3.12-slim python -c "print('from inside the container', 1 + 1)"
```

1. If you do not have the `python:3.12-slim` image locally, it is fetched automatically from Docker Hub (pull)
2. A container is made from that image, and `python -c ...` runs in it
3. When it finishes, the container is removed (`--rm`)

Even if Python 3.12 is not installed on your computer, this runs with 3.12.

### Image names and tags

The part after the `:` in `python:3.12-slim` is called the **tag**. It shows the version or variant.

| Example | Meaning |
| --- | --- |
| `python:3.12` | Python 3.12 (normal size) |
| `python:3.12-slim` | A small version with unneeded things left out |
| `ubuntu:24.04` | Ubuntu 24.04 |
| `nginx` | No tag means `latest`. Its contents can change, so it is better to write a fixed version |

## Using it interactively

```bash
docker run -it --rm python:3.12-slim          # Python's interactive mode (leave with exit())
docker run -it --rm ubuntu:24.04 bash         # a shell inside Ubuntu (leave with exit)
```

`-it` is the option that lets you type with the keyboard. Even if you run `apt install` and the like inside the Ubuntu container, your computer is not affected. Because of `--rm`, everything disappears when you leave.

## Running a web server in the background

```bash
docker run -d --name web -p 8080:80 nginx
```

Open `http://localhost:8080` in a browser and you will see the nginx page.

| Option | Meaning |
| --- | --- |
| `-d` | Run in the background (you get the terminal back right away) |
| `--name web` | Give the container a name (without it, you get a random name) |
| `-p 8080:80` | Connect port 8080 on your computer to port 80 in the container (in the order `computer:container`) |
| `-it` | Interact with the keyboard |
| `--rm` | Remove automatically when stopped |
| `-e NAME=value` | An environment variable (Chapter 5) |
| `-v place:place` | Connect a folder or volume (Chapter 5) |

## Controlling containers

| Command | What it does |
| --- | --- |
| `docker ps` | List running containers (`-a` includes stopped ones) |
| `docker logs web` | View the output (logs) (`-f` keeps following it) |
| `docker exec -it web bash` | Go inside a running container (leave with `exit`; the container keeps running) |
| `docker stop web` | Stop it |
| `docker start web` | Run a stopped container again |
| `docker rm web` | Remove a stopped container (`-f` removes it even if it is running) |
| `docker images` | List your local images |
| `docker pull name:tag` | Get an image |
| `docker rmi name:tag` | Remove an image (not possible while a container uses it) |

In VS Code, `web` appears under CONTAINERS in the whale icon on the left. Right-click it to use "View Logs", "Attach Shell" (go inside), "Stop" and "Remove", so you can control it even if you do not remember the commands.

## Changes inside a container disappear

Files and changes you make inside a container **disappear when you remove that container**. The image does not change.

- You can always get back to a clean state by making a new container from the same image (this is what makes it handy)
- Keep data you want to keep in a volume or a folder on your computer (Chapter 5)
- Write libraries you want installed in a Dockerfile and build them into an image (Chapter 4)

## Summary

- Run with `docker run image:tag command`. If you do not have the image, it is pulled automatically
- `-d` background, `--name` name, `-p computer:container` port, `-it` interactive, `--rm` remove automatically
- `ps`, `logs`, `exec -it ... bash`, `stop`, `rm`. You can also use the whale icon in VS Code
- Removing a container also removes the changes inside it
