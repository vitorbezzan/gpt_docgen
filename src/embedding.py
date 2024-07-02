"""
Creates README markdown file using LLMs.
"""
import pathlib

from langchain_chroma import Chroma
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pydantic import AfterValidator, validate_call
from typing_extensions import Annotated

from constants import _available_embeddings


def _is_acceptable_vendor(vendor: str) -> str:
    assert vendor in _available_embeddings  # noqa: S101
    return vendor


AcceptedVendor = Annotated[str, AfterValidator(_is_acceptable_vendor)]


@validate_call
def generate_embedding(
    current_path: pathlib.Path,
    vendor: AcceptedVendor,
) -> None:
    """
    Generates embedding for a given code path.

    Args:
        current_path: Path to the current running directory.
        vendor: Vendor of the model to use when generating README for.

    Returns:
        Generated embedding for code in docs/embeddings/.
    """
    documents = GenericLoader.from_filesystem(
        f"{current_path}",
        glob="**/*",
        suffixes=[".py"],
        exclude=["**/non-utf8-encoding.py"],
        parser=LanguageParser(
            language=Language.PYTHON,  # type: ignore
            parser_threshold=500,
        ),
    ).load()

    texts = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=2000,
        chunk_overlap=200,
    ).split_documents(documents)

    Chroma.from_documents(
        documents=texts,
        embedding=_available_embeddings.get(vendor, "openai")(disallowed_special=()),
        persist_directory=f"{current_path/'docs'/'embedding'}",
    )
