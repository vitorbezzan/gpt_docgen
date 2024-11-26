"""
Defines base CLI functions for the package.
"""
import glob
import os
import pathlib
import typing as tp

import typer
from dotenv import load_dotenv

from constants import __package_name__, __version__
from explain_file import explain_file
from initialize import create_vector_database

app = typer.Typer(name=f"{__package_name__}", no_args_is_help=True)
current_dir = pathlib.Path(os.getcwd()).resolve().absolute()


@app.command()
def describe_dir(
    embedding_name: str = "OPENAI_large",
    model_vendor: str = "OPENAI",
    model_name: str = "gpt-4o-2024-08-06",
):
    """
    Describes directory, and generates markdowns for each file in it using LLMs.

    Args:
        embedding_name: Name of the embedding to use when parsing files.
        model_vendor: Model vendor name to use when generating results.
        model_name:  Model name from vendor to use when generating results.
    """
    py_files = glob.glob(f"{current_dir}/**/*.py", recursive=True)

    for file_path in py_files:
        typer.echo(f"Generating description for {file_path}...")
        if "__init__" in file_path:
            continue

        if "test" in file_path:
            continue

        rel_to = pathlib.Path(file_path).relative_to(current_dir)
        md_location = (current_dir / "generated" / "markdown" / rel_to).with_suffix(
            ".md"
        )
        md_location.parent.mkdir(parents=True, exist_ok=True)

        result = explain_file(
            current_dir,
            file_path,
            embedding_name,
            model_vendor,
            model_name,
        )

        with open(f"{md_location}", "w") as result_file:
            result_file.write(result)

    typer.echo("Finished generating descriptions for files.")


@app.command()
def initialize(
    embedding_name: str = "OPENAI_large",
    parser_threshold: int = 0,
    chunk_size: int = 20,
    chunk_overlap: int = 10,
):
    """
    Initializes database for LLM future use.

    Args:
        embedding_name: name of the embedding to use.
        parser_threshold: Minimum number of lines to use when parsing a .py file.
            Default is 0.
        chunk_size: Chunk text size to use when parsing files.
        chunk_overlap: Chunk overlap to use when parsing files.
    """
    typer.echo("Initializing database for project...")

    create_vector_database(
        current_dir,
        embedding_name,
        parser_threshold,
        chunk_size,
        chunk_overlap,
    )

    typer.echo("Database initialized successfully.")


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
    environment: tp.Optional[str] = typer.Option(
        ".env",
        "--environment",
        "-e",
        help="Specific path to environment file.",
        callback=_environment,
        is_eager=True,
    ),
    version: tp.Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version,
        is_eager=True,
    ),
) -> None:
    return
