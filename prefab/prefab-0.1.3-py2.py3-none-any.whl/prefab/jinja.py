from typing import Any, Dict

from jinja2 import Environment


def render(
    *,
    template: str,
    context: Dict[str, Any] = None,
) -> str:
    context = context or {}
    return (
        Environment()
        .from_string(template)
        .render(**context)
    )
