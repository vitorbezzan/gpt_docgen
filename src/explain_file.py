"""
Explains file using LLMs and generated vector database.
"""
import os
import pathlib

import typer
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from pydantic import validate_call

from available_chats import AcceptedChats, available_chats
from available_embeddings import AcceptedEmbeds, available_embeddings


explain_prompt = """
You are an experienced python programmer with years of experience.
Your task is to generate markdown documentation for this code.

In order to fulfill this task please consider the following instructions:
- This documentation needs to describe what the code does and how it works.
- Please do not make any sentence about the quality of the code.
- Avoid using too overly optimistic tone.
- Avoid using special characters.
- Do not use inline code; You can make reference to code as long they are in their own
code blocks.

The answer needs to be structured as below, in markdown headings:

- Summary: a summary explaining what the code in the file does. Do not go over two
    paragraphs, be as technical as possible here so users can understand the content
    deeply. Use your context to enrich this description.

- Description:
    Explain each function and what it does, using function names as sub-headers.
    Please use wording that is resembles other software documentation: use
    the Python standard documentation as source of inspiration and style. You can also
    use the docstrings as source of information and inspiration, but do not use the
    docstrings directly in the text you generate. Avoid being too terse, or using too
    much jargon. Please also do not include any code snippets.

Please include the sentence "This documentation was generated using %s and following
strict privacy guidelines" at the end of the document, in italics.

The code is the following:

%s
"""


@validate_call
def explain_file(
    current_path: pathlib.Path,
    file_path: str,
    embedding_name: AcceptedEmbeds,
    model_vendor: AcceptedChats,
    model_name: str,
) -> str:
    """
    Explains a file, using the respective embedding and vector database generated in
    "initialize" function.

    Args:
        current_path: Path to the current running directory.
        file_path: Path to file to explain.
        embedding_name: Accepted embedding name for an embedding.
        model_vendor: Vendor of the model to use when generating README for.
        model_name: Model to use for the given vendor.

    Returns:
        Generated markdown file containing file description.
    """
    vector_db = current_path / ".gpt_docgen" / "embedding"

    if vector_db.exists():
        db = Chroma(
            persist_directory=f"{vector_db}",
            embedding_function=available_embeddings[embedding_name](),
        )

        chat_object = available_chats.get(model_vendor)
        selected_llm = chat_object(
            model=model_name,
            temperature=0.0,
            base_url=os.environ.get(f"{model_vendor}_BASE_URL", None),
        )

        qa = ConversationalRetrievalChain.from_llm(
            selected_llm,
            retriever=db.as_retriever(),
        )

        with open(f"{file_path}", "r") as code_file:
            code_text = code_file.read()

        result = qa(
            {"question": explain_prompt % (model_name, code_text), "chat_history": []}
        )
        return result["answer"]

    else:
        raise typer.Abort(
            "Vector database not found for project. Please run "
            "'initialize' command first."
        )
