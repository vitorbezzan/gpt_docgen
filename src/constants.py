"""
All constants for the package.
"""
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI

__package_name__ = "bezzanlabs.gpt_docgen"
__version__ = "0.1.0"
__author__ = "Vitor Bezzan <vitor@bezzan.com>"

_available_chats = {
    "openai": ChatOpenAI,
    "cohere": ChatCohere,
    "anthropic": ChatAnthropic,
}
