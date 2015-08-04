import os
import sys
import transaction

from dbas.helper import PasswordHandler
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.model import DBSession, User, Argument, Statement, TextValue, TextVersion, \
	PremisseGroup, Premisse, Group, Issue, Base


def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n'
		  '(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)


def main(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)
	engine = engine_from_config(settings, 'sqlalchemy.')
	DBSession.configure(bind=engine)
	Base.metadata.create_all(engine)

	with transaction.manager:
		# adding our main issue
		issue = Issue(text='Your familiy argues about whether to buy a cat or dog as pet. Now your opinion matters!')
		DBSession.add(issue)

		# adding groups
		group0 = Group(name='admins')
		group1 = Group(name='editors')
		group2 = Group(name='users')
		DBSession.add_all([group0, group1, group2])
		DBSession.flush()

		# adding some dummy users
		pwHandler = PasswordHandler()
		pw1 = pwHandler.get_hashed_password('admin')
		pw2 = pwHandler.get_hashed_password('tobias')
		pw3 = pwHandler.get_hashed_password('martin')
		pw4 = pwHandler.get_hashed_password('mladen123')
		pw5 = pwHandler.get_hashed_password('kalman')
		user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas@cs.uni-duesseldorf.de', password=pw1, gender='m')
		user2 = User(firstname='Tobias', surname='Krauthoff', nickname='tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2, gender='m')
		user3 = User(firstname='Martin', surname='Mauve', nickname='martin', email='mauve@cs.uni-duesseldorf', password=pw3, gender='m')
		user4 = User(firstname='mladen', surname='topic', nickname='mladen', email='mladen.topic@hhu.de', password=pw4, gender='m')
		user5 = User(firstname='kalman', surname='graffi', nickname='kalman', email='graffi@cs.uni-duesseldorf.de', password=pw5, gender='m')
		user1.group = group0.uid
		user2.group = group1.uid
		user3.group = group1.uid
		user4.group = group1.uid
		user5.group = group2.uid
		user4.group = group1.uid
		user5.group = group1.uid
		DBSession.add_all([user1, user2, user3, user4, user5])
		DBSession.flush()

		textversion1 = TextVersion(content="We should get a cat.", author_uid=user2.uid, weight=0)
		textversion2 = TextVersion(content="We should get a dog.", author_uid=user2.uid, weight=0)
		textversion3 = TextVersion(content="We could get both, a cat and a dog.", author_uid=user2.uid, weight=0)
		textversion4 = TextVersion(content="Cats are very independent.", author_uid=user2.uid, weight=0)
		textversion5 = TextVersion(content="Cats are capricious.", author_uid=user2.uid, weight=0)
		textversion6 = TextVersion(content="Dogs can act as watch dogs.", author_uid=user2.uid, weight=0)
		textversion7 = TextVersion(content="You have to take the dog for a walk every day, which is tedious.", author_uid=user2.uid, weight=0)
		textversion8 = TextVersion(content="We have no use for a watch dog.", author_uid=user2.uid, weight=0)
		textversion9 = TextVersion(content="Going for a walk with the dog every day is not bad, because it is good for social interaction and physical exercise.", author_uid=user2.uid, weight=0)
		textversion10 = TextVersion(content="It would be no problem to get both a cat and a dog.", author_uid=user2.uid, weight=0)
		textversion11 = TextVersion(content="A cat and a dog will generally not get along well.", author_uid=user2.uid, weight=0)
		textversion12 = TextVersion(content="We do not have enough money for two pets.", author_uid=user2.uid, weight=0)
		textversion13 = TextVersion(content="A dog costs taxes and will be more expensive than a cat.", author_uid=user2.uid, weight=0)
		textversion14 = TextVersion(content="Cats are fluffy.", author_uid=user2.uid, weight=0)
		textversion15 = TextVersion(content="Cats are small.", author_uid=user2.uid, weight=0)
		textversion16 = TextVersion(content="Fluffy animals losing much hair and I'm allergic to animal hair.", author_uid=user2.uid, weight=0)
		textversion17 = TextVersion(content="You could use a automatic vacuum cleaner.", author_uid=user2.uid, weight=0)
		DBSession.add_all([textversion1,textversion2,textversion3,textversion4,textversion5,textversion6,textversion7,textversion8,textversion9,textversion10,textversion11,textversion12,textversion13,textversion14,textversion15,textversion16,textversion17])
		DBSession.flush()

		textvalue1 = TextValue(textVersion_uid=textversion1.uid)
		textvalue2 = TextValue(textVersion_uid=textversion2.uid)
		textvalue3 = TextValue(textVersion_uid=textversion3.uid)
		textvalue4 = TextValue(textVersion_uid=textversion4.uid)
		textvalue5 = TextValue(textVersion_uid=textversion5.uid)
		textvalue6 = TextValue(textVersion_uid=textversion6.uid)
		textvalue7 = TextValue(textVersion_uid=textversion7.uid)
		textvalue8 = TextValue(textVersion_uid=textversion8.uid)
		textvalue9 = TextValue(textVersion_uid=textversion9.uid)
		textvalue10 = TextValue(textVersion_uid=textversion10.uid)
		textvalue11 = TextValue(textVersion_uid=textversion11.uid)
		textvalue12 = TextValue(textVersion_uid=textversion12.uid)
		textvalue13 = TextValue(textVersion_uid=textversion13.uid)
		textvalue14 = TextValue(textVersion_uid=textversion14.uid)
		textvalue15 = TextValue(textVersion_uid=textversion15.uid)
		textvalue16 = TextValue(textVersion_uid=textversion16.uid)
		textvalue17 = TextValue(textVersion_uid=textversion17.uid)
		textversion1.textValue_uid = textvalue1.uid
		textversion2.textValue_uid = textvalue2.uid
		textversion3.textValue_uid = textvalue3.uid
		textversion4.textValue_uid = textvalue4.uid
		textversion5.textValue_uid = textvalue5.uid
		textversion6.textValue_uid = textvalue6.uid
		textversion7.textValue_uid = textvalue7.uid
		textversion8.textValue_uid = textvalue8.uid
		textversion9.textValue_uid = textvalue9.uid
		textversion10.textValue_uid = textvalue10.uid
		textversion11.textValue_uid = textvalue11.uid
		textversion12.textValue_uid = textvalue12.uid
		textversion13.textValue_uid = textvalue13.uid
		textversion14.textValue_uid = textvalue14.uid
		textversion15.textValue_uid = textvalue15.uid
		textversion16.textValue_uid = textvalue16.uid
		textversion17.textValue_uid = textvalue17.uid
		DBSession.add_all([textvalue1,textvalue2,textvalue3,textvalue4,textvalue5,textvalue6,textvalue7,textvalue8,textvalue9,textvalue10,textvalue11,textvalue12,textvalue13,textvalue14,textvalue15,textvalue16,textvalue17])
		DBSession.flush()

		statement1 = Statement(text_uid=textvalue1.uid)
		statement2 = Statement(text_uid=textvalue2.uid)
		statement3 = Statement(text_uid=textvalue3.uid)
		statement4 = Statement(text_uid=textvalue4.uid)
		statement5 = Statement(text_uid=textvalue5.uid)
		statement6 = Statement(text_uid=textvalue6.uid)
		statement7 = Statement(text_uid=textvalue7.uid)
		statement8 = Statement(text_uid=textvalue8.uid)
		statement9 = Statement(text_uid=textvalue9.uid)
		statement10 = Statement(text_uid=textvalue10.uid)
		statement11 = Statement(text_uid=textvalue11.uid)
		statement12 = Statement(text_uid=textvalue12.uid)
		statement13 = Statement(text_uid=textvalue13.uid)
		statement14 = Statement(text_uid=textvalue14.uid)
		statement15 = Statement(text_uid=textvalue15.uid)
		statement16 = Statement(text_uid=textvalue16.uid)
		statement17 = Statement(text_uid=textvalue17.uid)
		DBSession.add_all([statement1,statement2,statement3,statement4,statement5,statement6,statement7,statement8,statement9,statement10,statement11,statement12,statement13,statement14,statement15,statement16,statement17])
		DBSession.flush()

		premisseGroup1 = PremisseGroup(author_uid=user2.uid)
		premisseGroup2 = PremisseGroup(author_uid=user2.uid)
		premisseGroup3 = PremisseGroup(author_uid=user2.uid)
		premisseGroup4 = PremisseGroup(author_uid=user2.uid)
		premisseGroup5 = PremisseGroup(author_uid=user2.uid)
		premisseGroup6 = PremisseGroup(author_uid=user2.uid)
		premisseGroup7 = PremisseGroup(author_uid=user2.uid)
		premisseGroup8 = PremisseGroup(author_uid=user2.uid)
		premisseGroup9 = PremisseGroup(author_uid=user2.uid)
		premisseGroup10 = PremisseGroup(author_uid=user2.uid)
		premisseGroup11 = PremisseGroup(author_uid=user2.uid)
		premisseGroup12 = PremisseGroup(author_uid=user2.uid)
		premisseGroup13 = PremisseGroup(author_uid=user2.uid)
		DBSession.add_all([premisseGroup1,premisseGroup2,premisseGroup3,premisseGroup4,premisseGroup5,premisseGroup6,premisseGroup7,premisseGroup8,premisseGroup9,premisseGroup10,premisseGroup11,premisseGroup12,premisseGroup13])
		DBSession.flush()

		premisse1 = Premisse(premissesGroup_uid=premisseGroup1, statement_uid=4, isNegated=False, author_uid=user2.uid)
		premisse2 = Premisse(premissesGroup_uid=premisseGroup2, statement_uid=5, isNegated=False, author_uid=user2.uid)
		premisse3 = Premisse(premissesGroup_uid=premisseGroup3, statement_uid=6, isNegated=False, author_uid=user2.uid)
		premisse4 = Premisse(premissesGroup_uid=premisseGroup4, statement_uid=7, isNegated=False, author_uid=user2.uid)
		premisse5 = Premisse(premissesGroup_uid=premisseGroup5, statement_uid=8, isNegated=False, author_uid=user2.uid)
		premisse6 = Premisse(premissesGroup_uid=premisseGroup6, statement_uid=9, isNegated=False, author_uid=user2.uid)
		premisse7 = Premisse(premissesGroup_uid=premisseGroup7, statement_uid=10, isNegated=False, author_uid=user2.uid)
		premisse8 = Premisse(premissesGroup_uid=premisseGroup8, statement_uid=11, isNegated=False, author_uid=user2.uid)
		premisse9 = Premisse(premissesGroup_uid=premisseGroup9, statement_uid=12, isNegated=False, author_uid=user2.uid)
		premisse10 = Premisse(premissesGroup_uid=premisseGroup10, statement_uid=13, isNegated=False, author_uid=user2.uid)
		premisse11 = Premisse(premissesGroup_uid=premisseGroup11, statement_uid=14, isNegated=False, author_uid=user2.uid)
		premisse12 = Premisse(premissesGroup_uid=premisseGroup11, statement_uid=15, isNegated=False, author_uid=user2.uid)
		premisse13 = Premisse(premissesGroup_uid=premisseGroup12, statement_uid=16, isNegated=False, author_uid=user2.uid)
		premisse14 = Premisse(premissesGroup_uid=premisseGroup13, statement_uid=17, isNegated=False, author_uid=user2.uid)
		DBSession.add_all([premisse1,premisse2,premisse3,premisse4,premisse5,premisse6,premisse7,premisse8,premisse9,premisse10,premisse11,premisse12,premisse13,premisse14])
		DBSession.flush()

		argument1 = Argument(premissegroup_uid=premisseGroup1, conclusion_uid=statement1, isSupportive=True, author_uid=user2.uid, weight=0)
		argument2 = Argument(premissegroup_uid=premisseGroup2, conclusion_uid=statement1, isSupportive=False, author_uid=user2.uid, weight=0)
		argument3 = Argument(premissegroup_uid=premisseGroup3, conclusion_uid=statement2, isSupportive=True, author_uid=user2.uid, weight=0)
		argument4 = Argument(premissegroup_uid=premisseGroup4, conclusion_uid=statement2, isSupportive=False, author_uid=user2.uid, weight=0)
		argument5 = Argument(premissegroup_uid=premisseGroup5, argument_uid=argument3, isSupportive=False, author_uid=user2.uid, weight=0)
		argument6 = Argument(premissegroup_uid=premisseGroup6, argument_uid=argument4, isSupportive=False, author_uid=user2.uid, weight=0)
		argument7 = Argument(premissegroup_uid=premisseGroup7, conclusion_uid=statement3, isSupportive=True, author_uid=user2.uid, weight=0)
		argument8 = Argument(premissegroup_uid=premisseGroup8, argument_uid=argument7, isSupportive=False, author_uid=user2.uid, weight=0)
		argument9 = Argument(premissegroup_uid=premisseGroup9, conclusion_uid=statement10, isSupportive=False, author_uid=user2.uid, weight=0)
		argument10 = Argument(premissegroup_uid=premisseGroup10, conclusion_uid=statement1, isSupportive=True, author_uid=user2.uid, weight=0)
		argument11 = Argument(premissegroup_uid=premisseGroup11, conclusion_uid=statement1, isSupportive=True, author_uid=user2.uid, weight=0)
		argument12 = Argument(premissegroup_uid=premisseGroup12, argument_uid=argument11, isSupportive=False, author_uid=user2.uid, weight=0)
		argument13 = Argument(premissegroup_uid=premisseGroup13, argument_uid=argument12, isSupportive=False, author_uid=user2.uid, weight=0)
		DBSession.add_all([argument1,argument2,argument3,argument4,argument5,argument6,argument7,argument8,argument9,argument10,argument11,argument12,argument13])
		DBSession.flush()

		transaction.commit()