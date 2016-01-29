from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015


class UrlManager(object):

	def __init__(self, application_url, slug='', for_api=False):
		"""

		:param application_url:
		:param slug:
		:param for_api:
		:return:
		"""
		logger('UrlManager','__init__', 'application_url: ' + application_url)
		logger('UrlManager','__init__', 'slug: ' + slug)
		logger('UrlManager','__init__', 'for_api: ' + str(for_api))
		self.url = application_url + '/'
		self.discussion_url = self.url + 'discuss/'
		self.api_url = 'api/'
		self.slug = slug
		self.for_api = for_api

	def get_url(self, path):
		"""
		
		:param path:
		:return:
		"""
		return self.api_url if self.for_api else self.url + path[1:]

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
		url = self.discussion_url + self.slug
		if self.for_api:
			return self.api_url + self.slug
		else:
			return ('location.href="' + url + '"') if as_location_href else url

	def get_url_for_statement_attitude(self, as_location_href, statement_uid):
		"""

		:param as_location_href:
		:param statement_uid:
		:return: discussion_url/slug/a/statement_uid
		"""
		url = self.discussion_url + self.slug + '/attitude/' + str(statement_uid)
		if self.for_api:
			return self.api_url + self.slug + '/attitude/' + str(statement_uid)
		else:
			return ('location.href="' + url + '"') if as_location_href else url

	def get_url_for_justifying_statement(self, as_location_href, statement_uid, mode):
		"""

		:param as_location_href:
		:param statement_uid:
		:param mode:
		:return:
		"""
		url = self.discussion_url + self.slug + '/justify/' + str(statement_uid) + '/' + mode
		if self.for_api:
			return self.api_url + self.slug + '/justify/' + str(statement_uid) + '/' + mode
		else:
			return ('location.href="' + url + '"') if as_location_href else url

	def get_url_for_justifying_argument(self, as_location_href, argument_uid, mode, attitude):
		"""

		:param as_location_href:
		:param argument_uid:
		:param mode:
		:param attitude:
		:return:
		"""
		url = self.discussion_url + self.slug + '/justify/' + str(argument_uid) + '/' + mode + '/' + attitude
		if self.for_api:
			return self.api_url + self.slug + '/justify/' + str(argument_uid) + '/' + mode + '/' + attitude
		else:
			return ('location.href="' + url + '"') if as_location_href else url

	def get_url_for_reaction_on_argument(self, as_location_href, argument_uid, mode, confrontation_argument):
		"""

		:param as_location_href:
		:param argument_uid:
		:param mode: 't' on supportive, 'f' otherwise
		:param confrontation_argument:
		:return:
		"""
		url = self.discussion_url + self.slug + '/reaction/' + str(argument_uid) + '/' + mode + '/' + str(confrontation_argument)
		if self.for_api:
			return self.api_url + self.slug + '/reaction/' + str(argument_uid) + '/' + mode + '/' + str(confrontation_argument)
		else:
			return ('location.href="' + url + '"') if as_location_href else url
