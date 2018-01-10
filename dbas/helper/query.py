"""
Provides helping function for database querys.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from pyshorteners import Shorteners, Shortener
from requests.exceptions import ReadTimeout, ConnectionError
from urllib3.exceptions import NewConnectionError
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, RevokedContent, \
    RevokedContentHistory, MarkedArgument, MarkedStatement, Settings, Language
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.handler import user
from dbas.handler.history import get_bubble_from_reaction_step, get_splitted_history
from dbas.helper.dictionary.bubbles import get_user_bubble_text_for_justify_statement
from dbas.helper.relation import get_rebuts_for_argument_uid, get_undermines_for_argument_uid, \
    get_undercuts_for_argument_uid, get_supports_for_argument_uid
from dbas.lib import get_text_for_premisesgroup_uid, pretty_print_options, is_author_of_argument, \
    is_author_of_statement, get_all_arguments_by_statement
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

statement_min_length = 10


def mark_statement_or_argument(uid, step, is_argument, is_supportive, should_mark, history, ui_loc, nickname) -> dict:
    """
    Marks statement or argument as current users opinion and returns status about the action

    :param uid: ID of statement or argument
    :param step: kind of step in current discussion
    :param is_argument: Boolean if the id is for an argument
    :param is_supportive: Boolean if the mark is supportive
    :param should_mark: Boolean if it should be (un-)marked
    :param history: Users history
    :param ui_loc: Current language
    :param nickname: Users nickname
    :rtype: dict
    :return: Dictionary with new text for the current bubble, where the user marked her opinion
    """
    _t = Translator(ui_loc)
    prepared_dict = __mark_or_unmark_it(uid, is_argument, should_mark, nickname, _t)
    prepared_dict['text'] = get_text_for_justification_or_reaction_bubble(uid, is_argument, is_supportive,
                                                                          nickname, step, history, _t)
    return prepared_dict


def __mark_or_unmark_it(uid, is_argument, should_mark, nickname, _t):
    """
    Marks or unmark an argument/statement, which represents the users opinion

    :param uid: Statement.uid / Argument.uid
    :param is_argument: Boolean
    :param should_mark: Boolean
    :param nickname: User.nickname
    :param _t: Translator
    :return: String, String
    """
    logger('QueryHelper', '__mark_or_unmark_it', '{} {} {}'.format(uid, is_argument, nickname))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return {'success': '', 'error': _t.get(_.internalError)}

    base_type = Argument if is_argument else Statement
    table = MarkedArgument if is_argument else MarkedStatement
    column = MarkedArgument.argument_uid if is_argument else MarkedStatement.statement_uid

    db_base = DBDiscussionSession.query(base_type).get(uid)
    if not db_base:
        return {'success': '', 'error': _t.get(_.internalError)}

    if should_mark:
        db_el = DBDiscussionSession.query(table).filter(column == uid).first()
        logger('QueryHelper', '__mark_or_unmark_it', 'Element is present{}'.format(' now' if db_el else ''))
        if not db_el:
            new_el = MarkedArgument(argument=uid, user=db_user.uid) if is_argument else MarkedStatement(statement=uid, user=db_user.uid)
            DBDiscussionSession.add(new_el)
    else:
        logger('QueryHelper', '__mark_or_unmark_it', 'Element is deleted')
        DBDiscussionSession.query(table).filter(column == uid).delete()

    DBDiscussionSession.flush()
    transaction.commit()

    return {'success': _t.get(_.opinionSaved), 'error': ''}


def set_user_language(nickname, ui_locales) -> dict:
    """
    Changes the users language of the web frontend

    :param nickname: the user's nickname creating the request
    :param ui_locales: current ui_locales
    :rtype: dict
    :return: prepared collection with status information
    """
    _tn = Translator(ui_locales)

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return {'error': _tn.get(_.checkNickname), 'ui_locales': ui_locales, 'current_lang': ''}

    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    if not db_settings:
        return {'error': _tn.get(_.checkNickname), 'ui_locales': ui_locales, 'current_lang': ''}

    db_language = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
    if not db_language:
        return {'error': _tn.get(_.internalError), 'ui_locales': ui_locales, 'current_lang': ''}

    current_lang = db_language.name
    db_settings.set_lang_uid(db_language.uid)
    transaction.commit()

    return {'error': '', 'ui_locales': ui_locales, 'current_lang': current_lang}


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
                                                                        TextVersion.author_uid == author_uid)).all()  # TODO #432
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
                                                                        TextVersion.author_uid == old_author_uid)).all()  # TODO #432
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


def get_default_locale_name(registry):
    return registry.settings.get('pyramid.default_locale_name', 'en')


def get_short_url(url, nickname, ui_locales) -> dict:
    """
    Shortens the url via external service.

    :param url: Url as string, which should be shortened
    :param nickname: current users nickname
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: dictionary with the url, services name and the url of the service or an error
    """
    user.update_last_action(nickname)

    try:
        service = Shorteners.TINYURL
        service_url = 'http://tinyurl.com/'
        shortener = Shortener(service)
        short_url = format(shortener.short(url))
    except (ReadTimeout, ConnectionError, NewConnectionError) as e:
        logger('getter', 'get_short_url', repr(e), error=True)
        _tn = Translator(ui_locales)
        prepared_dict = {'error': _tn.get(_.serviceNotAvailable)}
        return prepared_dict

    prepared_dict = dict()
    prepared_dict['url'] = short_url
    prepared_dict['service'] = service
    prepared_dict['service_url'] = service_url
    prepared_dict['error'] = ''

    return prepared_dict
