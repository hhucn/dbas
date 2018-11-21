def start_with_capital(some_string: str) -> str:
    """
    Just capitalize the first letter

    :param some_string: just any string you want
    :return: the same string, but with capitalized first letter
    """
    if len(some_string) > 0:
        return some_string[0:1].upper() + some_string[1:]
    return some_string


def start_with_small(some_string: str) -> str:
    """
    Just first letter in small

    :param some_string: just any string you want
    :return: the same string, but with a small first letter
    """
    if len(some_string) > 0:
        return some_string[0:1].lower() + some_string[1:]
    return some_string


def replace_multiple_chars(target: str, to_be_replace: list, to_be_filled_in: str) -> str:
    """
    This method can be used to replaces multiple chars in a string by some other char.

    :param target: The target string which should be changed
    :param to_be_replace: A list oft chars or word that should be searched in target
    :param to_be_filled_in: A char or word that should be filled in if to_be_replaces is found in target
    :return:
    """
    for elem in to_be_replace:
        if elem in target:
            target = target.replace(elem, to_be_filled_in)

    return target
