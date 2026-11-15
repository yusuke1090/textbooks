# 7. Dev Containers (developing inside a container)

## What are Dev Containers?

With VS Code's **Dev Containers** extension, the VS Code window stays on your computer, but you **open the folder inside a container** and develop there. The terminal, Python, the compiler and the extensions all run inside the container.

- You do not have to install Python or libraries on your computer. Your computer stays clean
- Each project can use a different version of Python or a different C++ compiler
- If you put the settings file (`.devcontainer/devcontainer.json`) on GitHub, you can get the same environment on other computers right away

## Getting started

1. In VS Code, open the folder you want to work in (for example `~/apps/py-study`)
2. **Ctrl + Shift + P** → "Dev Containers: Add Dev Container Configuration Files..."
3. "Add configuration to workspace" → choose what you want to use (for example **Python 3**) and the version. If you do not need extra features, just press OK
4. `.devcontainer/devcontainer.json` is created
5. Press "Reopen in Container" in the lower right (or Ctrl + Shift + P → "Dev Containers: Reopen in Container")

The first time, it downloads the image, so it takes a little while. When "Dev Container: Python 3" appears in the lower left, you are inside the container. If you open a terminal, it is a shell inside the container.

```bash
python --version      # the Python inside the container
pwd                   # /workspaces/py-study (your local folder is connected)
```

Your local folder is connected to `/workspaces/folder-name` in the container (a bind mount, Chapter 5). When you edit a file, the file on your computer changes.

## devcontainer.json

```json
{
  "name": "py-study",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter"
      ]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [5000]
}
```

| Item | Meaning |
| --- | --- |
| `image` | The image to use. `mcr.microsoft.com/devcontainers/...` are Microsoft images for development, with git and so on included |
| `customizations.vscode.extensions` | The VS Code extensions to install inside the container |
| `postCreateCommand` | A command run once after the container is created (to install libraries, for example) |
| `forwardPorts` | Connects a container port to your computer (open it at `localhost:5000`) |

For C++ there is `mcr.microsoft.com/devcontainers/cpp`, and for just Ubuntu there is `mcr.microsoft.com/devcontainers/base:ubuntu`, among others.

### Using your own Dockerfile or Compose

```json
{
  "name": "myapp",
  "build": { "dockerfile": "Dockerfile" }
}
```

```json
{
  "name": "counter",
  "dockerComposeFile": "../compose.yaml",
  "service": "web",
  "workspaceFolder": "/app"
}
```

With Compose, other containers such as a database run too (Chapter 6).

## Rebuild after changes

When you change `devcontainer.json` or the Dockerfile, rebuild with **Ctrl + Shift + P → "Dev Containers: Rebuild Container"**.

## Going back to your computer

**Ctrl + Shift + P → "Dev Containers: Reopen Folder Locally"** takes you back to the normal (local) folder. Clicking "Dev Container" in the lower left also shows the menu.

## git and GitHub

- You can use `git` inside the container too. Your local git name and email settings are passed into the container automatically
- If your SSH key (Chapter 3 of the GitHub Textbook) is registered with your local ssh-agent, you can use it from inside the container too (`ssh-add ~/.ssh/id_ed25519`)
- Put `.devcontainer/` on GitHub. When you clone and open it on another computer, "Reopen in Container" gives you the same environment right away

## Summary

- With Dev Containers, you open a folder inside a container and develop there. Your computer stays clean
- Create `devcontainer.json` with "Add Dev Container Configuration Files" and go in with "Reopen in Container"
- Write the extensions, `postCreateCommand` and `forwardPorts`. After changes, use "Rebuild Container"
- Put `.devcontainer/` on GitHub and you have the same environment everywhere

## Exercises

```quiz
Q: What is the Dev Containers settings file called?
A: devcontainer.json
E: Create it with "Add Dev Container Configuration Files".

Q: Which VS Code command reopens the folder inside the container?
A: Reopen in Container
E: To go back, use "Reopen Folder Locally".

Q: Which command rebuilds the container after you change settings?
A: Rebuild Container
E: Changes are not used until you rebuild.

Q: Which devcontainer.json setting holds a command that runs once after the container is created?
A: postCreateCommand
E: For example, a command that installs libraries.
```
