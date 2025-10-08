# General + Python Ruleset

## Meta Rule
- Ensure full compliance with recent industry best practices.
- Audit, refactor, and fix existing errors or issues before adding new code.
- Be concise and precise; avoid speculative or context-less code (no hallucinations).
- Prioritize readability, simplicity, and maintainability.
- Always implement code as **modular, reusable components**.
- Rules apply exclusively to **Python projects**.
- Use **Python 3.9+** features and libraries.
- Avoid deprecated libraries and practices.
- Ensure compatibility with the latest stable Python version.
- Follow **DRY (Don't Repeat Yourself)** principles.
- Use **virtual environments** for dependency management.
- Document all functions, classes, and modules with **docstrings**.
- Use **type hints** for function signatures.
- Ensure all code is **well-commented** where necessary.
- Follow **semantic versioning** for project releases.
- Use **Git** for version control and follow a consistent branching strategy.

## Code Quality
- Adhere to **PEP 8** style guide for Python code.
- Write unit tests for all new features and bug fixes.
- Use type hints to improve code clarity and enable static type checking.
- Regularly run linters and formatters to maintain code quality.
- Use **pytest** or **unittest** for testing.
- Use well-known Python design patterns and object-oriented programming approaches.
- Avoid using global variables; prefer passing parameters and returning values.
- Handle exceptions gracefully using try-except blocks.
- Use logging instead of print statements for debugging and information.
- Ensure code is compatible with both Windows and Unix-based systems.
- Use list comprehensions and generator expressions for concise and efficient code.
- Avoid using wildcard imports (e.g., `from module import *`).
- Use f-strings for string formatting (Python 3.9+).
- Avoid using mutable default arguments in function definitions.
- Use context managers (with statements) for resource management (e.g., file handling).
- Ensure proper use of Python's built-in data structures (lists, sets, dictionaries, tuples).
- Avoid deep nesting of code; refactor into smaller functions or methods.
- Use Python's standard library whenever possible before considering third-party libraries.
- Regularly update dependencies to their latest stable versions.
- Use virtual environments (e.g., venv, virtualenv, pipenv) to manage project dependencies.
- Ensure all third-party libraries are well-maintained and widely used in the Python community.