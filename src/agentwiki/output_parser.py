import re

from langchain_core.agents import AgentAction, AgentFinish
from agentwiki.agent_scratchpad import _format_docs


def extract_between_tags(tag: str, string: str, strip: bool = True) -> str:
    """
    Extracts the content between the specified tags in a given string.

    Args:
        tag (str): The name of the tag to extract content between.
        string (str): The string to search for the specified tags.
        strip (bool, optional): Whether to strip leading and trailing whitespace from the extracted content. Defaults to True.

    Returns:
        str: The content between the specified tags.

    Raises:
        ValueError: If there is more than one occurrence of the specified tag in the string.
    """
    ext_list = re.findall(f"<{tag}\s?>(.+?)</{tag}\s?>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    if ext_list:
        if len(ext_list) != 1:
            raise ValueError
        # Only return the first one
        return ext_list[0]


def parse_output(outputs):
    """
    Parses the output of a language model to extract the search query and the intermediate steps.
    
    Args:
        outputs (dict): A dictionary containing the partial completion and the intermediate steps.
        
    Returns:
        AgentFinish or AgentAction: If the search query is not found in the partial completion,
        an AgentFinish object is returned with the extracted documents and the formatted output.
        If the search query is found, an AgentAction object is returned with the search query as the tool input.
    """
    partial_completion = outputs["partial_completion"]
    steps = outputs["intermediate_steps"]
    search_query = extract_between_tags(
        "search_query", partial_completion + "</search_query>"
    )
    if search_query is None:
        docs = []
        str_output = ""
        for action, observation in steps:
            docs.extend(observation)
            str_output += action.log
            str_output += "</search_query>" + _format_docs(observation)
        str_output += partial_completion
        return AgentFinish({"docs": docs, "output": str_output}, log=partial_completion)
    else:
        return AgentAction(
            tool="search", tool_input=search_query, log=partial_completion
        )