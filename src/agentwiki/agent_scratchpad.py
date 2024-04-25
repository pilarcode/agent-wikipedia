def _format_docs(docs):
    """
    Formats a list of documents into a string representation.

    Parameters:
        docs (list): A list of documents to be formatted.

    Returns:
        str: The formatted string representation of the documents.
    """
    result = "\n".join(
        [
            f'<item index="{i+1}">\n<page_content>\n{r}\n</page_content>\n</item>'
            for i, r in enumerate(docs)
        ]
    )
    return result


def format_agent_scratchpad(intermediate_steps):
    """
    A function that formats the agent scratchpad based on the intermediate steps provided.

    Parameters:
        intermediate_steps (list): A list of tuples containing action and observation pairs.

    Returns:
        str: The formatted agent scratchpad text.
    """
    thoughts = ""
    for action, observation in intermediate_steps:
        thoughts += action.log
        thoughts += "</search_query>" + _format_docs(observation)
    return thoughts