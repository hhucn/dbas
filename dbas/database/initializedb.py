import os
import sys
import transaction

from dbas.helper import PasswordHandler
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.model import DBSession, User, Argument, Position, RelationArgArg, RelationArgPos, Group, Issue, Base


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
		user5 = User(firstname='Kalman', surname='Graffi', nickname='Kalman', email='graffi@cs.uni-duesseldorf.de', password=pw5, gender='m')
		user1.group = group0.uid
		user2.group = group1.uid
		user3.group = group1.uid
		user4.group = group1.uid
		user5.group = group2.uid
		user4.group = group1.uid
		user5.group = group1.uid
		DBSession.add_all([user1, user2, user3, user4, user5])
		DBSession.flush()

		# adding all positions out of the discussion
		position1 = Position(text='We should get a cat.', weight=0)
		position2 = Position(text='We should get a dog.', weight=0)
		position3 = Position(text='We should neither get a cat nor a dog.', weight=0)
		position4 = Position(text='We could get both, a cat and a dog.', weight=0)
		position1.author = user1.uid
		position2.author = user1.uid
		position3.author = user1.uid
		position4.author = user1.uid
		DBSession.add_all([position1, position2, position3, position4])
		DBSession.flush()

		# adding all arguments out of the discussion
		argument1 = Argument(text='Cats are very independent.', weight=0)
		argument2 = Argument(text='Cats are capricious.', weight=0)
		argument3 = Argument(text='Dogs can act as watch dogs.', weight=0)
		argument4 = Argument(text='You have to take the dog for a walk every day, which is tedious.', weight=0)
		argument5 = Argument(text='We have no use for a watch dog.', weight=0)
		argument6 = Argument(text='Going for a walk with the dog every day is not bad, because it is good for social interaction and physical exercise.', weight=0)
		argument7 = Argument(text='It would be no problem to get both a cat and a dog.', weight=0)
		argument8 = Argument(text='A cat and a dog will generally not get along well.', weight=0)
		argument9 = Argument(text='We do not have enough money for two pets.', weight=0)
		argument10 = Argument(text='A dog costs taxes and will be more expensive than a cat.', weight=0)
		argument11 = Argument(text='A cat will break our interior and will be more expensive than a dog.', weight=0)
		argument12 = Argument(text='I am allergic to animal hair.', weight=0)
		argument13 = Argument(text='Cats and dogs are loosing many hairs and this will cause more dirt in our flat.', weight=0)
		argument14 = Argument(text='A cat does not cost any taxes.', weight=0)
		argument15 = Argument(text='A dog can be trained to detect cancer in humans, neither can a cat.', weight=0)
		argument16 = Argument(text='A cat just shits in a box.', weight=0)
		argument17 = Argument(text='Dogs are dependent on human for everything with personality of a slave.', weight=0)
		argument18 = Argument(text='Trained animals are like slaves.', weight=0)
		argument19 = Argument(text='Dogs can be teached and learn cool tricks.', weight=0)
		argument20 = Argument(text='Neither we have use for a cat.', weight=0)
		argument21 = Argument(text='You cannot go on vaction, because you have to take care of your pet.', weight=0)
		argument22 = Argument(text='They are not like trained animals in the zoo, but rather well educated.', weight=0)
		argument23 = Argument(text='This is a cliche, which only happens in comics.', weight=0)
		argument24 = Argument(text='Cats must be fed, too.', weight=0)
		argument25 = Argument(text='Cats want expressives toys, dogs only a bone or branch.', weight=0)
		argument26 = Argument(text='There are naked cats without any hair.', weight=0)
		argument27 = Argument(text='Even a cat can be trained.', weight=0)
		argument28 = Argument(text='You have to dispose your dog\'s poop while taking him for a walk.', weight=0)
		argument29 = Argument(text='But there are still some races who cannot be trained.', weight=0)
		argument30 = Argument(text='They can get along well, if they are early next to each other.', weight=0)
		argument31 = Argument(text='They can get along well, because I\'ve seen this by a friend of mine.', weight=0)
		argument32 = Argument(text='You can go on vacation, because often family & friends take care of your pet.', weight=0)
		argument33 = Argument(text='Naked cats are ugly. Then I prefer dogs.', weight=0)
		argument34 = Argument(text='If you\'ve got a pet, this is your job, because you have the responsibility for a living beeing.', weight=0)
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
		argument12.author = user1.uid
		argument13.author = user1.uid
		argument14.author = user1.uid
		argument15.author = user1.uid
		argument16.author = user1.uid
		argument17.author = user1.uid
		argument18.author = user1.uid
		argument19.author = user1.uid
		argument20.author = user1.uid
		argument21.author = user1.uid
		argument22.author = user1.uid
		argument23.author = user1.uid
		argument24.author = user1.uid
		argument25.author = user1.uid
		argument26.author = user1.uid
		argument27.author = user1.uid
		argument28.author = user1.uid
		argument29.author = user1.uid
		argument30.author = user1.uid
		argument31.author = user1.uid
		argument32.author = user1.uid
		argument33.author = user1.uid
		argument34.author = user1.uid
		DBSession.add_all([argument1, argument2, argument3, argument4, argument5, argument6, argument7, argument8, argument9, argument10, argument11, argument12, argument13, argument14, argument15, argument16, argument17, argument18, argument19, argument20, argument21, argument22, argument23, argument24, argument25, argument26, argument27, argument28, argument29, argument30, argument31, argument32, argument33, argument34])
		DBSession.flush()

		# adding all relations out of the discussion
		relation1 = RelationArgPos(weight=0, is_supportive=True)
		relation2 = RelationArgPos(weight=0, is_supportive=False)
		relation3 = RelationArgPos(weight=0, is_supportive=True)
		relation4 = RelationArgPos(weight=0, is_supportive=False)
		relation5 = RelationArgArg(weight=0, is_supportive=False)
		relation6 = RelationArgArg(weight=0, is_supportive=False)
		relation7 = RelationArgPos(weight=0, is_supportive=True)
		relation8 = RelationArgPos(weight=0, is_supportive=True)
		relation9 = RelationArgArg(weight=0, is_supportive=False)
		relation10 = RelationArgArg(weight=0, is_supportive=False)
		relation11 = RelationArgPos(weight=0, is_supportive=False)
		relation12 = RelationArgPos(weight=0, is_supportive=False)
		relation13 = RelationArgArg(weight=0, is_supportive=False)
		relation14 = RelationArgArg(weight=0, is_supportive=False)
		relation15 = RelationArgPos(weight=0, is_supportive=True)
		relation16 = RelationArgPos(weight=0, is_supportive=True)
		relation17 = RelationArgPos(weight=0, is_supportive=False)
		relation18 = RelationArgPos(weight=0, is_supportive=False)
		relation19 = RelationArgPos(weight=0, is_supportive=False)
		relation20 = RelationArgPos(weight=0, is_supportive=False)
		relation21 = RelationArgPos(weight=0, is_supportive=True)
		relation22 = RelationArgArg(weight=0, is_supportive=True)
		relation23 = RelationArgArg(weight=0, is_supportive=False)
		relation24 = RelationArgArg(weight=0, is_supportive=False)
		relation25 = RelationArgPos(weight=0, is_supportive=True)
		relation26 = RelationArgPos(weight=0, is_supportive=False)
		relation27 = RelationArgArg(weight=0, is_supportive=True)
		relation28 = RelationArgPos(weight=0, is_supportive=False)
		relation29 = RelationArgPos(weight=0, is_supportive=False)
		relation30 = RelationArgArg(weight=0, is_supportive=False)
		relation31 = RelationArgArg(weight=0, is_supportive=True)
		relation32 = RelationArgPos(weight=0, is_supportive=False)
		relation33 = RelationArgPos(weight=0, is_supportive=True)
		relation34 = RelationArgArg(weight=0, is_supportive=False)
		relation35 = RelationArgArg(weight=0, is_supportive=False)
		relation36 = RelationArgPos(weight=0, is_supportive=True)
		relation37 = RelationArgArg(weight=0, is_supportive=True)
		relation38 = RelationArgArg(weight=0, is_supportive=True)
		relation39 = RelationArgArg(weight=0, is_supportive=False)
		relation40 = RelationArgPos(weight=0, is_supportive=False)
		relation41 = RelationArgPos(weight=0, is_supportive=False)
		relation42 = RelationArgPos(weight=0, is_supportive=True)
		relation43 = RelationArgArg(weight=0, is_supportive=True)
		relation44 = RelationArgArg(weight=0, is_supportive=False)
		relation45 = RelationArgArg(weight=0, is_supportive=False)
		relation46 = RelationArgArg(weight=0, is_supportive=False)
		relation47 = RelationArgArg(weight=0, is_supportive=False)
		relation48 = RelationArgArg(weight=0, is_supportive=False)
		relation49 = RelationArgArg(weight=0, is_supportive=False)
		relation50 = RelationArgArg(weight=0, is_supportive=False)
		relation51 = RelationArgArg(weight=0, is_supportive=False)
		relation52 = RelationArgPos(weight=0, is_supportive=False)
		relation53 = RelationArgPos(weight=0, is_supportive=False)
		relation54 = RelationArgPos(weight=0, is_supportive=True)
		relation55 = RelationArgPos(weight=0, is_supportive=False)
		relation56 = RelationArgArg(weight=0, is_supportive=False)
		relation57 = RelationArgArg(weight=0, is_supportive=False)
		relation58 = RelationArgArg(weight=0, is_supportive=False)
		relation59 = RelationArgArg(weight=0, is_supportive=False)
		relation60 = RelationArgArg(weight=0, is_supportive=False)
		relation61 = RelationArgArg(weight=0, is_supportive=False)
		relation62 = RelationArgArg(weight=0, is_supportive=False)

		# adding the startpoints of the relations
		relation1.arg_uid = argument1.uid
		relation2.arg_uid = argument2.uid
		relation3.arg_uid = argument3.uid
		relation4.arg_uid = argument4.uid
		relation5.arg_uid1 = argument5.uid
		relation6.arg_uid1 = argument6.uid
		relation7.arg_uid = argument7.uid
		relation8.arg_uid = argument7.uid
		relation9.arg_uid1 = argument8.uid
		relation10.arg_uid1 = argument9.uid
		relation11.arg_uid = argument10.uid
		relation12.arg_uid = argument11.uid
		relation13.arg_uid1 = argument11.uid
		relation14.arg_uid1 = argument10.uid
		relation15.arg_uid = argument11.uid
		relation16.arg_uid = argument12.uid
		relation17.arg_uid = argument12.uid
		relation18.arg_uid = argument12.uid
		relation19.arg_uid = argument13.uid
		relation20.arg_uid = argument13.uid
		relation21.arg_uid = argument13.uid
		relation22.arg_uid1 = argument13.uid
		relation23.arg_uid1 = argument14.uid
		relation24.arg_uid1 = argument11.uid
		relation25.arg_uid = argument15.uid
		relation26.arg_uid = argument15.uid
		relation27.arg_uid1 = argument15.uid
		relation28.arg_uid = argument16.uid
		relation29.arg_uid = argument17.uid
		relation30.arg_uid1 = argument16.uid
		relation31.arg_uid1 = argument19.uid
		relation32.arg_uid = argument21.uid
		relation33.arg_uid = argument14.uid
		relation34.arg_uid1 = argument18.uid
		relation35.arg_uid1 = argument18.uid
		relation36.arg_uid = argument19.uid
		relation37.arg_uid1 = argument14.uid
		relation38.arg_uid1 = argument10.uid
		relation39.arg_uid1 = argument21.uid
		relation40.arg_uid = argument21.uid
		relation41.arg_uid = argument14.uid
		relation42.arg_uid = argument20.uid
		relation43.arg_uid1 = argument20.uid
		relation44.arg_uid1 = argument21.uid
		relation45.arg_uid1 = argument22.uid
		relation46.arg_uid1 = argument23.uid
		relation47.arg_uid1 = argument24.uid
		relation48.arg_uid1 = argument25.uid
		relation49.arg_uid1 = argument26.uid
		relation50.arg_uid1 = argument26.uid
		relation51.arg_uid1 = argument27.uid
		relation52.arg_uid = argument8.uid
		relation53.arg_uid = argument9.uid
		relation54.arg_uid = argument7.uid
		relation55.arg_uid = argument28.uid
		relation56.arg_uid1 = argument28.uid
		relation57.arg_uid1 = argument32.uid
		relation58.arg_uid1 = argument33.uid
		relation59.arg_uid1 = argument34.uid
		relation60.arg_uid1 = argument29.uid
		relation61.arg_uid1 = argument30.uid
		relation62.arg_uid1 = argument31.uid


		# adding the endpoints of the relations
		relation1.pos_uid = position1.uid
		relation2.pos_uid = position1.uid
		relation3.pos_uid = position2.uid
		relation4.pos_uid = position2.uid
		relation5.arg_uid2 = argument3.uid
		relation6.arg_uid2 = argument4.uid
		relation7.pos_uid = position1.uid
		relation8.pos_uid = position2.uid
		relation9.arg_uid2 = argument7.uid
		relation10.arg_uid2 = argument7.uid
		relation11.pos_uid = position2.uid
		relation12.pos_uid = position1.uid
		relation13.arg_uid2 = argument10.uid
		relation14.arg_uid2 = argument11.uid
		relation15.pos_uid = position2.uid
		relation16.pos_uid = position3.uid
		relation17.pos_uid = position1.uid
		relation18.pos_uid = position2.uid
		relation19.pos_uid = position1.uid
		relation20.pos_uid = position2.uid
		relation21.pos_uid = position3.uid
		relation22.arg_uid2 = argument12.uid
		relation23.arg_uid2 = argument9.uid
		relation24.arg_uid2 = argument14.uid
		relation25.pos_uid = position2.uid
		relation26.pos_uid = position1.uid
		relation27.arg_uid2 = argument16.uid
		relation28.pos_uid = position1.uid
		relation29.pos_uid = position2.uid
		relation30.arg_uid2 = argument4.uid
		relation31.arg_uid2 = argument15.uid
		relation32.pos_uid = position1.uid
		relation33.pos_uid = position1.uid
		relation34.arg_uid2 = argument7.uid
		relation35.arg_uid2 = argument19.uid
		relation36.pos_uid = position2.uid
		relation37.arg_uid2 = argument10.uid
		relation38.arg_uid2 = argument14.uid
		relation39.arg_uid2 = argument6.uid
		relation40.pos_uid = position2.uid
		relation41.pos_uid = position2.uid
		relation42.pos_uid = position3.uid
		relation43.arg_uid2 = argument5.uid
		relation44.arg_uid2 = argument4.uid
		relation45.arg_uid2 = argument18.uid
		relation46.arg_uid2 = argument8.uid
		relation47.arg_uid2 = argument1.uid
		relation48.arg_uid2 = argument14.uid
		relation49.arg_uid2 = argument13.uid
		relation50.arg_uid2 = argument12.uid
		relation51.arg_uid2 = argument11.uid
		relation52.pos_uid = position4.uid
		relation53.pos_uid = position4.uid
		relation54.pos_uid = position4.uid
		relation55.pos_uid = position2.uid
		relation56.arg_uid2 = argument6.uid
		relation57.arg_uid2 = argument21.uid
		relation58.arg_uid2 = argument26.uid
		relation59.arg_uid2 = argument24.uid
		relation60.arg_uid2 = argument27.uid
		relation61.arg_uid2 = argument23.uid
		relation62.arg_uid2 = argument23.uid


		# adding the authors
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
		relation16.author = user1.uid
		relation17.author = user1.uid
		relation18.author = user1.uid
		relation19.author = user1.uid
		relation20.author = user1.uid
		relation21.author = user1.uid
		relation22.author = user1.uid
		relation23.author = user1.uid
		relation24.author = user1.uid
		relation25.author = user1.uid
		relation26.author = user1.uid
		relation27.author = user1.uid
		relation28.author = user1.uid
		relation29.author = user1.uid
		relation30.author = user1.uid
		relation31.author = user1.uid
		relation32.author = user1.uid
		relation33.author = user1.uid
		relation34.author = user1.uid
		relation35.author = user1.uid
		relation36.author = user1.uid
		relation37.author = user1.uid
		relation38.author = user1.uid
		relation39.author = user1.uid
		relation40.author = user1.uid
		relation41.author = user1.uid
		relation42.author = user1.uid
		relation43.author = user1.uid
		relation44.author = user1.uid
		relation45.author = user1.uid
		relation46.author = user1.uid
		relation47.author = user1.uid
		relation48.author = user1.uid
		relation49.author = user1.uid
		relation50.author = user1.uid
		relation51.author = user1.uid
		relation52.author = user1.uid
		relation53.author = user1.uid
		relation54.author = user1.uid
		relation55.author = user1.uid
		relation56.author = user1.uid
		relation57.author = user1.uid
		relation58.author = user1.uid
		relation59.author = user1.uid
		relation60.author = user1.uid
		relation61.author = user1.uid
		relation62.author = user1.uid

		DBSession.add_all([relation1, relation2, relation3, relation4, relation5, relation6, relation7, relation8, relation9, relation10,
		                   relation11, relation12, relation13, relation14, relation15, relation16, relation17, relation18, relation19,
		                   relation20, relation21, relation22, relation23, relation24, relation25, relation26, relation27, relation28,
		                   relation29, relation30, relation31, relation32, relation33, relation34, relation35, relation36, relation37,
		                   relation38, relation39, relation40, relation41, relation42, relation43, relation44, relation45, relation46,
		                   relation47, relation48, relation49, relation50, relation51, relation52, relation53, relation54, relation55,
		                   relation56, relation57, relation58, relation59, relation60, relation61, relation62])
		DBSession.flush()

		transaction.commit()