"""
Creates README markdown file using LLMs.
"""
import os
import pathlib

import typer
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pydantic import validate_call

from constants import AcceptedChats, available_chats, embeddings
from prompts import readme_prompt


@validate_call
def generate_embedding(current_path: pathlib.Path) -> None:
    """
    Generates embedding for a given code path. Needs to run in root directory for
        package.

    Args:
        current_path: Path to the current running directory.

    Returns:
        Generated embedding for code in generated/embeddings/.
    """
    db_path = current_path / "generated" / "embedding"
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

    Chroma.from_documents(
        documents=texts,
        embedding=embeddings(),  # To change in future
        persist_directory=f"{db_path}",
    )


@validate_call
def generate_readme(
    current_path: pathlib.Path,
    vendor: AcceptedChats,
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
    db_path = current_path / "generated" / "embedding"

    if db_path.exists():
        db = Chroma(
            persist_directory=f"{db_path}",
            embedding_function=embeddings(),  # To change in future
        )
        retriever = db.as_retriever()

        chat_object, requires_cred = available_chats.get(vendor)
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

        qa = ConversationalRetrievalChain.from_llm(
            selected_llm,
            retriever=retriever,
        )

        result = qa({"question": readme_prompt % model, "chat_history": []})

        with (current_path / "README.md").open("w") as readme:
            readme.write(result["answer"])

    else:
        raise typer.Abort("No embeddings found. Please run 'embedding' command first.")
