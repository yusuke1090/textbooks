# Appendix A. Common errors

## Errors and how to fix them

| Error | Meaning and fix |
| --- | --- |
| `Permission denied (publickey).` | GitHub (or the PC) does not accept the key. Check ① whether you have a key with `ls ~/.ssh`, ② whether the contents of that machine's `.pub` are registered under SSH keys on GitHub, and ③ whether the key is loaded with `ssh-add -l`. `ssh -vT git@github.com` shows which keys it tried |
| `Host key verification failed.` | It could not verify the other side (github.com or the PC). For example, you did not type `yes` the first time. Type `ssh -T git@github.com` and answer `yes` again |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | The other side's key is different from the last time you connected. This happens when you reinstall the Raspberry Pi's OS. If you know you reinstalled it yourself, delete the old record with `ssh-keygen -R raspberrypi.local`. If you have no idea why, do not connect |
| `ssh: connect to host … port 22: Connection refused` | No ssh server is running on the other side. For a PC, `sudo apt install openssh-server` |
| `remote: Support for password authentication was removed` | You typed your GitHub password with an HTTPS URL. Log in with `gh auth login`, or change to an SSH URL (`git remote set-url`; Chapter 3) |
| `ERROR: Repository not found.` | The URL is misspelled, or this key (account) cannot see the repository. For a deploy key, check that the nickname and repository match |
| `fatal: not a git repository` | You are in a folder that is not a git repository. Move with something like `cd ~/apps/collar` |
| `Author identity unknown` | Your name and email address are not registered. Make the settings in Chapter 2 |
| `error: src refspec main does not match any` | You have not made a single commit yet. Or the branch is named `master` (check with `git branch` and rename with `git branch -m master main`) |
| `! [rejected] main -> main (fetch first)` | GitHub has commits you do not have locally (you pushed from another PC). `git pull`, then `git push` |
| `fatal: Need to specify how to reconcile divergent branches.` | Both sides changed things, and how to combine them has not been set. Type `git config --global pull.rebase false` and `git pull` again |
| `CONFLICT (content): Merge conflict in …` | Both sides changed the same place. See "When both sides changed" in Chapter 7 |
| `fatal: refusing to merge unrelated histories` | You tried to connect your local repository to one made on GitHub with a README or the like. Combine them with `git pull origin main --allow-unrelated-histories`, then `git push` |
| `fatal: remote origin already exists.` | origin is already registered. Change the URL with `git remote set-url origin URL` |
| `error: Your local changes to the following files would be overwritten` | You have uncommitted changes, so you cannot pull or switch branches. Commit them, or set them aside with `git stash` |
| `refusing to update checked out branch` | You pushed directly into a PC's working folder. Use the bare repository from "When you also want to send from the Raspberry Pi" in Chapter 8 |
| `this exceeds GitHub's file size limit of 100.00 MB` | You committed a file that is too big. If it was the last commit: `git rm --cached filename` → write it in `.gitignore` → `git commit --amend --no-edit` → `git push` |
| A `:` or `(END)` appears at the bottom of the screen and it stops | You are partway through the output of `git log` or `git diff`. Quit with `q` |
| An unfamiliar screen (an editor) opened | It is the screen for writing a commit or merge description. In nano, Ctrl + O → Enter → Ctrl + X. In vim, type `:wq` and press Enter |
