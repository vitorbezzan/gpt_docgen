# cli.py

## Summary

This code implements a command-line interface (CLI) for a package that generates markdown documentation and README files using language models.

## Dependencies

### Standard Library
- glob
- os
- pathlib
- typing

### Other
- typer
- dotenv
- constants
- describe_file
- embedding

## Description

The `cli.py` module serves as the main entry point for a command-line application that leverages language models to generate documentation for Python files and projects. It utilizes the Typer library to create a user-friendly CLI with multiple commands.

The module defines several commands, each with a specific purpose:

1. `describe_file`: Generates a markdown description for a single Python file using a specified language model.
2. `describe_dir`: Recursively processes a directory, generating markdown descriptions for all Python files within it.
3. `debug_file`: Generates debug information for a single Python file in markdown format.
4. `embedding`: Creates a summary of the project's components using language models.
5. `readme`: Generates a README.md file for the project using the previously created embedding.

The application supports different language model vendors and models, with default values set to ANTHROPIC and claude-3-5-sonnet-20240620. It also includes functionality to load environment variables from a .env file and display version information.

The code is designed to be flexible and extensible, allowing users to easily generate documentation for their Python projects with minimal effort.

*This documentation was generated using claude-3-5-sonnet-20240620*
