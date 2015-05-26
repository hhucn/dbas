import os
import sys
import transaction

from dbas.helper import PasswordHandler
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.model import DBSession, User, Argument, Position, RelationArgArg, RelationArgPos, RelationPosArg, \
	RelationPosPos,\
	Group, Issue, Base


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
		issue = Issue(text="Your familiy argues about whether to buy a cat or dog as pet. Now your opinion matters!");
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
		pw2 = pwHandler.get_hashed_password('test123')
		pw3 = pwHandler.get_hashed_password('test123')
		pw4 = pwHandler.get_hashed_password('test')
		pw5 = pwHandler.get_hashed_password('test')
		user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas@cs.uni-duesseldorf.de', password=pw1)
		user2 = User(firstname='Tobias', surname='Krauthoff', nickname='Tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2)
		user3 = User(firstname='Martin', surname='Mauve', nickname='Martin', email='mauve@cs.uni-duesseldorf', password=pw3)
		user4 = User(firstname='editor', surname='editor', nickname='editor', email='nope1@nopeville.com', password=pw4)
		user5 = User(firstname='user', surname='user', nickname='user', email='nope2@nopeville.com', password=pw5)
		user1.group = group1.uid
		user2.group = group1.uid
		user3.group = group1.uid
		user4.group = group1.uid
		user5.group = group2.uid
		DBSession.add_all([user1, user2, user3, user4, user5])
		DBSession.flush()

		# adding some dummy positions
		position1 = Position(text='We should get a cat.', weight=100)
		position2 = Position(text='We should get a dog.', weight=20)
		position1.author = user1.uid
		position2.author = user2.uid
		DBSession.add_all([position1, position2])
		#transaction.commit()

		# adding some dummy arguments
		argument1 = Argument(text='Cats are very independent.', weight=10)
		argument2 = Argument(text='Cats are capricious.', weight=20)
		argument3 = Argument(text='Dogs can act as watch dog.', weight=30)
		argument4 = Argument(text='You have to take the dog for a walk every day, which is tedious.', weight=40)
		argument5 = Argument(text='We have no use for a watch dog.', weight=50)
		argument6 = Argument(text='Going for a walk with the dog every day is not bad, because it is good for social '
		                          'interaction and physical exercise.', weight=60)
		argument7 = Argument(text='It would be no problem to get both a cat and a dog.', weight=70)
		argument8 = Argument(text='A cat and a dog will generally not get along well.', weight=80)
		argument9 = Argument(text='We do not have enough money for two pets.', weight=90)
		argument10 = Argument(text='A dog costs taxes and will be more expensive than a cat.', weight=100)
		argument11 = Argument(text='A cat will break our interior and will be more expensive than a dog.', weight=110)

		argument1.author = user1.uid
		argument2.author = user1.uid
		argument3.author = user1.uid
		argument4.author = user1.uid
		argument5.author = user1.uid
		argument6.author = user1.uid
		argument7.author = user1.uid
		argument8.author = user1.uid
		argument9.author = user1.uid
		argument10.author = user1.uid
		argument11.author = user1.uid
		DBSession.add_all([argument1, argument2, argument3, argument4, argument5, argument6, argument7, argument8, argument9, argument10,
		                   argument11])
		DBSession.flush()

		# adding some dummy relations
		relation1 = RelationArgPos(weight=134, is_supportive=True)
		relation2 = RelationArgPos(weight=45, is_supportive=False)
		relation3 = RelationArgPos(weight=46, is_supportive=False)
		relation4 = RelationArgPos(weight=24, is_supportive=False)
		relation5 = RelationArgArg(weight=18, is_supportive=False)
		relation6 = RelationArgArg(weight=81, is_supportive=False)
		relation7 = RelationArgPos(weight=132, is_supportive=True)
		relation8 = RelationArgPos(weight=46, is_supportive=True)
		relation9 = RelationArgArg(weight=132, is_supportive=False)
		relation10 = RelationArgArg(weight=81, is_supportive=False)
		relation11 = RelationArgPos(weight=132, is_supportive=False)
		relation12 = RelationArgPos(weight=46, is_supportive=False)
		relation13 = RelationArgArg(weight=132, is_supportive=False)
		relation14 = RelationArgArg(weight=46, is_supportive=False)
		relation15 = RelationArgPos(weight=132, is_supportive=False)
		relation1.author = user1.uid
		relation2.author = user1.uid
		relation3.author = user1.uid
		relation4.author = user1.uid
		relation5.author = user1.uid
		relation6.author = user1.uid
		relation7.author = user1.uid
		relation8.author = user1.uid
		relation9.author = user1.uid
		relation10.author = user1.uid
		relation11.author = user1.uid
		relation12.author = user1.uid
		relation13.author = user1.uid
		relation14.author = user1.uid
		relation15.author = user1.uid

		relation1.arg_uid = argument1.uid
		relation2.arg_uid = argument2.uid
		relation3.arg_uid = argument3.uid
		relation4.arg_uid = argument4.uid
		relation5.arg_uid = argument5.uid
		relation6.arg_uid = argument6.uid
		relation7.arg_uid = argument7.uid
		relation8.arg_uid = argument7.uid
		relation9.arg_uid = argument8.uid
		relation10.arg_uid = argument9.uid
		relation11.arg_uid = argument10.uid
		relation12.arg_uid = argument11.uid
		relation13.arg_uid = argument11.uid
		relation14.arg_uid = argument10.uid
		relation15.arg_uid = argument11.uid

		relation1.pos_uid = position1.uid
		relation2.pos_uid = position1.uid
		relation3.pos_uid = position2.uid
		relation4.pos_uid = position2.uid
		relation5.arg_uid = argument3.uid
		relation6.arg_uid = argument4.uid
		relation7.pos_uid = position1.uid
		relation8.pos_uid = position2.uid
		relation9.arg_uid = argument7.uid
		relation10.arg_uid = argument7.uid
		relation11.pos_uid = position2.uid
		relation12.pos_uid = position1.uid
		relation13.arg_uid = argument10.uid
		relation14.arg_uid = argument11.uid
		relation15.pos_uid = position2.uid


		DBSession.add_all([relation1, relation2, relation3, relation4, relation5, relation6, relation7, relation8,
		                   relation9, relation10, relation11, relation12, relation13, relation14, relation15])
		DBSession.flush()

		transaction.commit()
