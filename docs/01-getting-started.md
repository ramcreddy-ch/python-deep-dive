# 01. Getting Started — Runtimes, Environments & Internals

> "The difference between a coder and a principal engineer is understanding not just how to run code, but the environment in which it lives. Mastering runtimes and isolated environments is the foundation of reliable, scalable software."

---

## ❓ The 'Why' (High-Level)
Python is the world's most popular language for AI, Data Science, and DevOps. Why? because it prioritizes **Developer Velocity** over raw CPU speed. In a world where developer time is more expensive than server time, Python wins. As an expert, you must understand the trade-offs: *High-level abstraction comes at the cost of the Global Interpreter Lock (GIL) and higher memory overhead.*

---

## 🌱 Module 1: The Basics (Junior) — Setting the Stage
To start, you need a runtime. But an expert never just "installs Python" from a website. We use tools to manage versions.

### 1. Version Management with `pyenv`
Never use the "System Python" (the one your OS uses for its own tasks). If you break it, you break your OS.
- **Tool**: `pyenv` (or `pyenv-win` for Windows).
- **Command**: `pyenv install 3.12.0` -> `pyenv global 3.12.0`.

### 2. The Survival Kit: `id()`, `type()`, `help()`
Before writing scripts, use the REPL (Read-Eval-Print Loop) to inspect objects.
```python
x = 42
print(type(x))  # <class 'int'> - Everything in Python is an object!
print(id(x))    # The unique memory address of this object.
help(print)     # Pull up documentation directly in the terminal.
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Isolation
Projects require different versions of libraries. Isolation is mandatory.

### 1. Virtual Environments (`venv`)
A `venv` is essentially a folder containing a copy of the Python binary and its own `site-packages` folder.
```bash
python -m venv .venv
source .venv/bin/activate  # Activates the local context
pip install requests       # Installed ONLY in this project
```

### 2. Modern Dependency Management: Poetry
Senior engineers avoid `requirements.txt` because it doesn't lock sub-dependencies.
- **Why Poetry?**: It uses `pyproject.toml` (PEP 517) and `poetry.lock`.
- **Benfit**: It guarantees that every developer on your team has the **exact** same environment, preventing "It works on my machine" bugs.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — The Interpreter
What happens when you run `python script.py`? It's a five-stage journey.

1.  **Lexing**: The code is broken into "tokens" (keywords, variables).
2.  **Parsing**: Tokens are organized into an **Abstract Syntax Tree (AST)**.
3.  **Compilation**: The AST is converted into **Bytecode**—low-level instructions for the Python Virtual Machine (PVM).
4.  **Storage**: Bytecode is cached in `__pycache__` as `.pyc` files for faster future startups.
5.  **Execution**: The PVM reads the bytecode and executes it.

### Inspecting Bytecode
You can see exactly what the CPU sees using the `dis` module.
```python
import dis
def add(a, b): return a + b
dis.dis(add)
# Shows: LOAD_FAST (a), LOAD_FAST (b), BINARY_OP (+), RETURN_VALUE
```

---

## 🔥 Module 4: Principal Architect (Principal) — Runtimes & Scaling
At the highest level, you choose the right **Implementation** of the Python language.

### 1. Implementation Flavors
- **CPython**: The standard (C-based). Great for general use and C-extensions (NumPy).
- **PyPy**: Uses a **JIT (Just-In-Time)** compiler. It analyzes code as it runs and compiles "hot spots" into machine code. It's often 5x faster for heavy math but uses more memory.
- **MicroPython**: Optimized for microcontrollers (tiny RAM/Flash).

### 2. The Global Interpreter Lock (GIL)
Python's memory management is not thread-safe. To prevent crashes, CPython uses the GIL—a "lock" that ensures only **one** thread executes Python bytecode at a time. This is why standard Python threads aren't great for CPU-bound tasks (use `multiprocessing` instead).

---

## 🏗️ Case Study: Environment Management at Scale
When **Instagram** scaled to millions of users, they faced a "Dependency Hell" with hundreds of microservices. 
- **The Solution**: They strictly enforced standard `pyproject.toml` files and used custom Docker base images that pre-compiled bytecode (`.pyc`) during the build phase. This reduced their cold-start time by 40%, saving thousands of dollars in compute costs during autoscaling events.

---

## ⚡ Anti-Patterns & Expert Traps
- **Trap 1: The Global Install**: Running `sudo pip install` is a death sentence for your system's stability.
- **Trap 2: Ignoring `.gitignore`**: Never commit your `.venv/` or `__pycache__/` folders to Git. It bloats the repo and breaks other people's builds.
- **Trap 3: Running as Root**: Never run your Python app as the `root` user in production; use a limited service account for security.

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
