def get_oauth_ret_dict(user_data: dict = None, missing_data: list = None, error_str: str = '') -> dict:
    """
    Creates the return dict of the oauth module

    :param user_data: dict of user data that could be fetched via oauth
    :param missing_data: list of user data that is still missing after using oauth
    :param error_str: just a string with error message
    :return:
    """
    if not user_data:
        user_data = {}
    if not missing_data:
        missing_data = []

    return {
        'user': user_data,
        'missing': missing_data,
        'error_str': error_str
    }
