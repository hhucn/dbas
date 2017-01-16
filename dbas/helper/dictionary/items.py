"""
Provides helping function for dictionaries, which are used for the radio buttons.

.. codeauthor: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

import dbas.recommender_system as rs
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, Issue, User
from dbas.lib import get_text_for_statement_uid, get_all_attacking_arg_uids_from_history, is_author_of_statement, is_author_of_argument
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_statement_as_query, get_not_disabled_arguments_as_query
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_relation_text_dict_with_substitution, get_jump_to_argument_text_list
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager
from dbas.helper.voting import add_seen_argument, add_seen_statement
from sqlalchemy import and_


class ItemDictHelper(object):
    """
    Provides all functions for creating the radio buttons.
    """

    def __init__(self, lang, issue_uid, application_url, for_api=False, path='', history=''):
        """
        Initialize default values

        :param lang: ui_locales
        :param issue_uid: Issue.uid
        :param application_url: application_url
        :param for_api: boolean
        :param path: String
        :param history: String
        :return:
        """
        self.lang = lang
        self.issue_uid = issue_uid
        self.application_url = application_url
        self.for_api = for_api
        if for_api:
            self.path = path[len('/api/' + DBDiscussionSession.query(Issue).get(issue_uid).get_slug()):]
        else:
            self.path = path[len('/discuss/' + DBDiscussionSession.query(Issue).get(issue_uid).get_slug()):]
        if len(history) > 0:
            self.path = history + '-' + self.path

    def get_array_for_start(self, nickname):
        """
        Prepares the dict with all items for the first step in discussion, where the user chooses a position.

        :param nickname: Boolean or String
        :return:
        """
        logger('ItemDictHelper', 'get_array_for_start', 'def user: ' + str(nickname))
        db_statements = get_not_disabled_statement_as_query()
        db_statements = db_statements.filter(and_(Statement.is_startpoint == True,
                                                  Statement.issue_uid == self.issue_uid)).all()

        uids = rs.get_uids_of_best_positions(db_statements)  # TODO # 166
        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()

        statements_array = []
        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        for statement in db_statements:
            if db_user and statement.uid in uids:  # add seen by if the statement is visible
                add_seen_statement(statement.uid, db_user.uid)
            statements_array.append(self.__create_answer_dict(statement.uid,
                                                              [{'title': get_text_for_statement_uid(statement.uid),
                                                                  'id': statement.uid}],
                                                              'start',
                                                              _um.get_url_for_statement_attitude(True, statement.uid),
                                                              is_flagable=True,
                                                              is_author=is_author_of_statement(nickname, statement.uid),
                                                              is_visible=statement.uid in uids))

        _tn = Translator(self.lang)
        if nickname:
            title = _tn.get(_.newConclusionRadioButtonText) if len(db_statements) > 0 else _tn.get(_.newConclusionRadioButtonTextNewIdea)
            statements_array.append(self.__create_answer_dict('start_statement',
                                                              [{'title': title, 'id': 0}],
                                                              'start',
                                                              'add'))
        else:
            statements_array.append(self.__create_answer_dict('login',
                                                              [{'id': '0', 'title': _tn.get(_.wantToStateNewPosition)}],
                                                              'justify',
                                                              'login'))

        return {'elements': statements_array, 'extras': {'cropped_list': len(uids) < len(db_statements)}}

    def prepare_item_dict_for_attitude(self, statement_uid):
        """
        Prepares the dict with all items for the second step in discussion, where the user chooses her attitude.

        :param statement_uid: Statement.uid
        :return:
        """
        logger('ItemDictHelper', 'prepare_item_dict_for_attitude', 'def')
        _tn = Translator(self.lang)

        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()
        # text = get_text_for_statement_uid(statement_uid)
        statements_array = []

        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)

        # colon = ' ' if self.lang == 'de' else ': '
        titleT = _tn.get(_.iAgreeWithInColor) + '.'  # + colon + text
        titleF = _tn.get(_.iDisagreeWithInColor) + '.'  # + colon + text
        titleD = _tn.get(_.iHaveNoOpinionYetInColor) + '.'  # + colon + text
        urlT = _um.get_url_for_justifying_statement(True, statement_uid, 't')
        urlF = _um.get_url_for_justifying_statement(True, statement_uid, 'f')
        urlD = _um.get_url_for_justifying_statement(True, statement_uid, 'd')
        statements_array.append(self.__create_answer_dict('agree', [{'title': titleT, 'id': 'agree'}], 'agree', urlT))
        statements_array.append(self.__create_answer_dict('disagree', [{'title': titleF, 'id': 'disagree'}], 'disagree', urlF))
        statements_array.append(self.__create_answer_dict('dontknow', [{'title': titleD, 'id': 'dontknow'}], 'dontknow', urlD))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def get_array_for_justify_statement(self, statement_uid, nickname, is_supportive):
        """
        Prepares the dict with all items for the third step in discussion, where the user justifies his position.

        :param statement_uid: Statement.uid
        :param nickname: User.nickname
        :param is_supportive: Boolean
        :return:
        """
        logger('ItemDictHelper', 'get_array_for_justify_statement', 'def')
        statements_array = []
        _tn = Translator(self.lang)
        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()
        db_arguments = rs.get_arguments_by_conclusion(statement_uid, is_supportive)
        uids = rs.get_uids_of_best_statements_for_justify_position(db_arguments)  # TODO # 166

        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        for argument in db_arguments:
                if db_user and argument.uid in uids:  # add seen by if the statement is visible
                    add_seen_argument(argument.uid, db_user.uid)

                # get all premises in the premisegroup of this argument
                db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
                premise_array = []
                for premise in db_premises:
                    text = get_text_for_statement_uid(premise.statement_uid)
                    premise_array.append({'title': text, 'id': premise.statement_uid})

                # get attack for each premise, so the urls will be unique
                arg_id_sys, attack = rs.get_attack_for_argument(argument.uid, self.lang, history=self.path)
                already_used = 'reaction/' + str(argument.uid) + '/' in self.path
                additional_text = '(' + _tn.get(_.youUsedThisEarlier) + ')'
                statements_array.append(self.__create_answer_dict(str(argument.uid),
                                                                  premise_array,
                                                                  'justify',
                                                                  _um.get_url_for_reaction_on_argument(True, argument.uid,
                                                                                                       attack, arg_id_sys),
                                                                  already_used=already_used,
                                                                  already_used_text=additional_text,
                                                                  is_flagable=True,
                                                                  is_author=is_author_of_argument(nickname, argument.uid),
                                                                  is_visible=argument.uid in uids))

        if nickname:
            statements_array.append(self.__create_answer_dict('start_premise',
                                                              [{'title': _tn.get(_.newPremiseRadioButtonText),
                                                                'id': 0}],
                                                              'justify',
                                                              'add'))
        else:
            statements_array.append(
                self.__create_answer_dict('login', [{'id': '0', 'title': _tn.get(_.onlyOneItem)}], 'justify', 'login'))

        return {'elements': statements_array, 'extras': {'cropped_list': len(uids) < len(db_arguments)}}

    def get_array_for_justify_argument(self, argument_uid, attack_type, logged_in, nickname):
        """
        Prepares the dict with all items for a step in discussion, where the user justifies his attack she has done.

        :param argument_uid: Argument.uid
        :param attack_type: String
        :param logged_in: String
        :param nickname:
        :return:
        """
        logger('ItemDictHelper', 'get_array_for_justify_argument', 'def: arg ' + str(argument_uid) + ', attack ' + attack_type)
        statements_array = []
        _tn = Translator(self.lang)
        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()
        # description in docs: dbas/logic
        db_arguments = self.__get_arguments_based_on_attack(attack_type, argument_uid)
        uids = rs.get_uids_of_best_statements_for_justify_position(db_arguments)  # TODO # 166

        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        for argument in db_arguments:
            if db_user:  # add seen by if the statement is visible
                add_seen_argument(argument_uid, db_user.uid)
            # get all premises in this group
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
            premises_array = []
            for premise in db_premises:
                text = get_text_for_statement_uid(premise.statement_uid)
                premises_array.append({'id': premise.statement_uid, 'title': text[0:1].upper() + text[1:]})

            # for each justifying premise, we need a new confrontation: (restriction is based on fix #38)
            is_undermine = 'undermine' if attack_type == 'undermine' else None
            attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)

            arg_id_sys, attack = rs.get_attack_for_argument(argument.uid, self.lang, last_attack=is_undermine,
                                                            restriction_on_arg_uids=attacking_arg_uids,
                                                            history=self.path)

            url = _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys)
            statements_array.append(self.__create_answer_dict(argument.uid, premises_array, 'justify', url,
                                                              is_flagable=True,
                                                              is_author=is_author_of_argument(nickname, argument.uid),
                                                              is_visible=argument.uid in uids))

        if logged_in:
            if len(statements_array) == 0:
                text = _tn.get(_.newPremiseRadioButtonTextAsFirstOne)
            else:
                text = _tn.get(_.newPremiseRadioButtonText)
            statements_array.append(self.__create_answer_dict('justify_premise', [{'id': '0', 'title': text}], 'justify', 'add'))
        else:
            # elif len(statements_array) == 1:
            statements_array.append(
                self.__create_answer_dict('login', [{'id': '0', 'title': _tn.get(_.onlyOneItem)}], 'justify', 'login'))

        return {'elements': statements_array, 'extras': {'cropped_list': len(uids) < len(db_arguments)}}

    def __get_arguments_based_on_attack(self, attack_type, argument_uid):
        """

        :param attack_type:
        :param argument_uid:
        :return:
        """
        db_argument = get_not_disabled_arguments_as_query().filter_by(uid=argument_uid).first()

        db_arguments = []
        db_arguments_not_disabled = get_not_disabled_arguments_as_query()
        if attack_type == 'undermine':
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
            for premise in db_premises:
                arguments = db_arguments_not_disabled.filter(and_(Argument.conclusion_uid == premise.statement_uid,
                                                                  Argument.is_supportive == False,
                                                                  Argument.issue_uid == self.issue_uid)).all()
                db_arguments = db_arguments + arguments

        elif attack_type == 'undercut':
            db_arguments = db_arguments_not_disabled.filter(and_(Argument.argument_uid == argument_uid,
                                                                 Argument.is_supportive == False,
                                                                 Argument.issue_uid == self.issue_uid)).all()

        elif attack_type == 'overbid':
            db_arguments = db_arguments_not_disabled.filter(and_(Argument.argument_uid == argument_uid,
                                                                 Argument.is_supportive == True,
                                                                 Argument.issue_uid == self.issue_uid)).all()

        elif attack_type == 'rebut':
            db_arguments = db_arguments_not_disabled.filter(and_(Argument.conclusion_uid == db_argument.conclusion_uid,
                                                                 Argument.argument_uid == db_argument.argument_uid,
                                                                 Argument.is_supportive == False,
                                                                 Argument.issue_uid == self.issue_uid)).all()

        elif attack_type == 'support':
            db_arguments = db_arguments_not_disabled.filter(and_(Argument.conclusion_uid == db_argument.conclusion_uid,
                                                                 Argument.argument_uid == db_argument.argument_uid,
                                                                 Argument.is_supportive == db_argument.is_supportive,
                                                                 Argument.issue_uid == self.issue_uid)).all()
        return db_arguments

    def get_array_for_dont_know_reaction(self, argument_uid, is_supportive, nickname, gender):
        """
        Prepares the dict with all items for the third step, where a supportive argument will be presented.

        :param argument_uid: Argument.uid
        :param is_supportive: Boolean
        :param nickname: nickname
        :return:
        """
        logger('ItemDictHelper', 'get_array_for_dont_know_reaction', 'def')
        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()
        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)
        statements_array = []

        db_arguments = get_not_disabled_arguments_as_query()
        db_argument = db_arguments.filter_by(uid=argument_uid).first()
        if not db_argument:
            return {'elements': statements_array, 'extras': {'cropped_list': False}}

        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        if db_user:  # add seen by if the statement is visible
            add_seen_argument(argument_uid, db_user.uid)

        rel_dict     = get_relation_text_dict_with_substitution(self.lang, False, False, False, is_dont_know=True, gender=gender)
        current_mode = 't' if is_supportive else 'f'
        not_current_mode = 'f' if is_supportive else 't'

        # relations = ['undermine', 'support', 'undercut', 'overbid', 'rebut'] # TODO 'overbid'
        relations = ['undermine', 'support', 'undercut', 'rebut']
        for relation in relations:
            if relation == 'undermine':
                if db_argument.conclusion_uid is not None:
                    url = _um.get_url_for_justifying_statement(True, db_argument.conclusion_uid, not_current_mode)
                else:
                    url = _um.get_url_for_justifying_argument(True, db_argument.argument_uid, not_current_mode, relation)
            elif relation == 'support':
                arg_id_sys, sys_attack = rs.get_attack_for_argument(argument_uid, self.lang)
                url = _um.get_url_for_reaction_on_argument(True, argument_uid, sys_attack, arg_id_sys)
            elif relation == 'undercut':
                url = _um.get_url_for_justifying_argument(True, argument_uid, current_mode, relation)
            elif relation == 'rebut':
                db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
                if len(db_premises) == 1:
                    url = _um.get_url_for_justifying_statement(True, db_premises[0].statement_uid, not_current_mode)
                else:
                    uids = [db_argument.premisesgroup_uid]
                    if db_argument.conclusion_uid is not None:
                        url = _um.get_url_for_choosing_premisegroup(True, False, db_argument.is_supportive, db_argument.conclusion_uid, uids)
                    else:
                        url = _um.get_url_for_choosing_premisegroup(True, True, db_argument.is_supportive, db_argument.argument_uid, uids)

            else:
                url = _um.get_url_for_justifying_argument(True, argument_uid, not_current_mode, relation)

            statements_array.append(self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation, url))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

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
        logger('ItemDictHelper', 'get_array_for_reaction', 'def')
        _tn  = Translator(self.lang)
        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()

        db_sys_argument = DBDiscussionSession.query(Argument).get(argument_uid_sys)
        db_user_argument = DBDiscussionSession.query(Argument).get(argument_uid_user)
        statements_array = []
        if not db_sys_argument or not db_user_argument:
            return {'elements': statements_array, 'extras': {'cropped_list': False}}

        rel_dict = get_relation_text_dict_with_substitution(self.lang, False, True, db_user_argument.is_supportive,
                                                            first_conclusion=_tn.get(_.myPosition),
                                                            attack_type=attack, gender=gender)
        mode = 't' if is_supportive else 'f'
        _um  = UrlManager(self.application_url, slug, self.for_api, history=self.path)

        relations = ['undermine', 'support', 'undercut', 'rebut']
        for relation in relations:
            url = self.__get_url_based_on_relation(relation, attack, _um, argument_uid_user, argument_uid_sys,
                                                   mode, db_user_argument, db_sys_argument)

            # TODO PREVENT LOOPING
            # newStepInUrl = url[url.index('/reaction/') if url.index('/reaction/') < url.index('/justify/') else url.index('/justify/'):url.index('?')]
            # additionalText = (' (<em>' + _tn.get(_.youUsedThisEarlier) + '<em>)') if newStepInUrl in url[url.index('?'):] else ''

            statements_array.append(self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id':relation}], relation, url))

        # last item is the change attack button or step back, if we have bno other attack
        attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)
        attacking_arg_uids.append(argument_uid_sys)
        arg_id_sys, new_attack = rs.get_attack_for_argument(argument_uid_user, self.lang,
                                                            restriction_on_attacks=attack,
                                                            restriction_on_arg_uids=attacking_arg_uids)

        if new_attack == 'no_other_attack' or new_attack.startswith('end'):
            relation = 'step_back'
            url = 'back' if self.for_api else 'window.history.go(-1)'
        else:
            relation = 'no_opinion'
            url = _um.get_url_for_reaction_on_argument(True, argument_uid_user, new_attack, arg_id_sys)
        statements_array.append(self.__create_answer_dict(relation, [{'title': rel_dict[relation + '_text'], 'id': relation}], relation, url))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def __get_url_based_on_relation(self, relation, attack, _um, argument_uid_user, argument_uid_sys, mode, db_user_argument, db_sys_argument):
        """

        :param relation:
        :param attack:
        :param rs:
        :param _um:
        :param argument_uid_user:
        :param argument_uid_sys:
        :param mode:
        :param db_user_argument:
        :param db_sys_argument:
        :return:
        """
        # special case, when the user selects the support, because this does not need to be justified!
        if relation == 'support':
            return self.__get_url_for_support(attack, _um, argument_uid_sys, db_sys_argument)
        elif relation == 'undermine' or relation == 'undercut':  # easy cases
            return self.__get_url_for_undermine(relation, _um, argument_uid_sys, mode)
        elif relation == 'overbid':  # it will be the attack again
            return self.__get_url_for_overbid(attack, _um, argument_uid_user, mode)
        elif relation == 'rebut':  # if we are having an rebut, everything seems different
            return self.__get_url_for_rebut(attack, _um, mode, db_user_argument, db_sys_argument)
        else:
            return _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)

    def __get_url_for_support(self, attack, _um, argument_uid_sys, db_sys_argument):
        """

        :param attack:
        :param _um:
        :param argument_uid_sys:
        :param db_sys_argument:
        :return:
        """
        attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)
        arg_id_sys, sys_attack = rs.get_attack_for_argument(argument_uid_sys, self.lang,
                                                            restriction_on_arg_uids=attacking_arg_uids)
        if sys_attack == 'rebut' and attack == 'undercut':
            # case: system makes an undercut and the user supports this new attack can be an rebut, so another
            # undercut for the users argument therefore now the users opinion is the new undercut (e.g. rebut)
            # because he supported it!
            url = _um.get_url_for_reaction_on_argument(True, arg_id_sys, sys_attack, db_sys_argument.argument_uid)
        else:
            url = _um.get_url_for_reaction_on_argument(True, argument_uid_sys, sys_attack, arg_id_sys)
        return url

    def __get_url_for_undermine(self, relation, _um, argument_uid_sys, mode):
        """

        :param relation:
        :param _um:
        :param argument_uid_sys:
        :param mode:
        :return:
        """
        return _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)

    def __get_url_for_overbid(self, attack, _um, argument_uid_user, mode):
        """

        :param attack:
        :param _um:
        :param argument_uid_user:
        :param mode:
        :return:
        """
        return _um.get_url_for_justifying_argument(True, argument_uid_user, mode, attack)

    def __get_url_for_rebut(self, attack, _um, mode, db_user_argument, db_sys_argument):
        """

        :param attack:
        :param _um:
        :param mode:
        :param db_user_argument:
        :param db_sys_argument:
        :return:
        """
        url = ''
        if attack == 'undermine':  # rebutting an undermine will be a support for the initial argument
            url = _um.get_url_for_justifying_statement(True, db_sys_argument.conclusion_uid, mode)

        elif attack == 'undercut':  # rebutting an undercut will be a overbid for the initial argument
            # url = _um.get_url_for_justifying_argument(True, argument_uid_user, mode, 'overbid')
            if db_user_argument.argument_uid is None:
                url = _um.get_url_for_justifying_statement(True, db_user_argument.conclusion_uid, mode)
            else:
                db_premises = DBDiscussionSession.query(Premise).filter_by(
                    premisesgroup_uid=db_user_argument.premisesgroup_uid).all()
                db_premise = db_premises[random.randint(0, len(db_premises) - 1)]  # TODO: ELIMINATE RANDOM
                url = _um.get_url_for_justifying_statement(True, db_premise.statement_uid, mode)

        # rebutting an rebut will be a justify for the initial argument
        elif attack == 'rebut':
            current_user_argument = db_user_argument
            conclusion_uid = current_user_argument.conclusion_uid
            while conclusion_uid is None:
                conclusion_uid = DBDiscussionSession.query(Argument).filter_by(
                    uid=current_user_argument.argument_uid).first().conclusion_uid
            url = _um.get_url_for_justifying_statement(True,
                                                       db_user_argument.conclusion_uid if conclusion_uid is None else conclusion_uid,
                                                       mode)
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
        logger('ItemDictHelper', 'get_array_for_choosing', 'def')
        statements_array = []
        slug = DBDiscussionSession.query(Issue).get(self.issue_uid).get_slug()
        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)
        conclusion = argument_or_statement_id if not is_argument else None
        argument = argument_or_statement_id if is_argument else None
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        for group_id in pgroup_ids:
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group_id).all()
            premise_array = []
            for premise in db_premises:
                text = get_text_for_statement_uid(premise.statement_uid)
                premise_array.append({'title': text, 'id': premise.statement_uid})
                if db_user:  # add seen by if the statement is visible
                    add_seen_statement(premise.statement_uid, db_user.uid)

            # get attack for each premise, so the urls will be unique
            logger('ItemDictHelper', 'get_array_for_choosing', 'premisesgroup_uid: ' + str(group_id) +
                   ', conclusion_uid: ' + str(conclusion) +
                   ', argument_uid: ' + str(argument) +
                   ', is_supportive: ' + str(is_supportive))
            db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == group_id,
                                                                          Argument.conclusion_uid == conclusion,
                                                                          Argument.argument_uid == argument,
                                                                          Argument.is_supportive == is_supportive)).first()
            if not db_argument:
                logger('ItemDictHelper', 'get_array_for_choosing', 'No argument found', error=True)
                return None
            attacking_arg_uids = get_all_attacking_arg_uids_from_history(self.path)
            arg_id_sys, attack = rs.get_attack_for_argument(db_argument.uid, self.lang,
                                                            restriction_on_arg_uids=attacking_arg_uids)
            url = _um.get_url_for_reaction_on_argument(True, db_argument.uid, attack, arg_id_sys)

            is_author = is_author_of_argument(nickname, argument) if is_argument else is_author_of_statement(nickname, conclusion)
            statements_array.append(self.__create_answer_dict(str(db_argument.uid), premise_array, 'choose', url,
                                                              is_flagable=True, is_author=is_author))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    def get_array_for_jump(self, arg_uid, slug, for_api):
        """

        :param arg_uid:
        :param slug:
        :param for_api:
        :return:
        """

        _um = UrlManager(self.application_url, slug, self.for_api, history=self.path)
        db_argument = DBDiscussionSession.query(Argument).get(arg_uid)
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()

        # Array with [Conclusion is (right, wrong), Premise is (right, wrong), Premise does not leads to the conclusion, both hold]
        item_text = get_jump_to_argument_text_list(self.lang)

        # which part of the argument should be attacked ?
        base = db_argument.argument_uid if db_argument.conclusion_uid is None else arg_uid
        arg_id_sys, sys_attack = rs.get_attack_for_argument(base, self.lang)

        url0 = _um.get_url_for_reaction_on_argument(not for_api, arg_uid, sys_attack, arg_id_sys)
        if db_argument.conclusion_uid is None:  # conclusion is an argument
            url1 = _um.get_url_for_reaction_on_argument(not for_api, db_argument.argument_uid, sys_attack, arg_id_sys)
            url3 = _um.get_url_for_justifying_argument(not for_api, db_argument.argument_uid, 'f', 'undercut')
        else:
            url1 = _um.get_url_for_justifying_statement(not for_api, db_argument.conclusion_uid, 't')
            url3 = _um.get_url_for_justifying_statement(not for_api, db_argument.conclusion_uid, 'f')
        url2 = _um.get_url_for_justifying_argument(not for_api, arg_uid, 't', 'undercut')
        if len(db_premises) == 1:
            url4 = _um.get_url_for_justifying_statement(not for_api, db_premises[0].statement_uid, 'f')
        else:
            url4 = _um.get_url_for_justifying_argument(not for_api, db_argument.uid, 'f', 'undermine')

        answers = list()
        answers.append({'text': item_text[0], 'url': url0})
        answers.append({'text': item_text[1], 'url': url1})
        answers.append({'text': item_text[2], 'url': url2})
        answers.append({'text': item_text[3], 'url': url3})
        answers.append({'text': item_text[4], 'url': url4})

        statements_array = []
        for no in range(0, len(answers)):
            arr = [{'title': answers[no]['text'], 'id': 0}]
            statements_array.append(self.__create_answer_dict('jump' + str(no), arr, 'jump', answers[no]['url']))

        return {'elements': statements_array, 'extras': {'cropped_list': False}}

    @staticmethod
    def __create_answer_dict(uid, premises, attitude, url, already_used=False, already_used_text='', is_flagable=False, is_author=False, is_visible=True):
        """
        Return dictionary

        :param uid: Integer
        :param premises: Array of dict with title and id
        :param attitude: String
        :param url: String
        :param already_used: Boolean
        :param already_used_text: String
        :param is_flagable: Boolean
        :param is_author: Boolean
        :param is_visible: Boolean
        :return: dict()
        """
        return {
            'id': 'item_' + str(uid),
            'premises': premises,
            'attitude': attitude,
            'url': url,
            'already_used': already_used,
            'already_used_text': already_used_text,
            'is_flagable': is_flagable,
            'is_editable': is_flagable,
            'is_deletable': is_author,
            'style': '' if is_visible else 'display: none;'}
