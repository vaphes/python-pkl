import os
import sys
from typing import Any


def debug(format: str, *a: Any) -> None:
    debug_enable = bool(os.environ.get("PKL_DEBUG"))
    if debug_enable:
        print(f"[pkl-go] {format % a}", file=sys.stdout)
