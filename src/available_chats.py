"""
Defines acceptable chats and respective validations for them.
"""
import typing as tp

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from pydantic import AfterValidator
from typing_extensions import Annotated

available_chats: tp.Dict[str, tp.Type[BaseChatModel]] = {
    "OPENAI": ChatOpenAI,
    "ANTHROPIC": ChatAnthropic,
}


def _is_acceptable_chat(vendor: str) -> str:
    assert vendor in available_chats  # noqa: S101
    return vendor


AcceptedChats = Annotated[str, AfterValidator(_is_acceptable_chat)]
