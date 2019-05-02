"""
Managing URLS can be done with a very hardcoded scheme. We are differentiating between several steps in the discussion.
"""
import random

from dbas.database.discussion_model import Statement, Issue
from dbas.handler import attacks
from dbas.lib import get_all_attacking_arg_uids_from_history, Attitudes, Relations


class UrlManager(object):
    """
    URL-Manager for building all URLs. This includes DBAS-URLs as well as the API-URLs
    """

    def __init__(self, slug='', history=''):
        """
        Initialization of an URL-Manager

        :param application_url: self.request.application_url
        :param slug: slugged issue.title
        :param history: String
        :return: None
        """
        self.review_url = 'review/'
        self.slug = slug
        self.history = history

    def get_review_url(self):
        """
        Returns url for reviewing a discussions

        :return: review_url/slug
        """
        return self.review_url + self.slug

    def get_url_for_statement_attitude(self, statement_uid: int):
        """
        Returns url for getting statement attitude of the user or the API-version

        :param statement_uid: Statement.uid
        :return: discussion_url/slug/attitude/statement_uid
        """
        url = '{}/attitude/{}'.format(self.slug, statement_uid)
        return self.__return_discussion_url(url)

    def get_url_for_justifying_statement(self, statement_uid: int, attitude: Attitudes):
        """
        Returns url for getting statement justification of the user or the API-version

        :param statement_uid: Statement.uid
        :param attitude:
        :return: discuss/{slug}/justify/{statement_or_arg_id}/{mode}
        """
        url = '{}/justify/{}/{}'.format(self.slug, statement_uid, attitude)
        return self.__return_discussion_url(url)

    def get_url_for_justifying_argument(self, argument_uid: int, attitude: Attitudes, relation: Relations,
                                        additional_id: int = -1):
        """
        Returns url for justifying an argument of the user or the API-version

        :param argument_uid: Argument.uid
        :param attitude: String
        :param relation: String
        :param additional_id: String
        :return: discuss/{slug}/justify/{statement_or_arg_id}/{mode}*attitude
        """
        url = '{}/justify/{}/{}/{}'.format(self.slug, argument_uid, attitude, relation)
        if additional_id != -1:
            url += '/{}'.format(additional_id)
        return self.__return_discussion_url(url)

    def get_url_for_reaction_on_argument(self, argument_uid: int, relation: Relations, confrontation_argument: int):
        """
        Returns url for getting the reaction regarding an argument of the user or the API-version

        :param argument_uid: Argument.uid
        :param relation:
        :param confrontation_argument: Argument.uid
        :return: discuss/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys
        """
        if not confrontation_argument:
            return self.get_url_for_discussion_finish(argument_uid)
        url = '{}/reaction/{}/{}/{}'.format(self.slug, argument_uid, relation, confrontation_argument)
        return self.__return_discussion_url(url)

    def get_url_for_choosing_premisegroup(self, pgroup_id_list: [int]) -> str:
        """
        Returns url for choosing between various pgroups

        :param pgroup_id_list: [int]
        :return: discuss/{slug}/choose/{p1}/{p2}/...
        """
        url = '{}/choose/{}'.format(self.slug, '/'.join(str(x) for x in pgroup_id_list))
        return self.__return_discussion_url(url)

    def get_url_for_jump(self, argument_uid):
        """
        Return url for the jump step in the discussion

        :param argument_uid: Argument.uid
        :return: {slug}/jump/{argument_uid}
        """
        url = '{}/jump/{}'.format(self.slug, argument_uid)
        return self.__return_discussion_url(url)

    def get_url_for_support_each_other(self, argument_uid_user, argument_uid_system):
        """
        Returns url for supporting another argument with the same conclusion
        :param argument_uid_user: Argument.uid
        :param argument_uid_system: Argument.uid
        :return: discuss/{slug}/support/{argument_uid1}/{argument_uid2}
        """
        url = '{}/support/{}/{}'.format(self.slug, argument_uid_user, argument_uid_system)
        return self.__return_discussion_url(url)

    def get_last_valid_url_before_reaction(self):
        """
        Parses the last valid step from the discussion before the last reaction step in history

        :return: String
        """
        splitted_history, last_valid_step = self.__cut_history()
        self.history = '-'.join(splitted_history)

        if last_valid_step.startswith('/'):
            last_valid_step = last_valid_step[1:]

        if len(self.slug) > 0:
            last_valid_step = '{}/{}'.format(self.slug, last_valid_step)

        return self.__return_discussion_url(last_valid_step)

    def get_url_for_new_argument(self, new_argument_uids: list) -> str:
        """
        Returns url for the reaction on a new argument

        :param new_argument_uids: List of Argument.uid
        :return: String
        """
        new_argument_uid = random.choice(new_argument_uids)  # TODO eliminate random
        attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.history)
        arg_id_sys, attack = attacks.get_attack_for_argument(new_argument_uid,
                                                             restrictive_arg_uids=attacking_arg_uids)
        if not arg_id_sys:
            url = self.get_url_for_discussion_finish(new_argument_uid)
        else:
            url = self.get_url_for_reaction_on_argument(new_argument_uid, attack, arg_id_sys)
        return url

    def __cut_history(self):
        """
        Realigns the history

        :return:
        """
        splitted_history = self.history.split('-')
        # get last valid step
        last_valid_step = ''
        for history in splitted_history:
            if 'reaction' not in history:
                last_valid_step = history

        # cut history
        if len(last_valid_step) > 0:
            try:
                splitted_history = splitted_history[:splitted_history.index(last_valid_step)]
            except ValueError:
                c = len(splitted_history)
                for index, step in enumerate, splitted_history:
                    if last_valid_step in step:
                        c = index
                splitted_history = splitted_history[:c]
        return splitted_history, last_valid_step

    def __return_discussion_url(self, url):
        """
        Puts everything together

        :param url: String
        :return: Valid URL
        """
        history = '?history=' + self.history if self.history and len(self.history) > 1 else ''
        return '/{}{}'.format(url, history)

    def get_url_for_discussion_finish(self, arg_uid):
        """

        :param arg_uid:
        :return:
        """
        url = '{}/finish/{}'.format(self.slug, arg_uid)
        return self.__return_discussion_url(url)


def url_to_statement(issue: Issue, statement: Statement, agree: bool = True) -> str:
    """
    Generate URL to given statement_uid in specific issue (by slug).
    Used to directly jump into the discussion.
    """
    if isinstance(agree, str):
        if agree == "true":
            mode = "agree"
        else:
            mode = "disagree"
    else:
        mode = "agree" if agree is True else "disagree"
    url_manager = UrlManager(slug=issue.slug)
    return "/api" + url_manager.get_url_for_justifying_statement(statement.uid, mode)
