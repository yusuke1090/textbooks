# 8. Cloning from another machine

## What you will learn

- Getting ready to develop on another PC
- How to put a read-only key (a deploy key) on a Raspberry Pi or Jetson
- How to lend your PC's key with ssh -A
- How to clone directly from your PC without going through GitHub

## Choosing a method

To get a **private** GitHub repository on a Raspberry Pi, Jetson or another PC, that machine also has to prove to GitHub that it is you. Choose according to how you use it.

| Method | What it allows | Good when |
| --- | --- | --- |
| **Make a key on that machine and register it with your account** | Clone and push all your repositories | Developing on another PC |
| **Deploy key** (registered for that repository only) | Only one repository. Usually read-only | A Raspberry Pi or Jetson that only fetches and runs a fixed program |
| **Lend your PC's key with ssh -A** | Use your PC's key only while you are logged in over ssh | You want to clone on a Raspberry Pi temporarily, without leaving a key on the machine |
| **Directly from your PC, not through GitHub** | Clone your PC's repository within the same LAN | You do not want to put it on GitHub, or there is no internet |

## Developing on another PC

On that PC, follow "1. Check whether you have a key" to "4. Check the connection" in Chapter 3. For `-C` and the Title, use a name that identifies that PC (for example `laptop`).
Then clone as in "Starting from a repository on GitHub (clone)" in Chapter 4. On the second PC too, do not forget to set your name and email address as in Chapter 2.

## Putting a read-only key on a Raspberry Pi or Jetson (deploy keys)

On a Raspberry Pi or Jetson, you usually only fetch code and run it; you rarely send anything to GitHub from there.
In that case, use a read-only key that works only for that repository (a deploy key). Even if the key is stolen, it cannot be used for other repositories or for writing.

First, log in to the Raspberry Pi and make a key.

```bash
ssh pi@raspberrypi.local
ssh-keygen -t ed25519 -C "raspi-collar" -f ~/.ssh/collar_deploy -N ""
cat ~/.ssh/collar_deploy.pub
```

- `-f` is the name of the key file. Because you use a separate key for each repository, give it a clear name rather than the standard one (`id_ed25519`)
- `-N ""` makes the passphrase empty. This is so that `git pull` can run automatically

Register the line that appears with GitHub.

1. On GitHub, open the repository's (`collar`) page → **Settings** → **Deploy keys** on the left
2. Press **Add deploy key**
3. Put `raspi` in **Title**, and paste the line into **Key**
4. **Leave Allow write access unchecked** (read-only), and press **Add key**

Next, write a "nickname" that uses this key in the Raspberry Pi's `~/.ssh/config` (`nano ~/.ssh/config`).

```text
Host github-collar
    HostName github.com
    User git
    IdentityFile ~/.ssh/collar_deploy
    IdentitiesOnly yes
```

Check using the nickname, then clone.

```bash
ssh -T git@github-collar
git clone git@github-collar:username/collar.git ~/collar
```

If `ssh -T` shows `Hi username/collar! You've successfully authenticated…`, you are connected (with a deploy key, the repository name is shown).
To get new code, move there with `cd ~/collar` and run `git pull`.

- `github-collar` is a nickname that means "connect to github.com with the `collar_deploy` key". Write `git@github-collar:` instead of `git@github.com:`
- One deploy key can be registered for only one repository. For a second repository, make another key (for example `logger_deploy`) and another nickname (for example `github-logger`)
- When you no longer use a key, delete it from GitHub's Deploy keys

## Lending your PC's key with ssh -A

If you add `-A` when logging in from your PC to a Raspberry Pi with ssh, you can connect to GitHub with your PC's key while you are logged in. The private key is not copied to the Raspberry Pi.

```bash
ssh -A pi@raspberrypi.local
ssh -T git@github.com
git clone git@github.com:username/collar.git
```

- Type the first line on your PC, and from the second line on, inside the Raspberry Pi
- Your PC's key must be in ssh-agent (typing `ssh-add -l` on your PC shows the key)
- Use this only on machines that you alone manage. On a machine where others can become administrators, they could use your key, so do not use it there

## Cloning directly from your PC, not through GitHub

Within the same LAN, you can clone your PC's repository directly over ssh without putting it on GitHub. Make your PC a machine you can log in to with ssh.

1. Install an ssh server on your PC (it starts running automatically once installed)

```bash
sudo apt install openssh-server
hostname
```

Other machines on the same LAN connect using the name shown by `hostname` with `.local` added (for example `main-pc.local`). If that does not work, use the IP address shown by `hostname -I` (for example `192.168.1.20`).

2. On the machine you want to clone to, such as the Raspberry Pi, make a key and register it with your PC

```bash
ssh-keygen -t ed25519 -C "raspi"
ssh-copy-id username@main-pc.local
ssh username@main-pc.local
```

`ssh-copy-id` asks for your PC's login password once. The public key is added to `~/.ssh/authorized_keys` on your PC.
If the third line logs you in without a password, it worked. Go back with `exit`.

3. Clone

```bash
git clone username@main-pc.local:apps/collar
```

After the `:` comes the location from your home folder on the PC. After cloning, you can bring in new commits from the PC with `git pull`.

### When you also want to send from the Raspberry Pi

You cannot push directly into your PC's working folder (`~/apps/collar`) from other machines (you get `refusing to update checked out branch`). When you want to send from both, make a "storage-only repository" (a bare repository) on your PC and use it in place of GitHub.

```bash
git clone --bare ~/apps/collar ~/git/collar.git
cd ~/apps/collar
git remote add lan ~/git/collar.git
```

- On the PC, send to the storage with `git push lan main` and bring things in with `git pull lan main`
- On other machines, clone with `git clone username@main-pc.local:git/collar.git` and use `git push` and `git pull` as normal
- `--bare` makes a repository with only the record and no working folder (the same form as the ones inside GitHub)

> This method only works while your PC is turned on and on the same LAN. Usually, using GitHub is easier.
> Since your PC can now be logged in to over ssh, use a PC password that is hard to guess. When you no longer need it, stop it with `sudo apt remove openssh-server`.

## Summary

- To develop on another PC, make a key on that PC too and register it with GitHub
- If a Raspberry Pi or Jetson only fetches code, use a read-only deploy key
- To avoid GitHub, connect to your PC over ssh and clone from it
