# 1. What are git and GitHub?

## What you will learn

- The difference between git and GitHub
- Words that come up often
- The places a file passes through, from your computer to GitHub

This textbook covers how to use git and GitHub with commands.

| Chapter | Contents |
| --- | --- |
| Chapter 2 | Settings you make only once, at the start |
| Chapter 3 | Make an SSH key, register it with GitHub, and clone and push without a password |
| Chapter 4 | Make a new repository and put it on GitHub |
| Chapter 5 | Everyday recording (commit, push, pull) |
| Chapter 6 | Going back to an earlier state |
| Chapter 7 | Trying things on a branch. How to fix things when both sides were changed |
| Chapter 8 | Making it possible to clone from a Raspberry Pi, Jetson or another PC (through GitHub or not) |
| Chapter 9 | Using git with VS Code's buttons. Handy extensions |
| Appendix | Common errors, a list of commands |

- Type the commands in a terminal on Ubuntu (the same on a Raspberry Pi or Jetson)
- The example repository is `collar` (`~/apps/collar` on the PC). Replace it with the name of your own repository
- Click a word in a command (such as `git` or `ssh-keygen`) to see its meaning in a speech bubble
- Chapters 1–8 explain things with commands. Much of the same can be done with buttons in VS Code, as summarized in Chapter 9. Settings that are hard to understand with buttons alone, such as SSH keys, are in Chapter 3

## git and GitHub

| Thing | What it is | Where it is |
| --- | --- | --- |
| **git** | Software that records changes to files. It keeps track of when and what changed, and lets you go back to an earlier state | Your PC |
| **GitHub** | A place on the internet to keep git's records. Used to share with other PCs and other people | github.com |
| **gh** (GitHub CLI) | A command for working with GitHub from the terminal. Logging in, making repositories | Your PC |

git alone can keep records inside your PC. Putting them on GitHub means your code survives even if your PC breaks, and you can get the same code from another PC or a Raspberry Pi.

## Words that come up often

| Word | Meaning |
| --- | --- |
| Repository (repo for short) | The unit of recording. One folder and the whole history of changes in it. Usually, one project = one repository |
| Commit | One record. A set of "the state of the files at that time" and "a description of what you did". You can go back to this state later |
| Stage | The place where you pick the changes to go into the next commit. You put them there with `git add` |
| Remote | A copy of your local repository that lives somewhere else. Usually GitHub. By convention it is named **origin** |
| Push | Sending your local commits to the remote |
| Pull | Bringing new commits from the remote into your local repository |
| Clone | Copying an entire remote repository to your computer. Only the first time |
| Branch | A branch of the flow of commits. The main branch is **main**. You make a branch when trying out changes |
| Tag | A name marker attached to a commit, such as `v1.0.0` |
| `.gitignore` | A file listing the files git should not record |

## The places a file passes through

![The places a file passes through in git](images/en/git-areas.svg)

1. Change files in the working folder
2. Use `git add` to pick the changes to go into the next commit (put them on the stage)
3. Use `git commit` to save them in your local record. Up to here, everything is inside your PC, and you do not need the internet
4. Use `git push` to send them to GitHub

On another PC, first copy everything from GitHub with `git clone`, and after that bring in just the new parts with `git pull`.

- The record is in a hidden folder called `.git` inside the project folder. **If you delete `.git`, the whole record is gone**
- In VS Code's Source Control, **＋** (Stage Changes) is `git add`, **Commit** is `git commit`, and **Sync Changes** is `git pull` and `git push`

## Summary

- git is software that keeps records inside your PC, and GitHub is where they are stored
- Send with `add` → `commit` → `push`, and on another machine get them with `clone` → `pull`
- The record is in the `.git` folder. Do not delete it

## Exercises

```quiz
Q: git keeps records of changes on your PC. What is the online service where those records are stored?
A: GitHub
E: git is software on your PC; GitHub is where you keep the records.

Q: To send changes to GitHub you run `add` → `commit` → what?
A: push | git push
E: On another machine you use `clone` → `pull` to get them.

Q: Which command copies a whole GitHub repository to another machine for the first time?
A: clone | git clone
E: After that, `git pull` brings only the new changes.

Q: What is the name of the folder that holds git's records, which you must not delete?
A: .git | git
E: Deleting it loses all the history.
```
