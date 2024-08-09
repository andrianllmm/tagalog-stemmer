from tglstemmer.helpers.words import get_words
from tglstemmer.helpers.validation import is_valid, is_acceptable
from tglstemmer.helpers.manipulation import replace_letter, swap_letters

from tglstemmer import stemmer
from tglstemmer.stem import Stem


valid_words = get_words()


def test_is_valid():
    assert is_valid(valid_words[0], valid_words)
    assert is_valid(valid_words[-1], valid_words)
    assert is_valid("OOV", ["OOV"])
    assert not is_valid("123", valid_words)


def test_is_acceptable():
    assert is_acceptable("word")
    assert not is_acceptable("aaa")
    assert not is_acceptable("bbbb")
    assert not is_acceptable("c")


def test_replace_letter():
    assert replace_letter(Stem("word"), 1, "u") == "wurd"


def test_swap_letters():
    assert swap_letters(Stem("now"), 0, -1) == "won"