# 6. Going back to an earlier state

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

## Exercises

```quiz
Q: Which command throws away changes that are not committed yet?
A: git restore | restore
E: The file goes back to its last committed state.

Q: Which command undoes a commit you already pushed, by adding a new commit?
A: git revert | revert
E: It does not rewrite history, so it is safe after pushing.

Q: `git commit --amend` fixes the last commit. When is it safe to use?
A: before pushing | before push | before you push
E: Using it after pushing makes your history differ from GitHub.

Q: This book says never to use `reset --hard` and what other command?
A: push --force | git push --force | --force | push -f
E: Both can destroy records in a way you cannot undo.
```
