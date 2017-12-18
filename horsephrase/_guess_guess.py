# Guess how many guesses it will take to guess a password.

from __future__ import unicode_literals

import six

from ._implementation import words

def how_long(length=4, choices=len(words), speed=1000 * 1000 * 1000 * 1000,
             optimism=2):
    """
    How long might it take to guess a password?

    @param length: the number of words that we're going to choose.
    @type length: L{int}

    @param choice: the number of words we might choose between.
    @type choice: L{int}

    @param speed: the speed of our hypothetical password guesser, in guesses
        per second.
    @type speed: L{int}

    @param optimism: When we start guessing all the options, we probably won't
        have to guess I{all} of them to get a hit.  This assumes that the
        guesser will have to guess only C{1/optimism} of the total number of
        possible options before it finds a hit.
    """
    return ((choices ** length) / (speed * optimism))



def redivmod(initial_value, factors):
    """
    Chop up C{initial_value} according to the list of C{factors} and return a
    formatted string.
    """
    result = []
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
        if six.PY2:
            addition = unicode(remainder) + ' ' + unicode(label)
        else:
            addition = str(remainder) + ' ' + str(label)
        result.insert(0, addition)
    if len(result) > 1:
        result[-1] = "and " + result[-1]
    if result:
        return ', '.join(result)
    else:
        return "instantly"



def humantime(seconds):
    """
    A human-readable interpretation of a time interval.

    @param seconds: A number of seconds.
    @type seconds: The type of seconds.

    @return: A string describing the time interval.
    @rtype: L{unicode}
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
