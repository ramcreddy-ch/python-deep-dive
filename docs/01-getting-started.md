# 01. Getting Started — Runtimes, Environments & Virtualization

> "The first step to expertise is understanding the difference between how code is written and how code is executed. An expert doesn't just 'install Python'; they manage isolated runtimes and understand the underlying interpreter mechanics."

---

## 🌱 The Basics: What is Python?
Python is an **Interpreted, High-Level** language. 
- **Interpreted**: Unlike C++, Python code isn't compiled into a binary first. It's read line-by-line by the Python Interpreter (CPython).
- **Dynamic**: You don't need to declare that a variable is an `int` or `string`. Python figures it out at runtime.

### Simple Setup
1.  **Installation**: Download from `python.org`.
2.  **Verification**: Run `python --version` in your terminal.
3.  **The REPL**: Type `python` to enter the interactive shell for quick testing.

---

## 🌿 Intermediate: Virtual Environments (venv)
**Why?** If Project A needs `pandas v1.0` and Project B needs `pandas v2.0`, a global install will break one of them.
**Solution**: `venv` creates a "copy" of the Python interpreter inside your project folder.

```bash
# 1. Create the environment
python -m venv .venv

# 2. Activate it 
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 3. Install packages locally
pip install requests
```

---

## 🌳 Advanced: Modern Dependency Management (Poetry)
In production, standard `requirements.txt` is often insufficient because it doesn't "lock" sub-dependencies. **Poetry** is the industry standard for senior engineers.

**Real Use (DevOps/Cloud)**:
- **Reproducibility**: `poetry.lock` ensures every developer and Every CI/CD runner has the *exact* same version of every package down to the byte.
- **Packaging**: Poetry makes it trivial to bundle your code into a `.whl` (Wheel) file for distribution.

---

## 🔥 Expert: Runtimes & Internals
For principal-level engineering, you must know that "Python" isn't just one thing.

### 1. CPython vs. Others
- **CPython**: The standard (C-based) implementation.
- **PyPy**: A JIT (Just-In-Time) compiler version that is 5x-10x faster for long-running math loops.
- **Jython/IronPython**: Python running on Java/C# runtimes.

---

## 🎯 Top 20 Principal Interview Questions (Runtimes & Setup)

1. **Q: Is Python truly an interpreted language?**
   - **Answer**: Technically, no. Python is compiled into **Bytecode** (.pyc files) and then interpreted by the Python Virtual Machine (PVM). It is more accurate to call it "Bytecode-compiled."
2. **Q: How does `venv` actually work under the hood?**
   - **Answer**: It copies the `python` executable to a local folder and modifies the `sys.prefix` and `sys.base_prefix` variables. When the interpreter starts, it sees its "Home" is the local folder and prioritizes the local `site-packages` directory for imports.
3. **Q: What is the difference between `pyproject.toml` and `setup.py`?**
   - **Answer**: `setup.py` is an executable script (unsafe), whereas `pyproject.toml` is a declarative configuration file (safe). PEP 517/518 standardized `pyproject.toml` as the modern way to define build systems like Poetry and Flit.
4. **Q: When would you use PyPy over CPython?**
   - **Answer**: When you have a CPU-bound application (like a heavy math algorithm) that cannot be easily moved to a C-extension or NumPy, and you need raw execution speed without changing the code.
5. **Q: What is the `sys.path` and how is it populated?**
   - **Answer**: It's a list of strings specifying the search path for modules. It's populated from the current directory, the `PYTHONPATH` environment variable, and the installation-dependent defaults (site-packages).
6. **Q: What is the difference between a virtual environment and a container (Docker)?**
   - **Answer**: A virtual environment isolates only Python libraries. A container isolates the **entire Operating System**, including the kernel, file system, and network stack.
7. **Q: How can you check all installed packages in a format that can be re-installed?**
   - **Answer**: Use `pip freeze > requirements.txt`.
8. **Q: What is a 'Wheel' (.whl) file?**
   - **Answer**: It is a "Built Distribution" format. Unlike a search distribution (.tar.gz), it is already compiled and ready to use, making installation much faster.
9. **Q: What is the 'Shebang' line (`#!`) in a Python script?**
   - **Answer**: It tells the Unix/Linux shell which interpreter to use to run the script (e.g., `#!/usr/bin/env python3`).
10. **Q: How do you handle multiple Python versions on one machine?**
    - **Answer**: Use a tool like **pyenv** or **conda** to manage and switch between different versions globally or per-project.
11. **Q: What is the difference between `pip install` and `pip install -e .`?**
    - **Answer**: `-e` stands for **Editable**. It creates a symbolic link to your source code, so any changes you make to the code are immediately reflected in the installed package without re-installing.
12. **Q: What is the `site-packages` directory?**
    - **Answer**: It is the default location where third-party libraries installed via `pip` are stored.
13. **Q: How does Python find its built-in modules like `os` or `sys`?**
    - **Answer**: These are either built into the C-interpreter itself (CPython) or located in the standard library directory that is automatically added to `sys.path`.
14. **Q: What is the `sys.executable` variable?**
    - **Answer**: It contains the absolute path to the Python interpreter binary currently running the script. Use it to ensure you are calling the "Correct" python in child processes.
15. **Q: What is a 'Namespace' in Python?**
    - **Answer**: A mapping from names to objects. Examples include global names in a module, local names in a function, and built-in names.
16. **Q: What is the purpose of `__pycache__` folders?**
    - **Answer**: They store the compiled bytecode (.pyc) so that Python doesn't have to re-compile the source code every time it's imported, speeding up startup time.
17. **Q: Can you run Python code without installing it?**
    - **Answer**: Yes, using the official "Embeddable" zip distribution or by running it inside a Docker container.
18. **Q: What is the difference between `bash` and `python` scripts for automation?**
    - **Answer**: Bash is better for simple OS-level commands. Python is better for complex logic, error handling, and cross-platform compatibility.
19. **Q: What is the `PYTHONPATH` environment variable?**
    - **Answer**: It is used to add custom directories to the `sys.path` search list for imports.
20. **Q: How do you verify the integrity of a package installed via pip?**
    - **Answer**: Use `pip check` to look for broken dependencies or use `pip show --files [package]` to see installed file paths.

---

[Next: Data Types & Variables →](02-data-types-variables.md)
