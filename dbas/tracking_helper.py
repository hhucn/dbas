import collections

from .database import DBDiscussionSession
from .database.discussion_model import User, Relation, Track, Issue
from .logger import logger
from .query_helper import QueryHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class TrackingHelper(object):

	def save_track_for_user(self, transaction, user, statement_id, premisesgroup_uid, argument_uid, attacked_by_relation, attacked_with_relation, session_id):
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param statement_id: id of the clicked statement
		:param premisesgroup_uid: id of the clicked premiseGroup
		:param argument_uid:
		:param attacked_by_relation: id of attacked by relation
		:param attacked_with_relation: id of attacked_w th relation
		:return: undefined
		"""
		if user is None:
			user = 'anonymous'

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('BreadcrumbHelper', 'save_track_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid) +
														', statememt_id ' + str(statement_id) +
														', premisesgroup_uid ' + str(premisesgroup_uid) +
														', argument_uid ' + str(argument_uid) +
														', attacked_by_relation ' + str(attacked_by_relation) +
														', attacked_with_relation ' + str(attacked_with_relation) +
		                                                ', session_id ' + str(session_id))
		DBDiscussionSession.add(Track(user=db_user.uid, statement=statement_id, premisegroup=premisesgroup_uid, argument = argument_uid,
		                    attacked_by=attacked_by_relation, attacked_with=attacked_with_relation, session_id=session_id))
		transaction.commit()

	def get_track_of_user(self, user, lang):
		"""
		Returns the complete track of given user
		:param user: current user id
		:return: track os the user id as dict
		"""
		logger('BreadcrumbHelper', 'get_track_of_user', 'user ' + user)
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			logger('BreadcrumbHelper', 'get_track_of_user', 'no user')
			return dict()

		db_tracks = DBDiscussionSession.query(Track).filter_by(author_uid=db_user.uid).all()
		qh = QueryHelper()

		if not db_tracks:
			logger('BreadcrumbHelper', 'get_track_of_user', 'no track')
			return dict()

		return_dict = collections.OrderedDict()

		db_issues = DBDiscussionSession.query(Issue).all()

		for issue in db_issues:
			issue_dict = collections.OrderedDict()
			for index, track in enumerate(db_tracks):
				logger('BreadcrumbHelper','get_track_of_user','track uid ' + str(track.uid))

				track_dict = dict()

				# get attacks
				attacked_by_relation = DBDiscussionSession.query(Relation).filter_by(uid=track.attacked_by_relation).first()
				attacked_with_relation = DBDiscussionSession.query(Relation).filter_by(uid=track.attacked_with_relation).first()
				attacked_by_relation_id = qh.get_relation_uid_by_name(attacked_by_relation.name) if attacked_by_relation else 'None'
				attacked_with_relation_id = qh.get_relation_uid_by_name(attacked_with_relation.name) if attacked_with_relation else 'None'

				# get text
				attacked_by_relation_str = attacked_by_relation.name if attacked_by_relation else '-'
				attacked_with_relation_str = attacked_with_relation.name if attacked_with_relation else '-'
				track_statement = '-' if track.statement_uid == 0 else qh.get_text_for_statement_uid(track.statement_uid, issue.uid)
				track_argument = '-' if track.argument_uid == 0 else qh.get_text_for_argument_uid(track.argument_uid, issue.uid, lang)
				if track_argument:
					track_argument = track_argument[1:-1]

					if track.premisesGroup_uid == 0:
						track_premisesGroup = '-'
					else:
						track_premisesGroup,tash = qh.get_text_for_premisesGroup_uid(track.premisesGroup_uid, issue.uid)

					if track_statement:

						# text
						track_dict['statement']                  = track_statement
						track_dict['premisesGroup']             = track_premisesGroup
						track_dict['argument']                   = track_argument
						track_dict['attacked_by_relation']       = attacked_by_relation_str
						track_dict['attacked_with_relation']     = attacked_with_relation_str

						# ids
						track_dict['uid']                        = str(track.uid)
						track_dict['statement_uid']              = str(track.statement_uid)
						track_dict['premisesGroup_uid']         = str(track.premisesGroup_uid)
						track_dict['argument_uid']               = str(track.argument_uid)
						track_dict['attacked_by_relation_uid']   = attacked_by_relation_id
						track_dict['attacked_with_relation_uid'] = attacked_with_relation_id
						track_dict['timestamp']                  = str(track.timestamp)

						if not attacked_by_relation_str == '-':
							track_dict['text'] = 'Others say: \'' + track_argument + \
							                     '\' <i>' + attacked_by_relation_str + 's</i> \'' + \
							                     track_premisesGroup + '\''
						if not attacked_with_relation_str == '-':
							if track_premisesGroup == '-':
								track_dict['text'] = 'You will <i>' + attacked_with_relation_str + '</i> \'' + \
							                         track_argument + '\''
							else:
								track_dict['text'] = 'You say: \'' + track_premisesGroup + \
							                         '\' <i>' + attacked_with_relation_str + 's</i> \'' + \
							                         track_argument + '\''

						issue_dict[str(index)] = track_dict
			issue_dict['uid'] = str(issue.uid)
			issue_dict['text'] = str(issue.text)
			issue_dict['date'] = str(issue.date)
			return_dict[str(issue.uid)] = issue_dict

		return return_dict

	def del_track_of_user(self, transaction, user):
		"""
		Deletes the complete track of given user
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('BreadcrumbHelper', 'del_track_of_user','user ' + str(db_user.uid))
		DBDiscussionSession.query(Track).filter_by(author_uid=db_user.uid).delete()
		transaction.commit()