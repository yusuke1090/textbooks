# 3. Connecting to GitHub with an SSH key

## What you will learn

- Two ways to connect to GitHub (SSH keys and HTTPS)
- How to make an SSH key and register it with GitHub
- How to check that the connection works
- How to switch a repository you used over HTTPS to SSH

## Choosing how to connect

To clone a private repository or to push, your PC has to prove to GitHub that it is you. **Your GitHub password cannot be used** (it is refused if you type it). There are two ways.

| Method | Repository URL | Preparation | Good when |
| --- | --- | --- | --- |
| **SSH key** (recommended) | `git@github.com:username/collar.git` | Make a key and register it with GitHub (below) | Everyday development. Machines without a browser, such as a Raspberry Pi or Jetson |
| HTTPS and gh | `https://github.com/username/collar.git` | Log in from a browser with `gh auth login` | You want to start quickly. VS Code's Publish to GitHub also uses this |

Either way, you can do the same things. You can use both on one PC. This textbook uses SSH keys.

## What is an SSH key?

![Connecting to GitHub with an SSH key](images/en/git-ssh-keys.svg)

An SSH key is a pair of two files: a **private key** and a **public key**.

| File | Contents | How to handle it |
| --- | --- | --- |
| `~/.ssh/id_ed25519` | Private key | **Never give it to anyone.** Do not copy it to other machines, and do not upload it to GitHub |
| `~/.ssh/id_ed25519.pub` | Public key (`.pub` is short for public) | Fine to share. Register it with GitHub |

GitHub lets a machine in as you only if it has the private key that pairs with a registered public key.
Make **one pair per machine** (one each for your PC, laptop, Raspberry Pi and Jetson). If you lose one, you can delete just that key from GitHub's list, and the other machines keep working.

## 1. Check whether you have a key

```bash
ls ~/.ssh
```

If `id_ed25519` and `id_ed25519.pub` are there, you have already made one. Go on to "3. Register the public key with GitHub".
If you see `No such file or directory`, or only `known_hosts` or `authorized_keys`, make one in the next step.

## 2. Make a key

```bash
ssh-keygen -t ed25519 -C "main-pc"
```

You are asked the following.

| Question | How to answer |
| --- | --- |
| `Enter file in which to save the key (/home/username/.ssh/id_ed25519):` | Just press Enter (make it in the standard place) |
| `Enter passphrase (empty for no passphrase):` | Type a passphrase (a password for the key). Nothing appears on screen. This keeps the key from being used even if your PC is stolen |
| `Enter same passphrase again:` | Type the same one again |

When a square pattern appears after `The key's randomart image is:`, you are done.

- `-t ed25519` is the type of key. It is the type recommended today: short and secure
- `-C` is a note attached to the key. Use a name that tells you which machine's key it is (to tell them apart in GitHub's list)
- On a machine without a screen, such as a Raspberry Pi, if you want it to `git pull` automatically, leave the passphrase empty (just press Enter). In exchange, register that key as "read-only" (deploy keys, Chapter 8)

## 3. Register the public key with GitHub

Show the contents of the public key.

```bash
cat ~/.ssh/id_ed25519.pub
```

You get one line like `ssh-ed25519 AAAAC3Nza…(long text)… main-pc`. Copy all of it (Ctrl + Shift + C in the terminal).

1. On GitHub, click your icon in the upper right → **Settings** → **SSH and GPG keys** on the left
2. Press **New SSH key**
3. In **Title**, write which machine's key it is (for example `main-pc`). Leave **Key type** as **Authentication Key**
4. Paste the line you copied into **Key**
5. Press **Add SSH key** (answer if asked for your password or two-factor authentication)

> **Do not paste the one without `.pub` (the private key).** A private key starts with `-----BEGIN OPENSSH PRIVATE KEY-----`.
> If you did paste it, delete that key from GitHub, go back to step 2 and make a new key.

### Registering in one go with gh

If you use gh, choosing SSH when you log in also registers the key (and makes one if you do not have it) in one go.

```bash
gh auth login
```

| Question | What to choose |
| --- | --- |
| Which GitHub | **GitHub.com** |
| Method used for git operations (protocol) | **SSH** |
| Whether to upload a public key (or make one, if you have none) | Choose `~/.ssh/id_ed25519.pub` (when making one, you are asked for a passphrase and a Title) |
| How to log in | **Login with a web browser** → enter the 8-character code shown into the browser that opens |

- `gh auth status` shows whether you are logged in and which method is used (`Git operations protocol: ssh`)
- If you are already logged in with HTTPS and want to switch to SSH, type `gh config set git_protocol ssh`. Repositories you make or clone with gh after this will use SSH URLs

## 4. Check the connection

```bash
ssh -T git@github.com
```

The first time, you are asked something like this.

```text
The authenticity of host 'github.com (…)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

If the part after `SHA256:` matches the one listed on GitHub's [SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) page, type `yes`.
This is to check that you are really talking to GitHub, and you are asked only the first time (it is remembered in `~/.ssh/known_hosts`). If you are asked for a passphrase, type the one you chose in step 2.

```text
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see this, it worked. The part about "shell access" means you cannot log in to GitHub and type commands there; git itself works.
If you see `Permission denied (publickey).`, see Appendix A "Common errors".

## 5. Stop being asked for the passphrase every time

On the Ubuntu desktop, a helper that remembers keys (ssh-agent) is running. If you are asked for the passphrase every time, write these two lines in `~/.ssh/config` (`nano ~/.ssh/config`).

```text
Host *
    AddKeysToAgent yes
```

After you type the passphrase once, you are not asked again until you log out. `ssh-add -l` shows the keys it remembers.

## Switching a repository you used over HTTPS to SSH

Repositories cloned with `git clone https://…` and repositories put up with VS Code's Publish to GitHub have HTTPS URLs. To switch to SSH, do the following.

```bash
cd ~/apps/collar
git remote -v
git remote set-url origin git@github.com:username/collar.git
git remote -v
```

Check with `git remote -v` that the URL of `origin` has changed to `git@github.com:…`.

## Summary

- You cannot clone or push with your GitHub password. Use an SSH key or `gh auth login`
- One SSH key pair per machine. Never give away the private key; register the public key (`.pub`) with GitHub
- Check with `ssh -T git@github.com`

## Exercises

```quiz
Q: Of the two SSH keys, which one do you register on GitHub?
A: public key | public | the public key
E: Never give your private key to anyone.

Q: What extension does the public key file end with?
A: .pub | pub
E: For example `~/.ssh/id_ed25519.pub`.

Q: Which command checks that you can connect to GitHub over SSH?
A: ssh -T git@github.com
E: If it greets you by name, you are connected.

Q: How many SSH key pairs do you make for each machine?
A: 1 | one
E: One pair per machine; register each public key on GitHub.
```
