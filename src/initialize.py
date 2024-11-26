"""
Initializes our vector database for our LLMs to consume.
"""
import pathlib

from langchain_chroma import Chroma
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pydantic import validate_call

from available_embeddings import AcceptedEmbeds, available_embeddings


@validate_call
def create_vector_database(
    current_path: pathlib.Path,
    embedding_name: AcceptedEmbeds,
    parser_threshold: int,
    chunk_size: int,
    chunk_overlap: int,
) -> None:
    """
    Generates embedding for a given code path. Needs to run in root directory for
        package.

    Args:
        current_path: Path to the current running directory.
        embedding_name: Accepted embedding name for an embedding.
        parser_threshold: Minimum lines to parse a python file.
        chunk_size: Chunk text size to use when parsing files.
        chunk_overlap: Chunk overlap to use when parsing files.

    Returns:
        Generated embedding for code in generated/embeddings/.
    """
    db_path = current_path / ".gpt_docgen" / "embedding"
    db_path.mkdir(parents=True, exist_ok=True)

    documents = GenericLoader.from_filesystem(
        f"{current_path}",
        glob="**/*",
        suffixes=[".py"],
        exclude=["**/non-utf8-encoding.py"],
        parser=LanguageParser(
            language=Language.PYTHON,  # type: ignore
            parser_threshold=parser_threshold,
        ),
    ).load()

    texts = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    ).split_documents(documents)

    Chroma.from_documents(
        documents=texts,
        embedding=available_embeddings[embedding_name](),
        persist_directory=f"{db_path}",
    )
