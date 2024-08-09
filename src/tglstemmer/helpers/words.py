import os


script_dir = os.path.dirname(os.path.realpath(__file__))


def get_words(file_path=os.path.join(script_dir, "../resources/tgl_wordlist.txt")):
    """Get list of words from a Tagalog word list txt file.

    Args:
            file_path (str, optional): Path to the Tagalog word lsit txt file. Defaults to '<script_dir>/../resources/tgl_wordlist.txt'.
    Returns:
            list: A list of words.
    """
    with open(file_path) as in_file:
        return [word.strip().lower() for word in in_file.readlines()]
