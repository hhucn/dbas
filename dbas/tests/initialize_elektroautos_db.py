# -*- coding: utf-8 -*-
"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


import arrow
import os
import sys
import transaction
import random
import dbas.password_handler as PasswordHandler

from math import trunc
from dbas.logger import logger
from sqlalchemy import engine_from_config, and_
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.discussion_model import User, Argument, Statement, TextVersion, PremiseGroup, Premise, Group, Issue,\
	Notification, Settings, VoteArgument, VoteStatement, Language
from dbas.database import DiscussionBase, NewsBase, DBDiscussionSession, DBNewsSession


def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)


def main_discussion(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	discussion_engine = engine_from_config(settings, 'sqlalchemy-discussion.')
	DBDiscussionSession.configure(bind=discussion_engine)
	DiscussionBase.metadata.create_all(discussion_engine)

	with transaction.manager:
		user2 = set_up_users(DBDiscussionSession)
		setup_discussion_database(DBDiscussionSession, user2)
		transaction.commit()


def main_discussion_reload(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	discussion_engine = engine_from_config(settings, 'sqlalchemy-discussion.')
	DBDiscussionSession.configure(bind=discussion_engine)
	DiscussionBase.metadata.create_all(discussion_engine)

	with transaction.manager:
		main_author = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
		setup_discussion_database(DBDiscussionSession, main_author)
		setup_dummy_votes(DBDiscussionSession)
		transaction.commit()


def main_dummy_votes(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	discussion_engine = engine_from_config(settings, 'sqlalchemy-discussion.')
	DBDiscussionSession.configure(bind=discussion_engine)
	DiscussionBase.metadata.create_all(discussion_engine)

	with transaction.manager:
		setup_dummy_votes(DBDiscussionSession)
		transaction.commit()


def set_up_users(session):
	"""
	Creates all users

	:param session: database session
	:return: User
	"""

	# adding groups
	group0 = Group(name='admins')
	group1 = Group(name='authors')
	group2 = Group(name='users')
	session.add_all([group0, group1, group2])
	session.flush()

	# adding some dummy users
	pwt = PasswordHandler.get_hashed_password('iamatestuser2016')
	pw0 = PasswordHandler.get_hashed_password('QMuxpuPXwehmhm2m93#I;)QX§u4qjqoiwhebakb)(4hkblkb(hnzUIQWEGgalksd')
	pw1 = PasswordHandler.get_hashed_password('pjÖKAJSDHpuiashw89ru9hsidhfsuihfapiwuhrfj098UIODHASIFUSHDF')
	pw2 = PasswordHandler.get_hashed_password('tobias')
	pw3 = PasswordHandler.get_hashed_password('martin')
	pw4 = PasswordHandler.get_hashed_password('christian')

	user0 = User(firstname='anonymous', surname='anonymous', nickname='anonymous', email='', password=pw0, group=group0.uid, gender='m')
	user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas.hhu@gmail.com', password=pw1, group=group0.uid, gender='m')
	user2 = User(firstname='Tobias', surname='Krauthoff', nickname='Tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2, group=group0.uid, gender='m')
	user3 = User(firstname='Martin', surname='Mauve', nickname='Martin', email='mauve@cs.uni-duesseldorf.de', password=pw3, group=group0.uid, gender='m')
	user4 = User(firstname='Christian', surname='Meter', nickname='Christian', email='meter@cs.uni-duesseldorf.de', password=pw4, group=group0.uid, gender='m')

	session.add_all([user0, user1, user2, user3, user4])
	session.flush()

	# adding settings
	settings0 = Settings(author_uid=user0.uid, send_mails=True, send_notifications=True, should_show_public_nickname=True)
	settings1 = Settings(author_uid=user1.uid, send_mails=True, send_notifications=True, should_show_public_nickname=True)
	settings2 = Settings(author_uid=user2.uid, send_mails=True, send_notifications=True, should_show_public_nickname=True)
	settings3 = Settings(author_uid=user3.uid, send_mails=True, send_notifications=True, should_show_public_nickname=True)
	settings4 = Settings(author_uid=user4.uid, send_mails=True, send_notifications=True, should_show_public_nickname=True)
	session.add_all([settings0, settings1, settings2, settings3, settings4])
	session.flush()

	# Adding welcome notifications
	notification0 = Notification(from_author_uid=user1.uid, to_author_uid=user2.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification1 = Notification(from_author_uid=user1.uid, to_author_uid=user3.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification2 = Notification(from_author_uid=user1.uid, to_author_uid=user4.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	session.add_all([notification0, notification1, notification2])
	session.flush()

	return user2


def setup_dummy_votes(session):
	"""
	Drops all votes and init new dummy votes

	:param session: DBDiscussionSession
	:return:
	"""
	DBDiscussionSession.query(VoteStatement).delete()
	DBDiscussionSession.query(VoteArgument).delete()

	db_arguments = DBDiscussionSession.query(Argument).all()
	db_statements = DBDiscussionSession.query(Statement).all()
	firstnames = ['Tobias', 'Pascal', 'Kurt', 'Torben', 'Thorsten', 'Friedrich', 'Aayden', 'Hermann', 'Wolf', 'Jakob',
	              'Alwin', 'Walter', 'Volker', 'Benedikt', 'Engelbert', 'Elias', 'Rupert', 'Marga', 'Larissa', 'Emmi',
	              'Konstanze', 'Catrin', 'Antonia', 'Nora', 'Nora', 'Jutta', 'Helga', 'Denise', 'Hanne', 'Elly',
	              'Sybille', 'Ingeburg']

	new_votes = []
	arg_up = 0
	arg_down = 0
	stat_up = 0
	stat_down = 0
	max_interval = len(firstnames) - 1
	for argument in db_arguments:
		up_votes = random.randint(1, max_interval)
		down_votes = random.randint(1, max_interval)
		arg_up += up_votes
		arg_down += down_votes

		tmp_firstname = list(firstnames)
		for i in range(0, up_votes):
			nick = tmp_firstname[random.randint(0, len(tmp_firstname) - 1)]
			db_rnd_tst_user = DBDiscussionSession.query(User).filter_by(firstname=nick).first()
			if not session.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
			                                               VoteArgument.author_uid == db_rnd_tst_user.uid,
			                                               VoteArgument.is_up_vote == True,
			                                               VoteArgument.is_valid == True)).first():
				new_votes.append(VoteArgument(argument_uid=argument.uid, author_uid=db_rnd_tst_user.uid, is_up_vote=True, is_valid=True))
				tmp_firstname.remove(nick)

		tmp_firstname = list(firstnames)
		for i in range(0, down_votes):
			nick = tmp_firstname[random.randint(0, len(tmp_firstname) - 1)]
			db_rnd_tst_user = DBDiscussionSession.query(User).filter_by(firstname=nick).first()
			if not session.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
			                                               VoteArgument.author_uid == db_rnd_tst_user.uid,
			                                               VoteArgument.is_up_vote == False,
			                                               VoteArgument.is_valid == True)).first():
				new_votes.append(VoteArgument(argument_uid=argument.uid, author_uid=db_rnd_tst_user.uid, is_up_vote=False, is_valid=True))
				tmp_firstname.remove(nick)

	for statement in db_statements:
		up_votes = random.randint(1, max_interval)
		down_votes = random.randint(1, max_interval)
		stat_up += up_votes
		stat_down += down_votes

		tmp_firstname = list(firstnames)
		for i in range(0, up_votes):
			nick = tmp_firstname[random.randint(0, len(tmp_firstname) - 1)]
			db_rnd_tst_user = DBDiscussionSession.query(User).filter_by(firstname=nick).first()
			if not session.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
			                                                VoteStatement.author_uid == db_rnd_tst_user.uid,
			                                                VoteStatement.is_up_vote == True,
			                                                VoteStatement.is_valid == True)).first():
				new_votes.append(VoteStatement(statement_uid=statement.uid, author_uid=db_rnd_tst_user.uid, is_up_vote=True, is_valid=True))
				tmp_firstname.remove(nick)

		tmp_firstname = list(firstnames)
		for i in range(0, down_votes):
			nick = tmp_firstname[random.randint(0, len(tmp_firstname) - 1)]
			db_rnd_tst_user = DBDiscussionSession.query(User).filter_by(firstname=nick).first()
			if not session.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
			                                                VoteStatement.author_uid == db_rnd_tst_user.uid,
			                                                VoteStatement.is_up_vote == False,
			                                                VoteStatement.is_valid == True)).first():
				new_votes.append(VoteStatement(statement_uid=statement.uid, author_uid=db_rnd_tst_user.uid, is_up_vote=False, is_valid=True))
				tmp_firstname.remove(nick)

	rat_arg_up = str(trunc(arg_up / len(db_arguments) * 100) / 100)
	rat_arg_down = str(trunc(arg_down / len(db_arguments) * 100) / 100)
	rat_stat_up = str(trunc(stat_up / len(db_statements) * 100) / 100)
	rat_stat_down = str(trunc(stat_down / len(db_statements) * 100) / 100)

	logger('INIT_DB', 'Dummy Votes', 'Created ' + str(arg_up) + ' up votes for ' + str(len(db_arguments)) + ' arguments (' + rat_arg_up + ' votes/argument)')
	logger('INIT_DB', 'Dummy Votes', 'Created ' + str(arg_down) + ' down votes for ' + str(len(db_arguments)) + ' arguments (' + rat_arg_down + ' votes/argument)')
	logger('INIT_DB', 'Dummy Votes', 'Created ' + str(stat_up) + ' up votes for ' + str(len(db_statements)) + ' statements (' + rat_stat_up + ' votes/statement)')
	logger('INIT_DB', 'Dummy Votes', 'Created ' + str(stat_down) + ' down votes for ' + str(len(db_statements)) + ' statements (' + rat_stat_down + ' votes/statement)')

	session.add_all(new_votes)
	session.flush()

	# random timestamps
	db_votestatements = session.query(VoteStatement).all()
	for vs in db_votestatements:
		vs.timestamp = arrow.utcnow().replace(days=-random.randint(0, 25))

	db_votearguments = session.query(VoteArgument).all()
	for va in db_votearguments:
		va.timestamp = arrow.utcnow().replace(days=-random.randint(0, 25))


def setup_discussion_database(session, user):
	"""
	Fills the database with dummy date, created by given user

	:param session: database session
	:param user: main author
	:return:
	"""

	# adding languages
	lang1 = Language(name='English', ui_locales='en')
	lang2 = Language(name='Deutsch', ui_locales='de')
	session.add_all([lang1, lang2])
	session.flush()

	# adding our main issue
	issue4 = Issue(title='Elektroautos', info='Elektroautos - Die Autos der Zukunft? Bitte diskutieren Sie dazu.', author_uid=user.uid, lang_uid=lang2.uid)
	session.add_all([issue4])
	session.flush()

	textversion200 = TextVersion(content="E-Autos keine Emissionen verursachen.", author=user.uid)
	textversion201 = TextVersion(content="Elektroautos sehr g&uuml;nstig im Unterhalt sind", author=user.uid)
	textversion202 = TextVersion(content="E-Autos optimal f&uuml;r den Stadtverkehr sind.", author=user.uid)
	textversion203 = TextVersion(content="sie keine stinkenden Abgase produzieren.", author=user.uid)
	textversion204 = TextVersion(content="die Herstellung der Autos und Batterien die Umwelt stark belasten", author=user.uid)
	textversion205 = TextVersion(content="sie sehr teuer in der Anschaffung sind.", author=user.uid)
	textversion206 = TextVersion(content="die Reichweite von Elektroautos ausreichend f&uuml;r mindestens 300km ist.", author=user.uid)
	textversion207 = TextVersion(content="die Ladezeit der Batterie bis zu 12h da&uuml;rn kann und so lange man tags&uuml;ber nicht warten kann.", author=user.uid)
	textversion208 = TextVersion(content="die Umweltbelastung und Rohstoffabh&auml;ngigkeit durch Batterien sehr hoch ist.", author=user.uid)
	textversion209 = TextVersion(content="die Umweltbelastung durch Batterien immernoch viel geringer als durch Verbrennungsmotoren ist.", author=user.uid)
	textversion210 = TextVersion(content="in der Stadt Fahrr&auml;der und oeffentliche Verkehrsmittel besser sind.", author=user.uid)
	textversion211 = TextVersion(content="man gezielt 'tanken' kann, genauso wie bei einem herk&ouml;mmlichen KFZ.", author=user.uid)

	session.add_all([textversion200, textversion201, textversion202, textversion203, textversion204, textversion205])
	session.add_all([textversion206, textversion207, textversion208, textversion209, textversion210, textversion211])
	session.flush()

	# random timestamps
	db_textversions = session.query(TextVersion).all()
	for tv in db_textversions:
		tv.timestamp = arrow.utcnow().replace(days=-random.randint(0, 25))

	# adding all statements
	statement200 = Statement(textversion=textversion200.uid, is_startpoint=True, issue=issue4.uid)
	statement201 = Statement(textversion=textversion201.uid, is_startpoint=True, issue=issue4.uid)
	statement202 = Statement(textversion=textversion202.uid, is_startpoint=True, issue=issue4.uid)
	statement203 = Statement(textversion=textversion203.uid, is_startpoint=False, issue=issue4.uid)
	statement204 = Statement(textversion=textversion204.uid, is_startpoint=False, issue=issue4.uid)
	statement205 = Statement(textversion=textversion205.uid, is_startpoint=False, issue=issue4.uid)
	statement206 = Statement(textversion=textversion206.uid, is_startpoint=False, issue=issue4.uid)
	statement207 = Statement(textversion=textversion207.uid, is_startpoint=False, issue=issue4.uid)
	statement208 = Statement(textversion=textversion208.uid, is_startpoint=False, issue=issue4.uid)
	statement209 = Statement(textversion=textversion209.uid, is_startpoint=False, issue=issue4.uid)
	statement210 = Statement(textversion=textversion210.uid, is_startpoint=False, issue=issue4.uid)
	statement211 = Statement(textversion=textversion211.uid, is_startpoint=False, issue=issue4.uid)

	session.add_all([statement200, statement201, statement202, statement203, statement204, statement205, statement206])
	session.add_all([statement207, statement208, statement209, statement210, statement211])
	session.flush()

	session.flush()

	# set textversions
	textversion200.set_statement(statement200.uid)
	textversion201.set_statement(statement201.uid)
	textversion202.set_statement(statement202.uid)
	textversion203.set_statement(statement203.uid)
	textversion204.set_statement(statement204.uid)
	textversion205.set_statement(statement205.uid)
	textversion206.set_statement(statement206.uid)
	textversion207.set_statement(statement207.uid)
	textversion208.set_statement(statement208.uid)
	textversion209.set_statement(statement209.uid)
	textversion210.set_statement(statement210.uid)
	textversion211.set_statement(statement211.uid)

	# adding all premisegroups
	premisegroup203 = PremiseGroup(author=user.uid)
	premisegroup204 = PremiseGroup(author=user.uid)
	premisegroup205 = PremiseGroup(author=user.uid)
	premisegroup206 = PremiseGroup(author=user.uid)
	premisegroup207 = PremiseGroup(author=user.uid)
	premisegroup208 = PremiseGroup(author=user.uid)
	premisegroup209 = PremiseGroup(author=user.uid)
	premisegroup210 = PremiseGroup(author=user.uid)
	premisegroup211 = PremiseGroup(author=user.uid)
	premisegroup212 = PremiseGroup(author=user.uid)

	session.add_all([premisegroup203, premisegroup204, premisegroup205, premisegroup206, premisegroup207])
	session.add_all([premisegroup208, premisegroup209, premisegroup210, premisegroup211, premisegroup212])
	session.flush()

	premise203 = Premise(premisesgroup=premisegroup203.uid, statement=statement203.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise204 = Premise(premisesgroup=premisegroup204.uid, statement=statement204.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise205 = Premise(premisesgroup=premisegroup205.uid, statement=statement205.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise206 = Premise(premisesgroup=premisegroup206.uid, statement=statement206.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise207 = Premise(premisesgroup=premisegroup207.uid, statement=statement207.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise208 = Premise(premisesgroup=premisegroup208.uid, statement=statement208.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise209 = Premise(premisesgroup=premisegroup209.uid, statement=statement209.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise210 = Premise(premisesgroup=premisegroup210.uid, statement=statement210.uid, is_negated=False, author=user.uid, issue=issue4.uid)
	premise211 = Premise(premisesgroup=premisegroup211.uid, statement=statement211.uid, is_negated=False, author=user.uid, issue=issue4.uid)

	session.add_all([premise203, premise204, premise205, premise206, premise207, premise208, premise209, premise210])
	session.add_all([premise211])
	session.flush()

	# adding all arguments and set the adjacency list
	argument201 = Argument(premisegroup=premisegroup203.uid, issupportive=True, author=user.uid, issue=issue4.uid, conclusion=statement200.uid)
	argument202 = Argument(premisegroup=premisegroup204.uid, issupportive=False, author=user.uid, issue=issue4.uid, conclusion=statement200.uid)
	argument203 = Argument(premisegroup=premisegroup205.uid, issupportive=False, author=user.uid, issue=issue4.uid, conclusion=statement201.uid)
	argument204 = Argument(premisegroup=premisegroup206.uid, issupportive=True, author=user.uid, issue=issue4.uid, conclusion=statement202.uid)
	argument205 = Argument(premisegroup=premisegroup207.uid, issupportive=False, author=user.uid, issue=issue4.uid, conclusion=statement202.uid)
	argument206 = Argument(premisegroup=premisegroup208.uid, issupportive=False, author=user.uid, issue=issue4.uid)
	argument207 = Argument(premisegroup=premisegroup209.uid, issupportive=False, author=user.uid, issue=issue4.uid)
	argument208 = Argument(premisegroup=premisegroup210.uid, issupportive=False, author=user.uid, issue=issue4.uid)
	argument209 = Argument(premisegroup=premisegroup211.uid, issupportive=False, author=user.uid, issue=issue4.uid)

	session.add_all([argument201, argument202, argument203, argument204, argument205, argument206, argument207])
	session.add_all([argument208, argument209])
	session.flush()

	argument206.conclusions_argument(argument201.uid)
	argument207.conclusions_argument(argument202.uid)
	argument208.conclusions_argument(argument204.uid)
	argument209.conclusions_argument(argument205.uid)
	session.flush()
