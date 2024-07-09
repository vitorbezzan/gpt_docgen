"""
Base package using LLMs with langchain.
"""
import pathlib

import typer
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from pydantic import AfterValidator, validate_call
from typing_extensions import Annotated

from constants import _available_chats

_description_message = """
You are a experienced python programmer.

Generate markdown documentation for this code.

The title of the document should be: %s

This documentation needs to describe what the code does and how it works.

Use headings to breakdown the documentation into the following sections:

- Summary: one sentence summary of what this code does.

- Dependencies: a list of the dependencies that this code requires. Please make two
    lists, using only the name of dependency modules:

    - Standard Library: a list of the dependencies coming from the python standard
        library. If there is none, please write "None".
    - Other: all other dependencies that are not part of the standard library. If there
        is none, please write "None".

- Description: A summary of at most four paragraphs describing what the file does and 
    how it works. Please use wording that is resembles other software documentation: use
    the Python standard documentation as source of inspiration ans style. You can also 
    use the docstrings as source of information, but do not use the docstrings directly
    in the text you generate.

Please include the sentence "This documentation was generated using %s" at the end of
the document, in italics.

The code is the following:
"""

_debug_message = """
You are a experienced python programmer.

Please generate a markdown documentation file with the following sections, divided by 
headings:

- Summary: one sentence summary of what this code does.
- Algorithm: Description of the main algorithm being used on the piece of code.
- Improvement opportunities: Remarks about how this code can be improved. Take other
    open source projects as source of inspiration. Do NOT suggest code in this block.
- Potential safety issues: Please flag any potential safety issues in this code. Please
    flag any code that can generate safety problems for users during execution.
    
Please include the sentence "This documentation was generated using %s" at the end of
the document, in italics.

The code is the following:
"""


def _is_acceptable_vendor(vendor: str) -> str:
    assert vendor in _available_chats  # noqa: S101
    return vendor


AcceptedVendor = Annotated[str, AfterValidator(_is_acceptable_vendor)]


@validate_call
def describe(
    in_file: pathlib.Path,
    out_file: pathlib.Path,
    vendor: AcceptedVendor,
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
                _description_message % (in_file.name, model),
                file_content,
            )
        )


@validate_call
def debug(
    in_file: pathlib.Path,
    vendor: AcceptedVendor,
    model: str,
) -> str:
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

    return call_description(
        vendor,
        model,
        _debug_message % model,
        file_content,
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
    try:
        selected_llm, parser = (
            _available_chats.get(vendor, "openai")(model=model),  # type: ignore
            StrOutputParser(),
        )
    except:  # noqa: E722
        raise typer.Exit(code=-1)

    messages = [
        SystemMessage(content=prompt_str),
        HumanMessage(content=code_block),
    ]

    try:
        result = selected_llm.invoke(input=messages)
    except:  # noqa: E722
        raise typer.Exit(code=-1)

    return parser.invoke(result)
