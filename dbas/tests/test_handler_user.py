import unittest

# this has to be used from dbas.handler import user


class UserHandlerTests(unittest.TestCase):

    def test_update_last_action(self):
        # TODO
        # this has to be used update_last_action(nick)
        return True

    def test_refresh_public_nickname(self):
        # TODO
        # this has to be used refresh_public_nickname(user)
        return True

    def test_is_in_group(self):
        # TODO
        # this has to be used is_in_group(nickname, groupname)
        return True

    def test_is_admin(self):
        # TODO
        # this has to be used is_admin(nickname)
        return True

    def test_get_public_data(self):
        # TODO
        # this has to be used get_public_data(nickname, lang)
        return True

    def test_get_reviews_of(self):
        # TODO
        # this has to be used get_reviews_of(user, only_today)
        return True

    def test_get_count_of_statements(self):
        # TODO
        # this has to be used get_count_of_statements(user, only_edits, limit_on_today=False)
        return True

    def test_get_count_of_votes_of_user(self):
        # TODO
        # this has to be used get_count_of_votes_of_user(user, limit_on_today=False)
        return True

    def test_get_count_of_clicks(self):
        # TODO
        # this has to be used get_count_of_clicks(user, limit_on_today=False)
        return True

    def test_get_textversions(self):
        # TODO
        # this has to be used get_textversions(public_nickname, lang, timestamp_after=None, timestamp_before=None)
        return True

    def test_get_marked_elements_of_user(self):
        # TODO
        # this has to be used get_marked_elements_of_user(user, is_argument, lang)
        return True

    def test_get_arg_clicks_of_user(self):
        # TODO
        # this has to be used get_arg_clicks_of_user(user, lang)
        return True

    def test_get_stmt_clicks_of_user(self):
        # TODO
        # this has to be used get_stmt_clicks_of_user(user, lang)
        return True

    def test_get_clicks_of_user(self):
        # TODO
        # this has to be used get_clicks_of_user(user, is_argument, lang)
        return True

    def test_get_information_of(self):
        # TODO
        # this has to be used get_information_of(db_user, lang)
        return True

    def test_get_summary_of_today(self):
        # TODO
        # this has to be used get_summary_of_today(nickname, lang)
        return True

    def test_change_password(self):
        # TODO
        # this has to be used change_password(user, old_pw, new_pw, confirm_pw, lang)
        return True

    def test_set_new_user(self):
        # TODO
        # this has to be used set_new_user(mailer, firstname, lastname, nickname, gender, email, password, _tn)
        return True

    def test_set_new_oauth_user(self):
        # TODO
        # this has to be used set_new_oauth_user(firstname, lastname, nickname, email, gender, password, id, provider, _tn)
        return True

    def test_get_users_with_same_opinion(self):
        # TODO
        # this has to be used get_users_with_same_opinion(uids, application_url, path, nickname, is_argument, is_attitude, is_reaction, is_position, ui_locales)
        return True
