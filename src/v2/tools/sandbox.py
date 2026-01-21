""" tools/sandbox.py
This module contains tools for sandboxed web crawling tasks.
"""

from ...v1.core.config import Config
from ..agent.registry import Toolbox

config = Config()

remote_kernel_tools = Toolbox('sandbox_tools')

@remote_kernel_tools
def sandbox_crawler(
    python_script: str,
    input_url: str = config.agent_sandbox
) -> str:
    """
    Crawl the provided URL using a sandboxed environment to extract relevant information.

    Args:
        input_url (str): The URL to be crawled.

    Returns:
        str: A summary of the information extracted from the URL.
    """
    # TODO: ENSURE DATASET IS ACCESSIBLE FROM SANDBOX
    # Placeholder implementation
    return python_script

@remote_kernel_tools
def subtract_two_numbers(a: int, b: int) -> int:
    """Subtract two numbers.

    Args:
        a (int): The first number to subtract from.
        b (int): The second number to subtract.

    Returns:
        int: The difference a - b.
    """
    return a - b
