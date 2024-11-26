"""
Starting point for the package CLI.
"""
from cli import app


def start_application():
    """
    Starts the application.
    """
    app(prog_name="bezzanlabs.gpt_docgen")


if __name__ == "__main__":
    start_application()
