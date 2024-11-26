"""
Defines acceptable embeddings and respective validations for them.
"""
from functools import partial
from langchain_openai import OpenAIEmbeddings
from typing_extensions import Annotated
from pydantic import AfterValidator


available_embeddings = {
    "OPENAI_large": partial(OpenAIEmbeddings, model="text-embedding-3-large"),
}


def _is_acceptable_embedding(vendor: str) -> str:
    assert vendor in available_embeddings  # noqa: S101
    return vendor


AcceptedEmbeds = Annotated[str, AfterValidator(_is_acceptable_embedding)]
