from __future__ import annotations
import sys

# See http://jbauman.com/aboutgsl.html
parent_module = ".".join(__name__.split(".")[:-1])
wordfile_name = "words.txt"

from typing import Callable

_read_text: Callable[[str, str], str]

if sys.version_info >= (3, 9):
    from importlib.resources import files

    def _read_text(module: str, filename: str) -> str:
        with (files(parent_module) / wordfile_name).open() as f:
            return f.read()

else:
    from importlib.resources import read_text as _read_text

words = _read_text(parent_module, wordfile_name).strip().split("\n")


from random import SystemRandom
from typing import TypeVar, Callable, Sequence


def generate(
    number: int = 4,
    choice: Callable[[Sequence[str]], str] = SystemRandom().choice,
    words: list[str] = words,
    joiner: str = " ",
) -> str:
    """
    Generate a random passphrase from the GSL.
    """
    return joiner.join(choice(words) for each in range(number))


def output() -> int:
    print(generate())
    return 0
