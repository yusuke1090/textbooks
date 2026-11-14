# 1. What is Python? Getting ready

## What you will learn

- Python's features and what it can be used for
- Getting ready to write and run Python on Ubuntu with VS Code (virtual environments)
- How to read errors

## What is Python?

| Feature | Explanation |
| --- | --- |
| Easy to read | No `;` at the end of statements and no `{ }`; indentation shows how code is grouped |
| Runs right away | You can run what you write without compiling (an interpreter) |
| Many libraries | Data analysis (NumPy, pandas), graphs (matplotlib), machine learning (scikit-learn, PyTorch), controlling a Raspberry Pi and more |

On the other hand, it runs slower than C++. Heavy calculations are left to libraries written in C or C++ inside (such as NumPy).

After this textbook, you can move on to the "Machine Learning Textbook" and the "Statistics Textbook". The differences from C++ are summarized in Appendix A of the "C++ Textbook".

## Getting ready (Ubuntu and VS Code)

### Python and virtual environments

Ubuntu comes with `python3` already installed.

```bash
python3 --version
sudo apt install python3-venv python3-pip
```

Install libraries into a per-folder **virtual environment** (venv). On current Ubuntu, running `pip install` outside a virtual environment gives the error `externally-managed-environment` (to avoid breaking the system's Python).

```bash
mkdir -p ~/apps/py-study
cd ~/apps/py-study
python3 -m venv .venv            # create a virtual environment in a folder called .venv
source .venv/bin/activate        # enter the virtual environment ((.venv) appears at the start of the line)
pip install numpy pandas matplotlib
deactivate                       # leave the virtual environment
```

While you are in the virtual environment, `python` and `pip` are the ones in this virtual environment.

### VS Code

1. Open the folder in VS Code with `code .`
2. Install the "Python" extension (Microsoft)
3. **Ctrl + Shift + P** → "Python: Select Interpreter" → choose the one in `.venv`. Now VS Code uses the virtual environment
4. Create `hello.py`, write the following line and save

```python
print("Hello, Python!")
```

5. Press ▶ in the upper right, or run it in the terminal (**Ctrl + `**)

```bash
python hello.py
```

```text
Hello, Python!
```

### Interactive mode

If you type just `python` in the terminal (`python3` outside a virtual environment), you get **interactive mode**, where you can try one line at a time.

```text
>>> 1 + 2
3
>>> exit()
```

### Jupyter notebooks

An `.ipynb` file lets you put code and its results and graphs one after another. Install the "Jupyter" extension in VS Code, run `pip install ipykernel`, and then create an `.ipynb` file to use it. It is good for data analysis, where you move forward while trying things.

## How to read errors

```text
Traceback (most recent call last):
  File "/home/user/apps/py-study/hello.py", line 3, in <module>
    print(total / count)
          ~~~~~~^~~~~~~
ZeroDivisionError: division by zero
```

- **The last line** gives the type of error and the reason (here, "divided by 0")
- Above it is the **file and line** where the error happened (line 3)
- If it happened inside a function, the calls are listed from the top in the order they were made. Start from the lowest line in your own file

Common errors are summarized in Chapter 6.

## Summary

- Python is easy to read, runs right away and has many data analysis libraries
- Install libraries in a virtual environment (`python3 -m venv .venv` → `source .venv/bin/activate` → `pip install`)
- In VS Code, choose `.venv` with "Python: Select Interpreter"
- Read errors from the last line
