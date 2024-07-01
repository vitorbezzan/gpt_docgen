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
from describe_file import generate_description

app = typer.Typer(name=f"{__package_name__}", no_args_is_help=True)
current_dir = pathlib.Path(os.getcwd())


def _environment(path: str) -> None:
    """
    Treats the environment variable path.

    Args:
        path: Path to the environment file.
    """
    environment_path = pathlib.Path(path).resolve()
    typer.echo(f"Current working dir is {current_dir.absolute()}")

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
    file_path = pathlib.Path(path).resolve()

    if file_path.is_file():
        typer.echo(f"Generating description for {file_path.absolute()}")
        with file_path.open(mode="r") as python_file:
            file_content = python_file.read()
    else:
        raise typer.BadParameter(f"File not found: {file_path}")

    md_file_location = file_path.with_suffix(".md").resolve().absolute()
    with md_file_location.open(mode="w") as md_file:
        md_file.write(
            generate_description(
                file_path.name,
                vendor,
                model,
                file_content,
            )
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
    dir_path = pathlib.Path(path)

    if dir_path.is_dir():
        typer.echo(f"Generating descriptions for dir {dir_path.absolute()}")
        pathlib.Path(current_dir/"descriptions").mkdir(parents=True, exist_ok=True)

        for file_path in glob.glob(f"{dir_path}/*.py", recursive=True):
            if "__init__" in file_path:
                continue

            typer.echo(f"Generating description for {file_path}")
            with open(file_path, "r") as python_file:
                file_content = python_file.read()

            md_file_location = (
                pathlib.Path(
                    current_dir/"descriptions"/file_path
                ).with_suffix(".md").resolve().absolute()
            )
            md_file_location.parent.mkdir(parents=True, exist_ok=True)
            with open(md_file_location, "w") as markdown_file:
                markdown_file.write(
                    generate_description(
                        pathlib.Path(file_path).name,
                        vendor,
                        model,
                        file_content,
                    )
                )


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
