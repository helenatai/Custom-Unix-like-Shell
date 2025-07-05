# Custom Unix-Like Shell

A modular, extensible command-line shell written in **Python**, supporting a wide range of Unix-style features. Developed in a team of three as part of the **COMP0010: Software Engineering** module at University College London (UCL), this project demonstrates modern design principles, test-driven development, and custom grammar parsing.

## 🚀 Features

- **Command execution** for built-in and user-defined applications
- **I/O redirection**: input `<`, output `>`, append `>>`
- **Piping**: chaining commands with the `|` operator
- **Command substitution** using backticks (`` `command` ``)
- **Custom shell commands**: `cut`, `uniq`, `sort`, `find`, `wc`, `clear`, `exit`, and unsafe variants of all applications
- **ANTLR-based grammar parsing** with a modular parse tree visitor architecture
- **Design patterns**: Command and Visitor patterns for extensibility and separation of concerns
- **Robust error handling** with custom exception types
- **High unit test coverage** across core features and commands
- **Structured, testable architecture** following software engineering best practices

## 🧪 Development Practices

- Modular and extensible design using OOP and design patterns
- Unit testing to validate command logic and shell behavior
- Static analysis and peer-reviewed code for maintainability
- Cleanly separated grammar, parsing, and execution layers

## 📁 Repository Structure

- `src/` – Shell core and command implementations
- `antlr/` – ANTLR grammar definitions and parser setup
- `tests/` – Unit tests for commands and features
- `README.md` – Project overview and instructions

## ▶️ Running the Shell

> Requires Python 3 and ANTLR. Developed for academic purposes.

1. Install dependencies
2. Generate the parser with ANTLR
3. Run the shell:
   ```bash
   python3 main.py

