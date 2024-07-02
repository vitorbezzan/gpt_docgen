"""
CLI base module for package.
"""
import glob
import os
import pathlib
from typing import Optional

import typer
from dotenv import dotenv_values, load_dotenv

from constants import __package_name__, __version__
from describe_file import describe
from embedding import generate_embedding, generate_readme

app = typer.Typer(name=f"{__package_name__}", no_args_is_help=True)
current_dir = pathlib.Path(os.getcwd()).resolve().absolute()


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
        keys_loaded = list(dotenv_values(path).keys())

        typer.echo(f"Environment keys loaded: {keys_loaded}")
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


@app.command()
def describe_file(
    path: str,
    vendor: str = "openai",
    model: str = "gpt-4-turbo-preview",
) -> None:
    """
    Runs language model in file to generate a markdown description for it.
    Generates explanation in the same working directory.

    Args:
        path: Path for file to generate explanation.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    file_path = pathlib.Path(path)
    describe(
        file_path,
        file_path.with_suffix(".md"),
        vendor,
        model,
    )


@app.command()
def describe_dir(
    path: str,
    vendor: str = "openai",
    model: str = "gpt-4-turbo-preview",
):
    """
    Runs language model in directory to generate a description for each file.

    Args:
        path: Path to dir to generate explanations for.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.

    Returns:
         Markdown files for each .py file in path.
    """
    dir_path = pathlib.Path(path).absolute().resolve()

    if dir_path.is_dir():
        typer.echo(f"Generating descriptions for dir {dir_path}")
        md_dir = current_dir / "docs" / "markdown"
        md_dir.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Markdown files will be saved in {md_dir}")

        py_files = glob.glob(f"{dir_path}/**/*.py", recursive=True)
        for file_path in py_files:
            if "__init__" in file_path:
                continue

            rel_to = pathlib.Path(file_path).relative_to(current_dir)

            md_location = (current_dir / "docs" / "markdown" / rel_to).with_suffix(
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
def embedding(vendor: str = "openai"):
    """
    Creates README markdown file using LLMs. Scans for a directory, generates a simple
    explanation for each component and consolidates it into a file.

    Args:
        vendor: Vendor to use for model.
    """
    (current_dir / "docs" / "embedding").mkdir(parents=True, exist_ok=True)
    generate_embedding(current_dir, vendor)


@app.command()
def readme(vendor: str = "openai", model: str = "gpt-4-turbo-preview"):
    """
    Generates README.md file in root using LLMs.

    Args:
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    generate_readme(current_dir, vendor, model)


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
