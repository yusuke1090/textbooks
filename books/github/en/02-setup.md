# 2. Settings you make only once

## What you will learn

- How to install git and gh
- Registering the name and email address that go into commits
- Preparing a GitHub account

## Installing git and gh

```bash
sudo apt install git gh
git --version
```

If you see `git version 2.…`, it is installed.

## Registering your name and email address

Each commit contains a name and email address showing who recorded it. Set them once on each PC, at the start.

```bash
git config --global user.name "Taro Yamada"
git config --global user.email "12345678+username@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor nano
git config --global --list
```

| Setting | Meaning |
| --- | --- |
| `user.name` | The name that goes into commits. Your GitHub username or your real name are both fine |
| `user.email` | The email address that goes into commits. Once on GitHub, anyone who looks at the commits can see it |
| `init.defaultBranch main` | Make the first branch of new repositories `main` (to match GitHub) |
| `pull.rebase false` | On `git pull`, if both sides changed things, combine them with a "merge" ("When both sides changed" in Chapter 7) |
| `core.editor nano` | Use nano as the editor that opens when you write a commit description and so on |

- If you do not want to show your email address, check "Keep my email addresses private" under GitHub's **Settings → Emails**, and use the `number+username@users.noreply.github.com` address shown there
- The final `git config --global --list` shows what you set. The settings are stored in `~/.gitconfig`
- `--global` means "all repositories of this user on this PC"

## A GitHub account

Create an account at [github.com](https://github.com) (free). You can also make private repositories for free.
Also set up **two-factor authentication** (when you log in, you confirm one more time, for example with an app on your phone). It is under GitHub's **Settings → Password and authentication**.

## Summary

- Install with `sudo apt install git gh`
- On each PC, set your name, email address and `main` once at the start
- Turn on two-factor authentication for your GitHub account
