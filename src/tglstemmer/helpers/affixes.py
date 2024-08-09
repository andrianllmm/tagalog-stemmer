import os


script_dir = os.path.dirname(os.path.realpath(__file__))


def get_affixes(type, folder_path=os.path.join(script_dir, "../resources/affixes/")):
    """Get list of affixes from file.

    Args:
            type (str): Type of affixes to get. Value can only be:
                    - 'pre': Prefixes
                    - 'in': Infixes
                    - 'suf': Suffixes
            folder_path (str, optional): Path to the folder containing .txt files of Tagalog affixes.

    Returns:
            list: A list of affixes of chosen type.
    """
    with open(os.path.join(folder_path, f"{type}fixes.txt")) as in_file:
        return sorted([affix.strip() for affix in in_file.readlines()], key=len)


PREFIXES = get_affixes("pre")
INFIXES = get_affixes("in")
SUFFIXES = get_affixes("suf")
