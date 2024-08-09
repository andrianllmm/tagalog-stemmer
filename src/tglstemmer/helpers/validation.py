from .alphabet import VOWELS, CONSONANTS


def is_valid(token, valid_words=None):
    """Checks if token is valid against a list of words.

    Args:
        token (str): Any word to be tested.
        valid_words (list): List of valid words. Defaults to None.

    Returns:
        str/bool: The token if token is valid, False otherwise.
    """
    if not valid_words:
        return token

    if token in valid_words:
        return token

    return False


def is_acceptable(token):
    """Checks if token is acceptable against certain acceptability conditions.

    Args:
        token (str): Any word to be tested.

    Returns:
        str/bool: The token if token is acceptable, False otherwise.
    """
    if is_vowel(token[0]):
        if len(token) == 2 or (len(token) >= 3 and any(is_consonant(c) for c in token)):
            return token
    elif is_consonant(token[0]):
        if len(token) == 3 or (len(token) >= 4 and any(is_vowel(c) for c in token)):
            return token
    return False


def is_vowel(*substring):
    """Checks if a substring is a consonant.

    Args:
        *substring: Substrings to be tested.

    Returns:
        bool: True if substring is consonant, False otherwise.
    """
    return all(letter.lower() in VOWELS for letter in "".join(substring))


def is_consonant(*substring):
    """Checks if a substring is a consonant.

    Args:
        *substring: Substrings to be tested.

    Returns:
        bool: True if substring is consonant, False otherwise.
    """
    return all(letter.lower() in CONSONANTS for letter in "".join(substring))
