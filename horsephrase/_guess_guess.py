# Guess how many guesses it will take to guess a password.

from __future__ import annotations
from typing import Iterable

from ._implementation import words

def how_long(length: int=4, choices: int=len(words), speed: int=1000 * 1000 * 1000 * 1000,
             optimism: int=2) -> int:
    """
    How long might it take to guess a password?

    @param length: the number of words that we're going to choose.

    @param choice: the number of words we might choose between.

    @param speed: the speed of our hypothetical password guesser, in guesses
        per second.

    @param optimism: When we start guessing all the options, we probably won't
        have to guess I{all} of them to get a hit.  This assumes that the
        guesser will have to guess only C{1/optimism} of the total number of
        possible options before it finds a hit.
    """
    # https://github.com/python/mypy/issues/7765
    assert choices > 0
    assert length > 0
    count: int = (choices ** length)
    return int(count / (speed * optimism))



def redivmod(initial_value: float, factors: Iterable[tuple[int,str]]) -> str:
    """
    Chop up C{initial_value} according to the list of C{factors} and return a
    formatted string.
    """
    result: list[str] = []
    value = initial_value
    for divisor, label in factors:
        if not divisor:
            remainder = value
            if not remainder:
                break
        else:
            value, remainder = divmod(value, divisor)
            if not value and not remainder:
                break
        if remainder == 1:
            # depluralize
            label = label[:-1]
        addition = str(remainder) + ' ' + str(label)
        result.insert(0, addition)
    if len(result) > 1:
        result[-1] = "and " + result[-1]
    if result:
        return ', '.join(result)
    else:
        return "instantly"



def humantime(seconds: float) -> str:
    """
    A human-readable interpretation of a time interval.

    @param seconds: A number of seconds.

    @return: A string describing the time interval.
    """
    return redivmod(seconds, [(60, "seconds"),
                              (60, "minutes"),
                              (24, "hours"),
                              (7, "days"),
                              (52, "weeks"),
                              (0, "years")])

if __name__ == "__main__":
    import sys
    print(humantime(how_long(*map(int, sys.argv[1:]))))
