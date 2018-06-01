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
