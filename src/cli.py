"""
CLI base module for package.
"""
import glob
import os
import pathlib
from typing import Optional

import typer
from dotenv import load_dotenv

from constants import __package_name__, __version__
from describe_file import debug, describe
from embedding import generate_embedding, generate_readme

app = typer.Typer(name=f"{__package_name__}", no_args_is_help=True)
current_dir = pathlib.Path(os.getcwd()).resolve().absolute()


@app.command()
def describe_file(
    path: str,
    vendor: str = "ANTHROPIC",
    model: str = "claude-3-5-sonnet-20240620",
) -> None:
    """
    Runs language model in file to generate a markdown description for it.
        Generates description in the same working directory.

    Args:
        path: Path for file to generate explanation.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    file_path = pathlib.Path(path).absolute().resolve()
    describe(
        file_path,
        file_path.with_suffix(".md"),
        vendor,
        model,
    )


@app.command()
def describe_dir(
    path: str,
    vendor: str = "ANTHROPIC",
    model: str = "claude-3-5-sonnet-20240620",
):
    """
    Runs language model in directory to generate a description for each file. Saves
        generated markdown description using same directory structure.

    Args:
        path: Path to dir to generate explanations for. Path can relative or absolute
            as long it exists.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.

    Returns:
         Markdown files for each .py file in path. Saves in ./generated/markdown
            directory.
    """
    dir_path = pathlib.Path(path).absolute().resolve()

    if dir_path.is_dir():
        md_dir = current_dir / "generated" / "markdown"
        md_dir.mkdir(parents=True, exist_ok=True)

        py_files = glob.glob(f"{dir_path}/**/*.py", recursive=True)
        for file_path in py_files:
            if "__init__" in file_path:
                continue

            rel_to = pathlib.Path(file_path).relative_to(current_dir)

            md_location = (current_dir / "generated" / "markdown" / rel_to).with_suffix(
                ".md"
            )
            md_location.parent.mkdir(parents=True, exist_ok=True)

            describe(
                pathlib.Path(file_path),
                md_location,
                vendor,
                model,
            )


@app.command()
def debug_file(
    path: str,
    vendor: str = "ANTHROPIC",
    model: str = "claude-3-5-sonnet-20240620",
) -> None:
    """
    Runs language model in file to generate a markdown debug information for it.
    Generates description in the same working directory.

    Args:
        path: Path for file to generate explanation.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    file_path = pathlib.Path(path).absolute().resolve()
    debug(
        file_path,
        file_path.with_suffix(".md"),
        vendor,
        model,
    )


@app.command()
def embedding():
    """
    Creates README markdown file using LLMs. Scans for a directory, generates a simple
        explanation for each component and consolidates it into a file.

    Currently, embedding function only works with "--vendor openai".
    """
    generate_embedding(current_dir)


@app.command()
def readme(vendor: str = "ANTHROPIC", model: str = "claude-3-5-sonnet-20240620"):
    """
    Generates README.md file in root using LLMs. User needs to run "embedding" command
        first in order to generate the summary of the content for the files.

    Args:
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    generate_readme(current_dir, vendor, model)


def _environment(path: str) -> None:
    """
    Treats the environment variable path.

    Args:
        path: Path to the environment file.
    """
    environment_path = pathlib.Path(path).resolve().absolute()
    typer.echo(f"Current working dir is {current_dir}")

    if environment_path.is_file():
        load_dotenv(path)
    else:
        raise typer.BadParameter(f"environment file not found: {path}")


def _version(value: bool) -> None:
    """
    Shows version information and exits.

    Args:
        value: Boolean value to show version information.
    """
    if value:
        typer.echo(f"{__package_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    environment: Optional[str] = typer.Option(
        ".env",
        "--environment",
        "-e",
        help="Specific path to environment file.",
        callback=_environment,
        is_eager=True,
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version,
        is_eager=True,
    ),
) -> None:
    return
