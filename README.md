# Unix-Like Shell

A custom-built command-line shell written in **Python**, emulating key Unix shell features such as I/O redirection, piping, and command substitution. This project was developed as part of the **Software Engineering** module at University College London (UCL).

## Features

- **Command execution** for built-in and external commands
- **I/O redirection** (input `<`, output `>`, append `>>`)
- **Piping** between commands (`|`)
- **Command substitution** using backticks (`` `command` ``)
- **Custom shell commands** including `cut`, `uniq`, `echo`, `wc`, `clear`, and `exit`
- **ANTLR-based grammar parsing** for structured command interpretation
- **Robust error handling** and unit testing for correctness

## Technologies Used

- **Python** for all implementation
- **ANTLR** for grammar definition and parse tree generation
- **Design patterns**: Command and Visitor patterns for modular and extensible architecture
- **Unit testing** to ensure reliability and maintainability

## Context

This project was completed in a team of three as part of the **COMP0010: Software Engineering** module at UCL. It demonstrates systems-level problem solving, parser design, and modular architecture in Python.

## How to Run

> ⚠️ Note: This project was developed in an academic setting and may require setup of **ANTLR** and specific Python dependencies. For demonstration purposes only.

## License

This project is for educational use only and is not intended for production environments.
