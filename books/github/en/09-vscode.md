# 9. Using git in VS Code

## What you will learn

- How to read the Source Control view, and how the big button changes
- Committing, pushing and pulling with buttons, and viewing changes
- How to put a repository on GitHub, clone, use branches, fix conflicts and go back to an earlier state in VS Code
- Handy extensions and settings

git is built into VS Code from the start, and you can do many of the commands from the earlier chapters with buttons.
What runs inside VS Code is the git installed on your PC (Chapter 2). Your name, email address and SSH key settings (Chapters 2 and 3) are used as they are.

Button names are written as they appear in the English display. If you use the Japanese display (Japanese Language Pack), read them as follows.

| English display | Japanese display |
| --- | --- |
| Source Control | ソース管理 |
| Changes / Staged Changes | 変更 / ステージされている変更 |
| Commit | コミット |
| Sync Changes | 変更の同期 |
| Publish Branch | Branch の発行 |
| Stage Changes (＋) / Discard Changes (↶) | 変更をステージ / 変更を破棄 |

## The Source Control view

Click the branching icon on the left (**Source Control**), or press **Ctrl + Shift + G**.

![The Source Control view](images/en/vscode-scm.svg)

- The number on icon ① tells you at a glance whether any files have changed
- The letters at ⑥ show the same thing as `git status` (Chapter 5). M is modified, U is untracked (a new file git does not know yet), and D is deleted
- Clicking ⑧ switches branches ("Branches" below), and clicking ↻ is the same as Sync Changes

### How the big button changes

The blue button at the top of Source Control changes to **the next thing to do in the current state**.

![How the big Source Control button changes](images/en/vscode-scm-button.svg)

When in doubt, look at the blue button and you will know what to do next.

## Putting a repository on GitHub (Publish to GitHub)

When you open a folder that is not yet a git repository, Source Control shows **Initialize Repository** and **Publish to GitHub** (doing with buttons what the commands in Chapter 4 do).

1. Press **Publish to GitHub**
2. The first time, you see "The extension 'GitHub' wants to sign in using GitHub." Press **Allow** → a browser opens, so allow it on GitHub
3. Choose **Publish to GitHub private repository** or **public repository**. The repository name is filled in with the folder name
4. When the list of files to upload appears, just press OK
5. When "Successfully published…" appears in the lower right, you are done. **Open on GitHub** shows it in the browser

- You can see which GitHub account you are signed in with from the person icon (Accounts) in the lower left
- A repository put up this way has an HTTPS URL. If you want SSH, follow "Switching a repository you used over HTTPS to SSH" in Chapter 3
- Without a `.gitignore`, `build` is uploaded too. Make one first (Chapter 4)

## Cloning

1. In **Ctrl + Shift + P** (the Command Palette), type `git clone` and choose **Git: Clone**
2. Choose **Clone from GitHub** to see a list of your repositories (you can also paste an SSH URL)
3. Choose `~/apps` as the place to put it
4. When asked "Would you like to open the cloned repository?", press **Open**

When no folder is open, you can also do the same from **Clone Repository** in Source Control.

## Everyday recording

1. Before you start, bring in what is new on GitHub with **Sync Changes** in Source Control (or ⋯ → **Pull**)
2. When you change and save a file, it appears under Changes. Click it to see the differences side by side (A in the figure below)
3. Press **＋** on the files you want to include to put them on the stage (＋ on the Changes row for all of them)
4. Write a description in the box at the top ("Add I2C reading" and so on), and press **Commit** (or Ctrl + Enter)
5. The blue button becomes **Sync Changes 1↑**, so press it to send to GitHub

![How changes look](images/en/vscode-diff.svg)

Along the way, you may be asked the following.

| Message | Meaning and how to answer |
| --- | --- |
| There are no staged changes to commit. Would you like to stage all your changes and commit them directly? | You pressed Commit without putting anything on the stage. **Yes** commits everything. **Always** stops it asking next time |
| This action will pull and push commits from and to 'origin/main'. | A confirmation that Sync Changes means "bring in, then send". **OK** (OK, Don't Show Again stops it asking) |
| Would you like Code to periodically run 'git fetch'? | Whether to check from time to time if GitHub has new commits. With **Yes**, a number appears by the ↓ at ⑧ (they are brought in when you press Sync) |
| Enter passphrase for key '/home/…/.ssh/id_ed25519' | The passphrase for your SSH key. After "5. Stop being asked for the passphrase every time" in Chapter 3, you will not be asked |

- **Commit & Push** or **Commit & Sync** under **Commit ▾** commit and send in one go
- To stop recording a new file, right-click it under Changes → **Add to .gitignore** to add it to `.gitignore`
- To mark a version you shipped, use **Git: Create Tag** → **Git: Push Tags** in the Command Palette

### Buttons and the matching commands

| Task | VS Code | Command |
| --- | --- | --- |
| See the state | The list in Source Control | `git status` |
| See what changed | Click a file in the list | `git diff` |
| Put on the stage | **＋** on the file | `git add` |
| Record | Write a description and press **Commit** | `git commit -m "…"` |
| Send / bring in | **Sync Changes** (⋯ → Push / Pull for just one) | `git push`, `git pull` |
| See the history | **Graph** in Source Control | `git log --oneline` |

## Going back to an earlier state

Many of the commands in Chapter 6 can also be done with buttons.

| What you want to do | VS Code | Command |
| --- | --- | --- |
| Throw away uncommitted changes | **↶** on the file (Discard Changes) | `git restore filename` |
| Undo only some lines | Click the color next to the line numbers → ↶ (B in the figure above) | |
| Take off the stage | **−** on a file under Staged Changes (Unstage Changes) | `git restore --staged filename` |
| Fix the description of the last commit (before pushing) | **Commit ▾** → **Commit (Amend)** | `git commit --amend` |
| Undo the last commit (before pushing) | ⋯ → Commit → **Undo Last Commit**. The changes go back to the stage | `git reset --soft HEAD~1` |
| Set aside work in progress for a while | ⋯ → Stash → **Stash** / **Pop Stash...** | `git stash`, `git stash pop` |
| See a file's history | **Timeline** at the bottom of Explorer. Click an entry to see the differences from then | `git log -p filename` |
| Undo a commit you pushed | In the Git Graph extension, right-click the commit → **Revert...** (below) | `git revert commit-number` |

> **↶ on a new file (U) deletes the file.** If you see "This file will be FOREVER LOST if you proceed.", check that you really do not need it before pressing **Delete File**.

## Branches

Click the branch name in the lower left to see a list for making and switching branches.

![Switching and making branches](images/en/vscode-branch.svg)

1. Click `main` in the lower left → **+ Create new branch...** → type a name (`try-sleep`) and press Enter. You move to that branch
2. Edit as usual and **Commit**. The blue button becomes **Publish Branch**; press it to send to GitHub
3. If it works, move to `main` in the lower left → **Git: Merge...** in the Command Palette → choose `try-sleep` → **Sync Changes**
4. Delete branches you no longer need with **Git: Delete Branch...**

- Before moving to another branch, commit your changes or set them aside with Stash (Chapter 7)
- If you want to compare on GitHub before bringing changes into `main`, use a Pull Request (the GitHub Pull Requests extension below)

## Fixing conflicts

If both sides changed the same place when you Sync Changes or Merge, a **Merge Changes** section appears in Source Control, listing files marked with `!`. When you open one, it looks like this.

![The conflict screen](images/en/vscode-conflict.svg)

1. Press one of **Accept Current Change**, **Accept Incoming Change** or **Accept Both Changes** above the markers (or rewrite it by hand)
2. When you have fixed every place, save, build and check that it works
3. Press **＋** on the file under Merge Changes
4. The description "Merge branch …" is already filled in, so just press **Commit** → **Sync Changes**

- Pressing **Resolve in Merge Editor** lets you fix it in a view with three panes: local, incoming and the result. When you are done, press **Complete Merge**
- To give up and go back to before the merge, run `git merge --abort` in the terminal (Chapter 7)

## Commonly used Git: commands

Press **Ctrl + Shift + P** and type `git` to choose operations that have no button.

| Command Palette | What it does | Command |
| --- | --- | --- |
| Git: Clone | Clone | `git clone` |
| Git: Initialize Repository | Make the current folder a repository | `git init` |
| Git: Create Branch... | Make a branch and move to it | `git switch -c` |
| Git: Checkout to... | Move to a branch | `git switch` |
| Git: Merge... | Bring changes into the current branch | `git merge` |
| Git: Delete Branch... | Delete a branch | `git branch -d` |
| Git: Create Tag / Git: Push Tags | Add a marker, send it | `git tag`, `git push --tags` |
| Git: Undo Last Commit | Undo the last commit (the changes are kept) | `git reset --soft HEAD~1` |
| Git: Show Git Output | See the git commands VS Code ran, and the full text of errors | |

When a button gives an error, look at the real error message with **Git: Show Git Output** and search for it in Appendix A.

## Handy extensions

git and signing in to GitHub are built into VS Code from the start. The following make things even easier if you install them.

| Extension (author) | Role | How to install |
| --- | --- | --- |
| **Git Graph** (mhutchie) | See the commit history as a branching diagram. Right-click for tags, branches and reverting | `code --install-extension mhutchie.git-graph` |
| **GitLens** (GitKraken) | Shows faintly to the right of each line "who changed it, when and in which commit". Lets you dig into the history (some features are paid) | `code --install-extension eamodio.gitlens` |
| **GitHub Pull Requests** (GitHub) | Make, view and review Pull Requests and Issues inside VS Code | `code --install-extension github.vscode-pull-request-github` |
| **GitHub Actions** (GitHub) | See the results of automatic builds on GitHub in VS Code | `code --install-extension github.vscode-github-actions` |
| **Remote - SSH** (Microsoft) | Open folders on a Raspberry Pi or Jetson in VS Code on your PC. Source Control also runs with that machine's git | `code --install-extension ms-vscode-remote.remote-ssh` |

You can see installed extensions under **Extensions** on the left (the icon of four squares, Ctrl + Shift + X). You can also install them by searching for the name and pressing **Install**.

### Git Graph

Open it with the Git Graph icon at the top of Source Control, or **Git Graph** in the lower left.

![The Git Graph extension](images/en/vscode-git-graph.svg)

- When you have branched and merged, you can see at a glance where things split and where they joined
- Click a commit to see the list of files it changed. Click a file to see the differences side by side
- You can also see the history with **Graph** in Source Control. The difference is that Git Graph lets you do more with right-click

### Remote - SSH

This lets you edit files on a Raspberry Pi or Jetson directly in VS Code on your PC.

1. In the lower left, click **><** (Open a Remote Window) → **Connect to Host...** → type `pi@raspberrypi.local`
2. A new window opens and connects to the Raspberry Pi (the first time, VS Code components are installed on the Raspberry Pi, so wait a little)
3. Open `~/collar` with **Open Folder**

Source Control and the terminal also run inside the Raspberry Pi. To send from the Raspberry Pi to GitHub, register an SSH key on the Raspberry Pi too (Chapter 8).

## Settings

Type a name in the box at the top of **Ctrl + ,** (Settings) to find that setting. Change them as you like.

| Setting | What changing it does | Recommended |
| --- | --- | --- |
| `git.autofetch` | Checks GitHub for new commits from time to time | ☑ (on) |
| `git.enableSmartCommit` | If you press Commit with nothing on the stage, commits everything | ☑ (when developing alone) |
| `git.confirmSync` | Shows the confirmation for Sync Changes | ☐ stops it asking |
| `git.postCommitCommand` | After committing, automatically send (`push`) or bring in and send (`sync`) | As you like |

## Summary

- The blue button in Source Control (Ctrl + Shift + G) is the next thing to do. Repeat Commit → Sync Changes
- Click a file to see the differences. The colors next to the line numbers mean added (green), changed (blue) and deleted (red)
- Branches are from the name in the lower left. For conflicts, press Accept … then ＋ → Commit
- For operations without a button, use `Git:` in the Command Palette. See errors with Git: Show Git Output
- To see the history as a diagram, use Git Graph; to work on a Raspberry Pi or Jetson from your PC, use Remote - SSH

## Exercises

```quiz
Q: Which keys open the Source Control view in VS Code?
A: Ctrl+Shift+G | Ctrl + Shift + G | Ctrl Shift G
E: The big blue button tells you what to do next.

Q: In VS Code, a green mark next to a line number means the line was what?
A: added | add
E: Blue means changed, red means deleted.

Q: Which extension shows branch history as a graph?
A: Git Graph | GitGraph
E: Remote - SSH lets you work on a Raspberry Pi or Jetson from your PC.

Q: What do you type in the Command Palette to find git actions that have no button?
A: Git: | Git
E: To see errors, use Git: Show Git Output.
```
