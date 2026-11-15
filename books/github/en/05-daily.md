# 5. Everyday recording

## What you will learn

- The commands to type at the start and end of your work
- How to read `git status`
- Things you must not upload to GitHub

## What to type at the start and end

When you start working and when you finish, type these in order.

```bash
git pull
git status
git diff
git add .
git commit -m "Add I2C reading"
git push
```

| Command | What it does |
| --- | --- |
| `git pull` | Brings in what is new on GitHub. If you also work on another PC, always do this before you start |
| `git status` | A list of the files you changed and the files on the stage. **When in doubt, start with this** |
| `git diff` | Shows changes not yet on the stage, line by line (`-` is a removed line, `+` an added line) |
| `git diff --staged` | Shows the changes on the stage (a last check before committing) |
| `git add filename` | Puts only that file on the stage |
| `git add .` | Puts all changed files on the stage |
| `git commit -m "description"` | Records them |
| `git push` | Sends them to GitHub |
| `git log --oneline` | A list of commits (newest at the top) |
| `git log -p filename` | The history of changes to that file |
| `git show commit-number` | What that commit changed |

- When the output of `git log` or `git diff` is long, it stops with a `:`. Move with the arrow keys, and quit with `q`
- **Commit numbers** are letters and digits like `3d3b5db`. They appear in the left column of `git log --oneline`. In commands, the first 7 or so characters are enough
- Put one thing in each commit ("Add I2C reading", "Change the LED pin"). It makes searching and going back easier later
- For commits you may want to come back to, such as a version you shipped, add a marker (a tag) with `git tag v1.0.0` → `git push --tags`

## How to read git status

`git status` shows something like this.

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
        modified:   collar.cpp

Changes not staged for commit:
        modified:   CMakeLists.txt

Untracked files:
        mpu6050.h
```

| Heading | Meaning |
| --- | --- |
| `Changes to be committed` | On the stage. Goes into the next commit |
| `Changes not staged for commit` | Changed, but not yet on the stage |
| `Untracked files` | New files git does not know yet. Not recorded until you `git add` them |
| `Your branch is ahead of 'origin/main' by 2 commits` | There are 2 commits not yet sent to GitHub. Run `git push` |

## Things you must not upload

| Thing | What to do |
| --- | --- |
| WiFi passwords, server passwords, API keys | Put them in a separate file and add it to `.gitignore` (below) |
| Things made by building (`build/`, `.uf2`) | Add them to `.gitignore`. You can always remake them from the source |
| Large data (CSV files of tens of MB, videos) | Add them to `.gitignore`. GitHub does not accept files over 100MB |

For example, when you use WiFi on a Pico W, write the password in `secrets.h` and add it to `.gitignore`, and upload only a sample with the contents left empty (`secrets.example.h`).

```cpp
// secrets.h (do not upload to git; make it by copying secrets.example.h)
#pragma once
#define WIFI_SSID     "my-wifi"
#define WIFI_PASSWORD "password-here"
```

- **Anything you have pushed stays in the history, even if you delete it later.** If you uploaded a password, change the password itself
- To stop recording a file you have already recorded: `git rm --cached secrets.h` (the file on your PC is not deleted) → write it in `.gitignore` → commit. For a folder, `git rm -r --cached build`

## Summary

- `git pull` before you start; `add` → `commit` → `push` when you finish
- When in doubt, `git status`
- Do not upload passwords or `build/`. Write them in `.gitignore`

## Exercises

```quiz
Q: Which command do you run before you start work?
A: git pull | pull
E: It brings in changes made on other machines first.

Q: Which command shows the current state when you are unsure?
A: git status | status
E: It shows which files changed and what will be recorded.

Q: Which file lists the files you do not want to upload, such as `build/`?
A: .gitignore | gitignore
E: Never upload passwords or `build/`.
```
