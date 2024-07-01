"""
CLI base module for package.
"""
from typing import Optional

import typer
from dotenv import dotenv_values, load_dotenv

from constants import __package_name__, __version__

app = typer.Typer(name=f"{__package_name__}")


def _environment_callback(path: str) -> None:
    """
    Treats the environment variable path.
    """
    load_dotenv(path if path else None)
    loaded_keys = list(dotenv_values(path if path else None).keys())

    typer.echo(f"Environment variables loaded from {path}")
    typer.echo(f"Environment keys loaded: {loaded_keys}")


def _version_callback(value: bool) -> None:
    """
    Shows version information and exits.
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
        callback=_environment_callback,
        is_eager=True,
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return
