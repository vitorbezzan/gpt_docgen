"""
All constants for the package.
"""
import typing as tp

from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

__package_name__ = "bezzanlabs.gpt_docgen"
__version__ = "0.1.0"
__author__ = "Vitor Bezzan <vitor@bezzan.com>"

_available_chats: tp.Dict[str, tp.Type[BaseChatModel]] = {
    "ollama": ChatOllama,
    "openai": ChatOpenAI,
}

_available_embeddings: tp.Dict[str, tp.Type[Embeddings]] = {
    "ollama": OllamaEmbeddings,
    "openai": OpenAIEmbeddings,
}
