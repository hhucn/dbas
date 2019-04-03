import logging
from os import environ
from typing import List, Tuple, Dict, Any, Optional

import transaction
from sqlalchemy import func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Statement, TextVersion, MarkedStatement, \
    sql_timestamp_pretty_print, Argument, Premise, PremiseGroup, SeenStatement, StatementToIssue
from dbas.decidotron.lib import add_associated_cost, to_cents
from dbas.handler import user, notification as nh
from dbas.handler.voting import add_seen_argument, add_seen_statement
from dbas.helper.relation import set_new_undermine_or_support_for_pgroup, set_new_support, set_new_undercut, \
    set_new_rebut
from dbas.helper.url import UrlManager
from dbas.input_validator import is_integer
from dbas.lib import get_profile_picture, escape_string, Relations, Attitudes
from dbas.review.queue import Code
from dbas.review.queue.edit import EditQueue
from dbas.review.reputation import add_reputation_for, has_access_to_review_system, get_reason_by_action, \
    ReputationReasons
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio

LOG = logging.getLogger(__name__)


def set_position(db_user: User, db_issue: Issue, statement_text: str, feature_data: dict = {}) -> dict:
    """
    Set new position for current discussion and returns collection with the next url for the discussion.

    :param statement_text: The text of the new position statement.
    :param db_issue: The issue which gets the new position
    :param db_user: The user who sets the new position.
    :param feature_data: More data which is used by additional features
    :rtype: dict
    :return: Prepared collection with statement_uids of the new positions and next url or an error
    """
    LOG.debug("%s", statement_text)

    user.update_last_action(db_user)

    new_statement: Statement = insert_as_statement(statement_text, db_user, db_issue, is_start=True)

    if db_issue.decision_process:
        if 'decidotron_cost' not in feature_data:
            transaction.abort()
            LOG.error('Cost missing for an issue with a decision_process')
            return {
                'status': 'fail',  # best error management
                'error': 'Cost missing for an issue with a decision_process'
            }
        else:
            cost = to_cents(float(feature_data['decidotron_cost']))

            if 0 <= cost <= db_issue.decision_process.budget and not db_issue.decision_process.position_ended():
                add_associated_cost(db_issue, new_statement, cost)
            else:
                transaction.abort()
                LOG.error(
                    'Cost has to be 0 <= cost <= {}. (In cents). cost is: '.format(db_issue.decision_process.budget,
                                                                                   cost))
                return {
                    'status': 'fail',
                    'error': 'Cost has to be 0 <= cost <= {}. (In cents)'.format(db_issue.decision_process.budget)
                }

    _um = UrlManager(db_issue.slug)
    url = _um.get_url_for_statement_attitude(new_statement.uid)
    rep_added = add_reputation_for(db_user, get_reason_by_action(ReputationReasons.first_position))
    had_access = has_access_to_review_system(db_user)
    if not rep_added:
        add_reputation_for(db_user, get_reason_by_action(ReputationReasons.new_statement))
    broke_limit = has_access_to_review_system(db_user) and not had_access
    if broke_limit:
        url += '#access-review'

    return {
        'status': 'success',
        'url': url,
        'statement_uids': [new_statement.uid],
        'error': ''
    }


def set_positions_premise(db_issue: Issue, db_user: User, db_conclusion: Statement, premisegroups: List[List[str]],
                          supportive: bool, history: str, mailer) -> dict:
    """
    Set new premise for a given position and returns dictionary with url for the next step of the discussion

    :param mailer:
    :param history:
    :param supportive:
    :param premisegroups:
    :param db_conclusion:
    :param db_user:
    :param db_issue:
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and an url or an error
    """
    user.update_last_action(db_user)

    prepared_dict = __process_input_of_start_premises(premisegroups, db_conclusion, supportive, db_issue, db_user)
    if prepared_dict['error']:
        return prepared_dict

    __set_url_of_start_premises(prepared_dict, db_conclusion, supportive, db_issue, db_user, history, mailer)
    __add_reputation(db_user, db_issue, prepared_dict['url'], prepared_dict)

    return prepared_dict


def __add_reputation(db_user: User, db_issue: Issue, url: str, prepared_dict: dict):
    """

    :param db_user:
    :param db_issue:
    :param url:
    :param prepared_dict:
    :return:
    """
    had_access = has_access_to_review_system(db_user)
    rep_added = add_reputation_for(db_user, get_reason_by_action(ReputationReasons.first_justification))
    if not rep_added:
        add_reputation_for(db_user, get_reason_by_action(ReputationReasons.new_statement))
    broke_limit = has_access_to_review_system(db_user) and not had_access
    if broke_limit:
        _t = Translator(db_issue.lang)
        send_request_for_info_popup_to_socketio(db_user.nickname, _t.get(_.youAreAbleToReviewNow), '/review')
        prepared_dict['url'] = '{}{}'.format(url, '#access-review')


def set_correction_of_statement(elements, db_user, translator) -> dict:
    """
    Adds a proposal for a statements correction and returns info if the proposal could be set

    :param elements: List of dicts with text and uids for proposals of edits for new statements
    :param db_user: User
    :param translator: Translator
    :rtype: dict
    :return: Dictionary with info and/or error
    """
    db_user.update_last_action()

    review_count = len(elements)
    added_reviews = [EditQueue().add_edit_reviews(db_user, el['uid'], el['text']) for el in elements]

    if added_reviews.count(Code.SUCCESS) == 0:  # no edits set
        if added_reviews.count(Code.DOESNT_EXISTS) > 0:
            LOG.debug("Internal Key Error")
            return {
                'info': translator.get(_.internalKeyError),
                'error': True
            }
        if added_reviews.count(Code.DUPLICATE) > 0:
            LOG.debug("Already edit proposals")
            return {
                'info': translator.get(_.alreadyEditProposals),
                'error': True
            }
        LOG.debug("No corrections given")
        return {
            'info': translator.get(_.noCorrections),
            'error': True
        }

    DBDiscussionSession.flush()
    transaction.commit()

    added_values = [EditQueue().add_edit_values_review(db_user, el['uid'], el['text']) for el in elements]
    if Code.SUCCESS not in added_values:
        return {
            'info': translator.get(_.alreadyEditProposals),
            'error': True
        }
    DBDiscussionSession.flush()
    transaction.commit()

    msg = ''
    if review_count > added_values.count(Code.SUCCESS) \
            or added_reviews.count(Code.SUCCESS) != added_values.count(Code.SUCCESS):
        msg = translator.get(_.alreadyEditProposals)
    return {
        'error': False,
        'info': msg
    }


def set_seen_statements(uids, path, db_user) -> dict:
    """
    Marks several statements as already seen.

    :param uids: Uids of statements which should be marked as seen
    :param path: Current path of the user
    :param db_user: User
    :rtype: dict
    :return: Dictionary with an error field
    """
    # are the statements connected to an argument?
    if 'justify' in path:
        url = path[path.index('justify/') + len('justify/'):]
        additional_argument = int(url[:url.index('/')])
        add_seen_argument(additional_argument, db_user)

    for uid in uids:
        # we get the premise group id's only
        if is_integer(uid):
            add_seen_statement(uid, db_user)
    return {'status': 'success'}


def get_logfile_for_statements(uids, lang, main_page):
    """
    Returns the logfile for the given statement uid

    :param uids: requested statement uid
    :param lang: ui_locales ui_locales
    :param main_page: URL
    :return: dictionary with the logfile-rows
    """
    LOG.debug("Enter get_logfile_for_statements with uids: %s", uids)

    main_dict = dict()
    for uid in uids:
        db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(
            TextVersion.uid.asc()).all()
        if len(db_textversions) == 0:
            continue
        return_dict = dict()
        content_dict = dict()
        # add all corrections
        for index, version in enumerate(db_textversions):
            content_dict[str(index)] = __get_logfile_dict(version, main_page, lang)
        return_dict['content'] = content_dict
        statement = DBDiscussionSession.query(Statement).get(uid)
        main_dict[statement.get_text()] = return_dict

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
    corr_dict['author'] = str(db_author.global_nickname)
    corr_dict['author_url'] = main_page + '/user/' + str(db_author.uid)
    corr_dict['author_gravatar'] = get_profile_picture(db_author, 20)
    corr_dict['date'] = sql_timestamp_pretty_print(textversion.timestamp, lang)
    corr_dict['text'] = str(textversion.content)
    return corr_dict


def insert_as_statement(text: str, db_user: User, db_issue: Issue, is_start=False) -> Statement:
    """
    Inserts the given text as statement and returns the uid

    :param text: String
    :param db_user: User
    :param db_issue: Issue
    :param is_start: Boolean
    :return: Statement
    """
    new_statement, is_duplicate = set_statement(text, db_user, is_start, db_issue)

    # add marked statement
    DBDiscussionSession.add(MarkedStatement(statement=new_statement.uid, user=db_user.uid))
    DBDiscussionSession.add(SeenStatement(statement_uid=new_statement.uid, user_uid=db_user.uid))

    return new_statement


def set_statement(text: str, db_user: User, is_position: bool, db_issue: Issue) -> Tuple[Statement, bool]:
    """
    Saves statement for user

    :param text: given statement
    :param db_user: User of given user
    :param is_position: if it is a start statement
    :param db_issue: Issue
    :return: Statement, is_duplicate or -1, False on error
    """

    LOG.debug("User_id: %s, text: %s, issue: %s", db_user.uid, text, db_issue.uid)

    # escaping and cleaning
    text = escape_string(' '.join(text.strip().split()))
    _tn = Translator(db_issue.lang)
    if text.startswith(_tn.get(_.because).lower() + ' '):
        text = text[len(_tn.get(_.because) + ' '):]
    while text.endswith(('.', '?', '!', ',')):
        text = text[:-1]

    # check, if the text already exists
    db_dupl = __check_duplicate(db_issue, text)
    if db_dupl:
        return db_dupl, True

    db_statement = __add_statement(is_position)
    __add_textversion(text, db_user.uid, db_statement.uid)
    __add_statement2issue(db_statement.uid, db_issue.uid)

    return db_statement, False


def __check_duplicate(db_issue: Issue, text: str) -> Optional[Statement]:
    """
    Check if there is already a textversion with the given text. If true the statement2issue relation will be
    checked and set and the duplicate (Statement) returned

    :param db_issue: related Issue
    :param text: the text
    :return:
    """
    db_tv = DBDiscussionSession.query(TextVersion).filter(func.lower(TextVersion.content) == text.lower()).first()
    if not db_tv:
        return None

    db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter(
        StatementToIssue.issue_uid == db_issue.uid,
        StatementToIssue.statement_uid == db_tv.statement_uid).all()

    if not db_statement2issue:
        __add_statement2issue(db_tv.statement_uid, db_issue.uid)

    db_statement = DBDiscussionSession.query(Statement).get(db_tv.statement_uid)
    return db_statement


def __add_statement(is_position: bool) -> Statement:
    """
    Adds a new statement to the database

    :param is_position: True if the statement should be a position
    :return: New statement object
    """
    db_statement = Statement(is_position=is_position)
    DBDiscussionSession.add(db_statement)
    DBDiscussionSession.flush()
    return db_statement


def __add_textversion(text: str, user_uid: int, statement_uid: int) -> TextVersion:
    """
    Adds a new statement to the database

    :param text: content of the textversion
    :param user_uid: uid of the author
    :param statement_uid: id of the related statement
    :return: New textversion object
    """
    db_textversion = TextVersion(content=text, author=user_uid, statement_uid=statement_uid)
    DBDiscussionSession.add(db_textversion)
    DBDiscussionSession.flush()
    return db_textversion


def __add_statement2issue(statement_uid: int, issue_uid: int) -> StatementToIssue:
    """
    Adds a new statement to issue link to the database

    :param statement_uid: id of the related statement
    :param issue_uid: id of the related issue
    :return: New statement to issue object
    """
    db_statement2issue = StatementToIssue(statement=statement_uid, issue=issue_uid)
    DBDiscussionSession.add(db_statement2issue)
    DBDiscussionSession.flush()
    return db_statement2issue


def __is_conclusion_in_premisegroups(premisegroups: list, db_conclusion: Statement) -> bool:
    for premisegroup in premisegroups:
        if any([db_conclusion.get_textversion().content.lower() in pg.lower() for pg in premisegroup]):
            return True
    return False


def __process_input_of_start_premises(premisegroups, db_conclusion: Statement, supportive, db_issue: Issue,
                                      db_user: User) -> Dict[str, Any]:
    """
    Inserts premises of groups as new arguments in dependence of the input parameters and returns a URL for forwarding.

    :param premisegroups: [[String, ..], ...]
    :param db_conclusion: Statement
    :param supportive: Boolean
    :param db_issue: Issue
    :param db_user: User
    :return: URL, [Statement.uid], String
    """
    LOG.debug("Entering __process_input_of_start_premises with # of premisegroups: %s", len(premisegroups))
    _tn = Translator(db_issue.lang)

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    new_statement_uids = []  # all statement uids are stored in this list to create the link to a possible reference
    if __is_conclusion_in_premisegroups(premisegroups, db_conclusion):
        return {
            'argument_uids': new_argument_uids,
            'statement_uids': new_statement_uids,
            'error': _tn.get(_.premiseAndConclusionAreEqual)
        }

    for premisegroup in premisegroups:  # premise groups is a list of lists
        new_argument, statement_uids = __create_argument_by_raw_input(db_user, premisegroup, db_conclusion, supportive,
                                                                      db_issue)

        new_argument_uids.append(new_argument.uid)
        new_statement_uids.append(statement_uids)

    error = None
    if len(new_argument_uids) == 0:
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = environ.get('MIN_LENGTH_OF_STATEMENT', 10)
        error = '{} ({}: {})'.format(a, b, c)

    return {
        'argument_uids': new_argument_uids,
        'statement_uids': new_statement_uids,
        'error': error
    }


def __set_url_of_start_premises(prepared_dict: dict, db_conclusion: Statement, supportive: bool, db_issue: Issue,
                                db_user: User, history, mailer):
    LOG.debug("Entering __set_url_of_start_premises")

    # arguments=0: empty input
    # arguments=1: deliver new url
    # arguments>1: deliver url where the user has to choose between her inputs
    _um = UrlManager(db_issue.slug, history)
    _main_um = UrlManager(db_issue.slug, history=history)
    new_argument_uids = prepared_dict['argument_uids']

    if len(new_argument_uids) == 1:
        url = _um.get_url_for_new_argument(new_argument_uids)

    else:
        pgroups = [DBDiscussionSession.query(Argument).get(arg_uid).premisegroup_uid for arg_uid in new_argument_uids]
        url = _um.get_url_for_choosing_premisegroup(pgroups)

    # send notifications and mails
    email_url = _main_um.get_url_for_justifying_statement(db_conclusion.uid,
                                                          Attitudes.AGREE if supportive else Attitudes.DISAGREE)
    nh.send_add_text_notification(email_url, db_conclusion.uid, db_user, mailer)
    prepared_dict['url'] = url


def insert_new_premises_for_argument(premisegroup: List[str], current_attack, arg_uid, db_issue: Issue, db_user: User):
    """
    Creates premises for a given argument

    :param premisegroup: List of strings
    :param current_attack: String
    :param arg_uid: Argument.uid
    :param db_issue: Issue
    :param db_user: User
    :return: Argument
    """
    LOG.debug("Entering insert_new_premises_for_argument with arg_uid: %s", arg_uid)

    statements = []
    for premise in premisegroup:
        statement = insert_as_statement(premise, db_user, db_issue)
        statements.append(statement)

    # set the new statements as premise group and get current user as well as current argument
    new_pgroup = set_statements_as_new_premisegroup(statements, db_user, db_issue)
    current_argument = DBDiscussionSession.query(Argument).get(arg_uid)

    new_argument = None
    if current_attack == Relations.UNDERMINE:
        new_argument = set_new_undermine_or_support_for_pgroup(new_pgroup.uid, current_argument, False, db_user,
                                                               db_issue)

    elif current_attack == Relations.SUPPORT:
        new_argument, duplicate = set_new_support(new_pgroup.uid, current_argument, db_user, db_issue)

    elif current_attack == Relations.UNDERCUT:
        new_argument, duplicate = set_new_undercut(new_pgroup.uid, current_argument, db_user, db_issue)

    elif current_attack == Relations.REBUT:
        new_argument, duplicate = set_new_rebut(new_pgroup.uid, current_argument, db_user, db_issue)

    if not new_argument:
        LOG.debug("No statement or any premise = conclusion")
        return Translator(db_issue.lang).get(_.premiseAndConclusionAreEqual)

    LOG.debug("Returning argument %s", new_argument.uid)
    return new_argument


def set_statements_as_new_premisegroup(statements: List[Statement], db_user: User, db_issue: Issue):
    """
    Set the given statements together as new premise group

    :param statements: [Statement]
    :param db_user: User
    :param db_issue: Issue
    :return: PremiseGroup.uid
    """
    LOG.debug("User: %s, statement: %s, issue: %s", db_user.uid, [s.uid for s in statements], db_issue.uid)
    # check for duplicate
    all_groups = []
    for statement in statements:
        # get the premise
        db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
        if db_premise:
            # getting all groups, where the premise is member
            db_premisegroup = DBDiscussionSession.query(Premise).filter_by(
                premisegroup_uid=db_premise.premisegroup_uid).all()
            groups = set()
            for group in db_premisegroup:
                groups.add(group.premisegroup_uid)
            all_groups.append(groups)
    # if every set in this array has one common member, they are all in the same group
    if len(all_groups) > 0:
        intersec = set.intersection(*all_groups)
        for group in intersec:
            db_premise = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=group).all()
            if len(db_premise) == len(statements):
                return DBDiscussionSession.query(PremiseGroup).get(group)

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

    return db_premisegroup


def __create_argument_by_raw_input(db_user: User, premisegroup: [str], db_conclusion: Statement, is_supportive,
                                   db_issue: Issue) \
        -> Tuple[Optional[Argument], List[int]]:
    """
    Consumes the input to create a new argument

    :param db_user: User
    :param premisegroup: String
    :param db_conclusion: Statement
    :param is_supportive: Boolean
    :param db_issue: Issue
    :return:
    """
    LOG.debug("Entering __create_argument_by_raw_input with premisegroup %s, conclusion %s in issue %s",
              premisegroup, db_conclusion.uid, db_issue.uid)

    new_statements = []

    for text in premisegroup:
        statement = insert_as_statement(text, db_user, db_issue)
        new_statements.append(statement)

    # second, set the new statements as premisegroup
    new_premisegroup = set_statements_as_new_premisegroup(new_statements, db_user, db_issue)
    LOG.debug("New pgroup %s", new_premisegroup.uid)

    # third, insert the argument
    new_argument = __create_argument_by_uids(db_user, new_premisegroup.uid, db_conclusion.uid, None, is_supportive,
                                             db_issue)
    transaction.commit()

    return new_argument, [s.uid for s in new_statements]


def __create_argument_by_uids(db_user: User, premisegroup_uid, conclusion_uid, argument_uid, is_supportive,
                              db_issue: Issue) -> Optional[Argument]:
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
    LOG.debug("Entering __create_argument_by_uids with user: %s, premisegroup_uid: %s, conclusion_uid :%s, "
              "argument_uid: %s, is_supportive: %s, issue: %s",
              db_user.nickname, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, db_issue.uid)

    new_argument = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == premisegroup_uid,
                                                              Argument.is_supportive == is_supportive,
                                                              Argument.conclusion_uid == conclusion_uid,
                                                              Argument.issue_uid == db_issue.uid).first()
    if not new_argument:
        new_argument = Argument(premisegroup=premisegroup_uid, is_supportive=is_supportive, author=db_user.uid,
                                issue=db_issue.uid, conclusion=conclusion_uid)
        new_argument.set_conclusions_argument(argument_uid)

        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()

        new_argument = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == premisegroup_uid,
                                                                  Argument.is_supportive == is_supportive,
                                                                  Argument.author_uid == db_user.uid,
                                                                  Argument.conclusion_uid == conclusion_uid,
                                                                  Argument.argument_uid == argument_uid,
                                                                  Argument.issue_uid == db_issue.uid).first()
    transaction.commit()
    if new_argument:
        LOG.debug("Argument was inserted")
        return new_argument
    else:
        LOG.debug("Argument was not inserted")
        return None
