import logging
import random
import transaction
from os import environ
from typing import List, Tuple, Optional

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Argument, Premise, MarkedArgument, ClickedArgument, \
    sql_timestamp_pretty_print, ClickedStatement, Statement
from dbas.handler import notification as nh
from dbas.handler.statements import insert_new_premises_for_argument
from dbas.helper.url import UrlManager
from dbas.input_validator import get_relation_between_arguments
from dbas.lib import get_all_arguments_with_text_and_url_by_statement, get_profile_picture, Relations, \
    get_text_for_argument_uid
from dbas.review.reputation import add_reputation_for, has_access_to_review_system, get_reason_by_action, \
    ReputationReasons
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


def set_arguments_premises(db_issue: Issue, db_user: User, db_argument: Argument, premisegroups: List[List[str]],
                           attack_type: Relations, history, mailer) -> dict:
    """
    Set new premise for a given conclusion and returns dictionary with url for the next step of the discussion

    :param db_issue:
    :param db_user:
    :param db_argument:
    :param premisegroups:
    :param attack_type:
    :param history:
    :param mailer:
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    # escaping will be done in QueryHelper().set_statement(...)
    langs = {'default_locale_name': db_issue.lang, 'discussion_lang': db_issue.lang}
    arg_infos = {
        'arg_id': db_argument.uid,
        'attack_type': attack_type,
        'premisegroups': premisegroups,
        'history': history
    }
    url, statement_uids, error = __process_input_premises_for_arguments_and_receive_url(langs, arg_infos, db_issue,
                                                                                        db_user, mailer)

    prepared_dict = {
        'error': error,
        'statement_uids': statement_uids
    }

    if url is None:
        return prepared_dict

    # add reputation
    had_access = has_access_to_review_system(db_user)
    rep_added = add_reputation_for(db_user, get_reason_by_action(ReputationReasons.first_new_argument))
    if not rep_added:
        add_reputation_for(db_user, get_reason_by_action(ReputationReasons.new_statement))
    broke_limit = has_access_to_review_system(db_user) and not had_access
    if broke_limit:
        url += '#access-review'
        prepared_dict['url'] = url

    prepared_dict['url'] = url

    LOG.debug("Returning %s", prepared_dict)
    return prepared_dict


def get_all_infos_about_argument(db_argument: Argument, main_page, db_user, lang) -> dict:
    """
    Returns bunch of information about the given argument

    :param db_argument: The argument
    :param main_page: url of the application
    :param db_user: User
    :param lang: Language
    :rtype: dict
    :return: dictionary with many information or an error
    """
    _t = Translator(lang.ui_locales)

    return_dict = dict()
    db_votes = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.argument_uid == db_argument.uid,
                                                                 ClickedArgument.is_valid == True,
                                                                 ClickedStatement.is_up_vote == True).all()

    db_author = DBDiscussionSession.query(User).get(db_argument.author_uid)
    return_dict['vote_count'] = str(len(db_votes))
    return_dict['author'] = db_author.global_nickname
    return_dict['author_url'] = main_page + '/user/' + str(db_author.uid)
    return_dict['gravatar'] = get_profile_picture(db_author)
    return_dict['timestamp'] = sql_timestamp_pretty_print(db_argument.timestamp, db_argument.lang)
    text = get_text_for_argument_uid(db_argument.uid)
    return_dict['text'] = start_with_capital(text)

    supporters = []
    gravatars = dict()
    public_page = dict()
    for vote in db_votes:
        db_author = DBDiscussionSession.query(User).get(vote.author_uid)
        name = db_author.global_nickname
        if db_user.nickname == db_author.nickname:
            name += ' (' + _t.get(_.itsYou) + ')'
        supporters.append(name)
        gravatars[name] = get_profile_picture(db_author)
        public_page[name] = main_page + '/user/' + str(db_author.uid)

    return_dict['supporter'] = supporters
    return_dict['gravatars'] = gravatars
    return_dict['public_page'] = public_page

    return return_dict


def get_arguments_by_statement(statement: Statement, issue: Issue) -> dict:
    """
    Collects every argument which uses the given statement.

    :param statement: Statement which is used for query
    :param issue: Extract information for url manager from issue
    :rtype: dict
    :return: prepared collection with several arguments
    """
    _um = UrlManager(issue.slug)
    return {'arguments': get_all_arguments_with_text_and_url_by_statement(statement, _um, True, is_jump=True)}


def __process_input_premises_for_arguments_and_receive_url(langs: dict, arg_infos: dict, db_issue: Issue, db_user: User,
                                                           mailer) -> Tuple[Optional[str], Optional[List[int]], str]:
    """
    Inserts given text in premisegroups as new arguments in dependence of the parameters and returns a URL

    :param langs: dict with default_locale_name and discussion_lang
    :param arg_infos: dict with arg_id, attack_type, premisegroups and the history
    :param db_issue: Issue
    :param db_user: User
    :return: URL, [Statement.uids], String
    """
    discussion_lang = langs['discussion_lang']
    arg_id: int = arg_infos['arg_id']
    attack_type: str = arg_infos['attack_type']
    premisegroups = arg_infos['premisegroups']
    history = arg_infos['history']

    LOG.debug("Count of new pgroups: %s", len(premisegroups))
    _tn = Translator(discussion_lang)

    slug = db_issue.slug
    error = ''

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    for premisegroup in premisegroups:  # premise groups is a list of lists
        new_argument = insert_new_premises_for_argument(premisegroup, attack_type, arg_id, db_issue, db_user)
        if not isinstance(new_argument, Argument):  # break on error
            a = _tn.get(_.notInsertedErrorBecauseEmpty)
            b = _tn.get(_.minLength)
            c = environ.get('MIN_LENGTH_OF_STATEMENT', 10)
            d = _tn.get(_.eachStatement)
            if isinstance(new_argument, str):
                error = new_argument
            else:
                error = '{} ({}: {} {})'.format(a, b, c, d)
            return None, None, error

        new_argument_uids.append(new_argument.uid)

    statement_uids = []
    # @OPTIMIZE
    # Query all recently stored premises (internally: statements) and collect their ids
    # This is a bad workaround, let's just think about it in future.
    for uid in new_argument_uids:
        current_pgroup = DBDiscussionSession.query(Argument).get(uid).premisegroup_uid
        current_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=current_pgroup).all()
        for premise in current_premises:
            statement_uids.append(premise.statement_uid)

    # #arguments=0: empty input
    # #arguments=1: deliver new url
    # #arguments>1: deliver url where the nickname has to choose between her inputs
    _um = url = UrlManager(slug, history)
    if len(new_argument_uids) == 0:
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = environ.get('MIN_LENGTH_OF_STATEMENT', 10)
        error = '{} ({}: {})'.format(a, b, c)

    elif len(new_argument_uids) == 1:
        url = _um.get_url_for_new_argument(new_argument_uids)

    else:
        url = __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, _um)

    # send notifications and mails
    if len(new_argument_uids) > 0:
        # add marked arguments
        DBDiscussionSession.add_all([MarkedArgument(argument=uid, user=db_user.uid) for uid in new_argument_uids])
        DBDiscussionSession.flush()
        transaction.commit()

        new_uid = random.choice(new_argument_uids)  # TODO eliminate random
        attack = get_relation_between_arguments(arg_id, new_uid)

        tmp_url = _um.get_url_for_reaction_on_argument(arg_id, attack, new_uid)

        nh.send_add_argument_notification(tmp_url, arg_id, db_user.nickname, mailer)

    return url, statement_uids, error


def __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, _um) -> str:
    """
    Return the 'choose' url, when the user entered more than one premise for an argument

    :param new_argument_uids: [Argument.uid]
    :param _um: UrlManager
    :return: String
    """
    pgroups = [DBDiscussionSession.query(Argument).get(uid).premisegroup_uid for uid in new_argument_uids]
    return _um.get_url_for_choosing_premisegroup(pgroups)


def get_another_argument_with_same_conclusion(uid, history):
    """
    Returns another supporting/attacking argument with the same conclusion as the given Argument.uid

    :param uid: Argument.uid
    :param history: String
    :return: Argument
    """
    LOG.debug("%s", uid)
    db_arg = DBDiscussionSession.query(Argument).get(uid)
    if not db_arg:
        return None

    if db_arg.conclusion_uid is None:
        return None

    # get forbidden uids
    splitted_histoy = history.split('-')
    forbidden_uids = [history.split('/')[2] for history in splitted_histoy if 'reaction' in history] + [uid]

    db_supports = DBDiscussionSession.query(Argument).filter(Argument.conclusion_uid == db_arg.conclusion_uid,
                                                             Argument.uid != db_arg.uid,
                                                             Argument.is_supportive == db_arg.is_supportive,
                                                             ~Argument.uid.in_(forbidden_uids)).all()
    if len(db_supports) == 0:
        return None

    return db_supports[random.randint(0, len(db_supports) - 1)]


def get_all_statements_for_args(graph_arg_list) -> List[int]:
    """

    :param graph_arg_list:
    :return:
    """
    statement_uids = []

    for arg in graph_arg_list:
        # getting all premises of current argument
        db_premises = DBDiscussionSession.query(Premise).filter(Premise.premisegroup_uid == arg.premisegroup_uid,
                                                                Premise.is_disabled == False).all()

        # fetching statement ids for the premises
        statement_uids += [premise.statement_uid for premise in db_premises if
                           premise.statement_uid not in statement_uids]

        # querying the arguments conclusion
        while arg.conclusion_uid is None:
            arg = DBDiscussionSession.query(Argument).get(arg.argument_uid)

        if arg.conclusion_uid not in statement_uids:
            statement_uids.append(arg.conclusion_uid)

    return statement_uids
