# 32. Modern Packaging & Distribution — Poetry, Wheels & PyPI

> "Shipping code is as important as writing it. An expert doesn't just 'pip install'; they build stable, versioned, and reproducible packages using `Poetry` and `pyproject.toml` to ensure their software runs exactly the same on a laptop as it does on a 1,000-node cluster."

---

## 🌱 The Basics: Pip & Virtual Environments
The entry-level way to manage dependencies.

- **`venv`**: A isolated folder for your project's libraries.
- **`requirements.txt`**: A list of libraries to install.

```bash
# 1. Create and Activate
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install
pip install requests
```

---

## 🌿 Intermediate: pyproject.toml & Poetry
Modern Python development has moved away from `setup.py` and `requirements.txt`. We now use **`pyproject.toml`** as the single source of truth for all project metadata.

**Poetry** is the industry standard for managing dependencies, virtualenvs, and publishing.

```toml
# pyproject.toml example
[tool.poetry]
name = "my-awesome-app"
version = "1.0.0"
description = "A professional Python application"

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.100.0"
```

---

## 🌳 Advanced: Building Wheels (.whl)
A **Wheel** is a "Built Distribution" format. It contains the pre-compiled code and metadata, making installation much faster and more reliable than installing from source (`sdist`).

**Real Use (Platform/DevOps)**:
Building a wheel of your internal library so it can be deployed to a private Artifactory or PyPI server in milliseconds.

```bash
# Building with Poetry
poetry build
# This creates a '.whl' file in the /dist/ folder
```

---

## 🔥 Expert: PyPI & Private Registries
Principal engineers automate the publishing of their packages.

### 1. Semantic Versioning (SemVer)
- **1.2.3**: Major (Breaking), Minor (New Feature), Patch (Bug Fix).

### 2. CI/CD Publishing
Using **GitHub Actions** to automatically build and push your package to **PyPI** (the public Python Package Index) or a private company repository whenever you create a new Git Tag.

---

## 🎯 Top 20 Principal Interview Questions (Packaging)

1. **Q: What is a 'Virtual Environment' and why is it mandatory?**
   - **Answer**: It is an isolated directory that contains its own Python interpreter and set of libraries. It prevents "Dependency Hell" where two different projects require two different versions of the same library.
2. **Q: What is the purpose of `pyproject.toml`?**
   - **Answer**: The modern standard for Python project configuration. It replaces `setup.py`, `requirements.txt`, and multiple other config files (`tox.ini`, `pytest.ini`, etc.) with a single, structured file.
3. **Q: Why is 'Poetry' preferred over 'Pip' for large teams?**
   - **Answer**: Poetry handles **Dependency Resolution** better (preventing conflicts), provides a **Lock File** (ensuring everyone has the exact same versions), and manages virtualenvs automatically.
4. **Q: What is a 'Lock File' (`poetry.lock`)?**
   - **Answer**: A file that records the **Exact Version** and **Hash** of every library in your project (including sub-dependencies). It ensures that a build today is identical to a build six months from now.
5. **Q: What is a 'Wheel' (.whl) vs a 'Source Distribution' (sdist)?**
   - **Answer**: A **Wheel** is a pre-built binary; it installs almost instantly and doesn't require a compiler. A **Source Distribution** is just the raw code; it must be "Built" and "Compiled" locally, which is slower and can fail.
6. **Q: Explain 'Semantic Versioning' (SemVer).**
   - **Answer**: A versioning scheme `MAJOR.MINOR.PATCH`. Increment MAJOR for breaking changes, MINOR for new features (backwards compatible), and PATCH for bug fixes.
7. **Q: How do you handle 'Private' dependencies that shouldn't be on PyPI?**
   - **Answer**: By hosting a private repository (using **Artifactory** or **Github Packages**) and configuring your tool (like Poetry) to check that private URL first.
8. **Q: What is the purpose of the `src/` layout in a professional Python project?**
   - **Answer**: It forces you to install the package before you can test it, preventing accidental imports of local code and ensuring your tests are running against the "Built" version of your app.
9. **Q: What is an 'Entry Point' in a package?**
   - **Answer**: A command defined in `pyproject.toml` that allows the user to run your Python code simply by typing a word (e.g., `my-app`) in the terminal.
10. **Q: How do you publish a package to PyPI?**
    - **Answer**: Using `poetry publish --build` or `twine upload dist/*`. You need a PyPI API token for authentication.
11. **Q: What is 'Dependency Resolution'?**
    - **Answer**: The complex math of finding a version of every library that satisfies all requirements simultaneously (e.g., Project A needs B > 1.0, and Project C needs B < 2.0).
12. **Q: Explain 'Transitive Dependencies'.**
    - **Answer**: The libraries that your libraries depend on. You might install 1 thing (Pandas) but end up with 10 things (NumPy, Six, etc.).
13. **Q: What is 'Vendoring' a library?**
    - **Answer**: The practice of copying the source code of a library directly into your project's folders to avoid needing to manage it as an external dependency.
14. **Q: What is the purpose of `.gitignore` in a Python project?**
    - **Answer**: To tell Git **not** to track temporary or sensitive files (like `venv/`, `__pycache__/`, or `.env`).
15. **: How do you manage different dependencies for 'Development' vs 'Production'?**
    - **Answer**: Using **Dependency Groups** in Poetry (e.g., `[tool.poetry.group.dev.dependencies]`). Development tools like `pytest` aren't installed in the final production image.
16. **Q: What is 'Namespace Packaging' (PEP 420)?**
    - **Answer**: A way to spread a single Python package across multiple different directories or repositories, allowed by having no `__init__.py` in the parent folders.
17. **Q: What is 'Manylinux' in the context of Wheels?**
    - **Answer**: A standard for building Linux wheels that are compatible with **almost all** Linux distributions (Ubuntu, CentOS, etc.) by linking against a very old, stable version of the C library.
18. **Q: How do you securely handle PyPI tokens in a CI/CD pipeline?**
    - **Answer**: Using **GitHub Actions Secrets** (e.g., `PYPI_API_TOKEN`) and injecting them into the build process. Never hardcode them in the `.yaml` file.
19. **Q: What is the purpose of `pip --no-cache-dir install`?**
    - **Answer**: It prevents pip from saving a copy of the downloaded libraries in a local cache. This is essential when building **Docker Images** to keep the image size as small as possible.
20. **Q: What is 'Tox' or 'Nox'?**
    - **Answer**: Tools for automating testing in **Multiple Environments**. They automatically create clean virtualenvs for every Python version and run your tests in each.

---

[← Previous: Internals](31-internals.md) | [Back to index](../README.md)
