from ..stem import Stem


def replace_letter(token, index, letter):
    """Replaces a letter in a token.

    Args:
            token (str): Word to be updated.
            index (int): Index of the letter to be replaced.
            letter (str): Letter used to replace.

    Returns:
            str: The updated word.
    """
    token_as_list = list(token)

    token_as_list[index] = letter

    return Stem("".join(token_as_list), **token.__dict__)


def swap_letters(token, index1, index2):
    """Swaps two letters in a token.

    Args:
            token (str): Word to be updated.
            index1 (int): Index of the first letter to be swapped.
            index2 (int): Index of the second letter to be swapped.

    Returns:
            str: The updated word.
    """
    token_as_list = list(token)

    index1_letter = token_as_list[index1]
    token_as_list[index1] = token_as_list[index2]
    token_as_list[index2] = index1_letter

    return Stem("".join(token_as_list), **token.__dict__)
