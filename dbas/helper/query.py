"""
Provides helping function for database querys.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
import transaction

import dbas.helper.notification as NotificationHelper
import dbas.recommender_system as RecommenderSystem
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, Issue, \
    RevokedContent, RevokedContentHistory, sql_timestamp_pretty_print, MarkedArgument, MarkedStatement
from dbas.helper.relation import get_rebuts_for_argument_uid, get_undermines_for_argument_uid, \
    get_undercuts_for_argument_uid, get_supports_for_argument_uid, set_new_rebut, set_new_support, \
    set_new_undercut, set_new_undermine_or_support_for_pgroup
from dbas.helper.voting import add_seen_statement, add_seen_argument
from dbas.input_validator import get_relation_between_arguments
from dbas.lib import escape_string, get_text_for_premisesgroup_uid, \
    get_all_attacking_arg_uids_from_history, get_profile_picture, get_text_for_statement_uid, pretty_print_options, \
    is_author_of_argument, is_author_of_statement, get_all_arguments_by_statement, get_text_for_argument_uid
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager
from sqlalchemy import and_, func
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.input_validator import is_integer
from dbas.handler.rss import append_action_to_issue_rss
from dbas.helper.dictionary.bubbles import get_user_bubble_text_for_justify_statement
from dbas.helper.history import get_bubble_from_reaction_step, get_splitted_history

statement_min_length = 10


def process_input_of_start_premises_and_receive_url(default_locale_name, premisegroups, conclusion_id, supportive,
                                                    issue, user, for_api, application_url, discussion_lang, history,
                                                    port, mailer):
    """
    Inserts the given text in premisegroups as new arguments in dependence of the input parameters and returns a URL for forwarding.

    :param default_locale_name: Default lang of the app
    :param premisegroups: [String]
    :param conclusion_id: Statement.uid
    :param supportive: Boolean
    :param issue: Issue.uid
    :param user: User.nickname
    :param for_api: Boolean
    :param application_url: URL
    :param discussion_lang: ui_locales
    :param history: History of the user
    :param port: Port of the notification server
    :param mailer: Instance of pyramid mailer
    :return: URL, [Statement.uid], String
    """
    logger('QueryHelper', 'process_input_of_start_premises_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    _tn = Translator(discussion_lang)
    if not db_user:
        return '', '', _tn.get(_.userNotFound)

    slug = DBDiscussionSession.query(Issue).get(issue).get_slug()
    error = ''
    url = ''

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    new_statement_uids = []  # all statement uids are stored in this list to create the link to a possible reference
    for group in premisegroups:  # premise groups is a list of lists
        new_argument, statement_uids = __create_argument_by_raw_input(application_url, default_locale_name, user, group, conclusion_id, supportive, issue, discussion_lang)
        if not isinstance(new_argument, Argument):  # break on error
            error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength),
                                         statement_min_length)
            return -1, None, error

        new_argument_uids.append(new_argument.uid)
        if for_api:
            new_statement_uids.append(statement_uids)

    # #arguments=0: empty input
    # #arguments=1: deliver new url
    # #arguments>1: deliver url where the user has to choose between her inputs
    _um = UrlManager(application_url, slug, for_api, history)
    _main_um = UrlManager(application_url, slug, False, history)
    if len(new_argument_uids) == 0:
        error = __get_error_for_empty_argument_list(_tn)

    elif len(new_argument_uids) == 1:
        url = __get_url_for_new_argument(new_argument_uids, history, discussion_lang, _um)

    else:
        pgroups = []
        for arg_uid in new_argument_uids:
            pgroups.append(DBDiscussionSession.query(Argument).get(arg_uid).premisesgroup_uid)
        url = _um.get_url_for_choosing_premisegroup(False, False, supportive, conclusion_id, pgroups)

    # send notifications and mails
    if len(new_argument_uids) > 0:
        email_url = _main_um.get_url_for_justifying_statement(False, conclusion_id, 't' if supportive else 'f')
        NotificationHelper.send_add_text_notification(email_url, conclusion_id, user, port, mailer)

    return url, new_statement_uids, error


def process_input_of_premises_for_arguments_and_receive_url(default_locale_name, arg_id, attack_type, premisegroups,
                                                            issue, user, for_api, application_url, discussion_lang,
                                                            history, port, mailer):
    """
    Inserts the given text in premisegroups as new arguments in dependence of the input parameters and returns a URL for forwarding.

    .. note::

        Optimize the "for_api" part

    :param default_locale_name: Default lang of the app
    :param arg_id: Argument.uid
    :param attack_type: String
    :param premisegroups: [Strings]
    :param issue: Issue.uid
    :param user: User.nickname
    :param for_api: Boolean
    :param application_url: URL
    :param discussion_lang: ui_locales
    :param history: History of the user
    :param port: Port of notification server
    :param mailer: Instance of pyramid mailer
    :return: URL, [Statement.uids], String
    """
    logger('QueryHelper', 'process_input_of_premises_for_arguments_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    _tn = Translator(discussion_lang)
    if not db_user:
        return '', '', _tn.get(_.userNotFound)

    slug = DBDiscussionSession.query(Issue).get(issue).get_slug()
    error = ''
    supportive = attack_type == 'support' or attack_type == 'overbid'

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    for group in premisegroups:  # premise groups is a list of lists
        new_argument = __insert_new_premises_for_argument(application_url, default_locale_name, group, attack_type,
                                                          arg_id, issue, user, discussion_lang)
        if not isinstance(new_argument, Argument):  # break on error
            a = _tn.get(_.notInsertedErrorBecauseEmpty)
            b = _tn.get(_.minLength)
            c = str(statement_min_length)
            d = _tn.get(_.eachStatement)
            error = '{} ({}: {} {})'.format(a, b, c, d)
            return -1, None, error

        new_argument_uids.append(new_argument.uid)

    statement_uids = []
    if for_api:
        # @OPTIMIZE
        # Query all recently stored premises (internally: statements) and collect their ids
        # This is a bad workaround, let's just think about it in future.
        for uid in new_argument_uids:
            current_pgroup = DBDiscussionSession.query(Argument).get(uid).premisesgroup_uid
            current_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_pgroup).all()
            for premise in current_premises:
                statement_uids.append(premise.statement_uid)

    # #arguments=0: empty input
    # #arguments=1: deliver new url
    # #arguments>1: deliver url where the user has to choose between her inputs
    _um = url = UrlManager(application_url, slug, for_api, history)
    if len(new_argument_uids) == 0:
        error = __get_error_for_empty_argument_list(_tn)

    elif len(new_argument_uids) == 1:
        url = __get_url_for_new_argument(new_argument_uids, history, discussion_lang, _um)

    else:
        url = __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, attack_type,
                                                                                    arg_id, _um, supportive)

    # send notifications and mails
    if len(new_argument_uids) > 0:
        # add marked arguments
        DBDiscussionSession.add_all([MarkedArgument(argument=uid, user=db_user.uid) for uid in new_argument_uids])
        DBDiscussionSession.flush()
        transaction.commit()

        new_uid = random.choice(new_argument_uids)   # TODO eliminate random
        attack = get_relation_between_arguments(arg_id, new_uid)

        tmp_url = _um.get_url_for_reaction_on_argument(False, arg_id, attack, new_uid)

        NotificationHelper.send_add_argument_notification(tmp_url, arg_id, user, port, mailer)

    return url, statement_uids, error


def process_seen_statements(uids, nickname, additional_argument=None):
    """
    Sets the given statement uids as seen by given user

    :param uids: [Statement.uid]
    :param nickname: User.nickname
    :param additional_argument: Argument.uid
    :return: String
    """
    logger('QueryHelper', 'process_seen_statements', 'user ' + str(nickname) + ', statements ' + str(uids) +
           ', additional argument ' + str(additional_argument))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    if not db_user:
        return None

    if additional_argument:
        add_seen_argument(additional_argument, db_user)

    for uid in uids:
        # we get the premise group id's only
        if not is_integer(uid):
            return _.internalKeyError

        add_seen_statement(uid, db_user)

    return None


def mark_or_unmark_statement_or_argument(uid, is_argument, should_mark, nickname, _t):
    """
    Marks or unmark an argument/statement, which represents the users opinion

    :param uid: Statement.uid / Argument.uid
    :param is_argument: Boolean
    :param should_mark: Boolean
    :param nickname: User.nickname
    :param _t: Translator
    :return: String, String
    """
    logger('QueryHelper', 'mark_or_unmark_statement_or_argument', '{} {} {}'.format(uid, is_argument, nickname))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return '', _t.get(_.internalError)

    base_type = Argument if is_argument else Statement
    table = MarkedArgument if is_argument else MarkedStatement
    column = MarkedArgument.argument_uid if is_argument else MarkedStatement.statement_uid

    db_base = DBDiscussionSession.query(base_type).get(uid)
    if not db_base:
        return '', _t.get(_.internalError)

    if should_mark:
        db_el = DBDiscussionSession.query(table).filter(column == uid).first()
        logger('QueryHelper', 'mark_or_unmark_statement_or_argument', 'Element {}is present'.format('yet ' if db_el else ''))
        if not db_el:
            new_el = MarkedArgument(argument=uid, user=db_user.uid) if is_argument else MarkedStatement(statement=uid, user=db_user.uid)
            DBDiscussionSession.add(new_el)
    else:
        DBDiscussionSession.query(table).filter(column == uid).delete()

    DBDiscussionSession.flush()
    transaction.commit()

    return _t.get(_.opinionSaved), ''


def get_text_for_justification_or_reaction_bubble(uid, is_argument, is_supportive, nickname, step, history, _tn):
    """
    Returns text for an justification or reaction bubble of the user

    :param uid: Argumebt.uid / Statement.uid
    :param is_argument: Boolean
    :param is_supportive: Boolean
    :param nickname: User.nickname
    :param step: String
    :param history: String
    :param _tn: Translator
    :return: String
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if is_argument:
        splitted_history = get_splitted_history(history)
        bubbles = get_bubble_from_reaction_step('', step, nickname, _tn.get_lang(), splitted_history, '', color_steps=True)
        text = bubbles[0]['message'] if bubbles else ''
    else:
        text, tmp = get_user_bubble_text_for_justify_statement(uid, db_user, is_supportive, _tn)
        text = pretty_print_options(text)

    return text


def __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, attack_type, arg_id, _um, supportive):
    """
    Return the 'choose' url, when the user entered more than one premise for an argument

    :param new_argument_uids: [Argument.uid]
    :param attack_type: String
    :param arg_id: Argument.uid
    :param _um: UrlManager
    :param supportive: Boolean
    :return: String
    """
    pgroups = []
    url = ''
    for uid in new_argument_uids:
        pgroups.append(DBDiscussionSession.query(Argument).get(uid).premisesgroup_uid)

    current_argument = DBDiscussionSession.query(Argument).get(arg_id)
    # relation to the arguments premise group
    if attack_type == 'undermine' or attack_type == 'support':  # TODO WHAT IS WITH PGROUPS > 1 ? CAN THIS EVEN HAPPEN IN THE WoR?
        db_premise = DBDiscussionSession.query(Premise).filter_by(
            premisesgroup_uid=current_argument.premisesgroup_uid).first()
        db_statement = DBDiscussionSession.query(Statement).get(db_premise.statement_uid)
        url = _um.get_url_for_choosing_premisegroup(False, False, supportive, db_statement.uid, pgroups)

    # relation to the arguments relation
    elif attack_type == 'undercut' or attack_type == 'overbid':
        url = _um.get_url_for_choosing_premisegroup(False, True, supportive, arg_id, pgroups)

    # relation to the arguments conclusion
    elif attack_type == 'rebut':
        # TODO WHAT IS WITH ARGUMENT AS CONCLUSION?
        is_argument = current_argument.conclusion_uid is not None
        uid = current_argument.argument_uid if is_argument else current_argument.conclusion_uid
        url = _um.get_url_for_choosing_premisegroup(False, is_argument, supportive, uid, pgroups)

    return url


def __get_error_for_empty_argument_list(_tn):
    """
    Returns error text

    :param _tn: Translator
    :return: String
    """
    return _tn.get(_.notInsertedErrorBecauseEmpty) + ' (' + _tn.get(_.minLength) + ': ' + str(
        statement_min_length) + ')'


def __get_url_for_new_argument(new_argument_uids, history, lang, url_manager):
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
    arg_id_sys, attack = RecommenderSystem.get_attack_for_argument(new_argument_uid, lang, restriction_on_arg_uids=attacking_arg_uids)
    if arg_id_sys == 0:
        attack = 'end'
    url = url_manager.get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
    return url


def correct_statement(user, uid, corrected_text):
    """
    Corrects a statement

    :param user: User.nickname requesting user
    :param uid: requested statement uid
    :param corrected_text: new text
    :return: dict()
    """
    logger('QueryHelper', 'correct_statement', 'def ' + str(uid))

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

    if not db_user:
        return -1

    while corrected_text.endswith(('.', '?', '!')):
        corrected_text = corrected_text[:-1]

    # duplicate check
    return_dict = dict()
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(TextVersion.uid.desc()).all()

    # duplicate or not?
    if db_textversion:
        textversion = DBDiscussionSession.query(TextVersion).get(db_textversion[0].uid)
    else:
        textversion = TextVersion(content=corrected_text, author=db_user.uid)
        textversion.set_statement(db_statement.uid)
        DBDiscussionSession.add(textversion)
        DBDiscussionSession.flush()

    # if request:
    #     NotificationHelper.send_edit_text_notification(db_user, textversion, url, request)

    db_statement.set_textversion(textversion.uid)
    # transaction.commit() # # 207

    return_dict['uid'] = uid
    return_dict['text'] = corrected_text
    return return_dict


def insert_as_statements(application_url, default_locale_name, text_list, user, issue, lang, is_start=False):
    """
    Inserts the given texts as statements and returns the uid's

    :param application_url: Url of the app itself
    :param default_locale_name: default lang of the app
    :param text_list: [String]
    :param user: User.nickname
    :param issue: Issue
    :param is_start: Boolean
    :return: [Statement]
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if not db_user:
        return -2

    statements = []
    input_list = text_list if isinstance(text_list, list) else [text_list]
    _tn = None
    for text in input_list:
        if len(text) < statement_min_length:
            return -1

        new_statement, is_duplicate = __set_statement(text, user, is_start, issue, lang)
        if new_statement:
            statements.append(new_statement)

            if not is_duplicate:
                _tn = Translator(new_statement.lang) if _tn is None else _tn
                db_issue = DBDiscussionSession.query(Issue).get(issue)
                _um = UrlManager(application_url, db_issue.get_slug())
                append_action_to_issue_rss(issue_uid=issue,
                                           author_uid=db_user.uid,
                                           title=_tn.get(_.positionAdded if is_start else _.statementAdded),
                                           description='...' + get_text_for_statement_uid(new_statement.uid) + '...',
                                           ui_locale=default_locale_name,
                                           url=_um.get_url_for_statement_attitude(False, new_statement.uid))

    return statements


def get_every_attack_for_island_view(arg_uid):
    """
    Select and returns every argument with an relation to the given Argument.uid

    :param arg_uid: Argument.uid
    :return: dict()
    """
    logger('QueryHelper', 'get_every_attack_for_island_view', 'def with arg_uid: ' + str(arg_uid))
    return_dict = {}
    db_argument = DBDiscussionSession.query(Argument).get(arg_uid)
    if not db_argument:
        return
    lang = db_argument.lang
    _t = Translator(lang)

    undermine = get_undermines_for_argument_uid(arg_uid)
    support = get_supports_for_argument_uid(arg_uid)
    undercut = get_undercuts_for_argument_uid(arg_uid)
    # overbid = get_overbids_for_argument_uid(arg_uid)
    rebut = get_rebuts_for_argument_uid(arg_uid)

    db_user = DBDiscussionSession.query(User).get(db_argument.author_uid)
    if db_user and db_user.gender == 'f':
        msg = _t.get(_.voteCountTextMayBeFirstF) + '.'
    else:
        msg = _t.get(_.voteCountTextMayBeFirst) + '.'

    no_entry_text = _t.get(_.no_arguments) + '. ' + msg
    undermine = undermine if undermine else [{'id': 0, 'text': no_entry_text}]
    support = support if support else [{'id': 0, 'text': no_entry_text}]
    undercut = undercut if undercut else [{'id': 0, 'text': no_entry_text}]
    # overbid = overbid if overbid else [{'id': 0, 'text': no_entry_text}]
    rebut = rebut if rebut else [{'id': 0, 'text': no_entry_text}]

    return_dict.update({'undermine': undermine})
    return_dict.update({'support': support})
    return_dict.update({'undercut': undercut})
    # return_dict.update({'overbid': overbid})
    return_dict.update({'rebut': rebut})

    # pretty print
    for d in return_dict:
        for entry in return_dict[d]:
            has_entry = False if entry['id'] == 0 or lang == 'de' else True
            entry['text'] = (_t.get(_.because) + ' ' if has_entry else '') + entry['text']

    logger('QueryHelper', 'get_every_attack_for_island_view', 'summary: ' +
           str(len(undermine)) + ' undermines, ' +
           str(len(support)) + ' supports, ' +
           str(len(undercut)) + ' undercuts, ' +
           str(len(rebut)) + ' rebuts')

    return return_dict


def get_logfile_for_statements(uids, lang, main_page):
    """
    Returns the logfile for the given statement uid

    :param uids: requested statement uid
    :param lang: ui_locales ui_locales
    :param main_page: URL
    :return: dictionary with the logfile-rows
    """
    logger('QueryHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uids))

    main_dict = dict()
    for uid in uids:
        db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(TextVersion.uid.asc()).all()
        if len(db_textversions) == 0:
            continue
        return_dict = dict()
        content_dict = dict()
        # add all corrections
        for index, version in enumerate(db_textversions):
            content_dict[str(index)] = __get_logfile_dict(version, main_page, lang)
        return_dict['content'] = content_dict
        main_dict[get_text_for_statement_uid(uid)] = return_dict

    return main_dict


def get_another_argument_with_same_conclusion(uid, history):
    """
    Returns another supporting/attacking argument with the same conclusion as the given Argument.uid

    :param uid: Argument.uid
    :param history: String
    :return: Argument
    """
    logger('QueryHelper', 'get_another_argument_with_same_conclusion', str(uid))
    db_arg = DBDiscussionSession.query(Argument).get(uid)
    if not db_arg:
        return None

    if db_arg.conclusion_uid is None:
        return None

    # get forbidden uids
    splitted_histoy = history.split('-')
    forbidden_uids = [history.split('/')[2] for history in splitted_histoy if 'reaction' in history] + [uid]

    db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == db_arg.conclusion_uid,
                                                                  Argument.is_supportive == db_arg.is_supportive,
                                                                  ~Argument.uid.in_(forbidden_uids))).all()
    if len(db_supports) == 0:
        return None

    return db_supports[random.randint(0, len(db_supports) - 1)]


def __get_logfile_dict(textversion, main_page, lang):
    """
    Returns dictionary with information about the given textversion

    :param textversion: TextVersion
    :param main_page: String
    :param lang: Language.ui_locales
    :return: dict()
    """
    db_author = DBDiscussionSession.query(User).get(textversion.author_uid)
    corr_dict = dict()
    corr_dict['uid'] = str(textversion.uid)
    corr_dict['author'] = str(db_author.get_global_nickname())
    corr_dict['author_url'] = main_page + '/user/' + str(db_author.uid)
    corr_dict['author_gravatar'] = get_profile_picture(db_author, 20)
    corr_dict['date'] = sql_timestamp_pretty_print(textversion.timestamp, lang)
    corr_dict['text'] = str(textversion.content)
    return corr_dict


def __insert_new_premises_for_argument(application_url, default_locale_name, text, current_attack, arg_uid, issue, user, discussion_lang):
    """
    Creates premises for a given argument

    :param application_url: Url of the app itself
    :param default_locale_name: default lang of the app
    :param text: String
    :param current_attack: String
    :param arg_uid: Argument.uid
    :param issue: Issue
    :param user: User.nickname
    :return: Argument
    """
    logger('QueryHelper', '__insert_new_premises_for_argument', 'def')

    statements = insert_as_statements(application_url, default_locale_name, text, user, issue, discussion_lang)
    if statements == -1:
        return -1

    # set the new statements as premise group and get current user as well as current argument
    new_pgroup_uid = __set_statements_as_new_premisegroup(statements, user, issue)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    current_argument = DBDiscussionSession.query(Argument).get(arg_uid)

    new_argument = None
    if current_attack == 'undermine':
        new_argument = set_new_undermine_or_support_for_pgroup(new_pgroup_uid, current_argument, False, db_user, issue)

    elif current_attack == 'support':
        new_argument, duplicate = set_new_support(new_pgroup_uid, current_argument, db_user, issue)

    elif current_attack == 'undercut' or current_attack == 'overbid':
        new_argument, duplicate = set_new_undercut(new_pgroup_uid, current_argument, db_user, issue)

    elif current_attack == 'rebut':
        new_argument, duplicate = set_new_rebut(new_pgroup_uid, current_argument, db_user, issue)

    logger('QueryHelper', '__insert_new_premises_for_argument', 'Returning argument ' + str(new_argument.uid))
    return new_argument


def __set_statement(text, nickname, is_start, issue, lang):
    """
    Saves statement for user

    :param text: given statement
    :param nickname: User.nickname of given user
    :param is_start: if it is a start statement
    :param issue: Issue
    :return: Statement, is_duplicate or -1, False on error
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None, False

    logger('QueryHelper', 'set_statement', 'user: ' + str(nickname) + ', user_id: ' + str(db_user.uid) +
           ', text: ' + str(text) + ', issue: ' + str(issue))

    # escaping and cleaning
    text = text.strip()
    text = ' '.join(text.split())
    text = escape_string(text)
    _tn = Translator(lang)
    if text.startswith(_tn.get(_.because).lower() + ' '):
        text = text[len(_tn.get(_.because) + ' '):]
    while text.endswith(('.', '?', '!', ',')):
        text = text[:-1]

    # check, if the text already exists
    db_duplicate = DBDiscussionSession.query(TextVersion).filter(func.lower(TextVersion.content) == text.lower()).first()
    if db_duplicate:
        db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == db_duplicate.statement_uid,
                                                                        Statement.issue_uid == issue)).first()
        return db_statement, True

    # add textversion
    textversion = TextVersion(content=text, author=db_user.uid)
    DBDiscussionSession.add(textversion)
    DBDiscussionSession.flush()

    # add text
    DBDiscussionSession.add(Statement(textversion=textversion.uid, is_position=is_start, issue=issue))
    DBDiscussionSession.flush()

    # get new text
    new_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid == textversion.uid,
                                                                     Statement.issue_uid == issue)).order_by(Statement.uid.desc()).first()
    textversion.set_statement(new_statement.uid)

    # add marked statement
    DBDiscussionSession.add(MarkedStatement(statement=new_statement.uid, user=db_user.uid))
    DBDiscussionSession.flush()

    transaction.commit()

    return new_statement, False


def __get_attack_or_support_for_justification_of_argument_uid(argument_uid, is_supportive):
    """
    Returns attacks or support for the reaction on an argument

    :param argument_uid: Argument.uid
    :param is_supportive: Boolean
    :return: [dict()]
    """
    return_array = []
    logger('QueryHelper', '__get_attack_or_support_for_justification_of_argument_uid',
           'db_undercut against Argument.argument_uid==' + str(argument_uid))
    db_related_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
                                                                           Argument.argument_uid == argument_uid)).all()
    given_relations = set()
    index = 0

    if not db_related_arguments:
        return None

    for relation in db_related_arguments:
        if relation.premisesgroup_uid not in given_relations:
            given_relations.add(relation.premisesgroup_uid)
            tmp_dict = dict()
            tmp_dict['id'] = relation.uid
            tmp_dict['text'], trash = get_text_for_premisesgroup_uid(relation.premisesgroup_uid)
            return_array.append(tmp_dict)
            index += 1
    return return_array


def __create_argument_by_raw_input(application_url, default_locale_name, user, text, conclusion_id, is_supportive, issue, discussion_lang):
    """
    Consumes the input to create a new argument

    :param application_url: Url of the app itself
    :param default_locale_name: default lang of the app
    :param user: User.nickname
    :param text: String
    :param conclusion_id:
    :param is_supportive: Boolean
    :param issue: Issue
    :return:
    """
    logger('QueryHelper', '__create_argument_by_raw_input', 'main with text ' + str(text) + ' as premisegroup, ' +
           'conclusion ' + str(conclusion_id) + ' in issue ' + str(issue))
    # current conclusion
    db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                     Statement.issue_uid == issue)).first()
    statements = insert_as_statements(application_url, default_locale_name, text, user, issue, discussion_lang)
    if statements == -1:
        return -1, None

    statement_uids = [s.uid for s in statements]

    # second, set the new statements as premisegroup
    new_premisegroup_uid = __set_statements_as_new_premisegroup(statements, user, issue)
    logger('QueryHelper', '__create_argument_by_raw_input', 'new pgroup ' + str(new_premisegroup_uid))

    # third, insert the argument
    new_argument = __create_argument_by_uids(user, new_premisegroup_uid, db_conclusion.uid, None, is_supportive, issue)
    transaction.commit()

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if new_argument and db_user:
        _tn = Translator(default_locale_name)
        db_issue = DBDiscussionSession.query(Issue).get(issue)
        _um = UrlManager(application_url, db_issue.get_slug())
        append_action_to_issue_rss(issue_uid=issue,
                                   author_uid=db_user.uid,
                                   title=_tn.get(_.argumentAdded),
                                   description='...' + get_text_for_argument_uid(new_argument.uid, anonymous_style=True) + '...',
                                   ui_locale=default_locale_name,
                                   url=_um.get_url_for_justifying_statement(False, new_argument.uid, 'd'))

    return new_argument, statement_uids


def __create_argument_by_uids(user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
    """
    Connects the given id's to a new argument

    :param user: User.nickname
    :param premisegroup_uid: PremiseGroup.uid
    :param conclusion_uid: Statement.uid
    :param argument_uid: Argument.uid
    :param is_supportive: Boolean
    :param issue: Issue.uid
    :return:
    """
    logger('QueryHelper', '__create_argument_by_uids', 'main with user: ' + str(user) +
           ', premisegroup_uid: ' + str(premisegroup_uid) +
           ', conclusion_uid: ' + str(conclusion_uid) +
           ', argument_uid: ' + str(argument_uid) +
           ', is_supportive: ' + str(is_supportive) +
           ', issue: ' + str(issue))

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                   Argument.is_supportive == is_supportive,
                                                                   Argument.conclusion_uid == conclusion_uid,
                                                                   Argument.issue_uid == issue)).first()
    if not new_argument:
        new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid,
                                conclusion=conclusion_uid, issue=issue)
        new_argument.set_conclusions_argument(argument_uid)

        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()

        new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.author_uid == db_user.uid,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.argument_uid == argument_uid,
                                                                       Argument.issue_uid == issue)).first()
    transaction.commit()
    if new_argument:
        logger('QueryHelper', '__create_argument_by_uids', 'argument was inserted')
        return new_argument
    else:
        logger('QueryHelper', '__create_argument_by_uids', 'argument was not inserted')
        return None


def __set_statements_as_new_premisegroup(statements, user, issue):
    """
    Set the given statements together as new premise group

    :param statements: [Statement.uid]
    :param user: User.nickname
    :param issue: Issue
    :return: PremiseGroup.uid
    """
    logger('QueryHelper', '__set_statements_as_new_premisegroup', 'user: ' + str(user) +
           ', statement: ' + str(statements) + ', issue: ' + str(issue))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

    # check for duplicate
    all_groups = []
    for statement in statements:
        # get the premise
        db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
        if db_premise:
            # getting all groups, where the premise is member
            db_premisegroup = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_premise.premisesgroup_uid).all()
            groups = set()
            for group in db_premisegroup:
                groups.add(group.premisesgroup_uid)
            all_groups.append(groups)
    # if every set in this array has one common member, they are all in the same group
    if len(all_groups) > 0:
        intersec = set.intersection(*all_groups)
        for group in intersec:
            db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group).all()
            if len(db_premise) == len(statements):
                return group

    premise_group = PremiseGroup(author=db_user.uid)
    DBDiscussionSession.add(premise_group)
    DBDiscussionSession.flush()

    premise_list = []
    for statement in statements:
        premise = Premise(premisesgroup=premise_group.uid, statement=statement.uid, is_negated=False, author=db_user.uid, issue=issue)
        premise_list.append(premise)

    DBDiscussionSession.add_all(premise_list)
    DBDiscussionSession.flush()

    db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

    return db_premisegroup.uid


def revoke_content(uid, is_argument, nickname, _tn):
    """
    Revokes the arguments/statements - e.g. the user is not the author anymore

    :param uid: Argument.uid / Statement.uid
    :param is_argument: Boolean
    :param nickname: User.nickname
    :param _tn: Translator
    :return:
    """
    logger('QueryHelper', 'revoke_content', str(uid) + (' argument' if is_argument else ' statement'))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        logger('QueryHelper', 'revoke_content', 'User not found')
        return _tn.get(_.userNotFound), False

    # get element, which should be revoked
    if is_argument:
        db_element, is_deleted, error = __revoke_argument(db_user, uid, _tn)
        if len(error) > 0:
            return error, False
    else:
        db_element, is_deleted, error = __revoke_statement(db_user, uid, _tn)
        if len(error) > 0:
            return error, False

    # write log
    if is_argument:
        DBDiscussionSession.add(RevokedContent(db_user.uid, argument=db_element.uid))
    else:
        DBDiscussionSession.add(RevokedContent(db_user.uid, statement=db_element.uid))

    DBDiscussionSession.add(db_element)
    DBDiscussionSession.flush()

    return '', is_deleted


def __revoke_argument(db_user, argument_uid, _tn):
    """
    Revokes the user as author of the argument

    :param db_user: User.uid
    :param argument_uid: Argument.uid
    :param _tn: Translator
    :return: Argument, Boolean, String
    """
    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)
    is_author = is_author_of_argument(db_user.nickname, argument_uid)

    # exists the argument
    if not db_argument:
        logger('QueryHelper', '__revoke_argument', 'Argument does not exists')
        return None, False, _tn.get(_.internalError)

    if not is_author:
        logger('QueryHelper', 'revoke_content', db_user.nickname + ' is not the author')
        return None, False, _tn.get(_.userIsNotAuthorOfArgument)

    # does the argument has any attack or supports?
    relations = [get_undermines_for_argument_uid(argument_uid),
                 get_supports_for_argument_uid(argument_uid),
                 get_undercuts_for_argument_uid(argument_uid),
                 get_rebuts_for_argument_uid(argument_uid)]
    is_involved = sum([len(rel) if rel else 0 for rel in relations]) > 0

    if is_involved:
        logger('QueryHelper', '__revoke_argument', 'Author of argument {} changed from {} to anonymous'.format(argument_uid, db_user.uid))
        db_new_author = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
        db_argument.author_uid = db_new_author.uid
        is_deleted = False
    else:
        logger('QueryHelper', '__revoke_argument', 'Disabling argument ' + str(argument_uid))
        db_argument.set_disable(True)
        is_deleted = True

    DBDiscussionSession.add(db_argument)
    DBDiscussionSession.flush()
    # transaction.commit()  # # 207
    return db_argument, is_deleted, ''


def __revoke_statement(db_user, statement_uid, _tn):
    """
    Revokes the user as author of the statement

    :param db_user: User
    :param statement_uid: Statement.uid
    :param _tn: Translator
    :return: Statement, Boolean, String
    """
    logger('QueryHelper', '__revoke_statement', 'Statement ' + str(statement_uid) + ' will be revoked (old author ' + str(db_user.uid) + ')')
    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    is_author = is_author_of_statement(db_user.nickname, statement_uid)

    is_revoked = False
    # exists the statement
    if not db_statement:
        logger('QueryHelper', '__revoke_statement', 'Statement does not exists')
        return None, is_revoked, _tn.get(_.internalError)

    if not is_author and False:
        logger('QueryHelper', '__revoke_statement', db_user.nickname + ' is not the author')
        return None, is_revoked, _tn.get(_.userIsNotAuthorOfStatement)

    __remove_user_from_arguments_with_statement(statement_uid, db_user, _tn)

    db_anonymous = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    logger('QueryHelper', '__revoke_statement', 'Statement ' + str(statement_uid) + ' will get a new author ' + str(db_anonymous.uid) + ' (old author ' + str(db_user.uid) + ')')
    db_statement.author_uid = db_anonymous.uid
    if not __transfer_textversion_to_new_author(statement_uid, db_user.uid, db_anonymous.uid):
        return None, is_revoked, _tn.get(_.userIsNotAuthorOfStatement)

    is_revoked = True

    # # transfer the responsibility to the next author (NOW ANONYMOUS), who used this statement
    # db_statement_as_conclusion = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == statement_uid,
    #                                                                              Argument.is_supportive == True,
    #                                                                              Argument.author_uid != db_user.uid)).first()
    # db_votes = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid != db_user.uid,
    #                                                                 ClickedStatement.is_up_vote == True,
    #                                                                 ClickedStatement.is_valid == True)).first()
    # # search new author who supported this statement
    # if db_statement_as_conclusion or db_votes:  # TODO 197 DO WE REALLY WANT TO SET A NEW AUTHOR HERE?
    #     db_anonymous = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    #     new_author_uid = db_anonymous.uid  # db_statement_as_conclusion.author_uid
    #     logger('QueryHelper', '__revoke_statement', 'Statement ' + str(statement_uid) + ' has a new author ' + str(new_author_uid) + ' (old author ' + str(db_user.uid) + ')')
    #     db_statement.author_uid = new_author_uid
    #     __transfer_textversion_to_new_author(statement_uid, db_user.uid, new_author_uid)
    #     is_revoked = False
    # else:
    #     logger('QueryHelper', '__revoke_statement',
    #            'Statement ' + str(statement_uid) + ' will be revoked (old author ' + str(db_user.uid) + ') and all arguments with this statement, cause we have no new author')
    #     db_statement.set_disable(True)
    #     __disable_textversions(statement_uid, db_user.uid)
    #     __remove_user_from_arguments_with_statement(statement_uid, db_user, _tn)
    #     is_revoked = True

    DBDiscussionSession.add(db_statement)
    DBDiscussionSession.flush()
    transaction.commit()

    return db_statement, is_revoked, ''


def __disable_textversions(statement_uid, author_uid):
    """
    Disables the textversions of the given statement

    :param statement_uid: Statement.uid
    :param author_uid: User.uid
    :return: None
    """
    db_textversion = DBDiscussionSession.query(TextVersion).filter(and_(TextVersion.statement_uid == statement_uid,
                                                                        TextVersion.author_uid == author_uid)).all()
    for textversion in db_textversion:
        logger('QueryHelper', '__disable_textversions', str(textversion.uid))
        textversion.set_disable(True)
        DBDiscussionSession.add(textversion)

    DBDiscussionSession.flush()
    transaction.commit()


def __transfer_textversion_to_new_author(statement_uid, old_author_uid, new_author_uid):
    """
    Sets a new author for the given textversion and creates a row in RevokedContentHistory

    :param statement_uid: Statement.uid
    :param old_author_uid: User.uid
    :param new_author_uid: User.uid
    :return: Boolean
    """
    logger('QueryHelper', '__revoke_statement', 'Textversion of {} will change author from {} to {}'.format(statement_uid, old_author_uid, new_author_uid))
    db_textversion = DBDiscussionSession.query(TextVersion).filter(and_(TextVersion.statement_uid == statement_uid,
                                                                        TextVersion.author_uid == old_author_uid)).all()
    if not db_textversion:
        return False

    for textversion in db_textversion:
        textversion.author_uid = new_author_uid
        DBDiscussionSession.add(textversion)
        DBDiscussionSession.add(RevokedContentHistory(old_author_uid, new_author_uid, textversion_uid=textversion.uid))

    DBDiscussionSession.flush()
    transaction.commit()

    return True


def __remove_user_from_arguments_with_statement(statement_uid, db_user, _tn):
    """
    Calls revoke_content(...) for all arguments, where the Statement.uid is used

    :param statement_uid: Statement.uid
    :param db_user: User
    :param _tn: Translator
    :return: None
    """
    logger('QueryHelper', '__remove_user_from_arguments_with_statement', '{} with user{}'.format(statement_uid, db_user.uid))
    db_arguments = get_all_arguments_by_statement(statement_uid, True)
    for arg in db_arguments:
        if arg.author_uid == db_user.uid:
            revoke_content(arg.uid, True, db_user.nickname, _tn)


def get_default_locale_name(request):
    try:
        if request and 'pyramid.default_locale_name' in request.registry.settings:
            return request.registry.settings['pyramid.default_locale_name']
    except KeyError:
        return 'en'
    return 'en'
