# 1. What is Docker?

## No more "but it works on my computer"

A program only runs when its **environment** — the OS, the Python version, the libraries and so on — is in place.

- It runs on your computer but not on a Raspberry Pi or someone else's computer
- Project A wants Python 3.10, and project B wants 3.12
- You want to try a database, but you do not want to install it directly and clutter your computer's settings

**Docker** is a tool that puts a program and the environment it runs in together into a box (a **container**), so that it runs the same way anywhere.

## How it differs from a virtual machine

![Virtual machine vs container](images/en/vm.svg)

| | Virtual machine (VirtualBox and others) | Container (Docker) |
| --- | --- | --- |
| What is inside | Runs a whole OS | Only the app and its libraries. The OS (the Linux kernel) is shared with the host |
| Size | Several GB | Tens to hundreds of MB |
| Startup | Tens of seconds to minutes | About 1 second |
| Running many | Heavy | Light |

Containers run on a Linux mechanism. On Windows and Mac, Docker Desktop runs a small Linux inside. On Ubuntu, a Raspberry Pi or a Jetson, they run directly.

## Images, containers and Dockerfiles

![From Dockerfile to container](images/en/flow.svg)

| Term | Meaning | Comparison |
| --- | --- | --- |
| **Dockerfile** | A text file that says how to build an image | A recipe |
| **Image** | The template for containers. It contains part of an OS, libraries and the app. Its contents do not change | A frozen meal |
| **Container** | The running thing made from an image. You can make as many as you like from one image | The meal heated up and served on a plate |
| **Docker Hub** | A place to keep images (a registry). It has official images for Python, Ubuntu, databases and more | A shop |

- `docker pull` gets an image from Docker Hub, and `docker run` makes a container and runs it (Chapter 3)
- For your own app, write a Dockerfile and build the image with `docker build` (Chapter 4)

## What you can do with Docker

| Use | Example |
| --- | --- |
| Try things out | Try a database or a new version of Python without cluttering your computer, and delete it right after |
| Set up the same development environment | Develop inside a per-project environment with VS Code's Dev Containers (Chapter 7) |
| Combine several things | Run a web app + a database together from one file (Chapter 6) |
| Distribute and deploy | Turn your app into an image and run it the same way on a Raspberry Pi, a Jetson or a server (Chapter 8) |

## Summary

- A container is a light box holding an app and its environment. It shares the host's Linux as its OS
- Dockerfile (recipe) → `docker build` → image (template) → `docker run` → container (the running thing)
- You can get images from Docker Hub

## Exercises

```quiz
Q: What is the template that containers are made from called?
A: image | Docker image
E: Dockerfile (recipe) → `docker build` → image → `docker run` → container.

Q: What is the name of the recipe file used to build an image?
A: Dockerfile
E: `docker build` turns a Dockerfile into an image.

Q: What is Docker's official registry where you can get many images?
A: Docker Hub | DockerHub
E: It has images such as `python` and `nginx`.

Q: Containers are lighter than virtual machines because they share what with the host?
A: OS | kernel | Linux | Linux kernel
E: Containers share the host's Linux kernel; a VM carries a whole OS.
```
