"""
Managing URLS can be done with a very hardcoded scheme. We are differentiating between several steps in the discussion:

* Staring discussion
* Getting attitude for the first position
* Justifying the first position with an premisegroup
* Getting confronted because the user clicked his first statement
* Justify the reaction due to the confrontation
* Choose an point for the discussion, when two or more statements we entered

Next to this we have a 404 page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import random

from dbas import recommender_system as RecommenderSystem
from dbas.lib import get_all_attacking_arg_uids_from_history


class UrlManager(object):
    """
    URL-Manager for building all URLs. This includes DBAS-URLs as well as the API-URLs
    """

    def __init__(self, application_url, slug='', for_api=False, history=''):
        """
        Initialization of an URL-Manager

        :param application_url: self.request.application_url
        :param slug: slugged issue.title
        :param for_api: Boolean
        :param history: String
        :return: None
        """
        # logger('UrlManager', '__init__',
        #        'application_url: ' + application_url + ', slug: ' + slug + ', for_api: ' + str(
        #            for_api) + ', history: ' + str(history))
        self.url = application_url + ('' if application_url.endswith('/') else '/')
        self.discussion_url = self.url + 'discuss/'
        self.review_url = self.url + 'review/'
        self.api_url = 'api/'
        self.slug = slug
        self.for_api = for_api
        self.history = history

    def get_url(self, path):
        """
        Returns current url with self.url as prefix or the API-version

        :param path: String
        :return:
        """
        return path if self.for_api else self.url + path

    def get_404(self, params, is_param_error=False, revoked_content=False):
        """
        Returns the 404 page or the API-version

        :param params: self.request.params
        :param is_param_error: boolean
        :param revoked_content: boolean
        :return: 404/params1/param2/
        """
        url = self.url + '404'
        for p in params:
            if p != '':
                url += '/' + str(p)
        params = '&' if '?' in url else '?'
        params += 'param_error=true' if is_param_error else ''
        params += 'revoked_content=true' if revoked_content else ''
        url += params if len(params) > 5 else ''
        return url

    def get_slug_url(self, as_location_href):
        """
        Returns url for starting a discussions

        :param as_location_href: Boolean
        :return: discussion_url/slug
        """
        url = self.slug
        return self.__return_discussion_url(as_location_href, url)

    def get_review_url(self, as_location_href):
        """
        Returns url for reviewing a discussions

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :return: review_url/slug
        """
        url = self.slug
        return self.__return_review_url(as_location_href, url)

    def get_url_for_statement_attitude(self, as_location_href, statement_uid):
        """
        Returns url for getting statement attitude of the user or the API-version

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param statement_uid: Statement.uid
        :return: discussion_url/slug/attitude/statement_uid
        """
        url = '{}/attitude/{}'.format(self.slug, statement_uid)
        return self.__return_discussion_url(as_location_href, url)

    def get_url_for_justifying_statement(self, as_location_href, statement_uid, mode):
        """
        Returns url for getting statement justification of the user or the API-version

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :type as_location_href: Boolean
        :param statement_uid: Statement.uid
        :param mode:
        :type mode: String
        :return: discuss/{slug}/justify/{statement_or_arg_id}/{mode}
        """
        url = '{}/justify/{}/{}'.format(self.slug, statement_uid, mode)
        return self.__return_discussion_url(as_location_href, url)

    def get_url_for_justifying_argument(self, as_location_href, argument_uid, mode, attitude, additional_id=-1):
        """
        Returns url for justifying an argument of the user or the API-version

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param argument_uid: Argument.uid
        :param mode: String
        :param attitude: String
        :param additional_id: String
        :return: discuss/{slug}/justify/{statement_or_arg_id}/{mode}*attitude
        """
        url = '{}/justify/{}/{}/{}'.format(self.slug, argument_uid, mode, attitude)
        if additional_id != -1:
            url += '/{}'.format(additional_id)
        return self.__return_discussion_url(as_location_href, url)

    def get_url_for_reaction_on_argument(self, as_location_href, argument_uid, mode, confrontation_argument):
        """
        Returns url for getting the reaction regarding an argument of the user or the API-version

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param argument_uid: Argument.uid
        :param mode: 't' on supportive, 'f' otherwise
        :param confrontation_argument: Argument.uid
        :return: discuss/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys
        """
        url = '{}/reaction/{}/{}/{}'.format(self.slug, argument_uid, mode, confrontation_argument)
        return self.__return_discussion_url(as_location_href, url)

    def get_url_for_choosing_premisegroup(self, as_location_href, is_argument, is_supportive, statement_or_argument_id,
                                          pgroup_id_list):
        """
        Returns url for choosing between various pgroups

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param is_argument: Boolean
        :param is_supportive: Boolean
        :param statement_or_argument_id: Statement.uid or Argument.uid
        :param pgroup_id_list: [int]
        :return: discuss/{slug}/choose/{p1}/{p2}/...
        """
        is_arg = 't' if is_argument else 'f'
        is_sup = 't' if is_supportive else 'f'
        pgroups = ''
        if len(pgroup_id_list) > 0:
            pgroups = '/' + '/'.join(str(x) for x in pgroup_id_list)
        url = '{}/choose/{}/{}/{}{}'.format(self.slug, is_arg, is_sup, statement_or_argument_id, pgroups)
        return self.__return_discussion_url(as_location_href, url)

    def get_url_for_jump(self, as_location_href, argument_uid):
        """
        Return url for the jump step in the discussion

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param argument_uid: Argument.uid
        :return: discuss/{slug}/jump/{argument_uid}
        """
        url = '{}/jump/{}'.format(self.slug, argument_uid)
        return self.__return_discussion_url(as_location_href, url)

    def get_url_for_support_each_other(self, as_location_href, argument_uid_user, argument_uid_system):
        """
        Returns url for supporting another argument with the same conclusion

        :param as_location_href: Boolean
        :param argument_uid_user: Argument.uid
        :param argument_uid_system: Argument.uid
        :return: discuss/{slug}/support/{argument_uid1}/{argument_uid2}
        """
        url = '{}/support/{}/{}'.format(self.slug, argument_uid_user, argument_uid_system)
        return self.__return_discussion_url(as_location_href, url)

    def get_last_valid_url_before_reaction(self, as_location_href):
        """
        Parses the last valid step from the discussion before the last reaction step in history

        :param as_location_href: Boolean
        :return: String
        """
        splitted_history, last_valid_step = self.__cut_history()
        self.history = '-'.join(splitted_history)

        if last_valid_step.startswith('/'):
            last_valid_step = last_valid_step[1:]

        if len(self.slug) > 0 and self.slug not in (self.api_url if self.for_api else self.discussion_url):
            last_valid_step = '{}/{}'.format(self.slug, last_valid_step)

        return self.__return_discussion_url(as_location_href, last_valid_step)

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

    def __return_discussion_url(self, as_location_href, url):
        """
        Puts everything togeter

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param url: String
        :return: Valid URL
        """
        history = '?history=' + self.history if self.history and len(self.history) > 1 else ''

        if self.for_api:
            return '{}{}{}'.format(self.api_url, url, history)
        else:
            prefix = 'location.href="' if as_location_href else ''
            suffix = '"' if as_location_href else ''
            return prefix + self.discussion_url + url + history + suffix

    def __return_review_url(self, as_location_href, url):
        """
        Returns some review url

        :param as_location_href: Set to True if you want to change the location using 'location.href'
        :type as_location_href: boolean
        :param url: String
        :return: Valid URL
        """
        prefix = 'location.href="' if as_location_href else ''
        suffix = '"' if as_location_href else ''
        return prefix + self.review_url + url + suffix


def get_url_for_new_argument(new_argument_uids, history, lang, url_manager):
    """
    Returns url for the reaction on a new argument

    :param new_argument_uids: Argument.uid
    :param history: String
    :param lang: Language.ui_locales
    :param url_manager: UrlManager
    :return: String
    """
    new_argument_uid = random.choice(new_argument_uids)  # TODO eliminate random
    attacking_arg_uids = get_all_attacking_arg_uids_from_history(history)
    arg_id_sys, attack = RecommenderSystem.get_attack_for_argument(new_argument_uid, lang, restriction_on_args=attacking_arg_uids)
    if arg_id_sys == 0:
        attack = 'end'
    url = url_manager.get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
    return url
