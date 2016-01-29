from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015


class UrlManager(object):

	def __init__(self, application_url, slug=''):
		"""

		:param application_url:
		:param slug:
		:return:
		"""
		self.url = application_url + '/'
		self.discussion_url = '/discuss'
		self.slug = slug

	def get_url(self, path):
		return self.url + path[1:]

	def get_404(self, params):
		"""

		:param params:
		:return:
		"""
		url = self.url + '404'
		for p in params:
			if p != '':
				url += '/' + p
		return url

	def get_slug_url(self, as_location_href):
		"""

		:param as_location_href:
		:return:
		"""
		return self.discussion_url + (('/' + self.slug) if self.slug != '' else '')

	def get_url_for_statement_attitude(self, as_location_href, statement_uid):
		"""

		:param as_location_href:
		:param statement_uid:
		:return: discussion_url/slug/a/statement_uid
		"""
		return self.discussion_url + '/' + self.slug + '/attitude/' + str(statement_uid)

	def get_url_for_justifying_statement(self, as_location_href, statement_uid, mode):
		"""

		:param as_location_href:
		:param statement_uid:
		:param mode:
		:return:
		"""
		return self.discussion_url + '/' + self.slug + '/justify/' + str(statement_uid) + '/' + mode

	def get_url_for_justifying_argument(self, as_location_href, argument_uid, mode, attitude):
		"""

		:param as_location_href:
		:param argument_uid:
		:param mode:
		:param attitude:
		:return:
		"""
		return self.discussion_url + '/' + self.slug + '/justify/' + str(argument_uid) + '/' + mode + '/' + attitude

	def get_url_for_reaction_on_argument(self, as_location_href, argument_uid, mode, confrontation_argument):
		"""

		:param as_location_href:
		:param argument_uid:
		:param mode: 't' on supportive, 'f' otherwise
		:param confrontation_argument:
		:return:
		"""
		return self.discussion_url + '/' + self.slug + '/reaction/' + str(argument_uid) + '/' + mode + '/' + str(confrontation_argument)
