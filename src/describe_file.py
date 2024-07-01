"""
Base package using LLMs with langchain.
"""
import typing as tp
import typer

from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

_vendors = {
    "openai": ChatOpenAI,
    "cohere": ChatCohere,
    "anthropic": ChatAnthropic,
}

_description_message = """
Generate markdown documentation for this file.

The title of the document should be: %s

This documentation needs to describe what the code does and how it works.

Use headings to breakdown the documentation into the following sections:

- Summary: one sentence summary of what this code does.

- Dependencies: a list of the dependencies that this code requires. Please make two
    lists:

    - Standard Library: a list of the dependencies coming from the python standard
        library. If there is none, please write "None".
    - Other: all other dependencies that are not part of the standard library. If there
        is none, please write "None".

    All module names should be formatted as code blocks in both sections. No need to
    include the version numbers of the dependencies or the python 'as' keyword to
    describe the import.

- Description: A summary of few paragraphs describing what the file does and how it works.
    Please use wording that is resembles other software documentation. Good examples
    of this can be found in the documentation of the Python standard library. Do not use
    anything from the docstrings in this section.

Please include the sentence "This documentation was generated using %s"
at the end of the document, in italics.

The code is the following:
"""


def generate_description(
    name: str,
    vendor: tp.Optional[BaseChatModel],
    model: str,
    code_block: str,
) -> str:
    """
    Generates documentation using a given model.

    Args:
        name: Name of the file to generate documentation for.
        vendor: Vendor of the model to use when generating documentation for.
        model: Model to use for documentation generation.
        code_block: Code block to document.

    Returns:
        Generated documentation.
    """
    try:
        selected_llm, parser = (
            _vendors.get(vendor, "openai")(model=model),  # type: ignore
            StrOutputParser(),
        )
    except:
        raise typer.Exit("Unknown error instantiating language model.")

    messages = [
        SystemMessage(content=_description_message % (name, model)),
        HumanMessage(content=code_block),
    ]

    try:
        result = selected_llm.invoke(input=messages)
    except:
        raise typer.Exit("Unknown error invoking language model.")

    return parser.invoke(result)
