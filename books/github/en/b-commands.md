# Appendix B. List of commands

## Commonly used commands

| Task | Command |
| --- | --- |
| Register your name and email address (first time only) | `git config --global user.name "name"`, `git config --global user.email "address"` |
| Make an SSH key (first time only, on each machine) | `ssh-keygen -t ed25519 -C "machine name"` |
| Show the public key | `cat ~/.ssh/id_ed25519.pub` |
| Check the connection to GitHub | `ssh -T git@github.com` |
| Log in with gh | `gh auth login` |
| Make the current folder a repository | `git init` |
| Make it on GitHub and send it | `gh repo create name --private --source=. --push` |
| Connect to a place on GitHub | `git remote add origin git@github.com:username/name.git` → `git push -u origin main` |
| See or change where it is connected | `git remote -v`, `git remote set-url origin URL` |
| Clone | `git clone git@github.com:username/name.git` |
| See the state | `git status` |
| See changes | `git diff`, `git diff --staged` |
| Record | `git add .` → `git commit -m "description"` |
| Send / bring in | `git push`, `git pull` |
| See the history | `git log --oneline`, `git show commit-number` |
| Throw away changes | `git restore filename` |
| Make a commit that undoes another | `git revert commit-number` |
| Set aside / bring back | `git stash`, `git stash pop` |
| Make, move to and merge branches | `git switch -c name`, `git switch name`, `git merge name` |
| Add a marker (tag) | `git tag v1.0.0` → `git push --tags` |
