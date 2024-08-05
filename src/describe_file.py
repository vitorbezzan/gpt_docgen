"""
Base package using LLMs with langchain.
"""
import os
import pathlib

import typer
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from pydantic import validate_call

from constants import AcceptedChats, available_chats
from prompts import debug_prompt, description_prompt


@validate_call
def describe(
    in_file: pathlib.Path,
    out_file: pathlib.Path,
    vendor: AcceptedChats,
    model: str,
) -> None:
    """
    Calls a description for one specific file.

    Args:
        in_file: File path to describe.
        out_file: File path to save the description.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    in_file_ = in_file.resolve().absolute()

    if in_file_.is_file():
        typer.echo(f"Generating description for {in_file_}")
        with in_file.open("r") as python_file:
            file_content = python_file.read()
    else:
        raise typer.BadParameter(f"File not found: {in_file_}")

    with out_file.resolve().absolute().open("w") as md_file:
        md_file.write(
            call_description(
                vendor,
                model,
                description_prompt % (in_file.name, model),
                file_content,
            )
        )


@validate_call
def debug(
    in_file: pathlib.Path,
    out_file: pathlib.Path,
    vendor: AcceptedChats,
    model: str,
) -> None:
    """
    Calls a debug description for one specific file.

    Args:
        in_file: File path to describe.
        out_file: File path to save the description.
        vendor: Vendor to use for model.
        model: Model to use from the selected vendor.
    """
    in_file_ = in_file.resolve().absolute()

    if in_file_.is_file():
        typer.echo(f"Generating description for {in_file_}")
        with in_file.open("r") as python_file:
            file_content = python_file.read()
    else:
        raise typer.BadParameter(f"File not found: {in_file_}")

    with out_file.resolve().absolute().open("w") as md_file:
        md_file.write(
            call_description(
                vendor,
                model,
                debug_prompt % model,
                file_content,
            )
        )


def call_description(
    vendor: str,
    model: str,
    prompt_str: str,
    code_block: str,
) -> str:
    """
    Generates documentation using a given model.

    Args:
        vendor: Vendor of the model to use when generating documentation for.
        model: Model to use for documentation generation.
        prompt_str: str containing prompt to use for request.
        code_block: Code block to document.

    Returns:
        Generated documentation.
    """
    chat_object, requires_cred = available_chats.get(vendor)
    parser = StrOutputParser()

    if requires_cred:
        selected_llm = chat_object(
            model=model,
            temperature=0.0,
            base_url=os.environ.get(f"{vendor}_BASE_URL", None),
        )
    else:
        selected_llm = chat_object(
            model=model,
            temperature=0.0,
        )

    messages = [SystemMessage(content=prompt_str), HumanMessage(content=code_block)]

    try:
        result = selected_llm.invoke(input=messages)
    except Exception as invoke_error:  # noqa: E722
        typer.echo(f"Error in invoke. {invoke_error}")
        raise typer.Exit(code=-1)

    return parser.invoke(result)
