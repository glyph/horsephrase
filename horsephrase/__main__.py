
from __future__ import annotations
from ._implementation import generate, words
from ._guess_guess import humantime, how_long

from typing import Iterator, ContextManager

import sys

if sys.version_info < (3,8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from os.path import join as pathjoin, normpath
import argparse
import string
from io import BytesIO, StringIO, TextIOWrapper

def do_generate(namespace: NameSpace) -> None:
    print(generate(number=namespace.count,
                   words=namespace.wordlist,
                   joiner=namespace.joiner))

def do_estimate(namespace: NameSpace) -> None:
    seconds = how_long(length=namespace.count,
                       choices=len(namespace.wordlist),
                       speed=namespace.guesses_per_second)
    if namespace.numeric:
        result = repr(seconds)
    else:
        result = humantime(seconds)
    print(result)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate secure passwords.")
    parser.add_argument(
        "--count", type=int, default=None,
        help="the number of tokens (words or hex digits) to print"
    )

    sourcegroup = parser.add_mutually_exclusive_group()
    sourcegroup.add_argument(
        "--words", type=argparse.FileType("r"),
        default=normpath(pathjoin(__file__, "..", "words.txt")),
        help="the filename of a words file to use"
    )
    sourcegroup.add_argument(
        "--hex", action="store_true",
        help="generate a hexidecimal key"
    )
    sourcegroup.add_argument(
        "--letters", action="store_true", help="generate a short combination of letters for easier typing, i.e. access points"
    )
    return parser


without_subparsers = make_parser()
parser = make_parser()
subparsers = parser.add_subparsers()
subparsers.required = True

parser_generate = subparsers.add_parser("generate")
parser_generate.set_defaults(do_verb=do_generate)

parser_estimate = subparsers.add_parser("estimate")
parser_estimate.add_argument("--guesses-per-second",
                             default=1000 * 1000 * 1000 * 1000,
                             type=int)
parser_estimate.add_argument("--numeric", action="store_true")
parser_estimate.set_defaults(do_verb=do_estimate)

import contextlib

@contextlib.contextmanager
def captured_output() -> Iterator[StringIO]:
    buffer = StringIO()
    out = sys.stdout
    err = sys.stderr
    sys.stdout = buffer
    sys.stderr = buffer
    try:
        yield buffer
    finally:
        sys.stdout = out
        sys.stderr = err

class NameSpace(Protocol):
    wordlist: list[str]
    count: int
    joiner: str
    guesses_per_second: int
    numeric: bool
    hex: bool
    letters: bool
    words: ContextManager[TextIOWrapper]

    def do_verb(self, namespace: NameSpace) -> None:
        pass

def parse_command_line(argv: list[str]) -> NameSpace:
    try:
        with captured_output() as captured:
            return parser.parse_args(argv)
    except:
        try:
            with captured_output() as recaptured:
                without_subparsers.parse_args(argv)
        except:
            print(captured.getvalue(), end="")
            raise
        else:
            print(recaptured.getvalue(), end="")
        return parser.parse_args(argv + ["generate"])


def main() -> None:
    namespace = parse_command_line(sys.argv[1:])
    if namespace.hex:
        namespace.wordlist = list(sorted(set(string.hexdigits.lower())))
        namespace.joiner = ""
        if namespace.count is None:
            namespace.count = 20
    elif namespace.letters:
        namespace.wordlist = list(string.ascii_letters)
        namespace.joiner = ""
        if namespace.count is None:
            namespace.count = 13
    else:
        if namespace.count is None:
            namespace.count = 5
        namespace.joiner = " "
        with namespace.words as wordfile:
            namespace.wordlist = wordfile.read().split()
    namespace.do_verb(namespace)

if __name__ == '__main__':
    main()
