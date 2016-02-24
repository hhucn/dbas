import sqlalchemy as sa

from dbas.database import APIBase

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class KeywordMapper(APIBase):
	"""
	Mapping-table with several columns.
	"""
	__tablename__ = 'keywordmappers'
	uid = sa.Column(sa.Integer, primary_key=True)
	issue_uid = sa.Column(sa.Integer, nullable=False)
	keyword = sa.Column(sa.Text, nullable=False)
	url = sa.Column(sa.Text, nullable=False)

	def __init__(self, url, keyword, issue_uid):
		"""
		Initializes a row in current news-table
		"""
		self.url = url
		self.keyword = keyword
		self.issue_uid = issue_uid
