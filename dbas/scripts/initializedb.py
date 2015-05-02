import os
import sys
import transaction

from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.model import DBSession, User, Argument, Position, RelationArgArg, RelationArgPos, RelationPosPos, Group, Issue, Base


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
		issue = Issue(text="Are you cat- or dog-person?");
		DBSession.add(issue)

		# addng groups
		group1 = Group(name='editor')
		group2 = Group(name='user')
		DBSession.add(group1)
		DBSession.add(group2)
		DBSession.flush()

		# adding some dummy users
		print(group1.uid)
		user1 = User(firstname='admin', surename='admin', email='dbas@cs.uni-duesseldorf', password='admin')
		user2 = User(firstname='Tobias', surename='Krauthoff', email='krauthoff@cs.uni-duesseldorf', password='test123')
		user3 = User(firstname='Martin', surename='Mauve', email='mauve@cs.uni-duesseldorf', password='test123')
		user4 = User(firstname='editor', surename='editor', email='nope1@nopeville.com', password='test')
		user5 = User(firstname='user', surename='user', email='nope2@nopeville.com', password='test')
		user1.group = group1.uid
		user2.group = group1.uid
		user3.group = group1.uid
		user4.group = group1.uid
		user5.group = group2.uid
		DBSession.add(user1)
		DBSession.add(user2)
		DBSession.add(user3)
		DBSession.add(user4)
		DBSession.add(user5)
		DBSession.flush()

		# adding some dummy positions
		position1 = Position(text='I like cats.', weight='100')
		position2 = Position(text='I like dogs.', weight='20')
		position1.author = user1.uid
		position2.author = user2.uid
		DBSession.add(position1)
		DBSession.add(position2)
		#transaction.commit()

		# adding some dummy arguments
		argument1 = Argument(text='They are fluffy.', weight='100')
		argument2 = Argument(text='They are indepently.', weight='50')
		argument3 = Argument(text='They are hating all humans!', weight='70')
		argument4 = Argument(text='They are very devoted.', weight='80')
		argument5 = Argument(text='They can protect you', weight='63')
		argument6 = Argument(text='They smell when it\'s raining', weight='110')
		argument1.author = user1.uid
		argument2.author = user1.uid
		argument3.author = user2.uid
		argument4.author = user3.uid
		argument5.author = user3.uid
		argument6.author = user1.uid
		DBSession.add(argument1)
		DBSession.add(argument2)
		DBSession.add(argument3)
		DBSession.add(argument4)
		DBSession.add(argument5)
		DBSession.add(argument6)
		DBSession.flush()

		# adding some dummy relations
		relation1 = RelationArgPos(weight='134', is_supportive='1')
		relation2 = RelationArgPos(weight='45', is_supportive='1')
		relation3 = RelationArgPos(weight='46', is_supportive='0')
		relation4 = RelationArgPos(weight='24', is_supportive='1')
		relation5 = RelationArgPos(weight='18', is_supportive='1')
		relation6 = RelationArgPos(weight='81', is_supportive='0')
		relation7 = RelationArgArg(weight='132', is_supportive='0')
		relation8 = RelationArgArg(weight='46', is_supportive='1')
		relation9 = RelationPosPos(weight='132', is_supportive='0')
		relation1.author = user1.uid
		relation2.author = user2.uid
		relation3.author = user3.uid
		relation4.author = user2.uid
		relation5.author = user2.uid
		relation6.author = user3.uid
		relation7.author = user3.uid
		relation8.author = user1.uid
		relation9.author = user3.uid
		relation1.arg_uid = argument1.uid
		relation2.arg_uid = argument2.uid
		relation3.arg_uid = argument3.uid
		relation4.arg_uid = argument4.uid
		relation5.arg_uid = argument5.uid
		relation6.arg_uid = argument6.uid
		relation7.arg_uid1 = argument6.uid
		relation8.arg_uid1 = argument5.uid
		relation9.pos_uid1 = argument1.uid
		relation1.pos_uid = position1.uid
		relation2.pos_uid = position1.uid
		relation3.pos_uid = position1.uid
		relation4.pos_uid = position2.uid
		relation5.pos_uid = position2.uid
		relation6.pos_uid = position2.uid
		relation7.arg_uid2 = argument1.uid
		relation8.arg_uid2 = argument4.uid
		relation9.pos_uid2 = argument6.uid
		DBSession.add(relation1)
		DBSession.add(relation2)
		DBSession.add(relation3)
		DBSession.add(relation4)
		DBSession.add(relation5)
		DBSession.add(relation6)
		DBSession.add(relation7)
		DBSession.add(relation8)
		DBSession.add(relation9)
		DBSession.flush()

		transaction.commit()
