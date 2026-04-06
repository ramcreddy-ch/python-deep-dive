# 32. Packaging & Distribution — Poetry, PyPI & Versioning

> "Code that only runs on your machine isn't a product; it's a prototype. An expert knows how to package their code so that anyone in the world can install it with a single command. Mastering 'Packaging' is the final stage of becoming a professional Python engineer."

---

## ❓ The 'Why' (High-Level)
The true power of Python isn't the language itself—it's the **200,000+ packages** on PyPI. If you want to use a database, a neural network, or a web server, someone has already built it for you. But to build your own "Library" that other people (or your future self) can use, you must understand how to "Package" your code, manage its "Dependencies" (the other libraries it needs), and "Version" it correctly.

---

## 🌱 Module 1: The Basics (Junior) — Installing Code
The most basic tool is **`pip`** (The Python Package Installer).

### 1. Simple Installation
```bash
pip install requests  # Install a package from the internet (PyPI)
```

### 2. `requirements.txt`
A "List" of all the packages your project needs.
- **Problem**: It doesn't track "Sub-dependencies" (the packages that YOUR packages need!), which can lead to "Version Hell."

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The Modern Standard
Mid-level engineers use modern tools like **Poetry** to manage their projects.

### 1. `pyproject.toml`
This is the **New Standard** for Python projects. It combines your package info, dependencies, and build settings into a single, clean file.

### 2. Virtual Environments (`venv`)
Never install packages globally on your computer. A **Virtual Environment** is a "Sandboxed" folder where you can install packages for one specific project without breaking others.
- **Expert Tool**: **Poetry** handles this automatically for you.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Building & Publishing
Senior engineers know how to "Ship" their code to the world.

### 1. Building a "Wheel" (.whl)
A **Wheel** is a pre-compiled version of your package that is lightning-fast to install.
```bash
poetry build  # Creates a .whl and a .tar.gz file
```

### 2. Publishing to PyPI
The **Python Package Index (PyPI)** is the global repository for Python code.
- **Expert Tool**: Use **Twine** or `poetry publish` to securely upload your code so that anyone can do `pip install your-package`.

---

## 🔥 Module 4: Principal Architect (Principal) — Enterprise Distribution
At the highest level, you manage the "Ecosystem" of a large company.

### 1. Namespace Packages
What if a company has 100 different libraries? Instead of 100 random names, they use **Namespace Packages**, allowing them to have `company.core`, `company.db`, and `company.auth` in different repositories but under the same "Folder" in Python.

### 2. Semantic Versioning (SemVer)
- **1.0.0**: The first stable release.
- **1.1.0**: Added a new feature.
- **2.0.0**: A **Breaking Change** happened (Old code might break!).
- **Principal Choice**: Always use "Pinned" versions (`requests == 2.31.0`) in applications to prevent unexpected breakage.

---

## 🏗️ Case Study: The Library that scaled a Corporation
A global tech firm had 100 different teams all writing the same "Database connection" code. Every team had different bugs.
- **The Junior Approach**: Copy-paste a "Good" version of the code into all 100 repos. (Took weeks, and updates were impossible).
- **The Principal Approach**: Built a single **Internal Package** called `corp-db-utils`. They hosted it on a **Private PyPI** server.
- **Result**: All 100 teams switched to `pip install corp-db-utils`. When the database moved to a new cloud, the Principal updated the package **Once**, and all 100 apps were fixed instantly.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding Versions
Always use a `lock` file (`poetry.lock` or `requirements.txt` with specific versions). If you just say "I need requests," one day a new version of requests will come out and break your whole project.

### 2. Not Testing the "Install"
Sometimes a program runs fine on your computer because you have a file that isn't included in the package. **Expert Fix**: Always test your package by installing it in a **Clean** virtual environment before shipping it.

---

## 🎯 Top 20 Principal Interview Questions (Packaging & Distribution)

1. **Q: What is the purpose of a 'Virtual Environment'?**
   - **Answer**: To provide an **Isolated** space for a project's dependencies, ensuring that different projects with conflicting library versions don't interfere with each other or the system's Python.
2. **Q: What is 'PyPI'?**
   - **Answer**: The **Python Package Index**. It's the official third-party repository for Python software, currently hosting over 200,000 packages.
3. **Q: What is the difference between `requirements.txt` and `pyproject.toml`?**
   - **Answer**: `requirements.txt` is a simple list of packages. `pyproject.toml` is the modern, standardized configuration file for Python that handles builds, dependencies, and tool settings in one place.
4. **Q: Explain 'Semantic Versioning' (SemVer).**
   - **Answer**: A versioning standard of **Major.Minor.Patch**. Increment Major for breaking changes, Minor for new features, and Patch for bug fixes.
5. **Q: What is a 'Wheel' (.whl) file in Python?**
   - **Answer**: A built-package format that is **Ready-to-Install**. It allows for faster installation than a source distribution because it doesn't need to be compiled on the user's machine.
6. **Q: What does 'Poetry' do that 'pip' does not?**
   - **Answer**: Consistency. Poetry automatically manages **Lock files**, virtual environments, and the build/publish process in a single, deterministic way.
7. **Q: What is the purpose of a `poetry.lock` file?**
   - **Answer**: To lock the **Exact version and hash** of every single dependency (and their sub-dependencies) used in the project, ensuring that every developer and server has the identical environment.
8. **Q: What is 'Namespace Packaging'?**
   - **Answer**: A feature that allows a single Python package to be split across multiple different distributions (installers), allowing for modular development of large corporate libraries.
9. **Q: Explain 'Entry Points' in a package.**
   - **Answer**: A way to map a Python function to a **Global Command Line Command**. For example, you can make your package run when the user types `my-tool` in the terminal.
10. **Q: What is the difference between an 'Application' and a 'Library' in packaging?**
    - **Answer**: **Applications** should have strictly pinned versions (`==`) to ensure stability. **Libraries** should have flexible version ranges (`>=`) to avoid conflicting with other libraries the user might have.
11. **Q: What is 'Twine' and why is it used?**
    - **Answer**: A utility used to **Securely Upload** packages to PyPI over HTTPS, ensuring the transmission is encrypted and the package hasn't been tampered with.
12. **Q: How do you handle 'Private' packages in a company?**
    - **Answer**: By using a **Private Package Registry** like Artifactory, AWS CodeArtifact, or GitHub Packages, rather than publishing to the public PyPI.
13. **Q: What is the 'src' layout and why is it recommended?**
    - **Answer**: Placing your code in a `src/` folder rather than the root directory. This forces you to use an "editable install" for testing, ensuring that your package can be correctly installed by others.
14. **Q: What is 'PEP 517' and 'PEP 518'?**
    - **Answer**: Standards that define how Python projects should be built and how build dependencies should be declared, moving the industry away from `setup.py` towards `pyproject.toml`.
15. **Q: Explain the 'MIT License' vs 'GPL'.**
    - **Answer**: **MIT**: Highly permissive (people can use your code for anything). **GPL**: "Copyleft" (anyone who modifies your code must also open-source their changes).
16. **Q: How can you install a package directly from a Git repository?**
    - **Answer**: Using the command: `pip install git+https://github.com/user/repo.git`.
17. **Q: What is 'Monkey Patching' in a distributed package?**
    - **Answer**: Dynamically replacing code at runtime. It's often used by libraries to "fix" bugs in other libraries they depend on, though it makes debugging very difficult.
18. **: What is `sys.path`?**
    - **Answer**: A list of strings that specifies the search path for modules. When you `import`, Python looks through these directories one-by-one.
19. **Q: What is a 'Self-Contained Executable' for Python (e.g., PyInstaller)?**
    - **Answer**: A tool that bundles the Python interpreter and all your code into a single `.exe` file so the user doesn't even need to have Python installed.
20. **Q: Why is 'Versioning' the most important part of a principal engineer's job?**
    - **Answer**: Because changing a library that is used by 1,000 other applications is a massive risk. Proper versioning communication (changelogs, deprecation warnings) is the only way to evolve a system safely.

---

[Previous: Internals](31-python-internals.md) | [Home: Masterclass Overview](../README.md)
