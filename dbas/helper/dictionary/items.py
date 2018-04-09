"""
Provides helping function for dictionaries, which are used for the radio buttons.

.. codeauthor: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import hashlib
import random
from typing import List

from dbas.lib import Relations
from dbas.handler import attacks
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, Issue, User
from dbas.handler.arguments import get_another_argument_with_same_conclusion
from dbas.handler.voting import add_seen_argument, add_seen_statement
from dbas.helper.url import UrlManager
from dbas.lib import get_all_attacking_arg_uids_from_history, is_author_of_statement, \
    is_author_of_argument
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_arguments_as_query
from dbas.review.helper.queues import is_statement_in_edit_queue, is_arguments_premise_in_edit_queue
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_relation_text_dict_with_substitution, get_jump_to_argument_text_list, \
    get_support_to_argument_text_list, nick_of_anonymous_user
from dbas.strings.translator import Translator


def shuffle_list_by_user(db_user: User, l: List) -> List:
    random.seed(int(hashlib.md5(str.encode(str(db_user.nickname))).hexdigest(), 16))
    return random.sample(l, len(l))


class ItemDictHelper(object):
    """
    Provides all functions for creating the radio buttons.
    """

    def __init__(self, lang, db_issue: Issue, path='', history=''):
        """
        Initialize default values

        :param lang: ui_locales
        :param db_issue Issue
        :param path: String
        :param history: String
        :return:
        """
        self.lang = lang
        self.db_issue = db_issue
        self.issue_read_only = db_issue.is_read_only
        limiter = '-' if len(history) > 0 else ''

        path = path.replace(db_issue.slug, '').replace('discuss', '').replace('api', '')
        while path.startswith('/'):
            path = path[1:]
        self.path = '{}{}/{}'.format(history, limiter, path)

    @staticmethod
    def get_empty_dict() -> dict:
        return {
            'elements': [],
            'extras': {'cropped_list': False}
        }

    def get_array_for_start(self, db_user: User) -> dict():
        """
        Prepares the dict with all items for the first step in discussion, where the user chooses a position.

        :param db_user: User
        :return:
        """
        logger('ItemDictHelper', 'def user: {}'.format(db_user.nickname))
        db_statements = DBDiscussionSession.query(Statement) \
            .filter(Statement.is_disabled == False,
                    Statement.is_position == True,
                    Statement.issue_uid == self.db_issue.uid).all()

        uids = [element.uid for element in db_statements if db_statements]
        slug = self.db_issue.slug

        statements_array = []
        _um = UrlManager(slug, history=self.path)

        for statement in db_statements:
            if statement.uid in uids:  # add seen by if the statement is visible
                add_seen_statement(statement.uid, db_user)
            statements_array.append(self.__create_answer_dict(statement.uid,
                                                              [{'title': statement.get_text(),
                                                                'id': statement.uid}],
                                                              'start',
                                                              _um.get_url_for_statement_attitude(statement.uid),
                                                              is_editable=not is_statement_in_edit_queue(statement.uid),
                                                              is_markable=True,
                                                              is_author=is_author_of_statement(db_user, statement.uid),
                                                              is_visible=statement.uid in uids))

        _tn = Translator(self.lang)

        shuffle_list_by_user(db_user, statements_array)

        if not self.issue_read_only:
            if db_user.nickname == nick_of_anonymous_user:
                statements_array.append(self.__create_answer_dict('login',
                                                                  [{'id': '0',
                                                                    'title': _tn.get(_.wantToStateNewPosition)}],
                                                                  'justify',
                                                                  'login'))
            else:
                title = _tn.get(_.newConclusionRadioButtonText) if len(db_statements) > 0 else _tn.get(
                    _.newConclusionRadioButtonTextNewIdea)
                statements_array.append(self.__create_answer_dict('start_statement',
                                                                  [{'title': title, 'id': 0}],
                                                                  'start',
                                                                  'add'))

        return {'elements': statements_array, 'extras': {'cropped_list': len(uids) < len(db_statements)}}

    def prepare_item_dict_for_attitude(self, statement_uid):
        """
        Prepares the dict with all items for the second step in discussion, where the user chooses her attitude.

        :param statement_uid: Statement.uid
        :return:
        """
        logger('ItemDictHelper', 'def')
        _tn = Translator(self.lang)

        slug = DBDiscussionSession.query(Issue).get(self.db_issue.uid).slug
        statements_array = []

        _um = UrlManager(slug, history=self.path)

        db_arguments = DBDiscussionSession.query(Argument).filter(Argument.conclusion_uid == statement_uid,
                                                                  Argument.is_supportive == True).all()
        uid = random.choice(db_arguments).uid if len(db_arguments) > 0 else 0

        title_t = _tn.get(_.iAgreeWithInColor) + '.'
        title_f = _tn.get(_.iDisagreeWithInColor) + '.'
        title_d = _tn.get(_.iHaveNoOpinionYetInColor) + '.'
        url_t = _um.get_url_for_justifying_statement(statement_uid, 'agree')
        url_f = _um.get_url_for_justifying_statement(statement_uid, 'disagree')
        url_d = _um.get_url_for_justifying_statement(uid, 'dontknow')
        d_t = self.__create_answer_dict('agree', [{'title': title_t, 'id': 'agree'}], 'agree', url_t)
        d_f = self.__create_answer_dict('disagree', [{'title': title_f, 'id': 'disagree'}], 'disagree', url_f)
        d_d = self.__create_answer_dict('dontknow', [{'title': title_d, 'id': 'dontknow'}], 'dontknow', url_d)
        statements_array.append(d_t)
        statements_array.append(d_f)
        statements_array.append(d_d)

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def get_array_for_justify_statement(self, db_statement: Statement, db_user: User, is_supportive: bool, history):
        """
        Prepares the dict with all items for the third step in discussion, where the user justifies his position.

        :param db_statement: Statement
        :param db_user: User
        :param is_supportive: Boolean
        :param history: history
        :return:
        """
        logger('ItemDictHelper', 'def')
        statements_array = []
        _tn = Translator(self.lang)
        slug = self.db_issue.slug
        db_arguments: List[Argument] = attacks.get_arguments_by_conclusion(db_statement.uid, is_supportive)
        uids: List[int] = [argument.uid for argument in db_arguments if db_arguments]

        _um = UrlManager(slug, history=self.path)

        for argument in db_arguments:
            if db_user and argument.uid in uids:  # add seen by if the statement is visible
                add_seen_argument(argument.uid, db_user)

            # get all premises in the premisegroup of this argument
            db_premises = DBDiscussionSession.query(Premise).filter_by(
                premisegroup_uid=argument.premisegroup_uid).all()
            premise_array = []
            for premise in db_premises:
                text = premise.get_text()
                premise_array.append({'title': text, 'id': premise.statement_uid})

            # filter forbidden attacks
            forbidden_attacks = attacks.get_forbidden_attacks_based_on_history(self.path)

            # get attack for each premise, so the urls will be unique
            arg_id_sys, attack = attacks.get_attack_for_argument(argument.uid, history=self.path,
                                                                 restrictive_arg_uids=forbidden_attacks)
            already_used = 'reaction/' + str(argument.uid) + '/' in self.path
            additional_text = '(' + _tn.get(_.youUsedThisEarlier) + ')'

            new_arg = None
            url = None
            if not attack:
                new_arg = get_another_argument_with_same_conclusion(argument.uid, history)
                if new_arg:
                    url = _um.get_url_for_support_each_other(argument.uid, new_arg.uid)

            if attack or new_arg is None or url is None:
                url = _um.get_url_for_reaction_on_argument(argument.uid, attack, arg_id_sys)

            statements_array.append(self.__create_answer_dict(str(argument.uid), premise_array, 'justify', url,
                                                              already_used=already_used,
                                                              already_used_text=additional_text,
                                                              is_editable=not is_arguments_premise_in_edit_queue(
                                                                  argument),
                                                              is_markable=True,
                                                              is_author=is_author_of_argument(db_user, argument.uid),
                                                              is_visible=argument.uid in uids,
                                                              attack_url=_um.get_url_for_jump(argument.uid)))

        shuffle_list_by_user(db_user, statements_array)

        if not self.issue_read_only:
            if db_user and db_user.nickname != nick_of_anonymous_user:
                statements_array.append(self.__create_answer_dict('start_premise',
                                                                  [{'title': _tn.get(_.newPremiseRadioButtonText),
                                                                    'id': 0}],
                                                                  'justify',
                                                                  'add'))
            else:
                statements_array.append(self.__create_answer_dict('login',
                                                                  [{'id': '0', 'title': _tn.get(_.onlyOneItem)}],
                                                                  'justify',
                                                                  'login'))

        return {'elements': statements_array, 'extras': {'cropped_list': len(uids) < len(db_arguments)}}

    def get_array_for_justify_argument(self, argument_uid, attack_type, db_user, history):
        """
        Prepares the dict with all items for a step in discussion, where the user justifies his attack she has done.

        :param argument_uid: Argument.uid
        :param attack_type: String
        :param db_user:
        :param history:
        :return:
        """
        logger('ItemDictHelper', 'def: arg {}, attack {}'.format(argument_uid, attack_type))
        statements_array = []
        _tn = Translator(self.lang)
        slug = self.db_issue.slug
        # description in docs: dbas/logic
        db_arguments = self.__get_arguments_based_on_attack(attack_type, argument_uid)
        uids = [argument.uid for argument in db_arguments if db_arguments]

        _um = UrlManager(slug, history=self.path)

        for argument in db_arguments:
            if db_user and db_user.nickname != nick_of_anonymous_user:  # add seen by if the statement is visible
                add_seen_argument(argument_uid, db_user)
            # get all premises in this group
            db_premises = DBDiscussionSession.query(Premise).filter_by(
                premisegroup_uid=argument.premisegroup_uid).all()
            premises_array = []
            for premise in db_premises:
                text = premise.get_text()
                premises_array.append({'id': premise.statement_uid,
                                       'title': text})

            # for each justifying premise, we need a new confrontation: (restriction is based on fix #38)
            is_undermine = Relations.UNDERMINE if attack_type == Relations.UNDERMINE else None
            attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)

            arg_id_sys, attack = attacks.get_attack_for_argument(argument.uid, last_attack=is_undermine,
                                                                 restrictive_arg_uids=attacking_arg_uids,
                                                                 history=self.path)
            the_other_one = True
            url = ''

            # with a chance of 50% or at the end we will seed the new "support step"
            if not attack:
                new_arg = get_another_argument_with_same_conclusion(argument.uid, history)
                the_other_one = new_arg is None
                if new_arg:
                    the_other_one = False
                    url = _um.get_url_for_support_each_other(argument.uid, new_arg.uid)

            if the_other_one:
                url = _um.get_url_for_reaction_on_argument(argument.uid, attack, arg_id_sys)

            statements_array.append(self.__create_answer_dict(argument.uid, premises_array, 'justify', url,
                                                              is_markable=True,
                                                              is_editable=not is_arguments_premise_in_edit_queue(
                                                                  argument),
                                                              is_author=is_author_of_argument(db_user, argument.uid),
                                                              is_visible=argument.uid in uids,
                                                              attack_url=_um.get_url_for_jump(argument.uid)))

        shuffle_list_by_user(db_user, statements_array)

        if not self.issue_read_only:
            if db_user and db_user.nickname != nick_of_anonymous_user:
                text = _tn.get(_.newPremiseRadioButtonText)
                if len(statements_array) == 0:
                    text = _tn.get(_.newPremiseRadioButtonTextAsFirstOne)
                a_dict = self.__create_answer_dict('justify_premise', [{'id': '0', 'title': text}], 'justify', 'add')
                statements_array.append(a_dict)

            else:
                # elif len(statements_array) == 1:
                a_dict = self.__create_answer_dict('login', [{'id': '0', 'title': _tn.get(_.onlyOneItem)}], 'justify',
                                                   'login')
                statements_array.append(a_dict)

        return {'elements': statements_array, 'extras': {'cropped_list': len(uids) < len(db_arguments)}}

    def __get_arguments_based_on_attack(self, attack_type, argument_uid):
        """
        Returns list of statements, which attack the argument by the given attack

        :param attack_type: String
        :param argument_uid: argument.uid
        :return: [Argument]
        """
        db_argument = get_not_disabled_arguments_as_query().filter_by(uid=argument_uid).first()

        db_arguments = []
        db_arguments_not_disabled = get_not_disabled_arguments_as_query()
        if attack_type == Relations.UNDERMINE:
            db_premises = DBDiscussionSession.query(Premise).filter_by(
                premisegroup_uid=db_argument.premisegroup_uid).all()
            for premise in db_premises:
                arguments = db_arguments_not_disabled.filter(Argument.conclusion_uid == premise.statement_uid,
                                                             Argument.is_supportive == False,
                                                             Argument.issue_uid == self.db_issue.uid).all()
                db_arguments = db_arguments + arguments

        elif attack_type == Relations.UNDERCUT:
            db_arguments = db_arguments_not_disabled.filter(Argument.argument_uid == argument_uid,
                                                            Argument.is_supportive == False,
                                                            Argument.issue_uid == self.db_issue.uid).all()

        elif attack_type == Relations.REBUT:
            db_arguments = db_arguments_not_disabled.filter(Argument.conclusion_uid == db_argument.conclusion_uid,
                                                            Argument.argument_uid == db_argument.argument_uid,
                                                            Argument.is_supportive == False,
                                                            Argument.issue_uid == self.db_issue.uid).all()

        elif attack_type == Relations.SUPPORT:
            db_arguments = db_arguments_not_disabled.filter(Argument.conclusion_uid == db_argument.conclusion_uid,
                                                            Argument.argument_uid == db_argument.argument_uid,
                                                            Argument.is_supportive == db_argument.is_supportive,
                                                            Argument.issue_uid == self.db_issue.uid).all()
        return db_arguments

    def get_array_for_dont_know_reaction(self, argument_uid, is_supportive, db_user, gender):
        """
        Prepares the dict with all items for the third step, where a supportive argument will be presented.

        :param argument_uid: Argument.uid
        :param is_supportive: Boolean
        :param db_user: User
        :param gender: m, f or n
        :return:
        """
        logger('ItemDictHelper', 'def')
        slug = self.db_issue.slug
        statements_array = []

        db_arguments = get_not_disabled_arguments_as_query()
        db_argument = db_arguments.filter_by(uid=argument_uid).first()
        if not db_argument:
            return {'elements': statements_array, 'extras': {'cropped_list': False}}

        # set real argument in history
        tmp_path = self.path.replace('/justify/{}/d'.format(db_argument.conclusion_uid),
                                     '/justify/{}/d'.format(argument_uid))
        _um = UrlManager(slug, history=tmp_path)

        if db_user and db_user.nickname != nick_of_anonymous_user:  # add seen by if the statement is visible
            add_seen_argument(argument_uid, db_user)

        rel_dict = get_relation_text_dict_with_substitution(self.lang, False, is_dont_know=True, gender=gender)
        current_mode = 'agree' if is_supportive else 'disagree'
        not_current_mode = 'disagree' if is_supportive else 'agree'

        relation = Relations.UNDERMINE
        url = self.__get_dont_know_item_for_undermine(db_argument, not_current_mode, _um)
        d = self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation,
                                      url)
        statements_array.append(d)

        relation = Relations.SUPPORT
        url = self.__get_dont_know_item_for_support(argument_uid, _um)
        d = self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation,
                                      url)
        statements_array.append(d)

        relation = Relations.UNDERCUT
        url = self.__get_dont_know_item_for_undercut(argument_uid, current_mode, _um)
        d = self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation,
                                      url)
        statements_array.append(d)

        relation = Relations.REBUT
        url = self.__get_dont_know_item_for_rebut(db_argument, not_current_mode, _um)
        d = self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation,
                                      url)
        statements_array.append(d)

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    @staticmethod
    def __get_dont_know_item_for_undermine(db_argument, is_not_supportive, _um):
        """
        Returns a random undermine url

        :param db_argument: Argument
        :param is_not_supportive: Boolean
        :param _um: UrlManager
        :return: String
        """
        if db_argument.conclusion_uid is not None:
            url = _um.get_url_for_justifying_statement(db_argument.conclusion_uid, is_not_supportive)
        else:
            url = _um.get_url_for_justifying_argument(db_argument.argument_uid, is_not_supportive, Relations.UNDERMINE)
        return url

    @staticmethod
    def __get_dont_know_item_for_support(argument_uid, _um):
        """
        Returns a random support url

        :param argument_uid: Argument.uid
        :param lang: Language.ui_locales
        :param _um: UrlManager
        :return: String
        """
        arg_id_sys, sys_attack = attacks.get_attack_for_argument(argument_uid)
        url = _um.get_url_for_reaction_on_argument(argument_uid, sys_attack, arg_id_sys)
        return url

    @staticmethod
    def __get_dont_know_item_for_undercut(argument_uid, current_mode, _um):
        """
        Returns a random undercut url

        :param argument_uid: Argument.uid
        :param current_mode: Boolean
        :param _um: UrlManager
        :return: String
        """
        url = _um.get_url_for_justifying_argument(argument_uid, current_mode, Relations.UNDERCUT)
        return url

    @staticmethod
    def __get_dont_know_item_for_rebut(db_argument, is_not_supportive, _um):
        """
        Returns a random rebut url

        :param db_argument: Argument
        :param is_not_supportive: Boolean
        :param _um: UrlManager
        :return: String
        """
        db_premises = DBDiscussionSession.query(Premise).filter_by(
            premisegroup_uid=db_argument.premisegroup_uid).all()
        if len(db_premises) == 1:
            url = _um.get_url_for_justifying_statement(db_premises[0].statement_uid, is_not_supportive)
        else:
            uids = [db_argument.premisegroup_uid]
            if db_argument.conclusion_uid is not None:
                url = _um.get_url_for_choosing_premisegroup(db_argument.is_supportive, db_argument.conclusion_uid, uids)
            else:
                url = _um.get_url_for_choosing_premisegroup(db_argument.is_supportive, db_argument.argument_uid, uids)
        return url

    def get_array_for_reaction(self, argument_uid_sys, argument_uid_user, is_supportive, attack, gender):
        """
        Prepares the dict with all items for the argumentation window.

        :param argument_uid_sys: Argument.uid
        :param argument_uid_user: Argument.uid
        :param is_supportive: Boolean
        :param attack: String
        :param gender: Gender of the author of the attack
        :return:
        """
        logger('ItemDictHelper', 'def')
        slug = self.db_issue.slug

        db_sys_argument = DBDiscussionSession.query(Argument).get(argument_uid_sys)
        db_user_argument = DBDiscussionSession.query(Argument).get(argument_uid_user)
        statements_array = []
        if not db_sys_argument or not db_user_argument:
            return {'elements': statements_array, 'extras': {'cropped_list': False}}

        rel_dict = get_relation_text_dict_with_substitution(self.lang, True, attack_type=attack, gender=gender)
        mode = 'agree' if is_supportive else 'disagree'
        _um = UrlManager(slug, history=self.path)

        relations = list(Relations)
        for relation in relations:
            url = self.__get_url_based_on_relation(relation, attack, _um, mode, db_user_argument, db_sys_argument)
            d = {'title': rel_dict[relation + '_text'], 'id': relation}
            tmp = self.__create_answer_dict(relation, [d], relation, url)
            statements_array.append(tmp)

        # last item is the change attack button or step back, if we have bno other attack
        attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)
        attacking_arg_uids.append(argument_uid_sys)
        arg_id_sys, new_attack = attacks.get_attack_for_argument(argument_uid_user,
                                                                 restrictive_arg_uids=attacking_arg_uids,
                                                                 history=self.path)

        if not new_attack:
            url = _um.get_last_valid_url_before_reaction()
            relation = 'step_back'
        else:
            relation = 'no_opinion'
            url = _um.get_url_for_reaction_on_argument(argument_uid_user, new_attack, arg_id_sys)
        statements_array.append(
            self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation,
                                      url))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def __get_url_based_on_relation(self, relation, attack, _um, mode, db_user_argument, db_sys_argument):
        """
        Returns a url based on the given relation

        :param relation: String
        :param attack: String
        :param _um: UrlManager
        :param mode: String
        :param db_user_argument: Argument.uid
        :param db_sys_argument: Argument.uid
        :return:
        """
        # special case, when the user selects the support, because this does not need to be justified!
        if relation == Relations.SUPPORT:
            return self.__get_url_for_support(attack, _um, db_user_argument, db_sys_argument)
        elif relation == Relations.UNDERMINE or relation == Relations.UNDERCUT:  # easy cases
            return self.__get_url_for_undermine(relation, _um, db_sys_argument.uid, mode)
        elif relation == Relations.REBUT:  # if we are having an rebut, everything seems different
            return self.__get_url_for_rebut(attack, _um, mode, db_user_argument, db_sys_argument)
        else:  # undercut
            return _um.get_url_for_justifying_argument(db_sys_argument.uid, mode, relation)

    def __get_url_for_support(self, attack, _um, db_user_argument, db_sys_argument):
        """
        Returns url to support an argument

        :param attack: String
        :param _um: UrlManager
        :param db_user_argument: Argument
        :param db_sys_argument: Argument
        :return: String
        """
        attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)
        restriction_on_attacks = Relations.REBUT if attack == Relations.UNDERCUT else None
        # if the user did rebutted A with B, the system shall not rebut B with A
        history = '{}/rebut/{}'.format(db_sys_argument.uid, db_user_argument.uid) if attack == Relations.REBUT else ''

        arg_id_sys, sys_attack = attacks.get_attack_for_argument(db_sys_argument.uid,
                                                                 restrictive_arg_uids=attacking_arg_uids,
                                                                 restrictive_attacks=[restriction_on_attacks],
                                                                 history=history)

        if sys_attack == Relations.REBUT and attack == Relations.UNDERCUT:
            # case: system makes an undercut and the user supports this new attack can be an rebut, so another
            # undercut for the users argument therefore now the users opinion is the new undercut (e.g. rebut)
            # because he supported it!
            url = _um.get_url_for_reaction_on_argument(arg_id_sys, sys_attack, db_sys_argument.argument_uid)
        else:
            url = _um.get_url_for_reaction_on_argument(db_sys_argument.uid, sys_attack, arg_id_sys)

        return url

    @staticmethod
    def __get_url_for_undermine(relation, _um, argument_uid_sys, mode):
        """
        Returns url to undermine an argument

        :param relation: String
        :param _um: UrlManager
        :param argument_uid_sys: Argument
        :param mode: String
        :return: String
        """
        return _um.get_url_for_justifying_argument(argument_uid_sys, mode, relation)

    @staticmethod
    def __get_url_for_rebut(attack, _um, mode, db_user_argument, db_sys_argument):
        """
        Returns url to rebut an argument

        :param attack: String
        :param _um: UrlManager
        :param mode: String
        :param db_user_argument: Argument
        :param db_sys_argument: Argument
        :return: String
        """
        url = ''
        if attack == Relations.UNDERMINE:  # rebutting an undermine will be a support for the initial argument
            url = _um.get_url_for_justifying_statement(db_sys_argument.conclusion_uid, mode)

        elif attack == Relations.UNDERCUT:  # rebutting an undercut will be a overbid for the initial argument
            if db_user_argument.argument_uid is None:
                url = _um.get_url_for_justifying_statement(db_user_argument.conclusion_uid, mode)
            else:
                db_premises = DBDiscussionSession.query(Premise).filter_by(
                    premisegroup_uid=db_user_argument.premisegroup_uid).all()
                db_premise = db_premises[random.randint(0, len(db_premises) - 1)]  # TODO: ELIMINATE RANDOM
                url = _um.get_url_for_justifying_statement(db_premise.statement_uid, mode)

        # rebutting an rebut will be a justify for the initial argument
        elif attack == Relations.REBUT:
            current_user_argument = db_user_argument
            conclusion_uid = current_user_argument.conclusion_uid
            while conclusion_uid is None:
                conclusion_uid = DBDiscussionSession.query(Argument).filter_by(
                    uid=current_user_argument.argument_uid).first().conclusion_uid
            uid = db_user_argument.conclusion_uid if conclusion_uid is None else conclusion_uid
            url = _um.get_url_for_justifying_statement(uid, mode)
        return url

    def get_array_for_choosing(self, argument_or_statement_id, pgroup_ids, is_argument, is_supportive, nickname):
        """
        Prepares the dict with all items for the choosing an premise, when the user inserted more than one new premise.

        :param argument_or_statement_id: Argument.uid or Statement.uid
        :param pgroup_ids: PremiseGroups.uid
        :param is_argument: Boolean
        :param is_supportive: Boolean
        :param nickname:
        :return: dict()
        """
        logger('ItemDictHelper', 'def')
        statements_array = []
        slug = self.db_issue.slug
        _um = UrlManager(slug, history=self.path)
        conclusion_uid = argument_or_statement_id if not is_argument else None
        argument_uid = argument_or_statement_id if is_argument else None
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        for group_id in pgroup_ids:
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=group_id).all()
            premise_array = []
            for premise in db_premises:
                text = premise.get_text()
                premise_array.append({'title': text, 'id': premise.statement_uid})
                if db_user and db_user.nickname != nick_of_anonymous_user:  # add seen by if the statement is visible
                    add_seen_statement(premise.statement_uid, db_user)

            # get attack for each premise, so the urls will be unique
            db_argument = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == group_id,
                                                                     Argument.is_supportive == is_supportive)
            if conclusion_uid and not is_argument:
                db_argument = db_argument.filter_by(conclusion_uid=conclusion_uid).first()
            else:
                db_argument = db_argument.filter_by(argument_uid=argument_uid).first()

            if not db_argument:
                print(group_id)
                return {'elements': statements_array, 'extras': {'cropped_list': False}}

            attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)
            arg_id_sys, attack = attacks.get_attack_for_argument(db_argument.uid,
                                                                 restrictive_arg_uids=attacking_arg_uids)
            url = _um.get_url_for_reaction_on_argument(db_argument.uid, attack, arg_id_sys)

            if is_argument:
                is_author = is_author_of_argument(db_user, argument_uid)
            else:
                is_author = is_author_of_statement(db_user, conclusion_uid)
            statements_array.append(self.__create_answer_dict(str(db_argument.uid), premise_array, 'choose', url,
                                                              is_markable=True, is_editable=True, is_author=is_author))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def get_array_for_jump(self, arg_uid, slug):
        """
        Returns a dictionary with elements, when the user jumps into the discussion

        :param arg_uid: Argument.uid
        :param slug: String
        :return: dict()
        """
        item_text = get_jump_to_argument_text_list(self.lang)
        url = self.__get_url_for_jump_array(slug, arg_uid)

        answers = list()
        for i in range(0, 5):
            if url[i]:
                answers.append({'text': item_text[i], 'url': url[i]})

        statements_array = []
        for no in range(0, len(answers)):
            arr = [{'title': answers[no]['text'], 'id': 0}]
            statements_array.append(self.__create_answer_dict('jump' + str(no), arr, 'jump', answers[no]['url']))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def get_array_for_support(self, arg_uid, slug):
        """
        Returns dict() for supporting an argument

        :param arg_uid: Argument.uid
        :param slug: String
        :return: dict()
        """
        item_text = get_support_to_argument_text_list(self.lang)
        url = self.__get_url_for_jump_array(slug, arg_uid)
        del url[3]  # remove step, where we could attack the premise
        url[1], url[3] = url[3], url[1]

        answers = list()
        for i in range(0, 4):
            if url[i]:
                answers.append({'text': item_text[i], 'url': url[i]})

        statements_array = []
        for no in range(0, len(answers)):
            arr = [{'title': answers[no]['text'], 'id': 0}]
            statements_array.append(self.__create_answer_dict('jump' + str(no), arr, 'jump', answers[no]['url']))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def __get_url_for_jump_array(self, slug, arg_uid):
        """
        Returns urls for the answers to jump to an argument

        :param slug: String
        :param arg_uid: Argument.uid
        :return: dict()
        """

        db_argument = DBDiscussionSession.query(Argument).get(arg_uid)
        _um = UrlManager(slug, history=self.path)
        db_premises = DBDiscussionSession.query(Premise).filter_by(
            premisegroup_uid=db_argument.premisegroup_uid).all()
        forbidden_attacks = attacks.get_forbidden_attacks_based_on_history(self.path)

        db_undercutted_arg = None
        len_undercut = 0
        if db_argument.argument_uid is not None:
            db_undercutted_arg = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)
            len_undercut = 1 if db_undercutted_arg.argument_uid is None else 2

        arg_id_sys, sys_attack = attacks.get_attack_for_argument(db_argument.uid, redirected_from_jump=True,
                                                                 restrictive_arg_uids=forbidden_attacks)
        url0 = _um.get_url_for_reaction_on_argument(db_argument.uid, sys_attack, arg_id_sys)

        if len_undercut == 0:
            url1 = _um.get_url_for_justifying_statement(db_argument.conclusion_uid, 'agree')
            url2 = _um.get_url_for_justifying_argument(db_argument.uid, 'agree', Relations.UNDERCUT)
            url3 = _um.get_url_for_justifying_statement(db_argument.conclusion_uid, 'disagree')
            if len(db_premises) == 1:
                url4 = _um.get_url_for_justifying_statement(db_premises[0].statement_uid, 'disagree')
            else:
                url4 = _um.get_url_for_justifying_argument(db_argument.uid, 'disagree', Relations.UNDERMINE)

        elif len_undercut == 1:
            url1 = None
            url2 = _um.get_url_for_justifying_argument(db_argument.uid, 'agree', Relations.UNDERCUT)
            url3 = _um.get_url_for_jump(db_undercutted_arg.uid)
            if len(db_premises) == 1:
                url4 = _um.get_url_for_justifying_statement(db_premises[0].statement_uid, 'disagree')
            else:
                url4 = _um.get_url_for_justifying_argument(db_argument.uid, 'disagree', Relations.UNDERMINE)

        else:
            url1 = None
            url2 = None
            url3 = _um.get_url_for_jump(db_undercutted_arg.uid)
            if len(db_premises) == 1:
                url4 = _um.get_url_for_justifying_statement(db_premises[0].statement_uid, 'disagree')
            else:
                url4 = _um.get_url_for_justifying_argument(db_argument.uid, 'disagree', Relations.UNDERMINE)

        return [url0, url1, url2, url3, url4]

    @staticmethod
    def __create_answer_dict(uid, premises, attitude, url, attack_url='', already_used=False, already_used_text='',
                             is_markable=False, is_editable=False, is_author=False, is_visible=True):
        """
        Return dictionary

        :param uid: Integer
        :param premises: Array of dict with title and id
        :param attitude: String
        :param url: String
        :param attack_url: String
        :param already_used: Boolean
        :param already_used_text: String
        :param is_markable: Boolean
        :param is_editable: Boolean
        :param is_author: Boolean
        :param is_visible: Boolean
        :return: dict()
        """
        # check punctuation
        for index, premise in enumerate(premises):
            if 'title' in premise and index == len(premises) - 1:
                premise['title'] += '.' if not premise['title'].endswith(('.', '?', '!')) else ''

        return {
            'id': 'item_' + str(uid),
            'premises': premises,
            'attitude': attitude,
            'url': url,
            'attack_url': attack_url,
            'already_used': already_used,
            'already_used_text': already_used_text,
            'is_markable': is_markable,
            'is_editable': is_editable,
            'is_deletable': is_author,
            'is_attackable': len(attack_url) > 0,
            'style': '' if is_visible else 'display: none;'
        }
