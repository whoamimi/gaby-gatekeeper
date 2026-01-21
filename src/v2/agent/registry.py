""" app/src/agent/registry.py
"""

import inspect
import docstring_parser
from functools import wraps
from typing import get_type_hints, Any

class Toolbox:
    """ Class decorator that registers all tool/action functions defined in this project. """

    _shed: dict[str, dict[str, Any]] = {}

    def __init__(self, workflow: str):
        """ Args workflow is the name of the group of tools being registered. """

        if workflow not in Toolbox._shed:
            print(f'First time registering {workflow}')
            Toolbox._shed[workflow] = {}

        self.current_workflow = workflow

    @classmethod
    def list_workflows(cls):
        return list(Toolbox._shed)

    @classmethod
    def get_action(cls, workflow_name: str, function_name: str):
        """ Returns the requested function. This is for the agent to use to call action by itself. """
        return Toolbox._shed.get(workflow_name, {}).get(function_name, None)

    def __call__(self, func):
        """Called when used as a decorator."""

        tool_name = func.__name__

        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        doc = func.__doc__ or "Unknown"
        parsed_doc = docstring_parser.parse(doc)

        # Map docstring arg descriptions
        doc_args = {p.arg_name: p.description for p in parsed_doc.params}

        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            annotation = type_hints.get(param_name, str)
            if annotation in (int, "int"):
                arg_type = "integer"
            elif annotation in (float, "float"):
                arg_type = "number"
            elif annotation in (bool, "bool"):
                arg_type = "boolean"
            else:
                arg_type = "string"

            if param.default == inspect._empty:
                required.append(param_name)

            desc = doc_args.get(param_name, f"Argument `{param_name}` of type {arg_type}")
            properties[param_name] = {"type": arg_type, "description": desc}

        # Register function metadata and callable
        Toolbox._shed[self.current_workflow][tool_name] = {
            "type": "function",
            "function": {
                "name": tool_name,
                "callable": func,
                "description": parsed_doc.short_description or doc.strip(),
                "parameters": {
                    "type": "object",
                    "required": required,
                    "properties": properties,
                },
            },
        }

        Toolbox._shed[self.current_workflow][tool_name] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper