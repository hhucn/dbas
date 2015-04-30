import os
import sys
import transaction

from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from ..models import DBSession, User, Argument, Position, RelationArgArg, RelationPosArg, Issue, Base


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

		# adding some dummy users
		model1 = User(firstname='admin', surename='admin', email='dbas@cs.uni-duesseldorf', password='admin', group='editors')
		model2 = User(firstname='Tobias', surename='Krauthoff', email='krauthoff@cs.uni-duesseldorf', password='test123', group='editors')
		model3 = User(firstname='Martin', surename='Mauve', email='mauve@cs.uni-duesseldorf', password='test123', group='editors')
		DBSession.add(model1)
		DBSession.add(model2)
		DBSession.add(model3)

		# adding some dummy positions
		position1 = Position(text='I like cats.', weight='100', author_id='1')
		position2 = Position(text='I like dogs.', weight='20', author_id='2')
		DBSession.add(position1)
		DBSession.add(position2)

		# adding some dummy arguments
		argument1 = Argument(text='They are fluffy.', weight='100', author_id='1')
		argument2 = Argument(text='They are indepently.', weight='50', author_id='2')
		argument3 = Argument(text='They are hating all humans!', weight='70', author_id='3')

		argument4 = Argument(text='They are very devoted.', weight='80', author_id='1')
		argument5 = Argument(text='They can protect you', weight='63', author_id='2')
		argument6 = Argument(text='They smell when it\'s raining', weight='110', author_id='2')
		DBSession.add(argument1)
		DBSession.add(argument2)
		DBSession.add(argument3)
		DBSession.add(argument4)
		DBSession.add(argument5)
		DBSession.add(argument6)

		# adding some dummy relations
		relation1 = RelationPosArg(weight='134', pos_uid='1', arg_uid='1', author_id='1', is_supportive='1')
		relation2 = RelationPosArg(weight='45', pos_uid='1', arg_uid='2', author_id='1', is_supportive='1')
		relation3 = RelationPosArg(weight='46', pos_uid='1', arg_uid='3', author_id='2', is_supportive='0')
		relation4 = RelationPosArg(weight='24', pos_uid='2', arg_uid='4', author_id='3', is_supportive='1')
		relation5 = RelationPosArg(weight='18', pos_uid='2', arg_uid='5', author_id='3', is_supportive='1')
		relation6 = RelationPosArg(weight='81', pos_uid='2', arg_uid='6', author_id='2', is_supportive='0')
		relation7 = RelationArgArg(weight='132', arg_uid1='1', arg_uid2='6', author_id='3', is_supportive='0')
		relation8 = RelationArgArg(weight='46', arg_uid1='4', arg_uid2='5', author_id='2', is_supportive='1')
		DBSession.add(relation1)
		DBSession.add(relation2)
		DBSession.add(relation3)
		DBSession.add(relation4)
		DBSession.add(relation5)
		DBSession.add(relation6)
		DBSession.add(relation7)
		DBSession.add(relation8)
