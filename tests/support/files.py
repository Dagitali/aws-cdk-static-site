"""
:mod:`tests.support.files` module.

Shared typing for temporary UTF-8 repository fixture writers.
"""

from collections.abc import Callable
from pathlib import Path

# SECTION: TYPE ALIASES


type FileWriter = Callable[[str, str], Path]


# !SECTION
