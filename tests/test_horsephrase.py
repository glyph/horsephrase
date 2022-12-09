from io import StringIO

import builtins as builtins_module
from unittest import mock
import sys


import horsephrase

def test_generate() -> None:
    pw = horsephrase._implementation.generate()
    assert all(word in horsephrase._implementation.words for word in pw.split(' '))

def test_estimate() -> None:
    with mock.patch.object(builtins_module, 'print') as mock_print:
        namespace = mock.MagicMock(
            count=5, wordlist=horsephrase._implementation.words,
            guesses_per_second=1000 * 1000 * 1000 * 1000,
            numeric=True
        )
        horsephrase.__main__.do_estimate(namespace)
        assert mock_print.call_count

def test_main() -> None:
    with (mock.patch.object(builtins_module, 'print') as mock_print,
          mock.patch.object(sys, "argv", ["horsephrase", "generate"])):
        horsephrase.__main__.main()
        assert mock_print.call_count
