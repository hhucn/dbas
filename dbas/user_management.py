"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


import random
import hashlib
from urllib import parse

from datetime import datetime
from cryptacular.bcrypt import BCRYPTPasswordManager
from .database import DBDiscussionSession
from .database.discussion_model import User, Group, VoteStatement, VoteArgument, TextVersion
from .lib import sql_timestamp_pretty_print
from .logger import logger

from .strings import Translator


class PasswordGenerator:
	"""
	Provides method for generating password
	"""

	# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
	@staticmethod
	def get_rnd_passwd():
		"""
		Generates a password with the length of 10 out of ([a-z][A-Z][+-*/#!*?])+
		:return: new secure password
		"""
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		upperalphabet = alphabet.upper()
		symbols = '+-*/#!*?'
		pw_len = 10
		pwlist = []

		for i in range(pw_len // 3):
			pwlist.append(alphabet[random.randrange(len(alphabet))])
			pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
			pwlist.append(str(random.randrange(10)))
		for i in range(pw_len - len(pwlist)):
			pwlist.append(alphabet[random.randrange(len(alphabet))])

		pwlist.append(symbols[random.randrange(len(symbols))])
		pwlist.append(symbols[random.randrange(len(symbols))])

		random.shuffle(pwlist)
		pwstring = ''.join(pwlist)

		return pwstring


class PasswordHandler:
	"""
	Handler for password
	"""

	@staticmethod
	def get_hashed_password(password):
		"""
		Returns encrypted password

		:param password: String
		:return: String
		"""
		manager = BCRYPTPasswordManager()
		return manager.encode(password)


class UserHandler:
	"""
	Handler for user-accounts
	"""

	# from https://moodlist.net/
	moodlist = ['Accepted', 'Accomplished', 'Aggravated', 'Alone', 'Amused', 'Angry', 'Annoyed', 'Anxious', 'Apathetic',
	            'Apologetic', 'Ashamed', 'Awake', 'Bewildered', 'Bitchy', 'Bittersweet', 'Blah', 'Blank', 'Blissful',
	            'Bored', 'Bouncy', 'Brooding', 'Calm', 'Cautious', 'Chaotic', 'Cheerful', 'Chilled', 'Chipper', 'Cold',
	            'Complacent', 'Confused', 'Content', 'Cranky', 'Crappy', 'Crazy', 'Crushed', 'Curious', 'Cynical',
	            'Dark', 'Defensive', 'Delusional', 'Demented', 'Depressed', 'Determined', 'Devious', 'Dirty',
	            'Disappointed', 'Discontent', 'Ditzy', 'Dorky', 'Drained', 'Drunk', 'Ecstatic', 'Energetic', 'Enraged',
	            'Enthralled', 'Envious', 'Exanimate', 'Excited', 'Exhausted', 'Fearful', 'Flirty', 'Forgetful',
	            'Frustrated', 'Full', 'Geeky', 'Giddy', 'Giggly', 'Gloomy', 'Good', 'Grateful', 'Groggy', 'Grumpy',
	            'Guilty', 'Happy', 'Heartbroken', 'High', 'Hopeful', 'Hot', 'Hungry', 'Hyper', 'Impressed',
	            'Indescribable', 'Indifferent', 'Infuriated', 'Irate', 'Irritated', 'Jealous', 'Joyful', 'Jubilant',
	            'Lazy', 'Lethargic', 'Listless', 'Lonely', 'Loved', 'Mad', 'Melancholy', 'Mellow', 'Mischievous',
	            'Moody', 'Morose', 'Naughty', 'Nerdy', 'Numb', 'Okay', 'Optimistic', 'Peaceful', 'Pessimistic',
	            'Pissed off', 'Pleased', 'Predatory', 'Quixotic', 'Rapturous', 'Recumbent', 'Refreshed', 'Rejected',
	            'Rejuvenated', 'Relaxed', 'Relieved', 'Restless', 'Rushed', 'Sad', 'Satisfied', 'Shocked', 'Sick',
	            'Silly', 'Sleepy', 'Smart', 'Stressed', 'Surprised', 'Sympathetic', 'Thankful', 'Tired', 'Touched',
	            'Uncomfortable', 'Weird']

	# https://en.wikipedia.org/wiki/List_of_animal_names
	animallist = ['Aardvark', 'Albatross', 'Alligator', 'Alpaca', 'Ant', 'Anteater', 'Antelope', 'Ape', 'Armadillo',
	              'Badger', 'Barracuda', 'Bat', 'Bear', 'Beaver', 'Bee', 'Bird', 'Bison', 'Boar', 'Buffalo', 'Butterfly',
	              'Camel', 'Caribou', 'Cassowary', 'Cat', 'Caterpillar', 'Cattle', 'Chamois', 'Cheetah', 'Chicken',
	              'Chimpanzee', 'Chinchilla', 'Chough', 'Coati', 'Cobra', 'Cockroach', 'Cod', 'Cormorant', 'Coyote',
	              'Crab', 'Crane', 'Crocodile', 'Crow', 'CurlewDeer', 'Dinosaur', 'Dog', 'Dolphin', 'Donkey', 'Dotterel',
	              'Dove', 'Dragonfly', 'Duck', 'Dugong', 'Dunlin Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant',
	              'Elephant Seal', 'Elk', 'Emu Falcon', 'Ferret', 'Finch', 'Fish', 'Flamingo', 'Fly', 'Fox', 'FrogGaur',
	              'Gazelle', 'Gerbil', 'Giant Panda', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goosander', 'Goose',
	              'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Guinea Pig', 'Gull Hamster', 'Hare', 'Hawk',
	              'Hedgehog', 'Heron', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Hummingbird', 'HyenaIbex',
	              'IbisJackal', 'Jaguar', 'Jay', 'Jellyfish Kangaroo', 'Kinkajou', 'Koala', 'Komodo Dragon', 'Kouprey',
	              'Kudu Lapwing', 'Lark', 'Lemur', 'Leopard', 'Lion', 'Llama', 'Lobster', 'Locust', 'Loris', 'Louse',
	              'Lyrebird Magpie', 'Mallard', 'Mammoth', 'Manatee', 'Mandrill', 'Mink', 'Mole', 'Mongoose', 'Monkey',
	              'Moose', 'Mouse', 'Mosquito Narwhal', 'Newt', 'Nightingale Octopus', 'Okapi', 'Opossum', 'Ostrich',
	              'Otter', 'Owl', 'Oyster Panther', 'Parrot', 'Partridge', 'Peafowl', 'Pelican', 'Penguin', 'Pheasant',
	              'Pig', 'Pigeon', 'Polar Bear', 'Porcupine', 'Porpoise', 'Quelea', 'Quetzal Rabbit', 'Raccoon', 'Rat',
	              'Raven', 'Red Deer', 'Red Panda', 'Reindeer', 'Rhinoceros', 'RookSalamander', 'Salmon', 'Sand Dollar',
	              'Sandpiper', 'Sardine', 'Sea Lion', 'Sea Urchin', 'Seahorse', 'Seal', 'Shark', 'Sheep', 'Shrew', 'Skunk',
	              'Sloth', 'Snail', 'Snake ', 'Spider', 'Squirrel', 'Starling', 'Swan Tapir', 'Tarsier', 'Termite', 'Tiger',
	              'Toad', 'Turkey', 'TurtleV', 'Walrus', 'Wasp', 'Water Buffalo', 'Weasel', 'Whale', 'Wolf', 'Wolverine',
	              'Wombat', 'Yak', 'Zebra']

	# http://www.manythings.org/vocabulary/lists/l/words.php?f=ogden-picturable
	thingslist = ['Angle', 'Ant', 'Apple', 'Arch', 'Arm', 'Army', 'Baby', 'Bag', 'Ball', 'Band', 'Basin', 'Basket',
	              'Bath', 'Bed', 'Bee', 'Bell', 'Berry', 'Bird', 'Blade', 'Board', 'Boat', 'Bone', 'Book', 'Boot',
	              'Bottle', 'Box', 'Boy', 'Brain', 'Brake', 'Branch', 'Brick', 'Bridge', 'Brush', 'Bucket', 'Bulb',
	              'Button', 'Cake', 'Camera', 'Card', 'Cart', 'Carriage', 'Cat', 'Chain', 'Cheese', 'Chest', 'Chin',
	              'Church', 'Circle', 'Clock', 'Cloud', 'Coat', 'Collar', 'Comb', 'Cord', 'Cow', 'Cup', 'Curtain',
	              'Cushion', 'Dog', 'Door', 'Drain', 'Drawer', 'Dress', 'Drop', 'Ear', 'Egg', 'Engine', 'Eye', 'Face',
	              'Farm', 'Feather', 'Finger', 'Fish', 'Flag', 'Floor', 'Fly', 'Foot', 'Fork', 'Fowl', 'Frame', 'Garden',
	              'Girl', 'Glove', 'Goat', 'Gun', 'Hair', 'Hammer', 'Hand', 'Hat', 'Head', 'Heart', 'Hook', 'Horn',
	              'Horse', 'Hospital', 'House', 'Island', 'Jewel', 'Kettle', 'Key', 'Knee', 'Knife', 'Knot', 'Leaf',
	              'Leg', 'Library', 'Line', 'Lip', 'Lock', 'Map', 'Match', 'Monkey', 'Moon', 'Mouth', 'Muscle', 'Nail',
	              'Neck', 'Needle', 'Nerve', 'Net', 'Nose', 'Nut', 'Office', 'Orange', 'Oven', 'Parcel', 'Pen', 'Pencil',
	              'Picture', 'Pig', 'Pin', 'Pipe', 'Plane', 'Plate', 'Plow', 'Pocket', 'Pot', 'Potato', 'Prison', 'Pump',
	              'Rail', 'Rat', 'Receipt', 'Ring', 'Rod', 'Roof', 'Root', 'Sail' 'School', 'Scissors', 'Screw', 'Seed',
	              'Sheep', 'Shelf', 'Ship', 'Shirt', 'Shoe', 'Skin', 'Skirt', 'Snake', 'Sock', 'Spade', 'Sponge', 'Spoon',
	              'Spring', 'Square', 'Stamp', 'Star', 'Station', 'Stem', 'Stick', 'Stocking', 'Stomach', 'Store',
	              'Street', 'Sun', 'Table', 'Tail', 'Thread', 'Throat', 'Thumb', 'Ticket', 'Toe', 'Tongue', 'Tooth',
	              'Town', 'Train', 'Tray', 'Tree', 'Trousers', 'Umbrella', 'Wall', 'Watch', 'Wheel', 'Whip', 'Whistle',
	              'Window', 'Wing', 'Wire', 'Worm']

	@staticmethod
	def update_last_action(transaction, nick):
		"""
		Updates the last action field of the user-row in database. Returns boolean if the users session
		is older than one hour or True, when she wants to keep the login

		:param transaction: transaction
		:param nick: User.nickname
		:return: Boolean
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nick)).first()
		if not db_user:
			return False

		timeout = 3600

		# check difference of
		try:  # sqlite
			last_action_object = datetime.strptime(str(db_user.last_action), '%Y-%m-%d %H:%M:%S')
			last_login_object  = datetime.strptime(str(db_user.last_login), '%Y-%m-%d %H:%M:%S')
			diff_action = (datetime.now() - last_action_object).seconds - 3600  # dirty fix for sqlite
			diff_login = (datetime.now() - last_login_object).seconds - 3600  # dirty fix for sqlite
		except ValueError:  # postgres
			last_action_object = datetime.strptime(str(db_user.last_action)[:-6], '%Y-%m-%d %H:%M:%S.%f')
			last_login_object  = datetime.strptime(str(db_user.last_login)[:-6], '%Y-%m-%d %H:%M:%S.%f')
			diff_action = (datetime.now() - last_action_object).seconds
			diff_login = (datetime.now() - last_login_object).seconds

		diff = diff_action if diff_action < diff_login else diff_login
		should_log_out = diff > timeout and not db_user.keep_logged_in
		logger('UserHandler', 'update_last_action', 'session run out: ' + str(should_log_out) + ', ' + str(diff) + 's (keep login: ' + str(db_user.keep_logged_in) + ')')
		db_user.update_last_action()

		transaction.commit()
		return should_log_out

	@staticmethod
	def is_user_in_group(nickname, groupname):
		"""
		Returns boolean if the user is in the group

		:param nickname: User.nickname
		:param groupname: Group.name
		:return: Boolean
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).join(Group).first()
		logger('UserHandler', 'is user in: ' + groupname, 'main')
		return db_user and db_user.groups.name == groupname

	@staticmethod
	def is_user_admin(user):
		"""
		Check, if the given uid has admin rights or is admin

		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).join(Group).first()
		logger('UserHandler', 'is_user_admin', 'main')
		return db_user and db_user.groups.name == 'admins'

	@staticmethod
	def get_profile_picture(user, size=80):
		"""
		Returns the url to a https://secure.gravatar.com picture, with the option wavatar and size of 80px

		:param user: User
		:param size: Integer, default 80
		:return: String
		"""
		email = user.email.encode('utf-8') if user else 'unknown@dbas.cs.uni-duesseldorf.de'.encode('utf-8')
		gravatar_url = 'https://secure.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + "?"
		gravatar_url += parse.urlencode({'d': 'wavatar', 's': str(size)})
		# logger('UserHandler', 'get_profile_picture', 'url: ' + gravatar_url)
		return gravatar_url

	def is_user_author(user):
		"""
		Check, if the given uid has admin rights or is admin

		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
		db_author_group = DBDiscussionSession.query(Group).filter_by(name='authors').first()
		logger('UserHandler', 'is_user_author', 'main')
		if db_user:
			if db_author_group.uid == db_admin_group.uid or db_user.group_uid == db_admin_group.uid:
				return True

		return False

	@staticmethod
	def is_user_logged_in(user):
		"""
		Checks if the user is logged in

		:param user: current user name
		:return: user or None
		"""
		return True if DBDiscussionSession.query(User).filter_by(nickname=str(user)).first() else False

	@staticmethod
	def get_random_anti_spam_question(lang):
		"""
		Returns a random math question

		:param lang: string
		:return: question, answer
		"""
		_t = Translator(lang)

		int1 = random.randint(0, 9)
		int2 = random.randint(0, 9)
		answer = 0
		question = _t.get(_t.antispamquestion) + ' '
		sign = _t.get(_t.signs)[random.randint(0, 3)]

		if sign is '+':
			sign = _t.get(sign)
			answer = int1 + int2

		elif sign is '-':
			sign = _t.get(sign)
			if int2 > int1:
				tmp = int1
				int1 = int2
				int2 = tmp
			answer = int1 - int2

		elif sign is '*':
			sign = _t.get(sign)
			answer = int1 * int2

		elif sign is '/':
			sign = _t.get(sign)
			while int1 == 0 or int2 == 0 or int1 % int2 != 0:
				int1 = random.randint(1, 9)
				int2 = random.randint(1, 9)
			answer = int1 / int2

		question += _t.get(str(int1)) + ' ' + sign + ' ' + _t.get(str(int2)) + '?'
		logger('UserHandler', 'get_random_anti_spam_question', 'question: ' + question + ', answer: ' + str(answer))

		return question, str(answer)

	@staticmethod
	def get_count_of_statements_of_user(user, only_edits):
		"""

		:param user:
		:param only_edits:
		:return:
		"""
		if not user:
			return 0

		edit_count      = 0
		statement_count = 0
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(author_uid=user.uid).all()

		for tv in db_textversions:
			db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=tv.statement_uid).first()
			if db_root_version.uid < tv.uid:
				edit_count += 1
			else:
				statement_count += 1

		return edit_count if only_edits else statement_count

	@staticmethod
	def get_count_of_votes_of_user(user):
		"""

		:param user:
		:return:
		"""
		if not user:
			return 0
		arg_votes = len(DBDiscussionSession.query(VoteArgument).filter_by(author_uid=user.uid).all())
		stat_votes = len(DBDiscussionSession.query(VoteStatement).filter_by(author_uid=user.uid).all())

		return arg_votes, stat_votes

	@staticmethod
	def get_statements_of_user(user, lang):
		"""

		:param user:
		:param lang:
		:return:
		"""
		return_array = []

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return return_array
		db_edits = DBDiscussionSession.query(TextVersion).filter_by(author_uid=db_user.uid).all()

		for edit in db_edits:
			db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=edit.statement_uid).first()
			if db_root_version.uid == edit.uid:
				edit_dict = dict()
				edit_dict['uid'] = str(edit.uid)
				edit_dict['statement_uid'] = str(edit.statement_uid)
				edit_dict['content'] = str(edit.content)
				edit_dict['timestamp'] = sql_timestamp_pretty_print(str(edit.timestamp), lang)
				return_array.append(edit_dict)

		return return_array

	@staticmethod
	def get_edits_of_user(user, lang):
		"""

		:param user:
		:param lang:
		:return:
		"""
		return_array = []

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return return_array

		db_edits = DBDiscussionSession.query(TextVersion).filter_by(author_uid=db_user.uid).all()

		for edit in db_edits:
			edit_dict = dict()
			edit_dict['uid'] = str(edit.uid)
			edit_dict['statement_uid'] = str(edit.statement_uid)
			edit_dict['content'] = str(edit.content)
			edit_dict['timestamp'] = sql_timestamp_pretty_print(str(edit.timestamp), lang)
			return_array.append(edit_dict)

		return return_array

	@staticmethod
	def get_votes_of_user(user, is_argument, lang, query_helper):
		"""

		:param user:
		:param is_argument:
		:param lang:
		:param query_helper:
		:return:
		"""
		return_array = []

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return return_array

		_qh = query_helper

		if is_argument:
			db_votes = DBDiscussionSession.query(VoteArgument).filter_by(author_uid=db_user.uid).all()
		else:
			db_votes = DBDiscussionSession.query(VoteStatement).filter_by(author_uid=db_user.uid).all()

		for vote in db_votes:
			vote_dict = dict()
			vote_dict['uid'] = str(vote.uid)
			vote_dict['timestamp'] = sql_timestamp_pretty_print(str(vote.timestamp), lang)
			vote_dict['is_up_vote'] = str(vote.is_up_vote)
			vote_dict['is_valid'] = str(vote.is_valid)
			if is_argument:
				vote_dict['argument_uid'] = str(vote.argument_uid)
				vote_dict['text'] = _qh.get_text_for_argument_uid(vote.argument_uid, lang)
			else:
				vote_dict['statement_uid'] = str(vote.statement_uid)
				vote_dict['text'] = _qh.get_text_for_statement_uid(vote.statement_uid)
			return_array.append(vote_dict)

		return return_array

	@staticmethod
	def get_information_of(db_user, lang):
		"""
		Returns public information of the given user

		:param db_user: User
		:param lang: ui_locales
		:return:
		"""
		ret_dict = dict()
		ret_dict['nickname']    = db_user.nickname
		ret_dict['last_login']  = sql_timestamp_pretty_print(str(db_user.last_login), lang)
		ret_dict['registered']  = sql_timestamp_pretty_print(str(db_user.registered), lang)
		ret_dict['last_action'] = '#'#sql_timestamp_pretty_print(str(db_user.last_action), lang)

		ret_dict['is_male']     = db_user.gender == 'm'
		ret_dict['is_female']   = db_user.gender == 'f'
		ret_dict['is_neutral']  = db_user.gender != 'm' and db_user.gender != 'f'

		edits       = UserHandler.get_count_of_statements_of_user(db_user, True)
		statements  = UserHandler.get_count_of_statements_of_user(db_user, False)
		arg_vote, stat_vote = UserHandler.get_count_of_votes_of_user(db_user)

		ret_dict['statemens_posted']      = statements
		ret_dict['edits_done']            = edits
		ret_dict['discussion_arg_votes']  = arg_vote
		ret_dict['discussion_stat_votes'] = stat_vote
		ret_dict['avatar_url']            = UserHandler.get_profile_picture(db_user, 120)

		return ret_dict

	@staticmethod
	def change_password(transaction, user, old_pw, new_pw, confirm_pw, lang):
		"""

		:param transaction: current database transaction
		:param user: current database user
		:param old_pw: old received password
		:param new_pw: new received password
		:param confirm_pw: confirmation of the password
		:param lang: current language
		:return: an message and boolean for error and success
		"""
		logger('UserHandler', 'change_password', 'def')
		_t = Translator(lang)

		error = False
		success = False

		# is the old password given?
		if not old_pw:
			logger('UserHandler', 'change_password', 'old pwd is empty')
			message = _t.get(_t.oldPwdEmpty)  # 'The old password field is empty.'
			error = True
		# is the new password given?
		elif not new_pw:
			logger('UserHandler', 'change_password', 'new pwd is empty')
			message = _t.get(_t.newPwdEmtpy)  # 'The new password field is empty.'
			error = True
		# is the confirmation password given?
		elif not confirm_pw:
			logger('UserHandler', 'change_password', 'confirm pwd is empty')
			message = _t.get(_t.confPwdEmpty)  # 'The password confirmation field is empty.'
			error = True
		# is new password equals the confirmation?
		elif not new_pw == confirm_pw:
			logger('UserHandler', 'change_password', 'new pwds not equal')
			message = _t.get(_t.newPwdNotEqual)  # 'The new passwords are not equal'
			error = True
		# is new old password equals the new one?
		elif old_pw == new_pw:
			logger('UserHandler', 'change_password', 'pwds are the same')
			message = _t.get(_t.pwdsSame)  # 'The new and old password are the same'
			error = True
		else:
			# is the old password valid?
			if not user.validate_password(old_pw):
				logger('UserHandler', 'change_password', 'old password is wrong')
				message = _t.get(_t.oldPwdWrong)  # 'Your old password is wrong.'
				error = True
			else:
				hashed_pw = PasswordHandler.get_hashed_password(new_pw)

				# set the hased one
				user.password = hashed_pw
				DBDiscussionSession.add(user)
				transaction.commit()

				logger('UserHandler', 'change_password', 'password was changed')
				message = _t.get(_t.pwdChanged)  # 'Your password was changed'
				success = True

		return message, error, success
