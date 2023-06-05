"""
This module provides utility functions for parsing and modifying strings.
These functions are particularly useful for working with strings that
contain placeholder keys denoted as '%key%'.

Functions:
    pkey_replace: Replaces placeholder keys in a string with corresponding values from a dictionary.
    substring_search: Searches for the next '%' symbol in a string, starting from a given index.
    extract_pkey_names: Extracts placeholder keys from a string.
    replace_matching_values: Replaces placeholders in a string with corresponding values from a dictionary.
    string_contains: Checks if a string contains any substrings from a provided list.

Note:
    This module is designed for use with strings that have placeholder keys denoted as '%key%'.
    It provides functionality to extract keys, replace keys with corresponding values,
    and to perform checks and searches on such strings.

Imported Libraries:
    None
"""

def pkey_replace(pkey_str: str, pkey_values: dict[str, str]) -> str:
    """
    Replace placeholder keys in a string with corresponding values from a dictionary.

    Args:
        pkey_str (str): The string with placeholders denoted as '%key%'.
        pkey_values (dict[str, str]): Dictionary \
            containing keys and corresponding values to replace in pkey_str.

    Returns:
        str: The modified string with placeholders replaced by their corresponding values.
    """
    keys = extract_pkey_names(pkey_str)
    return replace_matching_values(pkey_str, keys, pkey_values)


def substring_search(pkey_str: str, start_index: int) -> tuple[str, int]:
    """
    Search for the next '%' symbol in the string, starting from a given index.

    Args:
        pkey_str (str): The string to search.
        start_index (int): The index from where to start the search.

    Returns:
        tuple[str, int]: A tuple containing the substring from\
            start_index to the next '%' symbol, and the index of that symbol.

    Raises:
        KeyError: If there are two '%' symbols without a value in between.
        IndexError: If there is an unclosed '%' symbol in the string.
    """
    for sub_index, sub_char in enumerate(pkey_str[start_index:], start_index):
        if sub_char == "%" and sub_index == start_index:
            raise KeyError(
                'Template path can\'t have two "%" without a value in between'
            )

        if sub_char == "%":
            return (pkey_str[start_index:sub_index], sub_index)

    raise IndexError('Unclosed "%" symbol in template path')


def extract_pkey_names(pkey_str: str) -> list[str]:
    """
    Extract placeholders in the form of '%key%' from a string.

    Args:
        pkey_str (str): The string to extract placeholders from.

    Returns:
        list[str]: A list containing the extracted keys without the '%' symbols.
    """
    matches: list[str] = []
    memo: int = -1  # This is used for optimizing the for loop, python loops suck!
    for index, char in enumerate(pkey_str):
        if index <= memo:
            continue

        if char != "%":
            continue

        match, memo = substring_search(pkey_str, index + 1)
        matches.append(match)

    return matches


def replace_matching_values(
    pkey_str: str, pkey_keys: list[str], pkey_values: dict[str, str]
) -> str:
    """
    Replace placeholders in a string with corresponding values from a dictionary.

    Args:
        pkey_str (str): The string containing placeholders denoted as '%key%'.
        pkey_keys (list[str]): List of keys to replace in the string.
        pkey_values (dict[str, str]): Dictionary containing keys and\
            corresponding values to replace in pkey_str.

    Returns:
        str: The modified string with placeholders replaced by their corresponding values.
    """
    rendered_string = pkey_str
    for key in pkey_keys:
        pkey = f"%{key}%"
        value = pkey_values[key]

        rendered_string = rendered_string.replace(pkey, value)

    return rendered_string

def string_contains(substr_list: list[str], main_string: str) -> bool:
    """
    Checks if the main string contains any substring from the provided list.

    Args:
        substr_list (list[str]): List of substrings to search for.
        main_string (str): The string in which to search for the substrings.

    Returns:
        bool: True if any substring is found in the main string, False otherwise.
    """
    return any(substr in main_string for substr in substr_list)
