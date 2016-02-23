from .logger import logger
from .database import DBDiscussionSession
from .database.discussion_model import User, TextVersion, Notification, Settings
from .strings import Translator
from sqlalchemy import and_

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class NotificationHelper:

	def send_edit_text_notification(self, textversion, lang):
		"""
		Sends an notification to the root-author and last author, when their text was edited.
		:param textversion: new Textversion
		:param lang: ui_locales
		:return: None
		"""
		all_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=textversion.statement_uid).order_by(TextVersion.uid.desc()).all()
		oem = all_textversions[-1]
		root_author = oem.author_uid
		new_author = textversion.author_uid
		last_author = all_textversions[-2].author_uid if len(all_textversions) > 1 else root_author
		send_for_root_author = DBDiscussionSession.query(Settings).filter_by(uid=root_author).first().send_notifications
		send_for_last_author = DBDiscussionSession.query(Settings).filter_by(uid=last_author).first().send_notifications

		# check for different authors
		if root_author == new_author:
			return None

		# create content
		_t = Translator(lang)
		topic = _t.get(_t.textversionChangedTopic)
		content = _t.get(_t.textversionChangedContent) + ' ' + DBDiscussionSession.query(User).filter_by(uid=new_author).first().nickname
		content += '<br>' + (_t.get(_t.fromm)[0:1].upper() + _t.get(_t.fromm)[1:]) + ': ' + textversion.content + '<br>'
		content += (_t.get(_t.to)[0:1].upper() + _t.get(_t.to)[1:]) + ': ' + oem.content

		# send notifications
		if send_for_root_author:
			notification_to_root_author = Notification(from_author_uid=new_author, to_author_uid=root_author, topic=topic, content=content)
			DBDiscussionSession.add(notification_to_root_author)
		if last_author != root_author and send_for_last_author:
			notification_to_last_author = Notification(from_author_uid=new_author, to_author_uid=last_author, topic=topic, content=content)
			DBDiscussionSession.add(notification_to_last_author)

		DBDiscussionSession.flush()

	def send_welcome_message(self, transaction, user, lang='en'):
		"""
		Creates and send the welcome message to a new user
		:param transaction: transaction
		:param user: User.uid
		:param lang: ui_locales
		:return: None
		"""
		_tn = Translator(lang)
		topic = _tn.get(_tn.welcome)
		content = _tn.get(_tn.welcomeMessage)
		motification = Notification(from_author_uid=1, to_author_uid=user, topic=topic, content=content)
		DBDiscussionSession.add(motification)
		DBDiscussionSession.flush()
		transaction.commit()

	def count_of_new_notifications(self, user):
		"""
		Returns the count of unread messages of the given user
		:param user: User.nickname
		:return: integer
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		if db_user:
			return len(DBDiscussionSession.query(Notification).filter(and_(Notification.to_author_uid == db_user.uid,
			                                                               Notification.read == False)).all())
		else:
			return 0

	def get_notification_for(self, user):
		"""
		Returns all notifications for the user
		:param user: User.nickname
		:return: [Notification]
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		if not db_user:
			return []

		db_messages = DBDiscussionSession.query(Notification).filter_by(to_author_uid=db_user.uid).all()

		message_array = []
		for message in db_messages:
			tmp_dict = dict()
			tmp_dict['id']              = str(message.uid)
			tmp_dict['from']            = DBDiscussionSession.query(User).filter_by(uid=message.from_author_uid).first().nickname
			tmp_dict['timestamp']       = str(message.timestamp)
			tmp_dict['read']            = message.read
			tmp_dict['topic']           = message.topic
			tmp_dict['content']         = message.content
			tmp_dict['collapse_link']   = '#collapse' + str(message.uid)
			tmp_dict['collapse_id']     = 'collapse' + str(message.uid)
			message_array.append(tmp_dict)

		return message_array
