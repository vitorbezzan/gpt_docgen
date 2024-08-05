# constants.py

## Summary
This code defines constants and configurations for a Python package that interfaces with various chat and embedding models.

## Dependencies

### Standard Library
- typing
- functools

### Other
- langchain_anthropic
- langchain_community
- langchain_core
- langchain_openai
- pydantic
- typing_extensions

## Description

This file contains essential constants and configurations for a Python package named "bezzanlabs.gpt_docgen". It defines the package name, version, and author information.

The main focus of this code is to set up a dictionary of available chat models from different vendors (Ollama, OpenAI, and Anthropic) along with their corresponding LangChain classes and whether they require credentials in the environment. This allows for easy selection and initialization of different chat models within the package.

Additionally, the code sets up a partial function for OpenAI embeddings, specifically using the "text-embedding-3-large" model. This provides a convenient way to create embedding objects with pre-configured settings.

The file also includes a custom type validation mechanism using Pydantic's AfterValidator to ensure that only acceptable chat vendors are used throughout the package. This adds an extra layer of type safety when working with the chat models.

*This documentation was generated using claude-3-5-sonnet-20240620*
