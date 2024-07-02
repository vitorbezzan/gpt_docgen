# `gpt_docgen`

## Introduction

Welcome to the `gpt_docgen` repository, a cutting-edge documentation generation tool designed to streamline the process of creating detailed, accurate, and insightful documentation for your codebase using the power of language models.

The primary features of `gpt_docgen` include:

- **Automatic Markdown Generation**: Automatically generates markdown files that describe the functionalities and usage of your code files, making your documentation process as effortless as possible.
- **Custom Model Support**: With support for multiple language models, you can choose the model that best fits your needs and preferences for documentation style and detail level.
- **CLI Integration**: Easy-to-use command-line interface that simplifies the process of generating documentation for any project, regardless of size or complexity.

## Installation

To install `gpt_docgen`, you will need Python 3.11 or newer. Follow these steps to get started:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/vitorbezzan/gpt_docgen.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd gpt-docgen
   ```
3. Install the package in a virtual environment (Python 3.11) using pip:
   ```bash
   pip install .
   ```

You can also install the package directly from PyPI using pip:

```bash
pip install bezzanlabs.gpt_docgen
```

This package is made to be run inside its own virtual environment, so it is recommended to create one before running the package.

## Example

To generate documentation for your codebase, navigate to your project directory and run:

```bash
gpt_docgen describe_file --path /path/to/your/file.py
```

You can specify the model and vendor you wish to use with additional flags. For a detailed explanation of all available commands and options, use:

```bash
gpt_docgen --help
```

This will provide you with a help disclaimer.



*This documentation was generated using gpt-4-turbo-preview.*
