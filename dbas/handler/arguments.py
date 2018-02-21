import random

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Argument, Premise, MarkedArgument, ClickedArgument, \
    sql_timestamp_pretty_print, ClickedStatement, Statement
from dbas.handler import user, notification as NotificationHelper
from dbas.handler.statements import insert_new_premises_for_argument
from dbas.helper.query import statement_min_length
from dbas.input_validator import get_relation_between_arguments
from dbas.lib import get_all_arguments_with_text_and_url_by_statement_id, \
    get_profile_picture, get_text_for_argument_uid, resolve_issue_uid_to_slug
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for, rep_reason_new_statement, rep_reason_first_new_argument
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.helper.url import UrlManager


def set_arguments_premises(for_api, data) -> dict:
    """
    Set new premise for a given conclusion and returns dictionary with url for the next step of the discussion

    :param for_api: boolean if requests came via the API
    :param data: dict if requests came via the API
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    db_user = data['user']
    db_issue = data['issue']
    premisegroups = data['premisegroups']
    arg_uid = data['arg_uid']
    attack_type = data['attack_type']

    history = data.get('_HISTORY_')
    mailer = data.get('mailer')
    port = data.get('port')
    discussion_lang = db_issue.lang
    default_locale_name = data.get('default_locale_name', discussion_lang)

    application_url = data['application_url']

    # escaping will be done in QueryHelper().set_statement(...)
    langs = {'default_locale_name': default_locale_name, 'discussion_lang': discussion_lang}
    mail = {'mailer': mailer, 'port': port}
    arg_infos = {'arg_id': arg_uid, 'attack_type': attack_type, 'premisegroups': premisegroups, 'history': history}
    url, statement_uids, error = __process_input_premises_for_arguments_and_receive_url(langs, arg_infos, db_issue,
                                                                                        db_user, for_api,
                                                                                        application_url, mail)
    user.update_last_action(db_user)

    prepared_dict = {
        'error': error,
        'statement_uids': statement_uids
    }

    if url == -1:
        return prepared_dict

    # add reputation
    add_rep, broke_limit = add_reputation_for(db_user, rep_reason_first_new_argument)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(db_user, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        url += '#access-review'
        prepared_dict['url'] = url

    prepared_dict['url'] = url

    logger('ArgumentsHelper', 'set_new_premises_for_argument', 'returning {}'.format(prepared_dict))
    return prepared_dict


def get_all_infos_about_argument(db_argument, main_page, db_user, lang) -> dict:
    """
    Returns bunch of information about the given argument

    :param Argument: Argument
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
    return_dict['author'] = db_author.get_global_nickname()
    return_dict['author_url'] = main_page + '/user/' + str(db_author.uid)
    return_dict['gravatar'] = get_profile_picture(db_author)
    return_dict['timestamp'] = sql_timestamp_pretty_print(db_argument.timestamp, db_argument.lang)
    text = get_text_for_argument_uid(db_argument.uid)
    return_dict['text'] = text[0:1].upper() + text[1:] + '.'

    supporters = []
    gravatars = dict()
    public_page = dict()
    for vote in db_votes:
        db_author = DBDiscussionSession.query(User).get(vote.author_uid)
        name = db_author.get_global_nickname()
        if db_user.nickname == db_author.nickname:
            name += ' (' + _t.get(_.itsYou) + ')'
        supporters.append(name)
        gravatars[name] = get_profile_picture(db_author)
        public_page[name] = main_page + '/user/' + str(db_author.uid)

    return_dict['supporter'] = supporters
    return_dict['gravatars'] = gravatars
    return_dict['public_page'] = public_page

    return return_dict


def get_arguments_by_statement_uid(db_statement, application_url) -> dict:
    """
    Collects every argument which uses the given statement

    :param db_statement: Statement
    :param application_url: url of the application
    :rtype: dict
    :return: prepared collection with several arguments
    """
    slug = resolve_issue_uid_to_slug(db_statement.issue_uid)
    _um = UrlManager(application_url, slug)
    return {'arguments': get_all_arguments_with_text_and_url_by_statement_id(db_statement, _um, True, is_jump=True)}


def __process_input_premises_for_arguments_and_receive_url(langs, arg_infos, db_issue: Issue, db_user: User,
                                                           for_api, application_url, m):
    """
    Inserts given text in premisegroups as new arguments in dependence of the parameters and returns a URL

    .. note::

        Optimize the "for_api" part

    :param langs: dict with default_locale_name and discussion_lang
    :param arg_infos: dict with arg_id, attack_type, premisegroups and the history
    :param db_issue: Issue
    :param db_user: User
    :param for_api: Boolean
    :param application_url: URL
    :param m: dict with port and mailer
    :return: URL, [Statement.uids], String
    """
    default_locale_name = langs['default_locale_name']
    discussion_lang = langs['discussion_lang']
    arg_id = arg_infos['arg_id']
    attack_type = arg_infos['attack_type']
    premisegroups = arg_infos['premisegroups']
    history = arg_infos['history']

    logger('ArgumentsHelper', 'process_input_of_premises_for_arguments_and_receive_url',
           'count of new pgroups: ' + str(len(premisegroups)))
    _tn = Translator(discussion_lang)

    slug = db_issue.slug
    error = ''
    supportive = attack_type == 'support' or attack_type == 'overbid'

    # insert all premise groups into our database
    # all new arguments are collected in a list
    new_argument_uids = []
    for premisegroup in premisegroups:  # premise groups is a list of lists
        new_argument = insert_new_premises_for_argument(application_url, default_locale_name, premisegroup, attack_type,
                                                        arg_id, db_issue, db_user)
        if not isinstance(new_argument, Argument):  # break on error
            a = _tn.get(_.notInsertedErrorBecauseEmpty)
            b = _tn.get(_.minLength)
            c = str(statement_min_length)
            d = _tn.get(_.eachStatement)
            if isinstance(new_argument, str):
                error = new_argument
            else:
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
    # #arguments>1: deliver url where the nickname has to choose between her inputs
    _um = url = UrlManager(application_url, slug, for_api, history)
    if len(new_argument_uids) == 0:
        error = '{} ({}: {})'.format(_tn.get(_.notInsertedErrorBecauseEmpty), _tn.get(_.minLength),
                                     statement_min_length)

    elif len(new_argument_uids) == 1:
        url = _um.get_url_for_new_argument(new_argument_uids)

    else:
        url = __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, attack_type,
                                                                                    arg_id, _um, supportive)

    # send notifications and mails
    if len(new_argument_uids) > 0:
        # add marked arguments
        DBDiscussionSession.add_all([MarkedArgument(argument=uid, user=db_user.uid) for uid in new_argument_uids])
        DBDiscussionSession.flush()
        transaction.commit()

        new_uid = random.choice(new_argument_uids)  # TODO eliminate random
        attack = get_relation_between_arguments(arg_id, new_uid)

        tmp_url = _um.get_url_for_reaction_on_argument(arg_id, attack, new_uid)

        NotificationHelper.send_add_argument_notification(tmp_url, arg_id, db_user.nickname, m['port'], m['mailer'])

    return url, statement_uids, error


def __receive_url_for_processing_input_of_multiple_premises_for_arguments(new_argument_uids, attack_type, arg_id, _um,
                                                                          supportive):
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
        url = _um.get_url_for_choosing_premisegroup(False, supportive, db_statement.uid, pgroups)

    # relation to the arguments relation
    elif attack_type == 'undercut' or attack_type == 'overbid':
        url = _um.get_url_for_choosing_premisegroup(True, supportive, arg_id, pgroups)

    # relation to the arguments conclusion
    elif attack_type == 'rebut':
        # TODO WHAT IS WITH ARGUMENT AS CONCLUSION?
        is_argument = current_argument.conclusion_uid is not None
        uid = current_argument.argument_uid if is_argument else current_argument.conclusion_uid
        url = _um.get_url_for_choosing_premisegroup(False, is_argument, supportive, uid, pgroups)

    return url


def get_another_argument_with_same_conclusion(uid, history):
    """
    Returns another supporting/attacking argument with the same conclusion as the given Argument.uid

    :param uid: Argument.uid
    :param history: String
    :return: Argument
    """
    logger('ArgumentsHelper', 'get_another_argument_with_same_conclusion', str(uid))
    db_arg = DBDiscussionSession.query(Argument).get(uid)
    if not db_arg:
        return None

    if db_arg.conclusion_uid is None:
        return None

    # get forbidden uids
    splitted_histoy = history.split('-')
    forbidden_uids = [history.split('/')[2] for history in splitted_histoy if 'reaction' in history] + [uid]

    db_supports = DBDiscussionSession.query(Argument).filter(Argument.conclusion_uid == db_arg.conclusion_uid,
                                                             Argument.is_supportive == db_arg.is_supportive,
                                                             ~Argument.uid.in_(forbidden_uids)).all()
    if len(db_supports) == 0:
        return None

    return db_supports[random.randint(0, len(db_supports) - 1)]
