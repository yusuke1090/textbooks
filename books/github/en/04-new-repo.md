# 4. Making a new repository

The flow is "make it a repository locally and make the first commit → make a place on GitHub and send it". There are three ways to make the place, and they all give the same result.

| Method | What you do | Good when |
| --- | --- | --- |
| VS Code's **Publish to GitHub** | Press a button in Source Control | You want to put a project made in VS Code up as it is |
| **gh repo create** | One command | You are working in the terminal |
| **Make it on GitHub's website and connect** | Make it in the browser and connect with `git remote add` | A PC without gh. Works with git alone |

Projects made with VS Code extensions (such as "Raspberry Pi Pico") are not git repositories yet (only a `.gitignore` has been made).

## 1. Make it a repository locally

```bash
cd ~/apps/collar
git init
```

You see `Initialized empty Git repository in /home/username/apps/collar/.git/`.

If there is no `.gitignore`, make one (`nano .gitignore`). For a C++ project, do it like this.

```text
# things made by building
build/
# passwords and the like ("Things you must not upload" in Chapter 5)
secrets.h
# things used by Python
__pycache__/
.venv/
```

## 2. Make the first commit

```bash
git add .
git status
git commit -m "First version"
```

Look at the list under `Changes to be committed:` in `git status`. Check that `build/` and files with passwords are not there, then commit.

## 3. Put it on GitHub

Do either A or B below (pressing Publish to GitHub in VS Code is fine too).

### A. Make it with gh

```bash
gh repo create collar --private --source=. --push
```

This makes a private repository called `collar` on GitHub, registers it as `origin`, and sends up to the first commit.

### B. Make it on GitHub's website and connect

1. On GitHub, press **＋** in the upper right → **New repository**
2. Write `collar` in **Repository name** and choose **Private**
3. **Do not add** a README, .gitignore or license (make an empty repository, so that it does not conflict with your local one)
4. Press **Create repository**
5. On the page that appears, choose **SSH** and copy `git@github.com:username/collar.git`

```bash
git remote add origin git@github.com:username/collar.git
git push -u origin main
```

- `git remote add origin URL` registers the GitHub repository under the name `origin`
- `-u` makes git remember "from now on, `git push` and `git pull` alone talk to origin's main". Add it only the first time

## 4. Check that it is there

Open `https://github.com/username/collar` in a browser. If the files are listed, you are done (you can also open it with `gh repo view --web`).
If you add a README.md, it is shown at the bottom of this page. Writing what the program is, which machine it runs on and how to build it will help you later.

## Starting from a repository on GitHub (clone)

This is for when you continue development on another PC, or use someone else's repository.

```bash
cd ~/apps
git clone git@github.com:username/collar.git
cd collar
code .
```

- `gh repo clone collar` does the same (for your own repository, you can leave out the username)
- Public repositories (such as pico-examples) can be cloned with the HTTPS URL without logging in
- The folder is named after the repository (`collar`)

## Summary

- `git init` → first commit → `gh repo create` (or make it on GitHub's website and `git remote add`) → `git push -u origin main`
- Before the first commit, check with `git status` that `build/` and passwords are not included
- On another PC, start with `git clone`

## Exercises

```quiz
Q: Which command turns a folder into a git repository?
A: git init | init
E: Then you make your first commit.

Q: To create a GitHub repository with gh, what comes after `gh repo`?
A: create | gh repo create
E: If you create it on the GitHub website, connect it with `git remote add`.

Q: Which option do you add to the first push so git remembers where to send (`git push ? origin main`)?
A: -u | --set-upstream
E: After `git push -u origin main`, plain `git push` works.

Q: Which command checks that `build/` or passwords are not included before the first commit?
A: git status | status
E: Always look at what will be recorded before you commit.
```
