"""
Run with 'python -m horsephrase._regen_words > horsephrase/words.txt'

- Stop allowing words less than 3 characters; if we have the possibility
  of words that short, it's trivially possible to attack the password as
  letters rather than as selections from this list.

- Add words (both sourced from https://norvig.com/ngrams/) from a list of
  correctly-spelled words (the YAWL) in the order of word
  frequency (count_1w.txt) until we reach a desirable count

- The oldest recorded living human -- courtesy of this list
  https://en.wikipedia.org/wiki/List_of_oldest_living_people - is
  presently 116 years and 74 days old. Determine the desirable count
  from the number of guesses that will exceed that time with a 5-word
  passphrase assuming a trillion guesses per second.

- Remove words that are offensive, triggering or otherwise in poor taste.
  Horsephrases should be communicable to people over phone lines without
  being embarassing, offensive or unprofessional.
  If generating a horsephrase generates something offensive, add the sha256 of
  the offending word to _removed_words, run the command at the start of this
  module, and open a PR with both changes.
"""
if __name__ != "__main__":
    raise ImportError("module is not importable")

import hashlib
import itertools

import requests

# There's a whole bit about the oldest
# living human or something.
NUM_WORDS = 23600

# Removed words are specified by their hash,
# as we do not want to offend people who read the source.
_removed_words = set([
   '31506a8448a761a448a08aa69d9116ea8a6cb1c6b3f4244b3043051f69c9cc3c',
    'e9b6438440bf1991a49cfc2032b47e4bde26b7d7a6bf7594ec6f308ca1f5797c',
])

def get_words(session):
    yawl = session.get("https://norvig.com/ngrams/word.list")
    correct = set(yawl.text.split())
    counts = session.get("https://norvig.com/ngrams/count_1w.txt")
    for line in counts.text.splitlines():
        word, count = line.split()
        if word not in correct:
            continue
        yield word

def valid_words(words):
    for word in words:
        if len(word) <= 3:
            continue
        digest = hashlib.sha256(word.encode('ascii')).hexdigest()
        if digest in _removed_words:
            continue
        yield word

for word in sorted(itertools.islice(valid_words(get_words(requests.Session())),
                                    NUM_WORDS)):
    print(word)
