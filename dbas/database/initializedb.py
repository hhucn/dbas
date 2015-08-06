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
		pw4 = pwHandler.get_hashed_password('mladen')
		pw5 = pwHandler.get_hashed_password('kalman')
		user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas@cs.uni-duesseldorf.de', password=pw1, group=group0.uid, gender='m')
		user2 = User(firstname='Tobias', surname='Krauthoff', nickname='tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2, group=group1.uid, gender='m')
		user3 = User(firstname='Martin', surname='Mauve', nickname='martin', email='mauve@cs.uni-duesseldorf', password=pw3, group=group1.uid, gender='m')
		user4 = User(firstname='mladen', surname='topic', nickname='mladen', email='mladen.topic@hhu.de', password=pw4, group=group1.uid, gender='m')
		user5 = User(firstname='kalman', surname='graffi', nickname='kalman', email='graffi@cs.uni-duesseldorf.de', password=pw5, group=group1.uid, gender='m')
		DBSession.add_all([user1, user2, user3, user4, user5])
		DBSession.flush()

		textversion1 = TextVersion(content="We should get a cat.", author=user2.uid, weight=0)
		textversion2 = TextVersion(content="We should get a dog.", author=user2.uid, weight=0)
		textversion3 = TextVersion(content="We could get both, a cat and a dog.", author=user2.uid, weight=0)
		textversion4 = TextVersion(content="Cats are very independent.", author=user2.uid, weight=0)
		textversion5 = TextVersion(content="Cats are capricious.", author=user2.uid, weight=0)
		textversion6 = TextVersion(content="Dogs can act as watch dogs.", author=user2.uid, weight=0)
		textversion7 = TextVersion(content="You have to take the dog for a walk every day, which is tedious.", author=user2.uid, weight=0)
		textversion8 = TextVersion(content="We have no use for a watch dog.", author=user2.uid, weight=0)
		textversion9 = TextVersion(content="Going for a walk with the dog every day is not bad, because it is good for social interaction and physical exercise.", author=user2.uid, weight=0)
		textversion10 = TextVersion(content="It would be no problem to get both a cat and a dog.", author=user2.uid, weight=0)
		textversion11 = TextVersion(content="A cat and a dog will generally not get along well.", author=user2.uid, weight=0)
		textversion12 = TextVersion(content="We do not have enough money for two pets.", author=user2.uid, weight=0)
		textversion13 = TextVersion(content="A dog costs taxes and will be more expensive than a cat.", author=user2.uid, weight=0)
		textversion14 = TextVersion(content="Cats are fluffy.", author=user2.uid, weight=0)
		textversion15 = TextVersion(content="Cats are small.", author=user2.uid, weight=0)
		textversion16 = TextVersion(content="Fluffy animals losing much hair and I'm allergic to animal hair.", author=user2.uid, weight=0)
		textversion17 = TextVersion(content="You could use a automatic vacuum cleaner.", author=user2.uid, weight=0)
		DBSession.add_all([textversion1,textversion2,textversion3,textversion4,textversion5,textversion6,textversion7,textversion8,textversion9,textversion10,textversion11,textversion12,textversion13,textversion14,textversion15,textversion16,textversion17])
		DBSession.flush()

		textvalue1 = TextValue(textVersion=textversion1.uid)
		textvalue2 = TextValue(textVersion=textversion2.uid)
		textvalue3 = TextValue(textVersion=textversion3.uid)
		textvalue4 = TextValue(textVersion=textversion4.uid)
		textvalue5 = TextValue(textVersion=textversion5.uid)
		textvalue6 = TextValue(textVersion=textversion6.uid)
		textvalue7 = TextValue(textVersion=textversion7.uid)
		textvalue8 = TextValue(textVersion=textversion8.uid)
		textvalue9 = TextValue(textVersion=textversion9.uid)
		textvalue10 = TextValue(textVersion=textversion10.uid)
		textvalue11 = TextValue(textVersion=textversion11.uid)
		textvalue12 = TextValue(textVersion=textversion12.uid)
		textvalue13 = TextValue(textVersion=textversion13.uid)
		textvalue14 = TextValue(textVersion=textversion14.uid)
		textvalue15 = TextValue(textVersion=textversion15.uid)
		textvalue16 = TextValue(textVersion=textversion16.uid)
		textvalue17 = TextValue(textVersion=textversion17.uid)
		textversion1.textValue = textvalue1.uid
		textversion2.textValue = textvalue2.uid
		textversion3.textValue = textvalue3.uid
		textversion4.textValue = textvalue4.uid
		textversion5.textValue = textvalue5.uid
		textversion6.textValue = textvalue6.uid
		textversion7.textValue = textvalue7.uid
		textversion8.textValue = textvalue8.uid
		textversion9.textValue = textvalue9.uid
		textversion10.textValue = textvalue10.uid
		textversion11.textValue = textvalue11.uid
		textversion12.textValue = textvalue12.uid
		textversion13.textValue = textvalue13.uid
		textversion14.textValue = textvalue14.uid
		textversion15.textValue = textvalue15.uid
		textversion16.textValue = textvalue16.uid
		textversion17.textValue = textvalue17.uid
		DBSession.add_all([textvalue1,textvalue2,textvalue3,textvalue4,textvalue5,textvalue6,textvalue7,textvalue8,textvalue9,textvalue10,textvalue11,textvalue12,textvalue13,textvalue14,textvalue15,textvalue16,textvalue17])
		DBSession.flush()

		statement1 = Statement(text=textvalue1.uid)
		statement2 = Statement(text=textvalue2.uid)
		statement3 = Statement(text=textvalue3.uid)
		statement4 = Statement(text=textvalue4.uid)
		statement5 = Statement(text=textvalue5.uid)
		statement6 = Statement(text=textvalue6.uid)
		statement7 = Statement(text=textvalue7.uid)
		statement8 = Statement(text=textvalue8.uid)
		statement9 = Statement(text=textvalue9.uid)
		statement10 = Statement(text=textvalue10.uid)
		statement11 = Statement(text=textvalue11.uid)
		statement12 = Statement(text=textvalue12.uid)
		statement13 = Statement(text=textvalue13.uid)
		statement14 = Statement(text=textvalue14.uid)
		statement15 = Statement(text=textvalue15.uid)
		statement16 = Statement(text=textvalue16.uid)
		statement17 = Statement(text=textvalue17.uid)
		DBSession.add_all([statement1,statement2,statement3,statement4,statement5,statement6,statement7,statement8,statement9,statement10,statement11,statement12,statement13,statement14,statement15,statement16,statement17])
		DBSession.flush()

		premisseGroup1 = PremisseGroup(author=user2.uid)
		premisseGroup2 = PremisseGroup(author=user2.uid)
		premisseGroup3 = PremisseGroup(author=user2.uid)
		premisseGroup4 = PremisseGroup(author=user2.uid)
		premisseGroup5 = PremisseGroup(author=user2.uid)
		premisseGroup6 = PremisseGroup(author=user2.uid)
		premisseGroup7 = PremisseGroup(author=user2.uid)
		premisseGroup8 = PremisseGroup(author=user2.uid)
		premisseGroup9 = PremisseGroup(author=user2.uid)
		premisseGroup10 = PremisseGroup(author=user2.uid)
		premisseGroup11 = PremisseGroup(author=user2.uid)
		premisseGroup12 = PremisseGroup(author=user2.uid)
		premisseGroup13 = PremisseGroup(author=user2.uid)
		DBSession.add_all([premisseGroup1,premisseGroup2,premisseGroup3,premisseGroup4,premisseGroup5,premisseGroup6,premisseGroup7,premisseGroup8,premisseGroup9,premisseGroup10,premisseGroup11,premisseGroup12,premisseGroup13])
		DBSession.flush()

		premisse1 = Premisse(premissesGroup=premisseGroup1.uid, statement=statement4.uid, isNegated=False, author=user2.uid)
		premisse2 = Premisse(premissesGroup=premisseGroup2.uid, statement=statement5.uid, isNegated=False, author=user2.uid)
		premisse3 = Premisse(premissesGroup=premisseGroup3.uid, statement=statement6.uid, isNegated=False, author=user2.uid)
		premisse4 = Premisse(premissesGroup=premisseGroup4.uid, statement=statement7.uid, isNegated=False, author=user2.uid)
		premisse5 = Premisse(premissesGroup=premisseGroup5.uid, statement=statement8.uid, isNegated=False, author=user2.uid)
		premisse6 = Premisse(premissesGroup=premisseGroup6.uid, statement=statement9.uid, isNegated=False, author=user2.uid)
		premisse7 = Premisse(premissesGroup=premisseGroup7.uid, statement=statement10.uid, isNegated=False, author=user2.uid)
		premisse8 = Premisse(premissesGroup=premisseGroup8.uid, statement=statement11.uid, isNegated=False, author=user2.uid)
		premisse9 = Premisse(premissesGroup=premisseGroup9.uid, statement=statement12.uid, isNegated=False, author=user2.uid)
		premisse10 = Premisse(premissesGroup=premisseGroup10.uid, statement=statement13.uid, isNegated=False, author=user2.uid)
		premisse11 = Premisse(premissesGroup=premisseGroup11.uid, statement=statement14.uid, isNegated=False, author=user2.uid)
		premisse12 = Premisse(premissesGroup=premisseGroup11.uid, statement=statement15.uid, isNegated=False, author=user2.uid)
		premisse13 = Premisse(premissesGroup=premisseGroup12.uid, statement=statement16.uid, isNegated=False, author=user2.uid)
		premisse14 = Premisse(premissesGroup=premisseGroup13.uid, statement=statement17.uid, isNegated=False, author=user2.uid)
		DBSession.add_all([premisse1,premisse2,premisse3,premisse4,premisse5,premisse6,premisse7,premisse8,premisse9,premisse10,premisse11,premisse12,premisse13,premisse14])
		DBSession.flush()

		argument1 = Argument(premissegroup=premisseGroup1.uid, argument=None, conclusion=statement1.uid, isSupportive=True, author=user2.uid, weight=0)
		argument2 = Argument(premissegroup=premisseGroup2.uid, argument=None, conclusion=statement1.uid, isSupportive=False, author=user2.uid, weight=0)
		argument3 = Argument(premissegroup=premisseGroup3.uid, argument=None, conclusion=statement2.uid, isSupportive=True, author=user2.uid, weight=0)
		argument4 = Argument(premissegroup=premisseGroup4.uid, argument=None, conclusion=statement2.uid, isSupportive=False, author=user2.uid, weight=0)
		argument5 = Argument(premissegroup=premisseGroup5.uid, argument=argument3.uid, conclusion=None, isSupportive=False, author=user2.uid, weight=0)
		argument6 = Argument(premissegroup=premisseGroup6.uid, argument=argument4.uid, conclusion=None, isSupportive=False, author=user2.uid, weight=0)
		argument7 = Argument(premissegroup=premisseGroup7.uid, argument=None, conclusion=statement3.uid, isSupportive=True, author=user2.uid, weight=0)
		argument8 = Argument(premissegroup=premisseGroup8.uid, argument=argument7.uid, conclusion=None, isSupportive=False, author=user2.uid, weight=0)
		argument9 = Argument(premissegroup=premisseGroup9.uid, argument=None, conclusion=statement10.uid, isSupportive=False, author=user2.uid, weight=0)
		argument10 = Argument(premissegroup=premisseGroup10.uid, argument=None, conclusion=statement1.uid, isSupportive=True, author=user2.uid, weight=0)
		argument11 = Argument(premissegroup=premisseGroup11.uid, argument=None, conclusion=statement1.uid, isSupportive=True, author=user2.uid, weight=0)
		argument12 = Argument(premissegroup=premisseGroup12.uid, argument=argument11.uid, conclusion=None, isSupportive=False, author=user2.uid, weight=0)
		argument13 = Argument(premissegroup=premisseGroup13.uid, argument=argument12.uid, conclusion=None, isSupportive=False, author=user2.uid, weight=0)
		DBSession.add_all([argument1,argument2,argument3,argument4,argument5,argument6,argument7,argument8,argument9,argument10,argument11,argument12,argument13])
		DBSession.flush()

		transaction.commit()