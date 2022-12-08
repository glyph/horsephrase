from importlib.resources import files

# See http://jbauman.com/aboutgsl.html
parent_module = ".".join(__name__.split(".")[:-1])
with (files(parent_module) / "words.txt").open() as _:
    words = _.read().strip().split("\n")
del _

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
