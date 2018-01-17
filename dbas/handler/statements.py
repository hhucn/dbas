from typing import List, Tuple, Dict, Union

import transaction
from sqlalchemy import and_, func

import dbas.review.helper.queues as review_queue_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Statement, TextVersion, MarkedStatement, \
    sql_timestamp_pretty_print, Argument, Premise, PremiseGroup, SeenStatement
from dbas.exceptions import StatementToShort
from dbas.handler import user, notification as NotificationHelper
from dbas.handler.rss import append_action_to_issue_rss
from dbas.handler.voting import add_seen_argument, add_seen_statement
from dbas.helper.query import statement_min_length
from dbas.helper.relation import set_new_undermine_or_support_for_pgroup, set_new_support, set_new_undercut, \
    set_new_rebut
from dbas.input_validator import is_integer
from dbas.lib import get_text_for_statement_uid, get_profile_picture, escape_string, get_text_for_argument_uid
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_position, \
    rep_reason_first_justification, rep_reason_new_statement
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager, get_url_for_new_argument
from websocket.lib import send_request_for_info_popup_to_socketio


def set_position(for_api, data) -> dict:
    """
    Set new position for current discussion and returns collection with the next url for the discussion.

    :param for_api: boolean if requests came via the API
    :param data: dict of requests data
    :rtype: dict
    :return: Prepared collection with statement_uids of the new positions and next url or an error
    """
    try:
        statement = data['statement']
        db_user = data['user']
        db_issue = data['issue']
        default_locale_name = data.get('default_locale_name', db_issue.lang)
        application_url = data['application_url']
    except KeyError as e:
        logger('StatementsHelper', 'position', repr(e), error=True)
        _tn = Translator('en')
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    # escaping will be done in StatementsHelper().set_statement(...)
    user.update_last_action(db_user.nickname)
    _tn = Translator(db_issue.lang)

    if db_issue.is_read_only:
        return {'error': _tn.get(_.discussionIsReadOnly), 'statement_uids': ''}

    prepared_dict = {'error': '', 'statement_uids': ''}

    try:
        new_statement = insert_as_statement(application_url, default_locale_name, statement, db_user, db_issue,
                                            db_issue.lang, is_start=True)
    except StatementToShort as e:
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = _tn.get(_.eachStatement)
        error = '{} ({}: {} {})'.format(a, b, e.min_length, c)
        prepared_dict['error'] = error
        return prepared_dict

    url = UrlManager(application_url, db_issue.slug, for_api).get_url_for_statement_attitude(False,
                                                                                             new_statement.uid)
    prepared_dict['statement_uids'] = [new_statement.uid]

    # add reputation
    add_rep, broke_limit = add_reputation_for(db_user, rep_reason_first_position)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(db_user, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        url += '#access-review'

    prepared_dict['url'] = url

    return prepared_dict


def set_positions_premise(for_api: bool, data: Dict) -> dict:
    """
    Set new premise for a given position and returns dictionary with url for the next step of the discussion

    :param for_api: boolean if requests came via the API
    :param data: dict of requests data
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    try:
        nickname = data['nickname']
        premisegroups = data['statement']
        issue = data["issue"]
        conclusion_id = data['conclusion_id']
        supportive = data['supportive']
        application_url = data['application_url']
        history = data['history'] if '_HISTORY_' in data else None

        port = data.get('port')
        mailer = data.get('mailer')
        discussion_lang = data.get('discussion_lang', issue.lang)
        default_locale_name = data.get('default_locale_name', discussion_lang)

    except KeyError as e:
        logger('StatementsHelper', 'positions_premise', repr(e), error=True)
        _tn = Translator('en')
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    # escaping will be done in StatementsHelper().set_statement(...)

    user.update_last_action(nickname)

    _tn = Translator('discussion_lang')
    if issue.is_read_only:
        return {'error': _tn.get(_.discussionIsReadOnly), 'statement_uids': ''}

    url, statement_uids, error = '', '', _tn.get(_.userNotFound)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        url, statement_uids, error = __process_input_of_start_premises_and_receive_url(default_locale_name,
                                                                                       premisegroups,
                                                                                       conclusion_id, supportive,
                                                                                       issue,
                                                                                       db_user, for_api,
                                                                                       application_url,
                                                                                       discussion_lang, history, port,
                                                                                       mailer)

    prepared_dict = {'error': error,
                     'statement_uids': statement_uids}

    # add reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_justification)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        _t = Translator(discussion_lang)
        send_request_for_info_popup_to_socketio(nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                '{}/review'.format(application_url))
        prepared_dict['url'] = '{}{}'.format(url, '#access-review')

    if url == -1:
        return prepared_dict

    prepared_dict['url'] = url
    return prepared_dict


def set_correction_of_statement(elements, nickname, ui_locales) -> dict:
    """
    Adds a proposol for a statements correction and returns info if the proposal could be set

    :param elements: List of dicts with text and uids for proposals of edits for new statements
    :param nickname: Nickname of current user
    :param ui_locales: Language of current users session
    :rtype: dict
    :return: Dictionary with info and/or error
    """
    prepared_dict = dict()
    user.update_last_action(nickname)
    _tn = Translator(ui_locales)

    msg, error = review_queue_helper.add_proposals_for_statement_corrections(elements, nickname, _tn)
    prepared_dict['error'] = msg if error else ''
    prepared_dict['info'] = msg if len(msg) > 0 else ''

    return prepared_dict


def set_seen_statements(uids, path, nickname, ui_locales) -> dict:
    """
    Marks several statements as already seen.

    :param uids: Uids of statements which should be marked as seen
    :param path: Current path of the user
    :param nickname: Users nickname
    :param ui_locales: Current language
    :rtype: dict
    :return: Dictionary with an error field
    """
    # are the statements connected to an argument?
    additional_argument = None
    _tn = Translator(ui_locales)
    if 'justify' in path:
        url = path[path.index('justify/') + len('justify/'):]
        additional_argument = int(url[:url.index('/')])

    error_code = process_seen_statements(uids, nickname, additional_argument=additional_argument)
    error = '' if error_code is None else _tn.get(error_code)
    return {'error': error}


def process_seen_statements(uids, nickname, additional_argument=None):
    """
    Sets the given statement uids as seen by given user

    :param uids: [Statement.uid]
    :param nickname: User.nickname
    :param additional_argument: Argument.uid
    :return: String
    """
    logger('StatementsHelper', 'process_seen_statements', 'user ' + str(nickname) + ', statements ' + str(uids) +
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


def correct_statement(db_user, uid, corrected_text):
    """
    Corrects a statement

    :param user: User.nickname requesting user
    :param uid: requested statement uid
    :param corrected_text: new text
    :return: dict()
    """
    logger('StatementsHelper', 'correct_statement', 'def ' + str(uid))

    while corrected_text.endswith(('.', '?', '!')):
        corrected_text = corrected_text[:-1]

    # duplicate check
    return_dict = dict()
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(
        TextVersion.uid.desc()).all()

    # not a duplicate?
    if not db_textversion:
        textversion = TextVersion(content=corrected_text, author=db_user.uid)
        textversion.set_statement(db_statement.uid)
        DBDiscussionSession.add(textversion)
        DBDiscussionSession.flush()

    # if request:
    #     NotificationHelper.send_edit_text_notification(db_user, textversion, url, request)

    # transaction.commit() # # 207

    return_dict['uid'] = uid
    return_dict['text'] = corrected_text
    return return_dict


def get_logfile_for_statements(uids, lang, main_page):
    """
    Returns the logfile for the given statement uid

    :param uids: requested statement uid
    :param lang: ui_locales ui_locales
    :param main_page: URL
    :return: dictionary with the logfile-rows
    """
    logger('StatementsHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uids))

    main_dict = dict()
    for uid in uids:
        db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(
            TextVersion.uid.asc()).all()  # TODO #432
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


def __get_logfile_dict(textversion: TextVersion, main_page: str, lang: str) -> Dict:
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


def insert_as_statement(application_url: str, default_locale_name: str, text: str, db_user: User,
                        db_issue: Issue, lang: str, is_start=False) -> Statement:
    """
        Inserts the given text as statement and returns the uid

        :param lang: Language
        :param application_url: Url of the app itself
        :param default_locale_name: default lang of the app
        :param text: String
        :param db_user: User
        :param db_issue: Issue
        :param is_start: Boolean
        :return: Statement
        """
    if len(text) < statement_min_length:
        raise StatementToShort(text, statement_min_length)

    new_statement, is_duplicate = set_statement(text, db_user, is_start, db_issue, lang)

    # add marked statement
    DBDiscussionSession.add(MarkedStatement(statement=new_statement.uid, user=db_user.uid))
    DBDiscussionSession.add(SeenStatement(statement_uid=new_statement.uid, user_uid=db_user.uid))
    DBDiscussionSession.flush()

    if is_duplicate:
        pass

    _tn = Translator(new_statement.lang)
    _um = UrlManager(application_url, db_issue.slug)
    append_action_to_issue_rss(db_issue=db_issue,
                               db_author=db_user,
                               title=_tn.get(_.positionAdded if is_start else _.statementAdded),
                               description='...' + get_text_for_statement_uid(new_statement.uid) + '...',
                               ui_locale=default_locale_name,
                               url=_um.get_url_for_statement_attitude(False, new_statement.uid))

    return new_statement


def insert_as_statements(application_url: str, default_locale_name: str, text_list: List[str], db_user: User,
                         db_issue: Issue, lang: str, is_start=False) -> List[Statement]:
    """
    Inserts the given texts as statements and returns the uid's

    :param lang: Language
    :param application_url: Url of the app itself
    :param default_locale_name: default lang of the app
    :param text_list: [String]
    :param db_user: User
    :param db_issue: Issue
    :param is_start: Boolean
    :return: [Statement]
    """

    return [insert_as_statement(application_url, default_locale_name, text, db_user, db_issue, lang, is_start) for text
            in text_list]


def set_statement(text: str, db_user: User, is_start: bool, db_issue: Issue, lang) -> Tuple[Statement, bool]:
    """
    Saves statement for user

    :param lang:
    :param text: given statement
    :param db_user: User of given user
    :param is_start: if it is a start statement
    :param db_issue: Issue
    :return: Statement, is_duplicate or -1, False on error
    """

    logger('StatementsHelper', 'set_statement', 'user: ' + str(db_user.nickname) + ', user_id: ' + str(db_user.uid) +
           ', text: ' + str(text) + ', issue: ' + str(db_issue.uid))

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
    db_duplicate = DBDiscussionSession.query(TextVersion).filter(
        func.lower(TextVersion.content) == text.lower()).first()
    if db_duplicate:
        db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == db_duplicate.statement_uid,
                                                                        Statement.issue_uid == db_issue.uid)).one()
        return db_statement, True

    # add text
    statement = Statement(is_position=is_start, issue=db_issue.uid)
    DBDiscussionSession.add(statement)
    DBDiscussionSession.flush()

    # add textversion
    textversion = TextVersion(content=text, author=db_user.uid, statement_uid=statement.uid)
    DBDiscussionSession.add(textversion)
    DBDiscussionSession.flush()

    transaction.commit()
    return statement, False


def __process_input_of_start_premises_and_receive_url(default_locale_name, premisegroups, conclusion_id, supportive,
                                                      db_issue: Issue, db_user: User, for_api, application_url,
                                                      discussion_lang, history,
                                                      port, mailer):
    """
    Inserts the given text in premisegroups as new arguments in dependence of the input parameters and returns a URL for forwarding.

    :param default_locale_name: Default lang of the app
    :param premisegroups: [String]
    :param conclusion_id: Statement.uid
    :param supportive: Boolean
    :param issue_uid: Issue.uid
    :param user: User.nickname
    :param for_api: Boolean
    :param application_url: URL
    :param discussion_lang: ui_locales
    :param history: History of the user
    :param port: Port of the notification server
    :param mailer: Instance of pyramid mailer
    :return: URL, [Statement.uid], String
    """
    logger('StatementsHelper', '__process_input_of_start_premises_and_receive_url',
           'count of new pgroups: ' + str(len(premisegroups)))
    _tn = Translator(discussion_lang)

    error = ''
    url = ''

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    new_statement_uids = []  # all statement uids are stored in this list to create the link to a possible reference
    for group in premisegroups:  # premise groups is a list of lists
        new_argument, statement_uids = __create_argument_by_raw_input(application_url, default_locale_name, db_user,
                                                                      group, conclusion_id, supportive, db_issue,
                                                                      discussion_lang)
        if not new_argument:  # break on error
            error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength),
                                         statement_min_length)
            return -1, None, error

        new_argument_uids.append(new_argument.uid)
        if for_api:
            new_statement_uids.append(statement_uids)

    # #arguments=0: empty input
    # #arguments=1: deliver new url
    # #arguments>1: deliver url where the user has to choose between her inputs
    _um = UrlManager(application_url, db_issue.slug, for_api, history)
    _main_um = UrlManager(application_url, db_issue.slug, False, history)
    if len(new_argument_uids) == 0:
        error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength),
                                     statement_min_length)

    elif len(new_argument_uids) == 1:
        url = get_url_for_new_argument(new_argument_uids, history, discussion_lang, _um)

    else:
        pgroups = []
        for arg_uid in new_argument_uids:
            pgroups.append(DBDiscussionSession.query(Argument).get(arg_uid).premisesgroup_uid)
        url = _um.get_url_for_choosing_premisegroup(False, False, supportive, conclusion_id, pgroups)

    # send notifications and mails
    if len(new_argument_uids) > 0:
        email_url = _main_um.get_url_for_justifying_statement(False, conclusion_id, 't' if supportive else 'f')
        NotificationHelper.send_add_text_notification(email_url, conclusion_id, db_user, port, mailer)

    return url, new_statement_uids, error


def insert_new_premises_for_argument(application_url, default_locale_name, text, current_attack, arg_uid,
                                     db_issue: Issue, db_user: User,
                                     discussion_lang):
    """
    Creates premises for a given argument

    :param application_url: Url of the app itself
    :param default_locale_name: default lang of the app
    :param text: String
    :param current_attack: String
    :param arg_uid: Argument.uid
    :param db_issue: Issue
    :param db_user: User
    :return: Argument
    """
    logger('StatementsHelper', 'insert_new_premises_for_argument', 'def')

    statement = insert_as_statement(application_url, default_locale_name, text, db_user, db_issue,
                                    discussion_lang)

    # set the new statements as premise group and get current user as well as current argument
    new_pgroup_uid = set_statements_as_new_premisegroup([statement], db_user, db_issue)
    current_argument = DBDiscussionSession.query(Argument).get(arg_uid)

    new_argument = None
    if current_attack == 'undermine':
        new_argument = set_new_undermine_or_support_for_pgroup(new_pgroup_uid, current_argument, False, db_user,
                                                               db_issue)

    elif current_attack == 'support':
        new_argument, duplicate = set_new_support(new_pgroup_uid, current_argument, db_user, db_issue)

    elif current_attack == 'undercut' or current_attack == 'overbid':
        new_argument, duplicate = set_new_undercut(new_pgroup_uid, current_argument, db_user, db_issue)

    elif current_attack == 'rebut':
        new_argument, duplicate = set_new_rebut(new_pgroup_uid, current_argument, db_user, db_issue)

    logger('StatementsHelper', 'insert_new_premises_for_argument', 'Returning argument ' + str(new_argument.uid))
    return new_argument


def set_statements_as_new_premisegroup(statements: List[Statement], db_user: User, db_issue: Issue):
    """
    Set the given statements together as new premise group

    :param statements: [Statement]
    :param db_user: User
    :param db_issue: Issue
    :return: PremiseGroup.uid
    """
    logger('StatementsHelper', 'set_statements_as_new_premisegroup', 'user: ' + str(user) +
           ', statement: ' + str(statements) + ', issue: ' + str(db_issue.uid))

    # check for duplicate
    all_groups = []
    for statement in statements:
        # get the premise
        db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
        if db_premise:
            # getting all groups, where the premise is member
            db_premisegroup = DBDiscussionSession.query(Premise).filter_by(
                premisesgroup_uid=db_premise.premisesgroup_uid).all()
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
        premise = Premise(premisesgroup=premise_group.uid, statement=statement.uid, is_negated=False,
                          author=db_user.uid, issue=db_issue.uid)
        premise_list.append(premise)

    DBDiscussionSession.add_all(premise_list)
    DBDiscussionSession.flush()

    db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(
        PremiseGroup.uid.desc()).first()

    return db_premisegroup.uid


def __create_argument_by_raw_input(application_url, default_locale_name, db_user: User, text: str, conclusion_id,
                                   is_supportive, db_issue: Issue, discussion_lang) \
        -> Tuple[Union[Argument, None], List[int]]:
    """
    Consumes the input to create a new argument

    :param application_url: Url of the app itself
    :param default_locale_name: default lang of the app
    :param user: User.nickname
    :param text: String
    :param conclusion_id:
    :param is_supportive: Boolean
    :param db_issue: Issue
    :return:
    """
    logger('StatementsHelper', '__create_argument_by_raw_input', 'main with text ' + str(text) + ' as premisegroup, ' +
           'conclusion ' + str(conclusion_id) + ' in issue ' + str(db_issue.uid))
    # current conclusion
    db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                     Statement.issue_uid == db_issue.uid)).first()
    try:
        statement = insert_as_statement(application_url, default_locale_name, text, db_user, db_issue,
                                        discussion_lang)

        # second, set the new statements as premisegroup
        new_premisegroup_uid = set_statements_as_new_premisegroup([statement], db_user, db_issue)
        logger('StatementsHelper', '__create_argument_by_raw_input', 'new pgroup ' + str(new_premisegroup_uid))

        # third, insert the argument
        new_argument = __create_argument_by_uids(db_user, new_premisegroup_uid, db_conclusion.uid, None, is_supportive,
                                                 db_issue)
        transaction.commit()

        if new_argument:
            _tn = Translator(default_locale_name)
            _um = UrlManager(application_url, db_issue.slug)
            append_action_to_issue_rss(db_issue=db_issue,
                                       db_author=db_user,
                                       title=_tn.get(_.argumentAdded),
                                       description='...' + get_text_for_argument_uid(new_argument.uid,
                                                                                     anonymous_style=True) + '...',
                                       ui_locale=default_locale_name,
                                       url=_um.get_url_for_justifying_statement(False, new_argument.uid, 'd'))

        return new_argument, [statement.uid]
    except StatementToShort:
        raise


def __create_argument_by_uids(db_user: User, premisegroup_uid, conclusion_uid, argument_uid, is_supportive,
                              db_issue: Issue) -> Union[Argument, None]:
    """
    Connects the given id's to a new argument

    :param db_user: User.nickname
    :param premisegroup_uid: PremiseGroup.uid
    :param conclusion_uid: Statement.uid
    :param argument_uid: Argument.uid
    :param is_supportive: Boolean
    :param db_issue: Issue
    :return:
    """
    logger('StatementsHelper', '__create_argument_by_uids', 'main with user: ' + str(db_user.nickname) +
           ', premisegroup_uid: ' + str(premisegroup_uid) +
           ', conclusion_uid: ' + str(conclusion_uid) +
           ', argument_uid: ' + str(argument_uid) +
           ', is_supportive: ' + str(is_supportive) +
           ', issue: ' + str(db_issue.uid))

    new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                   Argument.is_supportive == is_supportive,
                                                                   Argument.conclusion_uid == conclusion_uid,
                                                                   Argument.issue_uid == db_issue.uid)).first()
    if not new_argument:
        new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid,
                                conclusion=conclusion_uid, issue=db_issue.uid)
        new_argument.set_conclusions_argument(argument_uid)

        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()

        new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.author_uid == db_user.uid,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.argument_uid == argument_uid,
                                                                       Argument.issue_uid == db_issue.uid)).first()
    transaction.commit()
    if new_argument:
        logger('StatementsHelper', '__create_argument_by_uids', 'argument was inserted')
        return new_argument
    else:
        logger('StatementsHelper', '__create_argument_by_uids', 'argument was not inserted')
        return None
