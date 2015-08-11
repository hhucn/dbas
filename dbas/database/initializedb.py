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
		pw4 = pwHandler.get_hashed_password('kalman')
		pw5 = pwHandler.get_hashed_password('mladen')
		user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas@cs.uni-duesseldorf.de', password=pw1, group=group0.uid, gender='m')
		user2 = User(firstname='Tobias', surname='Krauthoff', nickname='tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2, group=group1.uid, gender='m')
		user3 = User(firstname='Martin', surname='Mauve', nickname='martin', email='mauve@cs.uni-duesseldorf', password=pw3, group=group1.uid, gender='m')
		user4 = User(firstname='Kalman', surname='Graffi', nickname='kalman', email='graffi@cs.uni-duesseldorf.de', password=pw4, group=group1.uid, gender='m')
		user5 = User(firstname='Mladen', surname='Topic', nickname='mladen', email='mladen.topic@hhu.de', password=pw5, group=group1.uid, gender='m')
		DBSession.add_all([user1, user2, user3, user4, user5])
		DBSession.flush()

		#Adding all textversions
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

		#Adding all textvalues
		textvalue1 = TextValue(textversion=textversion1.uid)
		textvalue2 = TextValue(textversion=textversion2.uid)
		textvalue3 = TextValue(textversion=textversion3.uid)
		textvalue4 = TextValue(textversion=textversion4.uid)
		textvalue5 = TextValue(textversion=textversion5.uid)
		textvalue6 = TextValue(textversion=textversion6.uid)
		textvalue7 = TextValue(textversion=textversion7.uid)
		textvalue8 = TextValue(textversion=textversion8.uid)
		textvalue9 = TextValue(textversion=textversion9.uid)
		textvalue10 = TextValue(textversion=textversion10.uid)
		textvalue11 = TextValue(textversion=textversion11.uid)
		textvalue12 = TextValue(textversion=textversion12.uid)
		textvalue13 = TextValue(textversion=textversion13.uid)
		textvalue14 = TextValue(textversion=textversion14.uid)
		textvalue15 = TextValue(textversion=textversion15.uid)
		textvalue16 = TextValue(textversion=textversion16.uid)
		textvalue17 = TextValue(textversion=textversion17.uid)
		DBSession.add_all([textvalue1,textvalue2,textvalue3,textvalue4,textvalue5,textvalue6,textvalue7,textvalue8,textvalue9,textvalue10,textvalue11,textvalue12,textvalue13,textvalue14,textvalue15,textvalue16,textvalue17])
		DBSession.flush()

		#Set textvalues of the textversions
		textversion1.set_textvalue(textvalue1.uid)
		textversion2.set_textvalue(textvalue2.uid)
		textversion3.set_textvalue(textvalue3.uid)
		textversion4.set_textvalue(textvalue4.uid)
		textversion5.set_textvalue(textvalue5.uid)
		textversion6.set_textvalue(textvalue6.uid)
		textversion7.set_textvalue(textvalue7.uid)
		textversion8.set_textvalue(textvalue8.uid)
		textversion9.set_textvalue(textvalue9.uid)
		textversion10.set_textvalue(textvalue10.uid)
		textversion11.set_textvalue(textvalue11.uid)
		textversion12.set_textvalue(textvalue12.uid)
		textversion13.set_textvalue(textvalue13.uid)
		textversion14.set_textvalue(textvalue14.uid)
		textversion15.set_textvalue(textvalue15.uid)
		textversion16.set_textvalue(textvalue16.uid)
		textversion17.set_textvalue(textvalue17.uid)
		DBSession.flush()

		#Adding all statements
		statement1 = Statement(text=textvalue1.uid, isstartpoint=True)
		statement2 = Statement(text=textvalue2.uid, isstartpoint=True)
		statement3 = Statement(text=textvalue3.uid, isstartpoint=True)
		statement4 = Statement(text=textvalue4.uid, isstartpoint=False)
		statement5 = Statement(text=textvalue5.uid, isstartpoint=False)
		statement6 = Statement(text=textvalue6.uid, isstartpoint=False)
		statement7 = Statement(text=textvalue7.uid, isstartpoint=False)
		statement8 = Statement(text=textvalue8.uid, isstartpoint=False)
		statement9 = Statement(text=textvalue9.uid, isstartpoint=False)
		statement10 = Statement(text=textvalue10.uid, isstartpoint=False)
		statement11 = Statement(text=textvalue11.uid, isstartpoint=False)
		statement12 = Statement(text=textvalue12.uid, isstartpoint=False)
		statement13 = Statement(text=textvalue13.uid, isstartpoint=False)
		statement14 = Statement(text=textvalue14.uid, isstartpoint=False)
		statement15 = Statement(text=textvalue15.uid, isstartpoint=False)
		statement16 = Statement(text=textvalue16.uid, isstartpoint=False)
		statement17 = Statement(text=textvalue17.uid, isstartpoint=False)
		DBSession.add_all([statement1,statement2,statement3,statement4,statement5,statement6,statement7,statement8,statement9,statement10,statement11,statement12,statement13,statement14,statement15,statement16,statement17])
		DBSession.flush()

		#Adding all premissegroups
		premissegroup1 = PremisseGroup(author=user2.uid)
		premissegroup2 = PremisseGroup(author=user2.uid)
		premissegroup3 = PremisseGroup(author=user2.uid)
		premissegroup4 = PremisseGroup(author=user2.uid)
		premissegroup5 = PremisseGroup(author=user2.uid)
		premissegroup6 = PremisseGroup(author=user2.uid)
		premissegroup7 = PremisseGroup(author=user2.uid)
		premissegroup8 = PremisseGroup(author=user2.uid)
		premissegroup9 = PremisseGroup(author=user2.uid)
		premissegroup10 = PremisseGroup(author=user2.uid)
		premissegroup11 = PremisseGroup(author=user2.uid)
		premissegroup12 = PremisseGroup(author=user2.uid)
		premissegroup13 = PremisseGroup(author=user2.uid)
		DBSession.add_all([premissegroup1,premissegroup2,premissegroup3,premissegroup4,premissegroup5,premissegroup6,premissegroup7,premissegroup8,premissegroup9,premissegroup10,premissegroup11,premissegroup12,premissegroup13])
		DBSession.flush()

		premisse1 = Premisse(premissesgroup=premissegroup1.uid, statement=statement4.uid, isnegated=False, author=user2.uid)
		premisse2 = Premisse(premissesgroup=premissegroup2.uid, statement=statement5.uid, isnegated=False, author=user2.uid)
		premisse3 = Premisse(premissesgroup=premissegroup3.uid, statement=statement6.uid, isnegated=False, author=user2.uid)
		premisse4 = Premisse(premissesgroup=premissegroup4.uid, statement=statement7.uid, isnegated=False, author=user2.uid)
		premisse5 = Premisse(premissesgroup=premissegroup5.uid, statement=statement8.uid, isnegated=False, author=user2.uid)
		premisse6 = Premisse(premissesgroup=premissegroup6.uid, statement=statement9.uid, isnegated=False, author=user2.uid)
		premisse7 = Premisse(premissesgroup=premissegroup7.uid, statement=statement10.uid, isnegated=False, author=user2.uid)
		premisse8 = Premisse(premissesgroup=premissegroup8.uid, statement=statement11.uid, isnegated=False, author=user2.uid)
		premisse9 = Premisse(premissesgroup=premissegroup9.uid, statement=statement12.uid, isnegated=False, author=user2.uid)
		premisse10 = Premisse(premissesgroup=premissegroup10.uid, statement=statement13.uid, isnegated=False, author=user2.uid)
		premisse11 = Premisse(premissesgroup=premissegroup11.uid, statement=statement14.uid, isnegated=False, author=user2.uid)
		premisse12 = Premisse(premissesgroup=premissegroup11.uid, statement=statement15.uid, isnegated=False, author=user2.uid)
		premisse13 = Premisse(premissesgroup=premissegroup12.uid, statement=statement16.uid, isnegated=False, author=user2.uid)
		premisse14 = Premisse(premissesgroup=premissegroup13.uid, statement=statement17.uid, isnegated=False, author=user2.uid)
		DBSession.add_all([premisse1,premisse2,premisse3,premisse4,premisse5,premisse6,premisse7,premisse8,premisse9,premisse10,premisse11,premisse12,premisse13,premisse14])
		DBSession.flush()

		#Adding all arguments and set the adjacency list
		argument1 = Argument(premissegroup=premissegroup1.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement1.uid)
		argument2 = Argument(premissegroup=premissegroup2.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement1.uid)
		argument3 = Argument(premissegroup=premissegroup3.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement2.uid)
		argument4 = Argument(premissegroup=premissegroup4.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement2.uid)
		argument5 = Argument(premissegroup=premissegroup5.uid, issupportive=False, author=user2.uid, weight=0)
		argument6 = Argument(premissegroup=premissegroup6.uid, issupportive=False, author=user2.uid, weight=0)
		argument7 = Argument(premissegroup=premissegroup7.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement3.uid)
		argument8 = Argument(premissegroup=premissegroup8.uid, issupportive=False, author=user2.uid, weight=0)
		argument9 = Argument(premissegroup=premissegroup9.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement10.uid)
		argument10 = Argument(premissegroup=premissegroup10.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement1.uid)
		argument11 = Argument(premissegroup=premissegroup11.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement1.uid)
		argument12 = Argument(premissegroup=premissegroup12.uid, issupportive=False, author=user2.uid, weight=0)
		argument13 = Argument(premissegroup=premissegroup13.uid, issupportive=False, author=user2.uid, weight=0)
		DBSession.add_all([argument1,argument2,argument3,argument4,argument5,argument6,argument7,argument8,argument9,argument10,argument11,argument12,argument13])
		DBSession.flush()

		argument5.conclusions_argument(argument3.uid)
		argument6.conclusions_argument(argument4.uid)
		argument8.conclusions_argument(argument7.uid)
		argument12.conclusions_argument(argument11.uid)
		argument13.conclusions_argument(argument12.uid)
		DBSession.flush()

		transaction.commit()