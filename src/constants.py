"""
All constants for the package.
"""
import typing as tp
from functools import partial

from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import AfterValidator
from typing_extensions import Annotated

__package_name__ = "bezzanlabs.gpt_docgen"
__version__ = "0.3.0"
__author__ = "Vitor Bezzan <vitor@bezzan.com>"

# All objects being used by chats, embeddings and agents
# vendor: (object, requires_credentials_in_env)
available_chats: tp.Dict[str, tp.Tuple[tp.Type[BaseChatModel], bool]] = {
    "OLLAMA": (ChatOllama, False),
    "OPENAI": (ChatOpenAI, True),
    "ANTHROPIC": (ChatAnthropic, True),
}

embeddings = partial(OpenAIEmbeddings, model="text-embedding-3-large")


def _is_acceptable_chats(vendor: str) -> str:
    assert vendor in available_chats  # noqa: S101
    return vendor


AcceptedChats = Annotated[str, AfterValidator(_is_acceptable_chats)]
