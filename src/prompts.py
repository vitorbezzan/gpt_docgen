"""
.py file containing all prompts to be used when generating documentation.
"""
description_prompt = """
You are a experienced python programmer with years of experience and you to generate
markdown documentation for this code.

The title of the document should be: %s

This documentation needs to describe what the code does and how it works.

Use headings to breakdown the documentation into the following sections:

- Summary: one sentence summary of what this code does.
- Dependencies: a list of the dependencies that this code requires. Please make two
    lists, using only the name of dependency modules:
    - Standard Library: a list of the dependencies coming from the python standard
        library. If there is none, please write "None".
    - Other: all other dependencies that are not part of the standard library. If there
        is none, please write "None".
- Description: A summary of at most four paragraphs describing what the file does and
    how it works. Please use wording that is resembles other software documentation: use
    the Python standard documentation as source of inspiration and style. You can also
    use the docstrings as source of information and inspiration, but do not use the
    docstrings directly in the text you generate.

Please include the sentence "This documentation was generated using %s" at the end of
the document, in italics.

The code is the following:
"""

debug_prompt = """
You are a experienced python programmer with years of experience.

Please generate a markdown documentation file with the following sections, divided by
headings:

- Summary: one sentence summary of what this code does.
- Algorithm: Description of the main algorithm being used on the piece of code.
- Improvement opportunities: Remarks about how this code can be improved. Take other
    open source projects as source of inspiration. Do NOT suggest code in this block.
- Potential safety issues: Please flag any potential safety issues in this code. Please
    flag any code that can generate safety problems for users during execution.

Please include the sentence "This documentation was generated using %s" at the end of
the document, in italics.

The code is the following:
"""

readme_prompt = """
You are a experienced python programmer with years of experience.

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
