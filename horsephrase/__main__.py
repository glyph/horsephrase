
from __future__ import absolute_import, print_function, unicode_literals
from ._implementation import generate, words
from ._guess_guess import humantime, how_long
from pkg_resources import resource_filename

import six
import sys
import argparse
import string
from io import BytesIO, StringIO

def do_generate(namespace):
    print(generate(number=namespace.count,
                   words=namespace.wordlist,
                   joiner=namespace.joiner))

def do_estimate(namespace):
    seconds = how_long(length=namespace.count,
                       choices=len(namespace.wordlist),
                       speed=namespace.guesses_per_second)
    if namespace.numeric:
        result = repr(seconds)
    else:
        result = humantime(seconds)
    print(result)


def make_parser():
    parser = argparse.ArgumentParser(description="Generate secure passwords.")
    parser.add_argument(
        "--count", type=int, default=None,
        help="the number of tokens (words or hex digits) to print"
    )

    sourcegroup = parser.add_mutually_exclusive_group()
    sourcegroup.add_argument(
        "--words", type=argparse.FileType("rb"),
        default=resource_filename("horsephrase", "words.txt"),
        help="the filename of a words file to use"
    )
    sourcegroup.add_argument(
        "--hex", action="store_true",
        help=""
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
def captured_output():
    buffer = BytesIO() if six.PY2 else StringIO()
    class LenientIO(object):
        def write(self, data):
            if six.PY3 or isinstance(data, bytes):
                buffer.write(data)
            else:
                buffer.write(data.encode("utf-8"))
    out = sys.stdout
    err = sys.stderr
    sys.stdout = LenientIO()
    sys.stderr = LenientIO()
    try:
        yield buffer
    finally:
        sys.stdout = out
        sys.stderr = err

def parse_command_line(argv):
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


def main():
    namespace = parse_command_line(sys.argv[1:])
    if namespace.hex:
        namespace.wordlist = list(sorted(set(string.hexdigits.lower())))
        namespace.joiner = ""
        if namespace.count is None:
            namespace.count = 20
    else:
        if namespace.count is None:
            namespace.count = 5
        namespace.joiner = " "
        with namespace.words as wordfile:
            namespace.wordlist = wordfile.read().decode("utf-8").split()
    namespace.do_verb(namespace)

if __name__ == '__main__':
    main()
