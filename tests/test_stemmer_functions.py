from tglstemmer.helpers.words import get_words

from tglstemmer import stemmer


valid_words = get_words()


def test_stem_pre():
    stems = {
        "parami": "dami",
        "pangailangan": "kailangan",
        "pangingisda": "isda",
        "pangangailangan": "kailangan",
        "pamigay": "bigay",
        "pamagitan": "pagitan",
        "pamimigay": "bigay",
        "pamamagitan": "pagitan",
        "panamit": "damit",
        "panigarilyo": "sigarilyo",
        "panahi": "tahi",
        "pananamit": "damit",
        "paninigarilyo": "sigarilyo",
        "pananahi": "tahi"
    }
    for s in stems:
        assert stems[s] in stemmer.get_stem_candidates(s, valid_words + list(stems.values()))


def test_stem_inf():
    stems = {
        "inaral": "aral",
        "sinulat": "sulat",
        "chineck": "check",
        "splinit": "split",
    }
    for s in stems:
        assert stems[s] in stemmer.get_stem_candidates(s, valid_words + list(stems.values()))


def test_stem_suf():
    stems = {
        "bayaran": "bayad",
        "tauhan": "tao",
        "inuman": "inom",
        "kingkihan": "kingki",
        "paitin": "paet",
        "buksan": "bukas",
        "tamnin": "tanim",
    }
    for s in stems:
        assert stems[s] in stemmer.get_stem_candidates(s, valid_words + list(stems.values()))


def test_stem_rep():
    stems = {
        "aalis": "alis",
        "bibili": "bili",
        "cecheck": "check",
        "chcheck": "check",
        "checheck": "check",
        "sisplit": "split",
        "spsplit": "split",
        "spisplit": "split",
        "splsplit": "split",
        "splisplit": "split",
    }
    for s in stems:
        assert stems[s] in stemmer.get_stem_candidates(s, valid_words + list(stems.values()))


def test_stem_dup():
    stems = {
        "ano-ano": "ano",
        "panga-pangako": "pangako",
        "anu-ano": "ano",
        "iba't-iba": "iba",
        "larung-laro": "laro",
        "ating-atin": "atin",
        "hapung-hapon": "hapon",
        "ibat-iba": "iba",
        "libut-libo": "libo",
    }
    for s in stems:
        assert stems[s] in stemmer.get_stem_candidates(s, valid_words + list(stems.values()))