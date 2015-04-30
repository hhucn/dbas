import os
import sys
import transaction

from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from ..models import DBSession, User, Argument, Position, RelationArgArg, RelationArgPos, Group, Issue, Base


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

		# adding some dummy users
		user1 = User(firstname='admin', surename='admin', email='dbas@cs.uni-duesseldorf', password='admin')
		user2 = User(firstname='Tobias', surename='Krauthoff', email='krauthoff@cs.uni-duesseldorf', password='test123')
		user3 = User(firstname='Martin', surename='Mauve', email='mauve@cs.uni-duesseldorf', password='test123')
		user1.group.append(group1)
		user2.group.append(group1)
		user3.group.append(group1)
		DBSession.add(user1, user2, user3)

		# adding some dummy positions
		position1 = Position(text='I like cats.', weight='100')
		position2 = Position(text='I like dogs.', weight='20')
		position1.author.append(user1)
		position2.author.append(user2)
		DBSession.add(position1)
		DBSession.add(position2)

		# adding some dummy arguments
		argument1 = Argument(text='They are fluffy.', weight='100')
		argument2 = Argument(text='They are indepently.', weight='50')
		argument3 = Argument(text='They are hating all humans!', weight='70')
		argument4 = Argument(text='They are very devoted.', weight='80')
		argument5 = Argument(text='They can protect you', weight='63')
		argument6 = Argument(text='They smell when it\'s raining', weight='110')
		argument1.author.append(user1)
		argument2.author.append(user1)
		argument3.author.append(user2)
		argument4.author.append(user3)
		argument5.author.append(user3)
		argument6.author.append(user1)
		DBSession.add(argument1, argument2, argument3, argument4, argument5, argument6)

		# adding some dummy relations
		relation1 = RelationArgPos(weight='134', is_supportive='1')
		relation2 = RelationArgPos(weight='45', is_supportive='1')
		relation3 = RelationArgPos(weight='46', is_supportive='0')
		relation4 = RelationArgPos(weight='24', is_supportive='1')
		relation5 = RelationArgPos(weight='18', is_supportive='1')
		relation6 = RelationArgPos(weight='81', is_supportive='0')
		relation7 = RelationArgArg(weight='132', is_supportive='0')
		relation8 = RelationArgArg(weight='46', is_supportive='1')
		relation1.author.append(user1)
		relation2.author.append(user2)
		relation3.author.append(user3)
		relation4.author.append(user2)
		relation5.author.append(user2)
		relation6.author.append(user3)
		relation7.author.append(user3)
		relation8.author.append(user1)
		relation1.arg_uid.append(argument1)
		relation2.arg_uid.append(argument2)
		relation3.arg_uid.append(argument3)
		relation4.arg_uid.append(argument4)
		relation5.arg_uid.append(argument5)
		relation6.arg_uid.append(argument6)
		relation7.arg_uid1.append(argument6)
		relation8.arg_uid1.append(argument5)
		relation1.pos_uid.append(position1)
		relation2.pos_uid.append(position1)
		relation3.pos_uid.append(position1)
		relation4.pos_uid.append(position2)
		relation5.pos_uid.append(position2)
		relation6.pos_uid.append(position2)
		relation7.arg_uid2.append(argument1)
		relation8.arg_uid2.append(argument4)
		DBSession.add(relation1, relation2, relation3, relation4, relation5, relation6, relation7, relation8)
