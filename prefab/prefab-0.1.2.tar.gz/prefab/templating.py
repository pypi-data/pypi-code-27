"""
Render jinja templates from the templating/ directory.
"""
from pathlib import Path
from typing import Any, Dict

from prefab.jinja import render


def ensure(
    *,
    source: str,
    destination: str,
    context: Dict[str, Any] = None,
) -> bool:
    prefab_root = Path(__file__).parent
    with Path(f'{prefab_root}/templates/{source}').open() as f:
        unrendered_template = f.read()
    rendered_template = render(
        template=unrendered_template,
        context=context,
    )
    try:
        with Path(destination).open(mode='r') as f:
            old_file = f.read()
            if old_file == rendered_template:
                print(f'{destination} up to date.')
                return False
    except FileNotFoundError:
        pass
    with Path(destination).open(mode='w') as f:
        f.write(rendered_template)
        print(f'{destination} updated!')
    return True
