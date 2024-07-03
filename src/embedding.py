"""
Creates README markdown file using LLMs.
"""
import pathlib
import typing as tp

import typer
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pydantic import AfterValidator, validate_call
from typing_extensions import Annotated

from constants import _available_chats, _available_embeddings


def _is_acceptable_vendor(vendor: str) -> str:
    assert vendor in _available_embeddings  # noqa: S101
    return vendor


AcceptedVendor = Annotated[str, AfterValidator(_is_acceptable_vendor)]


@validate_call
def generate_embedding(
    current_path: pathlib.Path,
    vendor: AcceptedVendor,
    model: tp.Optional[str] = None,
) -> None:
    """
    Generates embedding for a given code path. Needs to run in root directory for
    package.

    Args:
        current_path: Path to the current running directory.
        vendor: Vendor of the model to use when generating README for.
        model: Model to use in embedding.

    Returns:
        Generated embedding for code in docs/embeddings/.
    """
    db_path = current_path / "docs" / "embedding"
    db_path.mkdir(parents=True, exist_ok=True)

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

    if model is None:
        embeddings = _available_embeddings.get(vendor, "openai")()
    else:
        embeddings = _available_embeddings.get(vendor, "openai")(model=model)

    Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=f"{db_path}",
    )


_question = """
You are a developer with several years of experience.

You need to generate a README markdown file for a codebase, taking inspiration in all
READMEs you have seen in the past from different open source projects. It needs to
have some sections:

- Introduction: where you introduce what the codebase does, and summarizes the main
    features.
- Installation: where you explain how to install the codebase.
- Example: where you explain how to use the codebase briefly.

Please include the sentence "This documentation was generated using %s" at the end of
the document, in italics.
"""


@validate_call
def generate_readme(
    current_path: pathlib.Path,
    vendor: AcceptedVendor,
    model: str,
) -> None:
    """
    Generates README for a given code path.

    Args:
        current_path: Path to the current running directory.
        vendor: Vendor of the model to use when generating README for.
        model: Model to use for the given vendor.

    Returns:
        Generated README for code in README.md.
    """
    db_path = current_path / "docs" / "embedding"

    if db_path.exists():
        if model is None:
            embeddings = _available_embeddings.get(vendor, "openai")()
        else:
            embeddings = _available_embeddings.get(vendor, "openai")(model=model)

        db = Chroma(
            persist_directory=f"{db_path}",
            embedding_function=embeddings,
        )
        retriever = db.as_retriever()
        qa = ConversationalRetrievalChain.from_llm(
            _available_chats.get(vendor, "openai")(model=model),
            retriever=retriever,
        )

        result = qa({"question": _question % model, "chat_history": []})

        with (current_path / "README.md").open("w") as readme:
            readme.write(result["answer"])

    else:
        raise typer.Abort("No embeddings found. Please run 'embedding' command first.")
