# 8. Troubleshooting, cleaning up, Raspberry Pi and Jetson

## Common errors

| Message | Cause | Fix |
| --- | --- | --- |
| `permission denied while trying to connect to the Docker daemon socket` | You are not in the `docker` group, or you have not logged in again after joining | After `sudo usermod -aG docker $USER`, log in again (Chapter 2) |
| `Cannot connect to the Docker daemon` | Docker is not running | `sudo systemctl start docker` (use `enable` to start it automatically at boot) |
| `port is already allocated` / `address already in use` | Another container or app is using that port | Find it with `docker ps` and stop it, or change the local port, as in `-p 8081:80` |
| `The container name "/web" is already in use` | A container with the same name exists (even if stopped) | Remove it first with `docker rm -f web` |
| `exec format error` / `no matching manifest for linux/arm64` | The CPU type (architecture) of your computer and the image are different | See "Raspberry Pi and Jetson" below |
| `no space left on device` | Images and containers have piled up and the disk is full | See "Cleaning up" below |
| Cannot connect from the browser | The app is listening on `127.0.0.1`, or you forgot `-p` | Make the app listen on `0.0.0.0` (Chapter 4). Check PORTS in `docker ps` |
| Changed the code but nothing changes | The image is still the old one | `docker compose up -d --build`, or use a bind mount (Chapter 5) |
| The container stops right away | The `CMD` command finished, or it crashed with an error | Check the reason with `docker logs name` |

First look at the logs with `docker logs name`, then go inside to check (`docker exec -it name bash`, or `sh` if there is no `bash`). In VS Code, use "View Logs" and "Attach Shell" from the whale icon.

## Cleaning up

Before you know it, images and containers are using a lot of disk space.

```bash
docker system df             # what is using how much
docker container prune       # remove all stopped containers
docker image prune           # remove unnamed (outdated) images
docker image prune -a        # remove all unused images (they are downloaded again next time)
docker volume prune          # remove unused volumes (the data is removed too; be careful)
docker system prune          # containers, networks, unnamed images and more, all at once
```

`prune` asks before removing, but volume data cannot be restored. Check the names before removing volumes with important data.

## Raspberry Pi and Jetson

### CPU type (architecture)

| Machine | Architecture |
| --- | --- |
| A normal PC | `amd64` (x86_64) |
| Raspberry Pi (64-bit OS), Jetson | `arm64` (aarch64) |

Images are built for each architecture. Official images such as Python, Ubuntu, nginx and Redis have both versions, so they run under the same name on a Raspberry Pi. Build your own images for the same architecture as the machine that runs them.

- The easiest way is to **run `docker build` on the Raspberry Pi or Jetson itself**
- To build for arm64 on a PC, use buildx (it uses a mechanism called QEMU to pretend to be another CPU, so it is slow)

```bash
docker run --privileged --rm tonistiigi/binfmt --install arm64   # only once (installs QEMU)
docker buildx build --platform linux/arm64 -t username/myapp:arm64 --push .
```

### Raspberry Pi

On Raspberry Pi OS (64-bit), you can install it with Docker's official instructions (for Debian). As an easy way, there is also an official install script.

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER      # log in again after this
```

On models with little memory, use light images (`-slim`, `alpine`).

### Jetson

- JetPack includes Docker and NVIDIA's container runtime (which lets containers use the GPU)
- To use the GPU, add it like `docker run --runtime nvidia ...`
- Use images **that match the L4T (JetPack) version** of your Jetson. Check the version with `cat /etc/nv_tegra_release`. NVIDIA's NGC (`nvcr.io`) has images for L4T

### Using them from VS Code

If you connect to a Raspberry Pi or Jetson with VS Code's **Remote - SSH** (Chapter 9 of the GitHub Textbook), the whale icon shows the containers on the machine you connected to. Dev Containers' "Reopen in Container" also opens in a container on that machine.

## Summary

- Look at `docker logs` first. Port conflicts, name conflicts and forgetting to log in again after joining the group are common
- Check with `docker system df` and clean up with `prune`. Volume data cannot be recovered once removed
- Raspberry Pi and Jetson are arm64. Build on them, or use `buildx --platform linux/arm64`
- To use the GPU on a Jetson, use `--runtime nvidia` and an image that matches your L4T version

## Exercises

```quiz
Q: What command do you check first when a container is not working?
A: docker logs | logs
E: Port clashes, name clashes and needing to log in again are common causes.

Q: What CPU architecture do Raspberry Pi and Jetson use?
A: arm64 | aarch64 | ARM
E: To build on a PC (amd64), use `buildx --platform linux/arm64`.

Q: Which word cleans up unused images and containers (`docker system ???`)?
A: prune
E: First check usage with `docker system df`.

Q: Which `docker run` option lets a container use the GPU on a Jetson?
A: --runtime nvidia | --runtime=nvidia
E: Use an image that matches your L4T version.
```
