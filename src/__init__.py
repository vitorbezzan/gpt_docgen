"""
Starting point for the package.
"""
from cli import app


def start_application():
    app(prog_name="bezzanlabs.gpt_docgen")


if __name__ == "__main__":
    start_application()