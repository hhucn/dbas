import transaction
from sqlalchemy import and_, func

import dbas.review.helper.queues as review_queue_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Statement, TextVersion, MarkedStatement, \
    sql_timestamp_pretty_print, Argument, Premise, PremiseGroup, SeenStatement
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
        nickname = data['nickname']
        statement = data['statement']
        issue_id = data['issue_id']
        issue_db = DBDiscussionSession.query(Issue).get(issue_id)
        slug = issue_db.slug
        discussion_lang = data.get('discussion_lang', issue_db.lang)
        default_locale_name = data.get('default_locale_name', discussion_lang)
        application_url = data['application_url']
    except KeyError as e:
        logger('StatementsHelper', 'position', repr(e), error=True)
        _tn = Translator('en')
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    # escaping will be done in StatementsHelper().set_statement(...)
    user.update_last_action(nickname)
    _tn = Translator(discussion_lang)

    if DBDiscussionSession.query(Issue).get(issue_id).is_read_only:
        return {'error': _tn.get(_.discussionIsReadOnly), 'statement_uids': ''}

    new_statement = insert_as_statements(application_url, default_locale_name, statement, nickname, issue_id,
                                         discussion_lang, is_start=True)
    prepared_dict = {'error': '', 'statement_uids': ''}

    if new_statement == -1:
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = _tn.get(_.eachStatement)
        error = '{} ({}: {} {})'.format(a, b, 10, c)
        prepared_dict['error'] = error
        return prepared_dict

    if new_statement == -2:
        prepared_dict['error'] = _tn.get(_.noRights)
        return prepared_dict

    url = UrlManager(application_url, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
    prepared_dict['url'] = url
    prepared_dict['statement_uids'] = [new_statement[0].uid]

    # add reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_position)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        url += '#access-review'
        prepared_dict['url'] = url

    return prepared_dict


def set_positions_premise(for_api, data) -> dict:
    """
    Set new premise for a given position and returns dictionary with url for the next step of the discussion

    :param for_api: boolean if requests came via the API
    :param data: dict of requests data
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    prepared_dict = dict()

    try:
        nickname = data['nickname']
        premisegroups = data['statement']
        issue_id = data['issue_id']
        conclusion_id = data['conclusion_id']
        supportive = data['supportive']
        application_url = data['application_url']
        history = data.get('history')
        port = data.get('port')
        mailer = data.get('mailer')
        discussion_lang = data.get('discussion_lang', DBDiscussionSession.query(Issue).get(issue_id).lang)
        default_locale_name = data.get('default_locale_name', discussion_lang)
    except KeyError as e:
        logger('StatementsHelper', 'positions_premise', repr(e), error=True)
        _tn = Translator('en')
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    # escaping will be done in StatementsHelper().set_statement(...)
    user.update_last_action(nickname)

    _tn = Translator('discussion_lang')
    if DBDiscussionSession.query(Issue).get(issue_id).is_read_only:
        return {'error': _tn.get(_.discussionIsReadOnly), 'statement_uids': ''}

    url, statement_uids, error = __process_input_of_start_premises_and_receive_url(default_locale_name, premisegroups,
                                                                                   conclusion_id, supportive, issue_id,
                                                                                   nickname, for_api, application_url,
                                                                                   discussion_lang, history, port,
                                                                                   mailer)

    prepared_dict['error'] = error
    prepared_dict['statement_uids'] = statement_uids

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


def correct_statement(user, uid, corrected_text):
    """
    Corrects a statement

    :param user: User.nickname requesting user
    :param uid: requested statement uid
    :param corrected_text: new text
    :return: dict()
    """
    logger('StatementsHelper', 'correct_statement', 'def ' + str(uid))

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

    if not db_user:
        return -1

    while corrected_text.endswith(('.', '?', '!')):
        corrected_text = corrected_text[:-1]

    # duplicate check
    return_dict = dict()
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(TextVersion.uid.desc()).all()

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
        db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(TextVersion.uid.asc()).all()  # TODO #432
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
    for text in input_list:
        if len(text) < statement_min_length:
            return -1

        new_statement, is_duplicate = set_statement(text, user, is_start, issue, lang)
        if not new_statement:
            continue

        statements.append(new_statement)

        # add marked statement
        DBDiscussionSession.add(MarkedStatement(statement=new_statement.uid, user=db_user.uid))
        DBDiscussionSession.add(SeenStatement(statement_uid=new_statement.uid, user_uid=db_user.uid))
        DBDiscussionSession.flush()

        if is_duplicate:
            continue

        _tn = Translator(new_statement.lang)
        db_issue = DBDiscussionSession.query(Issue).get(issue)
        _um = UrlManager(application_url, db_issue.slug)
        append_action_to_issue_rss(issue_uid=issue,
                                   author_uid=db_user.uid,
                                   title=_tn.get(_.positionAdded if is_start else _.statementAdded),
                                   description='...' + get_text_for_statement_uid(new_statement.uid) + '...',
                                   ui_locale=default_locale_name,
                                   url=_um.get_url_for_statement_attitude(False, new_statement.uid))

    return statements


def set_statement(text, nickname, is_start, issue, lang):
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

    logger('StatementsHelper', 'set_statement', 'user: ' + str(nickname) + ', user_id: ' + str(db_user.uid) +
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

    # add text
    statement = Statement(is_position=is_start, issue=issue)
    DBDiscussionSession.add(statement)
    DBDiscussionSession.flush()

    # add textversion
    textversion = TextVersion(content=text, author=db_user.uid, statement_uid=statement.uid)
    DBDiscussionSession.add(textversion)
    DBDiscussionSession.flush()

    transaction.commit()
    return statement, False


def __process_input_of_start_premises_and_receive_url(default_locale_name, premisegroups, conclusion_id, supportive,
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
    logger('StatementsHelper', '__process_input_of_start_premises_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    _tn = Translator(discussion_lang)
    if not db_user:
        return '', '', _tn.get(_.userNotFound)

    slug = DBDiscussionSession.query(Issue).get(issue).slug
    error = ''
    url = ''

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    new_statement_uids = []  # all statement uids are stored in this list to create the link to a possible reference
    for group in premisegroups:  # premise groups is a list of lists
        new_argument, statement_uids = __create_argument_by_raw_input(application_url, default_locale_name, user, group,
                                                                      conclusion_id, supportive, issue, discussion_lang)
        if not isinstance(new_argument, Argument):  # break on error
            if error is -1:
                error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength), statement_min_length)
            else:
                error = '{}'.format(_tn.get(_.premiseAndConclusionAreEqual))
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
        error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength), statement_min_length)

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
        NotificationHelper.send_add_text_notification(email_url, conclusion_id, user, port, mailer)

    return url, new_statement_uids, error


def insert_new_premises_for_argument(application_url, default_locale_name, text, current_attack, arg_uid, issue, user,
                                     discussion_lang):
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
    logger('StatementsHelper', 'insert_new_premises_for_argument', 'def')
    current_argument = DBDiscussionSession.query(Argument).get(arg_uid)

    statements = insert_as_statements(application_url, default_locale_name, text, user, issue, discussion_lang)
    if statements == -1 or not current_argument or current_argument and any([s.uid == current_argument.conclusion.uid for s in statements]):
        logger('StatementsHelper', 'insert_new_premises_for_argument', 'No statement or any premise = conclusion')
        return -1

    # set the new statements as premise group and get current user as well as current argument
    new_pgroup = set_statements_as_new_premisegroup(statements, user, issue)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

    new_argument = None
    if current_attack == 'undermine':
        new_argument = set_new_undermine_or_support_for_pgroup(new_pgroup.uid, current_argument, False, db_user, issue)

    elif current_attack == 'support':
        new_argument, duplicate = set_new_support(new_pgroup.uid, current_argument, db_user, issue)

    elif current_attack == 'undercut':
        new_argument, duplicate = set_new_undercut(new_pgroup.uid, current_argument, db_user, issue)

    elif current_attack == 'rebut':
        new_argument, duplicate = set_new_rebut(new_pgroup.uid, current_argument, db_user, issue)

    logger('StatementsHelper', 'insert_new_premises_for_argument', 'Returning argument ' + str(new_argument.uid))
    return new_argument


def set_statements_as_new_premisegroup(statements, user, issue):
    """
    Set the given statements together as new premise group

    :param statements: [Statement.uid]
    :param user: User.nickname
    :param issue: Issue
    :return: PremiseGroup.uid
    """
    logger('StatementsHelper', 'set_statements_as_new_premisegroup', 'user: ' + str(user) +
           ', statement: ' + str([s.uid for s in statements]) + ', issue: ' + str(issue))
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
                return DBDiscussionSession.query(PremiseGroup).get(group)

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

    return db_premisegroup


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
    logger('StatementsHelper', '__create_argument_by_raw_input', 'main with text ' + str(text) + ' as premisegroup, ' +
           'conclusion ' + str(conclusion_id) + ' in issue ' + str(issue))
    # current conclusion
    db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                     Statement.issue_uid == issue)).first()
    statements = insert_as_statements(application_url, default_locale_name, text, user, issue, discussion_lang)
    if statements == -1:
        return -1, None

    statement_uids = [s.uid for s in statements]

    # second, set the new statements as premisegroup
    new_premisegroup = set_statements_as_new_premisegroup(statements, user, issue)
    logger('StatementsHelper', '__create_argument_by_raw_input', 'new pgroup ' + str(new_premisegroup.uid))

    # sanity check whether any premise and the conclusion are the same
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=new_premisegroup.uid).all()
    for premise in db_premises:
        if premise.statement_uid is db_conclusion.uid:
            logger('StatementsHelper', '__create_argument_by_uids', 'One premise and conclusion are the same', error=True)
            return -2, None

    # third, insert the argument
    new_argument = __create_argument_by_uids(user, new_premisegroup, db_conclusion.uid, None, is_supportive, issue)
    transaction.commit()

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if new_argument and db_user:
        _tn = Translator(default_locale_name)
        db_issue = DBDiscussionSession.query(Issue).get(issue)
        _um = UrlManager(application_url, db_issue.slug)
        append_action_to_issue_rss(issue_uid=issue,
                                   author_uid=db_user.uid,
                                   title=_tn.get(_.argumentAdded),
                                   description='...' + get_text_for_argument_uid(new_argument.uid, anonymous_style=True) + '...',
                                   ui_locale=default_locale_name,
                                   url=_um.get_url_for_justifying_statement(False, new_argument.uid, 'd'))

    return new_argument, statement_uids


def __create_argument_by_uids(user, premisegroup, conclusion_uid, argument_uid, is_supportive, issue):
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
    logger('StatementsHelper', '__create_argument_by_uids', 'main with user: ' + str(user) +
           ', premisegroup_uid: ' + str(premisegroup.uid) +
           ', conclusion_uid: ' + str(conclusion_uid) +
           ', argument_uid: ' + str(argument_uid) +
           ', is_supportive: ' + str(is_supportive) +
           ', issue: ' + str(issue))

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup.uid,
                                                                   Argument.is_supportive == is_supportive,
                                                                   Argument.conclusion_uid == conclusion_uid,
                                                                   Argument.issue_uid == issue)).first()
    if not new_argument:
        new_argument = Argument(premisegroup=premisegroup.uid, issupportive=is_supportive, author=db_user.uid,
                                conclusion=conclusion_uid, issue=issue)
        new_argument.set_conclusions_argument(argument_uid)

        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()

        new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup.uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.author_uid == db_user.uid,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.argument_uid == argument_uid,
                                                                       Argument.issue_uid == issue)).first()
    transaction.commit()
    if new_argument:
        logger('StatementsHelper', '__create_argument_by_uids', 'argument was inserted')
        return new_argument
    else:
        logger('StatementsHelper', '__create_argument_by_uids', 'argument was not inserted')
        return None
