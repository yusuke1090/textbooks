# 6. Going back to an earlier state

## What you will learn

- How to throw away changes you have not committed
- How to fix the last commit
- How to undo a commit you have pushed
- How to look at or take out an earlier state

## Commands by what you want to do

| What you want to do | Command | Caution |
| --- | --- | --- |
| Throw away uncommitted changes | `git restore filename` | Changes you throw away cannot be recovered |
| Take something off the stage (keep the changes) | `git restore --staged filename` | |
| Fix the description of the last commit | `git commit --amend -m "new description"` | **Only before pushing** |
| Add a file you forgot to the last commit | `git add filename` → `git commit --amend --no-edit` | **Only before pushing** |
| Undo a commit you pushed | `git revert commit-number` → `git push` | A new "undo" commit is made. The history is not erased |
| Take out one file from an earlier commit | `git restore --source commit-number filename` | Replaces the current file (it is recorded if you commit) |
| Just look at the state of an earlier commit | `git switch --detach commit-number` → to go back, `git switch main` | Changes made while looking are thrown away when you go back to main |
| Set aside work in progress for a while | `git stash` → later `git stash pop` | When you cannot pull or switch branches |
| Rebuild a version you shipped | `git switch --detach v1.0.0` → build → `git switch main` | If you added a tag (Chapter 5) |

> `git reset --hard` and `git push --force`, which you will find when searching, **are commands that erase records.** Do not use them until you understand what they do.
> When you are stuck, first type `git status` and check what is going on.

## Summary

- Undo uncommitted changes with `git restore`, and pushed commits with `git revert`
- `--amend` only before pushing
- Do not use `reset --hard` or `push --force`
