"""This module provides functions to perform Tagalog stemming on word/s.
"""


import os
from tabulate import tabulate
from typing import Optional
from nltk import word_tokenize
from string import punctuation as PUNCS

from .helpers.alphabet import VOWELS
from .helpers.validation import is_valid, is_acceptable, is_vowel, is_consonant
from .helpers.manipulation import replace_letter, swap_letters
from .helpers.words import get_words
from .helpers.affixes import PREFIXES, INFIXES, SUFFIXES

from .stem import Stem


script_dir = os.path.dirname(os.path.realpath(__file__))


valid_words = get_words()
valid_words.extend(["split"])


def get_stems(text: str, valid_words: Optional[list[str]] = valid_words, exclude_punc: bool=True) -> list[str]:
    """Get the stem of each word in a text.

    Args:
        text (str): Any text.
        valid_words (Optional[list[str]]): A list of valid words to consider for stemming. If None, no validation is performed.
        exclude_punc (bool): Whether to exclude punctuation from tokens. Defaults to a list of valid Tagalog words.

    Returns:
        list[str]: Stems of each word in the text.
    """
    # Tokenize the text
    tokens = word_tokenize(text)

    # Optionally exclude punctuation
    if exclude_punc:
        tokens = [token for token in tokens if token not in PUNCS]

    # Get stems for each token
    return [get_stem(token, valid_words) for token in tokens]


def get_stem(token: str, valid_words: Optional[list[str]] = valid_words) -> Stem:
    """Get the stem of a word.

    Args:
        token (str): Word to be stemmed.
        valid_words (str, optional): A list of valid words to consider for stemming. If None, no validation is performed.
            Defaults to a list of valid Tagalog words.

    Returns:
        Stem: Stem of the token.
    """
    token = Stem(token.strip().lower())

    candidates = list(get_stem_candidates(token, valid_words))

    # Filter out original token
    candidates = [c for c in candidates if c != token]
    if not candidates:
        return token

    # Filter out candidates with transformations and contractions
    no_transformations = [c for c in candidates if c.count_transformations() == 0]
    no_contractions = [c for c in candidates if not c.contraction]

    if no_tran_cont := list(set(no_transformations) & set(no_contractions)):
        return sort_candidates(no_tran_cont)[0]
    elif no_contractions:
        return sort_candidates(no_contractions)[0]
    elif no_transformations:
        return sort_candidates(no_transformations)[0]
    else:
        return sort_candidates(candidates)[0]


def get_stem_candidates(token: str, valid_words: Optional[list[str]] = valid_words) -> list[Stem]:
    """Get the possible stems of a word.

    Args:
        token (str): Word to be stemmed.
        valid_words (str, optional): A list of valid words to consider for stemming. If None, no validation is performed.
            Defaults to a list of valid Tagalog words.

    Returns:
        list[Stem]: A list of possible valid and acceptable stems or candidates of the token.
    """
    token = Stem(token.strip().lower())

    # Initialize a list of all stemming attempts
    stems = {token}

    # Apply all stemming functions in order
    stems = apply_stemming(
        functions=(
            stem_dup,
            stem_pre,
            stem_rep,
            stem_inf,
            stem_rep,
            stem_suf,
            stem_dup,
        ),
        tokens=stems,
        valid_words=valid_words,
    )

    if candidates := [
        stem for stem in stems if is_valid(stem, valid_words) and is_acceptable(stem)
    ]:
        return sort_candidates(candidates)
    else:
        return [token]


def sort_candidates(candidates: list[Stem]) -> list[Stem]:
    """Sorts stem candidates by longest affix and reduplication.

    Args:
        candidates (list[Stem]): A list of stem candidates.

    Returns:
        list[Stem]: Ordered list of the stem candidates.
    """
    return sorted(candidates, key=lambda c: c.count_affixes() + c.count_reduplication(), reverse=True)


def apply_stemming(
    functions: tuple, tokens: set[Stem], valid_words: Optional[list[str]] = valid_words
) -> set[Stem]:
    """Apply all stemming functions to a list of tokens.

    Args:
        functions (tuple): A tuple of stemming functions to be applied to the tokens.
        tokens (set[Stem]): A set of words to be stemmed.
        valid_words (str, optional): A list of valid words to consider for stemming. If None, no validation is performed.
            Defaults to None.

    Returns:
        set[Stem]: A set of stemming attempts for each token.
    """
    for f in functions:
        if f in [stem_suf]:
            tokens.update(f(tokens, valid_words))
        else:
            tokens.update(f(tokens))
    return tokens


def stem_pre(tokens: set[Stem]) -> set[Stem]:
    """Stems tokens with prefixes.

    Args:
        tokens (set[Stem]): A set of words to be stemmed.

    Returns:
        set[Stem]: A set of stemming attempts for each token, empty otherwise.
    """
    stems = set()

    for token in tokens:
        for prefix in PREFIXES:
            if token.startswith(prefix) and len(token) > len(prefix):
                stem = token[len(prefix) :]
                stem.pre = prefix

                if stem[0] == "-":
                    stem = stem[1:]

                stems.add(stem)

                # Phoneme change (d/r) (e.g. parami => dami)
                if stem[0] == "r" and is_vowel(prefix[-1], stem[1]):
                    stem_phch_dr = "d" + stem[1:]
                    stem_phch_dr.phoneme_change = "pre: d/r"
                    stems.add(stem_phch_dr)

                # Assimilation
                if is_acceptable(stem) and is_vowel(stem[0]):
                    # -ng: k/null (e.g. pangailangan => kailangan)
                    if prefix.endswith("ng"):
                        stem_asml_knull = "k" + stem
                        stem_asml_knull.assimilation = "k/null"
                        stems.add(stem_asml_knull)

                        # '-ng' repetition
                        if (
                            len(stem) > 3
                            and stem[1:3] == "ng"
                            and stem[0] == stem[3]
                            and is_vowel(stem[0])
                        ):
                            # (e.g. pangingisda => isda)
                            stem_ng_rep = stem[3:]
                            stem_ng_rep.rep = str(stem[:3])
                            stems.add(stem_ng_rep)

                            if is_acceptable(stem_ng_rep):
                                # Assimilation (k/null) (e.g. pangangailangan => kailangan)
                                stem_ng_rep_asml = "k" + stem_ng_rep
                                stem_ng_rep_asml.assimilation = "k/null"
                                stems.add(stem_ng_rep_asml)

                    # -m: b/p (e.g. pamigay = bigay, pamagitan => pagitan)
                    elif prefix.endswith("m"):
                        for l in "bp":
                            stem_asml_bp = l + stem
                            stem_asml_bp.assimilation = "b/p: " + l
                            stems.add(stem_asml_bp)

                        # '-m' repetition
                        if (
                            len(stem) > 2
                            and stem[1] == "m"
                            and stem[0] == stem[2]
                            and is_vowel(stem[0])
                        ):
                            # Assimilation (b/p)
                            # (e.g. pamimigay => bigay, pamamagitan => pagitan)
                            for l in "bp":
                                stem_m_rep_asml = l + stem[2:]
                                stem_m_rep_asml.assimilation = "b/p: " + l
                                stems.add(stem_m_rep_asml)

                    # -n: d/s/t (e.g. panamit => damit, panigarilyo => sigarilyo, panahi => tahi)
                    elif prefix.endswith("n"):
                        for l in "dst":
                            stem_asml_dst = l + stem
                            stem_asml_dst.assimilation = "d/s/t: " + l
                            stems.add(stem_asml_dst)

                        # '-n' repetition
                        if (
                            len(stem) > 2
                            and prefix.endswith("n")
                            and stem[1] == "n"
                            and stem[0] == stem[2]
                            and is_vowel(stem[0])
                        ):
                            # Assimilation (d/s/t)
                            # (e.g. pananamit => damit, paninigarilyo => sigarilyo, pananahi => tahi)
                            for l in "dst":
                                stem_n_rep_asml = l + stem[2:]
                                stem_n_rep_asml.assimilation = "d/s/t: " + l
                                stems.add(stem_n_rep_asml)

    return stems


def stem_inf(tokens: set[Stem]) -> set[Stem]:
    """Stems tokens with infixes.

    Args:
        tokens (set[Stem]): A set of words to be stemmed.

    Returns:
        set[Stem]: A set of stemming attempts for each token, empty otherwise.
    """
    stems = set()

    for token in tokens:
        for infix in INFIXES:
            if len(token) > len(infix) + 1:
                stem = None

                # <infix>V... (e.g. inaral => aral)
                if token.startswith(infix) and is_vowel(token[2]):
                    stem = token[2:]

                # C<infix>V... (e.g. sinulat => sulat)
                elif (
                    len(token) > 3
                    and token[1:3] == infix
                    and is_consonant(token[0])
                    and is_vowel(token[3])
                ):
                    stem = token[0] + token[3:]

                # CC<infix>V... (e.g. chineck => check)
                elif (
                    len(token) > 4
                    and token[2:4] == infix
                    and is_consonant(token[:2])
                    and is_vowel(token[4])
                ):
                    stem = token[0:2] + token[4:]

                # CCC<infix>V... (e.g. splinit => split)
                elif (
                    len(token) > 5
                    and token[3:5] == infix
                    and is_consonant(token[:3])
                    and is_vowel(token[5])
                ):
                    stem = token[0:3] + token[5:]

                if stem:
                    stem.inf = infix
                    stems.add(stem)

    return stems


def stem_suf(tokens: set[Stem], valid_words: Optional[list[str]] = valid_words) -> set[Stem]:
    """Stems tokens with suffixes.

    Args:
        tokens (set[Stem]): A set of words to be stemmed.
        valid_words (str, optional): A list of valid words to consider for stemming. If None, no validation is performed.
            Defaults to a list of valid Tagalog words.

    Returns:
        set[Stem]: A set of stemming attempts for each token, empty otherwise.
    """
    stems = set()

    for token in tokens:
        for suffix in SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix):
                stem = token[0 : len(token) - len(suffix)]
                if suffix in ("ng", "g", "'t", "'y"):
                    # 'g' contraction
                    if suffix == "g" and stem[-1] != "n":
                        continue

                    # "'t" or "'y" contraction
                    if suffix in ("'t", "'y") and not is_vowel(stem[-1]):
                        continue

                    stem.contraction = suffix
                else:
                    stem.suf = suffix

                stems.add(stem)

                # Phoneme change (d/r) (e.g. bayaran => bayad)
                if suffix in ("in", "an") and stem[-1] == "r":
                    stem_phch_dr = replace_letter(stem, -1, "d")
                    stem_phch_dr.phoneme_change = "suf: d/r"
                    stems.add(stem_phch_dr)

                # Phoneme change (o/u)
                # (e.g. tauhan => tao)
                if len(stem) > 1 and stem[-1] == "u":
                    stem_phch_ou = replace_letter(stem, -1, "o")
                    stem_phch_ou.phoneme_change = "suf: o/u"
                    stems.add(stem_phch_ou)
                # (e.g. inuman => inom)
                elif len(stem) > 2 and stem[-2] == "u":
                    stem_phch_ou = replace_letter(stem, -2, "o")
                    stem_phch_ou.phoneme_change = "suf: o/u"
                    stems.add(stem_phch_ou)

                # Phoneme change (e/i)
                # (e.g. kingkihan => kingke)
                if len(stem) > 1 and stem[-1] == "i":
                    stem_phch_ei = replace_letter(stem, -1, "e")
                    stem_phch_ei.phoneme_change = "suf: e/i"
                    stems.add(stem_phch_ei)
                # (e.g. paitin => paet)
                elif len(stem) > 2 and stem[-2] == "i":
                    stem_phch_ei = replace_letter(stem, -2, "e")
                    stem_phch_ei.phoneme_change = "suf: e/i"
                    stems.add(stem_phch_ei)

                if len(stem) > 2 and is_acceptable(stem) and is_consonant(stem[-2:]):
                    # Vowel loss (e.g. buksan => bukas)
                    if stems_vwls := stem_vowel_loss({stem}, valid_words):
                        stems.update(stems_vwls)

                    # Metathesis (e.g. tamnin => tanim)
                    stem_mtts = swap_letters(stem, -1, -2)
                    stem_mtts.metathesis = True

                    if is_valid(stem_mtts, valid_words):
                        stems.add(stem_mtts)

                    elif stems_vwls_mtts := stem_vowel_loss(
                        {stem_mtts}, valid_words
                    ):
                        stems.update(stems_vwls_mtts)

    return stems


def stem_vowel_loss(
    tokens: set[Stem], valid_words: Optional[list[str]] = valid_words
) -> set[Stem]:
    """Stems tokens with vowel loss.

    Args:
        tokens (set[Stem]): A set of words to be stemmed.
        valid_words (str, optional): A list of valid words to consider for stemming. If None, no validation is performed.
            Defaults to a list of valid Tagalog words.

    Returns:
        set[Stem]: A set of stemming attempts for each token, empty otherwise.
    """
    stems = set()

    for token in tokens:
        for vowel in VOWELS:
            if len(token) > 1:
                stem = token + vowel
                if valid_stem := is_valid(stem, valid_words):
                    valid_stem.vowel_loss = vowel
                    stems.add(valid_stem)

            if len(token) > 2:
                stem = token[0:-1] + vowel + token[-1]
                if valid_stem := is_valid(stem, valid_words):
                    valid_stem.vowel_loss = vowel
                    stems.add(valid_stem)

    return stems


def stem_rep(tokens: set[Stem]) -> set[Stem]:
    """Stems tokens with partial reduplication (simply referred as repetition).

    Args:
        tokens (set[Stem]): A set of words to be stemmed.

    Returns:
        set[Stem]: A set of stemming attempts for each token, empty otherwise.
    """
    stems = set()

    for token in tokens:
        stem = None

        # Starts with a vowel (V-V) (e.g. aalis => alis)
        if len(token) > 2 and token[0] == token[1] and is_vowel(token[0:2]):
            stem = token[1:]
            stem.rep = str(token[0])

        # Starts with a consonant-vowel (CV-CV) (e.g. bibili => bili)
        elif len(token) > 4 and token[0:2] == token[2:4] and is_consonant(token[0]):
            stem = token[2:]
            stem.rep = str(token[:2])

        # Starts with a 2-consonant cluster
        elif len(token) > 5:
            # Repeats first consonant and vowel (CV-CCV) (e.g. cecheck)
            if (
                token[0] == token[2]
                and token[1] == token[4]
                and is_consonant(token[0])
                and is_vowel(token[1])
            ):
                stem = token[2:]
                stem.rep = str(token[:2])

            # Repeats all consonants (CC-CCV) (e.g. chcheck => check)
            elif (
                token[0:2] == token[2:4]
                and is_consonant(token[0:2])
                and is_vowel(token[4])
            ):
                stem = token[2:]
                stem.rep = str(token[:2])

            # Repeats all consonants and vowel (CCV-CCV) (e.g. checheck => check)
            elif (
                token[0:2] == token[3:5]
                and is_consonant(token[0:2])
                and is_vowel(token[2])
            ):
                stem = token[3:]
                stem.rep = str(token[:3])

        # Starts with a 3-consonant cluster
        if len(token) > 6:
            # Repeats first consonant and vowel (CV-CCCV) (e.g. sisplit => split)
            if (
                token[0] == token[2]
                and token[1] == token[5]
                and is_consonant(token[0])
                and is_vowel(token[1])
            ):
                stem = token[2:]
                stem.rep = str(token[:2])

            # Repeats first two consonants (CC-CCCV) (e.g. spsplit => split)
            elif (
                token[0:2] == token[2:4]
                and is_consonant(token[0:2])
                and is_vowel(token[5])
            ):
                stem = token[2:]
                stem.rep = str(token[:2])

            # Repeats first two consonants and vowel (CCV-CCCV) (e.g. spisplit => split)
            elif (
                token[0:2] == token[3:5]
                and token[2] == token[6]
                and is_consonant(token[0:2])
                and is_vowel(token[6])
            ):
                stem = token[3:]
                stem.rep = str(token[:3])

            # Repeats all consonants (CCC-CCCV) (e.g. splsplit => split)
            elif (
                token[0:3] == token[3:6]
                and is_consonant(token[0:3])
                and is_vowel(token[6])
            ):
                stem = token[3:]
                stem.rep = str(token[:3])

            # Repeats all consonants and vowel (CCCV-CCCV) (e.g. splisplit => split)
            elif (
                token[0:4] == token[4:8]
                and is_consonant(token[0:3])
                and is_vowel(token[3])
            ):
                stem = token[4:]
                stem.rep = str(token[:4])

        if stem:
            stems.add(stem)

    return stems


def stem_dup(tokens: set[Stem]) -> set[Stem]:
    """Stems tokens with full reduplication (simply referred as duplication).

    Args:
        tokens (set[Stem]): A set of words to be stemmed.

    Returns:
        set[Stem]: A set of stemming attempts for each token, empty otherwise.
    """
    stems = set()

    for token in tokens:

        if (
            "-" in token
            and "-" not in (token[0], token[-1])
            and len(token.split("-")) == 2
        ):

            first, second = token.split("-")

            if len(first) > 1 and len(second) > 1:

                # Exact match (e.g. ano-ano => ano)
                if first == second:
                    stem = first
                    stem.dup = str(first)
                    stems.add(stem)

                # Repeat first 2 syllables for >3-syllable words (e.g. panga-pangako => pangako)
                elif len(first) > 2 and len(second) > 4 and second.startswith(first):
                    stem = second
                    stem.dup = str(first)
                    stems.add(stem)

                # Phoneme change (o/u) (e.g. anu-ano => ano)
                elif (
                    len(first) > 2
                    and first[-1] == "u"
                    and replace_letter(first, -1, "o") == second
                    or first[-2] == "u"
                    and replace_letter(first, -2, "o") == second
                ):
                    stem = second
                    stem.dup = str(second)
                    stem.phoneme_change = "dup: o/u"
                    stems.add(stem)

                # Contractions on first part

                # 2-character contractions
                elif len(first) > 3 and first[-2:] in ("ng", "'t"):

                    # Exact match after contraction removal (e.g. iba't-iba => iba)
                    if first[:-2] == second:
                        stem = second
                        stem.dup = str(second)
                        stem.contraction = first[-2:]
                        stems.add(stem)

                    else:
                        # Phoneme change (o/u) (e.g. larung-laro => laro)
                        if first[-3] == "u" and first[0:-3] + "o" == second:
                            stem = second
                            stem.dup = str(second)
                            stem.contraction = first[-2:]
                            stems.add(stem)

                        # Token ends with 'n' with 'ng' contraction
                        elif first[-2:] == "ng":
                            # (e.g. ating-atin => atin)
                            if first[:-1] == second:
                                stem = second
                                stem.dup = str(second)
                                stem.contraction = first[-1]
                                stems.add(stem)

                            # (e.g. hapung-hapon => hapon)
                            elif (
                                first[-3] == "u"
                                and replace_letter(first[:-1], -2, "o") == second
                            ):
                                stem = second
                                stem.dup = str(second)
                                stem.contraction = first[-1]
                                stem.phoneme_change = "dup: o/u"
                                stems.add(stem)

                # 1-character contractions
                elif len(first) > 2 and first[-1] in ("t"):

                    # Exact match after contraction removal (e.g. ibat-iba => iba)
                    if first[:-1] == second:
                        stem = second
                        stem.dup = str(second)
                        stem.contraction = first[-1]
                        stems.add(stem)

                    # Phoneme change (o/u) (e.g. libut-libo => libo)
                    elif first[-2] == "u" and first[0:-2] + "o" == second:
                        stem = second
                        stem.dup = str(second)
                        stem.contraction = first[-1]
                        stem.phoneme_change = "dup: o/u"
                        stems.add(stem)

    return stems


if __name__ == "__main__":
    text = input("\ntext: ")
    print()

    stems = get_stems(text)
    print("stems:", stems)
    print()

    for token in word_tokenize(text):
        candidates = get_stem_candidates(token)
        if candidates:
            table = [{"stem": c, **c.__dict__} for c in candidates]
            print(token)
            print(tabulate(table, headers="keys"))
            print()
