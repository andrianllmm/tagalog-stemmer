"""This module provides a class to store Tagalog stems.
"""


from typing import Optional


class Stem(str):
    """A stem of a word containing its affixes and transformations.

    Attributes:
        pre (str, optional): Prefix. Defaults to None.
        inf (str, optional): Infix. Defaults to None.
        suf (stf, optional): Suffix. Defaults to None.
        rep (rep, optional): Partial reduplication or repetition. Defaults to None.
        dup (dup, optional): Full reduplication or duplication. Defaults to None.
        phoneme_change (str, optional): Phoneme change transformation. Defaults to None.
        assimilation (str, optional): Assimilation transformation. Defaults to None.
        vowel_loss (str, optional): Vowel loss transformation. Defaults to None.
        metathesis (str, optional): Metathesis transformation. Defaults to None.
    """

    def __new__(cls, stem: str, *args, **kwargs):
        # Create a new instance of Stem with the string value stem
        return super().__new__(cls, stem)

    def __init__(
        self,
        stem,
        pre: Optional[str] = None,
        inf: Optional[str] = None,
        suf: Optional[str] = None,
        rep: Optional[str] = None,
        dup: Optional[str] = None,
        contraction: Optional[str] = None,
        phoneme_change: Optional[str] = None,
        assimilation: Optional[str] = None,
        vowel_loss: Optional[str] = None,
        metathesis: Optional[str] = None,
    ):
        # Initialize additional attributes
        self.pre = pre
        self.inf = inf
        self.suf = suf
        self.rep = rep
        self.dup = dup
        self.contraction = contraction
        self.phoneme_change = phoneme_change
        self.assimilation = assimilation
        self.vowel_loss = vowel_loss
        self.metathesis = metathesis

    def count_affixes(self):
        """Counts the length of affixes.
        """
        return (
            len(self.pre or "")
            + len(self.inf or "")
            + len(self.suf or "")
        )

    def count_reduplication(self):
        """Counts the length of reduplication (repetition and duplication).
        """
        return (
            len(self.rep or "")
            + len(self.dup or "")
        )

    def count_transformations(self):
        """Counts the number of transformations.
        """
        return (
            int(bool(self.phoneme_change))
            + int(bool(self.assimilation))
            + int(bool(self.vowel_loss))
            + int(bool(self.metathesis))
        )

    # Override str methods
    def __getitem__(self, key):
        # Override slicing
        return Stem(super().__getitem__(key), **self.__dict__)

    def __add__(self, other):
        # Override concatenation
        if isinstance(other, str):
            other = Stem(other)

        if not isinstance(other, Stem):
            return NotImplemented

        return Stem(super().__add__(other), **self.__dict__)

    def __radd__(self, other):
        # Override concatenation
        if isinstance(other, str):
            other = Stem(other)

        if not isinstance(other, Stem):
            return NotImplemented

        return Stem(other + self, **self.__dict__)

    def split(self, sep=None, maxsplit=-1):
        substrings = super().split(sep, maxsplit)
        return [Stem(substring, **self.__dict__) for substring in substrings]

    def replace(self, old, new, count=-1):
        return Stem(super().replace(old, new, count), **self.__dict__)

    def strip(self, chars=None):
        return Stem(super().strip(chars), **self.__dict__)

    def lstrip(self, chars=None):
        return Stem(super().lstrip(chars), **self.__dict__)

    def rstrip(self, chars=None):
        return Stem(super().rstrip(chars), **self.__dict__)

    def upper(self):
        return Stem(super().upper(), **self.__dict__)

    def lower(self):
        return Stem(super().lower(), **self.__dict__)

    def title(self):
        return Stem(super().title(), **self.__dict__)

    def capitalize(self):
        return Stem(super().capitalize(), **self.__dict__)
