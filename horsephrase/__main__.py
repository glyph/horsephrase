
from __future__ import absolute_import, print_function, unicode_literals
from ._implementation import generate
from ._guess_guess import humantime, how_long
from pkg_resources import resource_filename

import sys
import argparse

parser = argparse.ArgumentParser(description="Generate secure passwords.")
parser.add_argument("--count", type=int, default=5)
parser.add_argument("--words", type=argparse.FileType("rb"),
                    default=resource_filename("horsephrase", "words.txt"))


subparsers = parser.add_subparsers()

parser_generate = subparsers.add_parser("generate")

def do_generate(namespace):
    print(generate(number=namespace.count))

parser_generate.set_defaults(do_verb=do_generate)

parser_estimate = subparsers.add_parser("estimate")
parser_estimate.add_argument("--guesses-per-second",
                             default=1000 * 1000 * 1000 * 1000,
                             type=int)
parser_estimate.add_argument("--numeric")
def do_estimate(namespace):
    seconds = how_long(length=namespace.count,
                       choices=len(namespace.words.read().split()),
                       speed=namespace.guesses_per_second)
    if namespace.numeric:
        result = repr(seconds)
    else:
        result = humantime(seconds)
    print(result)
parser_estimate.set_defaults(do_verb=do_estimate)


def main():
    argv = sys.argv[1:]
    if not argv:
        argv = ["generate"]
    namespace = parser.parse_args(argv)
    namespace.do_verb(namespace)

if __name__ == '__main__':
    main()
