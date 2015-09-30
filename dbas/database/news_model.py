import sqlalchemy as sa

from dbas.database import NewsBase

class News(NewsBase):
	"""
	News-table with several columns.
	"""
	__tablename__ = 'news'
	uid = sa.Column(sa.Integer, primary_key=True)
	title = sa.Column(sa.Text, nullable=False)
	author = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.Text, nullable=False)
	news = sa.Column(sa.Text, nullable=False)

	def __init__(self, title, author, news, date):
		"""
		Initializes a row in current news-table
		"""
		self.title = title
		self.author = author
		self.news = news
		self.date = date