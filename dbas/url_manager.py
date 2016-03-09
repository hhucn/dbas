from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class UrlManager(object):
	"""
	URL-Manager for building all URLs. This includes DBAS-URLs as well as the API-URLs
	"""

	def __init__(self, application_url, slug='', for_api=False):
		"""
		Initialization of an URL-Manager
		:param application_url: self.request.application_url
		:param slug: slugged issue.title
		:param for_api: Boolean
		:return: None
		"""
		logger('UrlManager', '__init__', 'application_url: ' + application_url + ', slug: ' + slug + ', for_api: ' + str(for_api))
		self.url = application_url + ('' if application_url.endswith('/') else '/')
		self.discussion_url = self.url + 'discuss/'
		self.api_url = 'api/'
		self.slug = slug
		self.for_api = for_api

	def __verify_path(self, path): # TODO
		"""

		:param path:
		:return:
		"""
		splitted = path.split('/')
		if splitted[0] == 'discuss':
			if splitted[2] == 'reaction':
				# /discuss/{slug}/reaction/{arg_id_user}/{mode}/{arg_id_sys}'
				return True
			elif splitted[2] == 'justify':
				# /discuss/{slug}/justify/{statement_or_arg_id}/{mode}*relation'
				return True
			elif splitted[2] == 'attitude':
				# /discuss/{slug}/attitude/*statement_id'
				return True
			elif splitted[2] == 'choose':
				# /discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids'
				return True
			else:
				return True

			# /discuss*slug'
		return False

	def get_url(self, path):
		"""
		Returns current url with self.url as prefix or the API-version
		:param path: String
		:return:
		"""
		return path if self.for_api else (self.url + path[1:])

	def get_404(self, params):
		"""
		Returns the 404 page or the API-version
		:param params: self.request.params
		:return: 404/params1/param2/
		"""
		url = self.url + '404'
		for p in params:
			if p != '':
				url += '/' + p
		return url

	def get_slug_url(self, as_location_href):
		"""
		Returns url with slugified issue.title or the API-version
		:param as_location_href: Boolean
		:return: discussion_url/slug
		"""
		url = self.slug
		return self.__return_url(as_location_href, url)

	def get_url_for_statement_attitude(self, as_location_href, statement_uid):
		"""
		Returns url for getting statement attitude of the user or the API-version
		:param as_location_href: Boolean
		:param statement_uid: Statement.uid
		:return: discussion_url/slug/a/statement_uid
		"""
		url = self.slug + '/attitude/' + str(statement_uid)
		return self.__return_url(as_location_href, url)

	def get_url_for_justifying_statement(self, as_location_href, statement_uid, mode):
		"""
		Returns url for getting statement justification of the user or the API-version
		:param as_location_href: Boolean
		:param statement_uid: Statement.uid
		:param mode: String
		:return: discuss/{slug}/justify/{statement_or_arg_id}/{mode}
		"""
		url = self.slug + '/justify/' + str(statement_uid) + '/' + mode
		return self.__return_url(as_location_href, url)

	def get_url_for_justifying_argument(self, as_location_href, argument_uid, mode, attitude, additional_id=-1):
		"""
		Returns url for justifyng an argument of the user or the API-version
		:param as_location_href: Boolean
		:param argument_uid: Argument.uid
		:param mode: String
		:param attitude: String
		:param additional_id: String
		:return: discuss/{slug}/justify/{statement_or_arg_id}/{mode}*attitude
		"""
		url = self.slug + '/justify/' + str(argument_uid) + '/' + mode + '/' + attitude
		if additional_id != -1:
			url += '/' + str(additional_id)
		return self.__return_url(as_location_href, url)

	def get_url_for_reaction_on_argument(self, as_location_href, argument_uid, mode, confrontation_argument):
		"""
		Returns url for getting teh reaction regarding an argument of the user or the API-version
		:param as_location_href: Boolean
		:param argument_uid: Argument.uid
		:param mode: 't' on supportive, 'f' otherwise
		:param confrontation_argument: Argument.uid
		:return: discuss/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys
		"""
		url = self.slug + '/reaction/' + str(argument_uid) + '/' + mode + '/' + str(confrontation_argument)
		return self.__return_url(as_location_href, url)

	def get_url_for_choosing_premisegroup(self, as_location_href, is_argument, is_supportive, statement_or_argument_id, pgroup_id_list):
		"""

		:param as_location_href: Boolean
		:param is_argument: Boolean
		:param is_supportive: Boolean
		:param statement_or_argument_id: Statement.uid or Argument.uid
		:param pgroup_id_list: int[]
		:return:
		"""
		is_arg = 't' if is_argument else 'f'
		is_sup = 't' if is_supportive else 'f'
		pgroups = ('/' + '/'.join(str(x) for x in pgroup_id_list)) if len(pgroup_id_list) > 0 else ''
		url = self.slug + '/choose/' + is_arg + '/' + is_sup + '/' + str(statement_or_argument_id) + str(pgroups)
		return self.__return_url(as_location_href, url)

	def __return_url(self, as_location_href, url):
		"""

		:param as_location_href:
		:param url:
		:return:
		"""
		if self.for_api:
			return self.api_url + url
		else:
			prefix = 'location.href="' if as_location_href else ''
			suffix = '"' if as_location_href else ''
			return prefix + self.discussion_url + url + suffix
