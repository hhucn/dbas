"""
Provides helping function for getting some opinions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, VoteArgument, VoteStatement, Premise, ArgumentSeenBy, Settings, StatementSeenBy
from dbas.helper.relation import RelationHelper
from dbas.lib import sql_timestamp_pretty_print, get_text_for_statement_uid, get_text_for_argument_uid,\
    get_text_for_premisesgroup_uid, get_profile_picture, get_text_for_conclusion
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import TextGenerator
from dbas.strings.translator import Translator
from sqlalchemy import and_


class OpinionHandler:
    """
    Provides function for getting users with the same opinons as the user
    """

    def __init__(self, lang, nickname, mainpage):
        """

        :param self.lang: ui_locales ui_locales
        :param self.nickname: self.nickname
        :param self.mainpage: URL
        :return: None
        """
        self.lang = lang
        self.nickname = nickname
        self.mainpage = mainpage

    def get_user_and_opinions_for_argument(self, argument_uids, attack=None):
        """
        Returns nested dictionary with all kinds of attacks for the argument as well as the users who are supporting
        these attacks.

        :param argument_uids: Argument.uid
        :return: { 'attack_type': { 'message': 'string', 'users': [{'self.nickname': 'string', 'avatar_url': 'url' 'vote_timestamp': 'string' ], ... }],...}
        """

        logger('OpinionHandler', 'get_user_and_opinions_for_argument', 'Arguments ' + str(argument_uids))
        db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
        db_user_uid = db_user.uid if db_user else 0

        # preparation
        all_users = []
        _t = Translator(self.lang)
        _tg = TextGenerator(self.lang)
        try:
            db_user_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[0]).first()
        except TypeError:
            return None
        db_syst_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[1]).first()

        # sanity check
        if not db_user_argument or not db_syst_argument:
            ret_dict = dict()
            ret_dict['message'] = _t.get(_.internalError) + '.'
            ret_dict['users'] = all_users
            ret_dict['opinions'] = ret_dict
            ret_dict['title'] = _t.get(_.internalError)
            return ret_dict

        title = _t.get(
            _.reaction)  # For) + ': ' + get_text_for_argument_uid(argument_uids[0], with_html_tag=True, attack_type='for_modal')

        # getting uids of all reactions
        _rh = RelationHelper(argument_uids[0], self.lang)

        arg_uids_for_reactions = [
            _rh.get_undermines_for_argument_uid(),
            _rh.get_supports_for_argument_uid(),
            _rh.get_undercuts_for_argument_uid(),
            _rh.get_rebuts_for_argument_uid()
        ]

        relation = ['undermine', 'support', 'undercut', 'rebut']

        # getting the text of all reactions
        db_tmp_argument = db_syst_argument
        while db_tmp_argument.argument_uid and not db_tmp_argument.conclusion_uid:
            db_tmp_argument = DBDiscussionSession.query(Argument).filter_by(uid=db_tmp_argument.argument_uid).first()

        first_conclusion = get_text_for_statement_uid(db_tmp_argument.conclusion_uid)
        first_conclusion = first_conclusion[0:1].lower() + first_conclusion[1:]

        if not attack:
            relation_text = _tg.get_relation_text_dict_with_substitution(False, True, db_user_argument.is_supportive,
                                                                         first_conclusion=first_conclusion,
                                                                         attack_type=attack)
        else:
            if attack == 'undercut':
                db_argument0 = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[0]).first()
                db_argument1 = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[1]).first()
                premises, trash = get_text_for_premisesgroup_uid(db_argument1.premisesgroup_uid)
                conclusion = get_text_for_conclusion(db_argument0)
            else:
                db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[1]).first()
                premises, trash = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
                conclusion = get_text_for_conclusion(db_argument)

                intro = ''
                if not db_argument.is_supportive:
                    forr = _t.get(_.forText)
                    the = _t.get(_.the_die)
                    intro = forr + ' ' + the + ' '
                rejection = _t.get(_.strongerStatementForRecjecting2)
                of = _t.get(_.strongerStatementForRecjecting3)
                conclusion = intro + rejection + ' ' + of  + conclusion

            relation_text = _tg.get_relation_text_dict_without_substitution(False, True, db_user_argument.is_supportive,
                                                                            first_conclusion=first_conclusion,
                                                                            attack_type=attack, premise=premises,
                                                                            conclusion=conclusion)
            relation_text['rebut_text'] = relation_text['rebut_text'].replace(_t.get(_.accepting), _t.get(_.forThat))

        # getting votes for every reaction
        ret_list = self.__get_votes_for_reactions(relation, arg_uids_for_reactions, relation_text, db_user_uid, _t)

        return {'opinions': ret_list, 'title': title[0:1].upper() + title[1:]}

    def __get_votes_for_reactions(self, relation, arg_uids_for_reactions, relation_text, db_user_uid, _t):
        """

        :param relation:
        :param arg_uids_for_reactions:
        :param relation_text:
        :param db_user_uid:
        :param _t:
        :return:
        """
        ret_list = []

        for rel in relation:
            all_users       = []
            message         = ''
            seen_by         = 0

            for uid in arg_uids_for_reactions[relation.index(rel)]:
                db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == uid['id'],
                                                                               VoteArgument.is_up_vote == True,
                                                                               VoteArgument.is_valid == True,
                                                                               VoteArgument.author_uid != db_user_uid)).all()

                for vote in db_votes:
                    voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
                    users_dict = self.create_users_dict(voted_user, vote.timestamp)
                    all_users.append(users_dict)

                if len(db_votes) == 0:
                    message = _t.get(_.voteCountTextMayBeFirst) + '.'
                elif len(db_votes) == 1:
                    message = _t.get(_.voteCountTextOneOther) + '.'
                else:
                    message = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextMore) + '.'
                db_seen_by = DBDiscussionSession.query(ArgumentSeenBy).filter_by(argument_uid=int(uid['id'])).all()
                seen_by += len(db_seen_by) if db_seen_by else 0

            ret_list.append({'users': all_users,
                             'message': message,
                             'text': relation_text[rel + '_text'],
                             'seen_by': seen_by})
        return ret_list

    def get_user_with_same_opinion_for_statements(self, statement_uids, is_supportive):
        """
        Returns nested dictionary with all kinds of information about the votes of the statements.

        :param statement_uids: Statement.uid
        :param is_supportive: Boolean
        :return: {'users':[{self.nickname1.avatar_url, self.nickname1.vote_timestamp}*]}
        """
        logger('OpinionHandler', 'get_user_with_same_opinion_for_statements', 'Statement ' + str(statement_uids))
        db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
        db_user_uid = db_user.uid if db_user else 0

        opinions = []
        _t = Translator(self.lang)
        title = _t.get(_.informationForStatements)

        for uid in statement_uids:
            statement_dict = dict()
            all_users = []
            db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
            if not db_statement:
                statement_dict['uid']       = None
                statement_dict['text']      = None
                statement_dict['message']   = None
                statement_dict['users']     = None
                statement_dict['seen_by']   = None

            statement_dict['uid'] = str(uid)
            text = get_text_for_statement_uid(uid)
            try:
                text = text[0:1].upper() + text[1:]
                if db_statement.is_startpoint and self.lang == 'de':
                    text = _t.get(_.statementIsAbout) + ' ' + text
                statement_dict['text'] = text
            except TypeError:
                statement_dict['uid']       = None
                statement_dict['text']      = None
                statement_dict['message']   = None
                statement_dict['users']     = None
                statement_dict['seen_by']   = None

            if is_supportive is not None:
                is_supportive = True if str(is_supportive) == 'True' else False
            else:
                is_supportive = False

            db_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == uid,
                                                                            VoteStatement.is_up_vote == is_supportive,
                                                                            VoteStatement.is_valid == True,
                                                                            VoteStatement.author_uid != db_user_uid)).all()

            for vote in db_votes:
                voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
                users_dict = self.create_users_dict(voted_user, vote.timestamp)
                all_users.append(users_dict)
            statement_dict['users'] = all_users

            if len(db_votes) == 0:
                statement_dict['message'] = _t.get(_.voteCountTextMayBeFirst) + '.'
            elif len(db_votes) == 1:
                statement_dict['message'] = _t.get(_.voteCountTextOneOther) + '.'
            else:
                statement_dict['message'] = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextMore) + '.'

            db_seen_by = DBDiscussionSession.query(StatementSeenBy).filter_by(statement_uid=int(uid)).all()
            statement_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0

            opinions.append(statement_dict)

        return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

    def get_user_with_same_opinion_for_premisegroups(self, argument_uids):
        """
        Returns nested dictionary with all kinds of information about the votes of the premisegroups.

        :param argument_uids: Argument.uid
        :return: {'users':[{self.nickname1.avatar_url, self.nickname1.vote_timestamp}*]}
        """
        logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'Arguments ' + str(argument_uids))
        db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
        db_user_uid = db_user.uid if db_user else 0

        opinions = []
        _t = Translator(self.lang)
        title = _t.get(_.informationForStatements)

        for uid in argument_uids:
            logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'argument ' + str(uid))
            statement_dict = dict()
            all_users = []
            db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
            if not db_premises:
                statement_dict['uid']       = None
                statement_dict['text']      = None
                statement_dict['message']   = None
                statement_dict['users']     = None
                statement_dict['seen_by']   = None

            statement_dict['uid'] = str(uid)
            text, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
            statement_dict['text'] = _t.get(_.because) + ' ' + text

            db_votes = []
            for premise in db_premises:
                logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'group ' + str(uid) +
                       ' premises statement ' + str(premise.statement_uid))
                db_votes += DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == premise.statement_uid,
                                                                                 VoteStatement.is_up_vote == True,
                                                                                 VoteStatement.is_valid == True,
                                                                                 VoteStatement.author_uid != db_user_uid)).all()

            for vote in db_votes:
                voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
                users_dict = self.create_users_dict(voted_user, vote.timestamp)
                all_users.append(users_dict)
            statement_dict['users'] = all_users

            if len(db_votes) == 0:
                statement_dict['message'] = _t.get(_.voteCountTextMayBeFirst) + '.'
            elif len(db_votes) == 1:
                statement_dict['message'] = _t.get(_.voteCountTextOneOther) + '.'
            else:
                statement_dict['message'] = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextMore) + '.'

            db_seen_by = DBDiscussionSession.query(ArgumentSeenBy).filter_by(argument_uid=int(uid)).all()
            statement_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0

            opinions.append(statement_dict)

        return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

    def get_user_with_same_opinion_for_argument(self, argument_uid):
        """
        Returns nested dictionary with all kinds of information about the votes of the argument.

        :param argument_uid: Argument.uid
        :return: {'users':[{self.nickname1.avatar_url, self.nickname1.vote_timestamp}*]}
        """
        try:
            logger('OpinionHandler', 'get_user_with_same_opinion_for_argument', 'Argument ' + str(argument_uid) + ' ' + get_text_for_argument_uid(argument_uid, 'de'))
        except TypeError:
            return None
        db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
        db_user_uid = db_user.uid if db_user else 0

        opinions = dict()
        all_users = []
        _t = Translator(self.lang)
        text = get_text_for_argument_uid(argument_uid, self.lang)
        title = _t.get(_.reactionFor) + ': ' + text[0:1].upper() + text[1:]

        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
        if not db_argument:
            opinions['uid']       = None
            opinions['text']      = None
            opinions['message']   = None
            opinions['users']     = None
            opinions['seen_by']   = None

        opinions['uid'] = str(argument_uid)
        text = get_text_for_argument_uid(argument_uid, self.lang)
        opinions['text'] = text[0:1].upper() + text[1:]

        db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
                                                                       VoteArgument.is_up_vote == True,
                                                                       VoteArgument.is_valid == True,
                                                                       VoteArgument.author_uid != db_user_uid)).all()

        for vote in db_votes:
            voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
            users_dict = self.create_users_dict(voted_user, vote.timestamp)
            all_users.append(users_dict)
        opinions['users'] = all_users

        if len(db_votes) == 0:
            opinions['message'] = _t.get(_.voteCountTextMayBeFirst) + '.'
        elif len(db_votes) == 1:
            opinions['message'] = _t.get(_.voteCountTextOneOther) + '.'
        else:
            opinions['message'] = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextMore) + '.'

        db_seen_by = DBDiscussionSession.query(ArgumentSeenBy).filter_by(argument_uid=int(argument_uid)).all()
        opinions['seen_by'] = len(db_seen_by) if db_seen_by else 0

        return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

    def get_user_with_opinions_for_attitude(self, statement_uid):
        """
        Returns dictionary with agree- and disagree-votes

        :param statement_uid: Statement.uid
        :return:
        """

        logger('OpinionHandler', 'get_user_with_opinions_for_attitude', 'Statement ' + str(statement_uid))
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
        _t = Translator(self.lang)
        text = get_text_for_statement_uid(statement_uid)
        try:
            title = _t.get(_.attitudeFor) + ': ' + text[0:1].upper() + text[1:]
        except TypeError:
            return None

        ret_dict = dict()

        if not db_statement:
            ret_dict = {'text': None, 'agree': None, 'disagree': None, 'agree_users': [], 'disagree_users': [], 'title': title[0:1].upper() + title[1:]}

        text = get_text_for_statement_uid(statement_uid)
        ret_dict['text'] = text[0:1].upper() + text[1:]
        ret_dict['agree'] = None
        ret_dict['disagree'] = None

        db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
        db_user_uid = db_user.uid if db_user else 0

        db_pro_votes = DBDiscussionSession.query(VoteStatement).filter(
            and_(VoteStatement.statement_uid == statement_uid,
                 VoteStatement.is_up_vote == True,
                 VoteStatement.is_valid == True,
                 VoteStatement.author_uid != db_user_uid)).all()

        db_con_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement_uid,
                                                                            VoteStatement.is_up_vote == False,
                                                                            VoteStatement.is_valid == True,
                                                                            VoteStatement.author_uid != db_user_uid)).all()
        pro_array = []
        for vote in db_pro_votes:
            voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
            users_dict = self.create_users_dict(voted_user, vote.timestamp)
            pro_array.append(users_dict)
        ret_dict['agree_users'] = pro_array
        ret_dict['agree_text'] = _t.get(_.iAgreeWith)

        con_array = []
        for vote in db_con_votes:
            voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
            users_dict = self.create_users_dict(voted_user, vote.timestamp)
            con_array.append(users_dict)
        ret_dict['disagree_users'] = con_array
        ret_dict['disagree_text'] = _t.get(_.iDisagreeWith)

        ret_dict['title'] = title[0:1].upper() + title[1:]

        db_seen_by = DBDiscussionSession.query(StatementSeenBy).filter_by(statement_uid=int(statement_uid)).all()
        ret_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0

        return ret_dict

    def create_users_dict(self, db_user, timestamp):
        """
        Creates dictionary with self.nickname, url and timestamp

        :param db_user: User
        :param timestamp: SQL Timestamp
        :return: dict()
        """
        db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
        name = db_user.nickname if db_settings.should_show_public_nickname else db_user.public_nickname
        return {'nickname': name,
                'public_profile_url': self.mainpage + '/user/' + name,
                'avatar_url': get_profile_picture(db_user),
                'vote_timestamp': sql_timestamp_pretty_print(timestamp, self.lang)}

    @staticmethod
    def get_infos_about_argument(uid, mainpage):
        """
        Returns several infos about the argument.

        :param uid: Argument.uid
        :param mainpage: url
        :return: dict()
        """
        return_dict = dict()
        db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == uid,
                                                                       VoteArgument.is_valid == True,
                                                                       VoteStatement.is_up_vote == True)).all()
        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
        if not db_argument:
            return return_dict

        db_author = DBDiscussionSession.query(User).filter_by(uid=db_argument.author_uid).first()
        return_dict['vote_count'] = str(len(db_votes))
        return_dict['author'] = db_author.public_nickname
        return_dict['timestamp'] = sql_timestamp_pretty_print(db_argument.timestamp, db_argument.lang)
        text = get_text_for_argument_uid(uid)
        return_dict['text'] = text[0:1].upper() + text[1:] + '.'

        supporters = []
        gravatars = dict()
        public_page = dict()
        for vote in db_votes:
            db_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
            name = db_user.get_global_nickname()
            supporters.append(name)
            gravatars[name] = get_profile_picture(db_user)
            public_page[name] = mainpage + '/user/' + name

        return_dict['supporter'] = supporters
        return_dict['gravatars'] = gravatars
        return_dict['public_page'] = public_page

        return return_dict
