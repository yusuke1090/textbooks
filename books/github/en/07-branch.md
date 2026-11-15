# 7. Trying things on a branch

## Making a branch

When you want to try a big change (adding power saving, changing a sensor and so on) without breaking a working main, make a branch.
If you develop alone and just commit small changes often, main alone is fine.

```bash
git switch -c try-sleep
git add .
git commit -m "Try sleep mode"
git push -u origin try-sleep
```

This makes a branch called `try-sleep`, moves to it, and commits there. main stays as it was.

If it works, bring it into main.

```bash
git switch main
git merge try-sleep
git push
git branch -d try-sleep
git push origin --delete try-sleep
```

To give up, go back to main and delete the branch (`-D` also deletes branches that were not merged).

```bash
git switch main
git branch -D try-sleep
```

| Command | Meaning |
| --- | --- |
| `git branch` | A list of branches. The one with `*` is the branch you are on |
| `git switch -c name` | Make a new branch and move to it |
| `git switch name` | Move to that branch. The files in the working folder change to that branch's state |
| `git merge name` | Bring that branch's changes into the branch you are on |
| `git branch -d name` | Delete a branch that has been merged |

- In VS Code, the name of the current branch is shown in the lower left. Click it to switch or make branches
- Before moving to another branch, commit your changes or set them aside with `git stash`
- On GitHub, you can also make a **Pull Request** from a branch, compare the changes, and then bring them into main (when several people develop together)

## When both sides changed (conflicts)

If you change the same place in the same file on two PCs and then run `git pull` or `git merge`, git cannot decide which one to keep and shows this.

```text
CONFLICT (content): Merge conflict in collar.cpp
Automatic merge failed; fix conflicts and then commit the result.
```

Both versions are in the file, with markers.

```text
<<<<<<< HEAD
const int SAMPLE_HZ = 50;
=======
const int SAMPLE_HZ = 100;
>>>>>>> 9f8e7d6
```

From `<<<<<<<` to `=======` is your local side, and from `=======` to `>>>>>>>` is the side you tried to bring in.

1. When you open the file in VS Code, **Accept Current Change** (keep local), **Accept Incoming Change** (keep the incoming side) and **Accept Both Changes** (both) appear above the markers. Press one, or rewrite it by hand and delete the three marker lines
2. Build it and check that it works
3. `git add collar.cpp` → `git commit` → `git push`

- If nano opens on `git commit`, leave the description as it is, then Ctrl + O → Enter (save) → Ctrl + X (close)
- To give up and go back to before the merge, `git merge --abort`
- If you only changed different places, git combines them automatically (nano still opens so you can write a description for the merge record; save and close it the same way)
- To prevent conflicts, make it a habit to `git pull` before you start and `git push` when you finish

## Summary

- Try big changes on a separate branch with `git switch -c`, and if they work, bring them into main with `git merge`
- For a conflict, choose which side to keep, delete the three marker lines, then `add` → `commit` → `push`
- Prevent conflicts with `git pull` before you start and `git push` when you finish

## Exercises

```quiz
Q: Which command creates a new branch and switches to it?
A: git switch -c | switch -c
E: Try big changes on a separate branch.

Q: Which command brings a finished branch into main?
A: git merge | merge
E: Switch to main, then run `git merge branch-name`.

Q: What is it called when both branches changed the same lines and git cannot combine them?
A: conflict | merge conflict
E: Choose what to keep, delete the three marker lines, then `add` → `commit` → `push`.
```
