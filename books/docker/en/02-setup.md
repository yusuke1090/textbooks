# 2. Setting up (Ubuntu and VS Code)

## Installing Docker

The easiest way is with Ubuntu's packages.

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2 docker-buildx
```

| Package | What it contains |
| --- | --- |
| `docker.io` | Docker itself (Docker Engine) |
| `docker-compose-v2` | `docker compose` (Chapter 6) |
| `docker-buildx` | The newer version of the image-building tool (Chapter 4) |

If you want a newer version, follow "Install Docker Engine on Ubuntu" on Docker's official site and install it from Docker's apt repository (the package names change to `docker-ce` and so on; do not install both).

> On Windows or Mac, install **Docker Desktop**. The commands in this textbook work as they are.

## Using it without sudo

At first, `docker` commands need `sudo`. If you add yourself to the `docker` group, you can use them without it.

```bash
sudo usermod -aG docker $USER
```

**Log out once and log back in** (restarting the computer also works). Then check.

```bash
docker run hello-world
docker compose version
```

If you see `Hello from Docker!`, it worked.

> Being in the `docker` group lets you do almost anything root (the administrator) can. Only set this up on a computer that you alone use.

Docker starts automatically when the computer starts. If it is not running, start it with `sudo systemctl start docker`.

## VS Code extensions

In VS Code's Extensions view (the icon of four squares on the left), install these two.

| Extension | Author | What it does |
| --- | --- | --- |
| **Container Tools** (search for "Docker"; its old name was Docker) | Microsoft | Adds a whale icon on the left. Lists and controls containers, images and volumes, and completes your typing in Dockerfiles and compose.yaml |
| **Dev Containers** | Microsoft | Opens a folder inside a container in VS Code so you can develop there (Chapter 7) |

Click the whale icon to see these lists. Right-click to stop, remove, view logs, go inside (Attach Shell) and more.

| List | What it shows |
| --- | --- |
| CONTAINERS | Running and stopped containers |
| IMAGES | Images you have locally |
| REGISTRIES | Connections to Docker Hub and others |
| VOLUMES | Places to keep data (Chapter 5) |
| NETWORKS | Networks that connect containers to each other |

In this textbook, we type commands in the terminal (**Ctrl + `**) and also check the results in the lists on the left.

## A folder for practice

```bash
mkdir -p ~/apps/docker-study
cd ~/apps/docker-study
code .
```

## Summary

- Install with `sudo apt install docker.io docker-compose-v2 docker-buildx`
- After `sudo usermod -aG docker $USER`, log in again and you can use it without sudo
- Check with `docker run hello-world`
- Install Container Tools and Dev Containers in VS Code

## Exercises

```quiz
Q: Which group do you join to use Docker without sudo?
A: docker
E: Run `sudo usermod -aG docker $USER`, then log in again.

Q: What test image do you run to check that Docker works?
A: hello-world | hello world
E: If `docker run hello-world` prints a greeting, it works.

Q: Which VS Code extension lets you open a folder inside a container to develop?
A: Dev Containers | DevContainers
E: Also install Container Tools.
```
