"""
Creates README markdown file using LLMs.
"""
import typer
import pathlib

from langchain_chroma import Chroma
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pydantic import AfterValidator, validate_call
from typing_extensions import Annotated
from langchain.chains import ConversationalRetrievalChain


from constants import _available_embeddings, _available_chats


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

    Returns:
        Generated README for code in README.md.
    """
    db_path = current_path / "docs" / "embedding"
    if db_path.exists():
        db = Chroma(
            persist_directory=f"{db_path}",
            embedding_function=_available_embeddings.get(vendor, "openai")(disallowed_special=()),
        )
        retriever = db.as_retriever()
        qa = ConversationalRetrievalChain.from_llm(
            _available_chats.get(vendor, "openai")(model=model),
            retriever=retriever,
        )

        history = []
        result = qa({"question": _question % model, "chat_history": history})

        with (current_path/"README.md").open("w") as readme:
            readme.write(result["answer"])

    else:
        raise typer.Abort("No embeddings found. Please run generate_embedding first.")