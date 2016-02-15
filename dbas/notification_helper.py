from .logger import logger
from .database import DBDiscussionSession
from .database.discussion_model import User, TextVersion, Message
from .strings import Translator
from sqlalchemy import and_

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

class NotificationHelper():

	def send_edit_text_notification(self, textversion, lang):
		"""

		:param textversion:
		:return:
		"""
		oem = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=textversion.statement_uid).first()
		author = oem.author_uid
		new_author = textversion.author_uid

		if author == new_author:
			return None

		_t = Translator(lang)
		topic = _t.get(_t.textversionChangedTopic)
		content = _t.get(_t.textversionChangedContent) + ' ' + DBDiscussionSession.query(User).filter_by(uid=new_author).first().nickname
		content += '<br>' + (_t.get(_t.fromm)[0:1].upper() + _t.get(_t.fromm)[1:]) + ': ' + textversion.content + '<br>'
		content += (_t.get(_t.to)[0:1].upper() + _t.get(_t.to)[1:]) + ': ' + oem.content

		message = Message(from_author_uid=new_author, to_author_uid=author, topic=topic, content=content)
		DBDiscussionSession.add(message)
		DBDiscussionSession.flush()

	def count_of_new_messages(self, user):
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		if db_user:
			return len(DBDiscussionSession.query(Message).filter(and_(Message.to_author_uid == db_user.uid,
			                                                          Message.read == False)).all())
		else:
			return 0

	def get_message_for(self, user):
		"""

		:param user:
		:return:
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		db_messages = DBDiscussionSession.query(Message).filter_by(to_author_uid=db_user.uid).all()

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