"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
import re

from datetime import datetime
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, Issue, Bubble, VoteArgument, VoteStatement, Breadcrumb
from .lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion
from .logger import logger
from .recommender_system import RecommenderHelper
from .query_helper import QueryHelper
from .strings import Translator, TextGenerator
from .url_manager import UrlManager
from .user_management import UserHandler
from .notification_helper import NotificationHelper


class DiscussionDictHelper(object):
	"""

	"""

	def __init__(self, lang=''):
		"""
		Initialize default values

		:param lang: ui_locales
		:return:
		"""
		self.lang = lang
