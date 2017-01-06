"""
Handler for user-accounts

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
import random
from datetime import date, timedelta

import arrow
import dbas.handler.password as password_handler
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, VoteStatement, VoteArgument, TextVersion, Settings, \
    ReviewEdit, ReviewDelete, ReviewOptimization, get_now, sql_timestamp_pretty_print
from dbas.helper import email as email_helper
from dbas.helper.notification import send_welcome_notification
from dbas.lib import python_datetime_pretty_print, get_text_for_argument_uid,\
    get_text_for_statement_uid, get_user_by_private_or_public_nickname, get_profile_picture
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from sqlalchemy import and_

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
            'Uncomfortable', 'Weird', 'Sexy', 'Aggressive']

# https://en.wikipedia.org/wiki/List_of_animal_names
# list = '';
# $.each($($('table')[3]).find('tbody td:first-child'), function(){if ($(this).text().length > 2 ) list += ', ' + '"' + $(this).text().replace(' (list) ', '') + '"'});
# console.log(list)
animallist = ['Aardvark', 'Albatross', 'Alligator', 'Alpaca', 'Ant', 'Anteater', 'Antelope', 'Ape', 'Armadillo',
              'Badger', 'Barracuda', 'Bat', 'Bear', 'Beaver', 'Bee', 'Bird', 'Bison', 'Boar', 'Buffalo', 'Butterfly',
              'Camel', 'Caribou', 'Cassowary', 'Cat', 'Caterpillar', 'Cattle', 'Chamois', 'Cheetah', 'Chicken',
              'Chimpanzee', 'Chinchilla', 'Chough', 'Coati', 'Cobra', 'Cockroach', 'Cod', 'Cormorant', 'Coyote',
              'Crab', 'Crane', 'Crocodile', 'Crow', 'Curlew', 'Deer', 'Dinosaur', 'Dog', 'Dolphin', 'Donkey', 'Dotterel',
              'Dove', 'Dragonfly', 'Duck', 'Dugong', 'Dunlin', 'Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant',
              'Elephant Seal', 'Elk', 'Emu Falcon', 'Ferret', 'Finch', 'Fish', 'Flamingo', 'Fly', 'Fox', 'FrogGaur',
              'Gazelle', 'Gerbil', 'Giant Panda', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goosander', 'Goose',
              'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Guinea Pig', 'Gull ', 'Hamster', 'Hare', 'Hawk',
              'Hedgehog', 'Heron', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Hummingbird', 'Hyena', 'Ibex',
              'Ibis', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Kangaroo', 'Kinkajou', 'Koala', 'Komodo Dragon',
              'Kouprey', 'Kudu', 'Lapwing', 'Lark', 'Lemur', 'Leopard', 'Lion', 'Llama', 'Lobster', 'Locust', 'Loris',
              'Louse', 'Lyrebird Magpie', 'Mallard', 'Mammoth', 'Manatee', 'Mandrill', 'Mink', 'Mole', 'Mongoose',
              'Monkey', 'Moose', 'Mouse', 'Mosquito', 'Narwhal', 'Newt', 'Nightingale', 'Octopus', 'Okapi', 'Opossum', 'Ostrich',
              'Otter', 'Owl', 'Oyster', 'Panther', 'Parrot', 'Partridge', 'Peafowl', 'Pelican', 'Penguin', 'Pheasant',
              'Pig', 'Pigeon', 'Polar Bear', 'Porcupine', 'Porpoise', 'Quelea', 'Quetzal', 'Rabbit', 'Raccoon', 'Rat',
              'Raven', 'Red Deer', 'Red Panda', 'Reindeer', 'Rhinoceros', 'RookSalamander', 'Salmon', 'Sand Dollar',
              'Sandpiper', 'Sardine', 'Sea Lion', 'Sea Urchin', 'Seahorse', 'Seal', 'Shark', 'Sheep', 'Shrew', 'Skunk',
              'Sloth', 'Snail', 'Snake ', 'Spider', 'Squirrel', 'Starling', 'Swan', 'Tapir', 'Tarsier', 'Termite', 'Tiger',
              'Toad', 'Turkey', 'Turtle', 'Walrus', 'Wasp', 'Water Buffalo', 'Weasel', 'Whale', 'Wolf', 'Wolverine',
              'Wombat', 'Yak', 'Zebra', 'Baboon', 'Eagle']

# http://www.manythings.org/vocabulary/lists/l/words.php?f=ogden-picturable
thingslist = ['Angle', 'Ant', 'Apple', 'Arch', 'Arm', 'Army', 'Baby', 'Bag', 'Ball', 'Band', 'Basin', 'Basket',
              'Bath', 'Bed', 'Bee', 'Bell', 'Berry', 'Bird', 'Blade', 'Board', 'Boat', 'Bone', 'Book', 'Boot',
              'Bottle', 'Box', 'Boy', 'Brain', 'Brake', 'Branch', 'Brick', 'Bridge', 'Brush', 'Bucket', 'Bulb',
              'Button', 'Cake', 'Camera', 'Card', 'Cart', 'Carriage', 'Cat', 'Chain', 'Cheese', 'Chest', 'Chin',
              'Church', 'Circle', 'Clock', 'Cloud', 'Coat', 'Collar', 'Comb', 'Cord', 'Cow', 'Cup', 'Curtain',
              'Cushion', 'Dog', 'Drain', 'Drawer', 'Dress', 'Drop', 'Ear', 'Egg', 'Engine', 'Eye', 'Face',
              'Farm', 'Feather', 'Finger', 'Fish', 'Flag', 'Floor', 'Fly', 'Foot', 'Fork', 'Fowl', 'Frame', 'Garden',
              'Girl', 'Glove', 'Goat', 'Gun', 'Hair', 'Hammer', 'Hand', 'Hat', 'Head', 'Heart', 'Hook', 'Horn',
              'Horse', 'Hospital', 'House', 'Island', 'Jewel', 'Kettle', 'Key', 'Knee', 'Knife', 'Knot', 'Leaf',
              'Leg', 'Library', 'Line', 'Lip', 'Lock', 'Map', 'Match', 'Monkey', 'Moon', 'Mouth', 'Muscle', 'Nail',
              'Neck', 'Needle', 'Nerve', 'Net', 'Nose', 'Nut', 'Office', 'Orange', 'Oven', 'Parcel', 'Pen', 'Pencil',
              'Picture', 'Pig', 'Pin', 'Pipe', 'Plane', 'Plate', 'Plow', 'Pocket', 'Pot', 'Potato', 'Prison', 'Pump',
              'Rail', 'Rat', 'Receipt', 'Ring', 'Rod', 'Roof', 'Root', 'Sail', 'School', 'Scissors', 'Screw', 'Seed',
              'Sheep', 'Shelf', 'Ship', 'Shirt', 'Shoe', 'Skin', 'Skirt', 'Snake', 'Sock', 'Spade', 'Sponge', 'Spoon',
              'Spring', 'Square', 'Stamp', 'Star', 'Station', 'Stem', 'Stick', 'Stocking', 'Stomach', 'Store',
              'Street', 'Sun', 'Table', 'Tail', 'Thread', 'Throat', 'Thumb', 'Ticket', 'Toe', 'Tongue', 'Tooth',
              'Town', 'Train', 'Tray', 'Tree', 'Trousers', 'Umbrella', 'Wall', 'Watch', 'Wheel', 'Whip', 'Whistle',
              'Window', 'Wing', 'Wire', 'Worm']

# https://www.randomlists.com/food?qty=200
foodlist = ['Acorn Squash', 'Adobo', 'Aioli', 'Alfredo Sauce', 'Almond Paste', 'Amaretto', 'Ancho Chile Peppers',
            'Anchovy Paste', 'Andouille Sausage', 'Apple Butter', 'Apple Pie Spice', 'Apricots', 'Aquavit',
            'Artificial Sweetener', 'Asiago Cheese', 'Asparagus', 'Avocados', 'Baking Powder', 'Baking Soda', 'Basil',
            'Bass', 'Bay Leaves', 'Bean Sauce', 'Bean Sprouts', 'Bean Threads', 'Beans', 'Beer', 'Beets', 'Berries',
            'Black Olives', 'Blackberries', 'Blue Cheese', 'Bok Choy', 'Breadfruit', 'Broccoli', 'Broccoli Raab',
            'Brown Rice', 'Brown Sugar', 'Bruschetta', 'Buttermilk', 'Cabbage', 'Canadian Bacon', 'Capers',
            'Cappuccino Latte', 'Cayenne Pepper', 'Celery', 'Chambord', 'Chard', 'Chaurice Sausage', 'Cheddar Cheese',
            'Cherries', 'Chicory', 'Chile Peppers', 'Chili Powder', 'Chili Sauce', 'Chocolate', 'Cinnamon', 'Cloves',
            'Cocoa Powder', 'Cod', 'Condensed Milk', 'Cooking Wine', 'Coriander', 'Corn Flour', 'Corn Syrup',
            'Cornmeal', 'Cornstarch', 'Cottage Cheese', 'Couscous', 'Crabs', 'Cream', 'Cream Cheese', 'Croutons',
            'Cumin', 'Curry Paste', 'Date Sugar', 'Dates', 'Dill', 'Dried Leeks', 'Eel', 'Eggplants', 'Eggs', 'Figs',
            'Fish Sauce', 'Flounder', 'Flour', 'French Fries', 'Geese', 'Gouda', 'Grapes', 'Green Beans',
            'Green Onions', 'Grits', 'Grouper', 'Habanero Chilies', 'Haddock', 'Half-and-half', 'Ham', 'Hash Browns',
            'Heavy Cream', 'Honey', 'Horseradish', 'Hot Sauce', 'Huckleberries', 'Irish Cream Liqueur', 'Jelly Beans',
            'Ketchup', 'Kumquats', 'Lamb', 'Leeks', 'Lemon Grass', 'Lemons', 'Lettuce', 'Lima Beans', 'Lobsters',
            'Mackerel', 'Maple Syrup', 'Margarine', 'Marshmallows', 'Melons', 'Mesclun Greens', 'Monkfish', 'Mushrooms',
            'Mussels', 'Mustard Seeds', 'Oatmeal', 'Octopus', 'Okra', 'Olives', 'Onion Powder', 'Orange Peels',
            'Oregano', 'Pancetta', 'Paprika', 'Pea Beans', 'Peanut Butter', 'Peanuts', 'Pears', 'Pecans', 'Pesto',
            'Pheasants', 'Pickles', 'Pico De Gallo', 'Pineapples', 'Pink Beans', 'Pinto Beans', 'Plum Tomatoes',
            'Pomegranates', 'Poppy Seeds', 'Pork', 'Portabella Mushrooms', 'Potato Chips', 'Poultry Seasoning',
            'Prosciutto', 'Raw Sugar', 'Red Chile Powder', 'Red Snapper', 'Remoulade', 'Rhubarb', 'Rice Wine',
            'Romaine Lettuce', 'Romano Cheese', 'Rosemary', 'Salmon', 'Salt', 'Sardines', 'Sausages', 'Sea Cucumbers',
            'Shallots', 'Shitakes', 'Shrimp', 'Snow Peas', 'Spaghetti Squash', 'Split Peas', 'Summer Squash', 'Sushi',
            'Sweet Chili Sauce', 'Sweet Peppers', 'Swiss Cheese', 'Tartar Sauce', 'Tomato Juice', 'Tomato Paste',
            'Tomato Puree', 'Tomato Sauce', 'Tonic Water', 'Tortillas', 'Tuna', 'Turtle', 'Unsweetened Chocolate',
            'Vanilla', 'Vanilla Bean', 'Vegemite', 'Venison', 'Wasabi', 'Water Chestnuts', 'Wine Vinegar',
            'Won Ton Skins', 'Worcestershire Sauce', 'Yogurt', 'Zinfandel Wine']


def update_last_action(nick):
    """
    Updates the last action field of the user-row in database. Returns boolean if the users session
    is older than one hour or True, when she wants to keep the login

    :param nick: User.nickname
    :return: Boolean
    """
    logger('UserManager', 'update_last_action', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nick)).first()
    if not db_user:
        return False
    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)

    timeout_in_sec = 60 * 60 * 24 * 7

    # check difference of
    diff_action = (get_now() - db_user.last_action).seconds
    diff_login = (get_now() - db_user.last_login).seconds

    diff = diff_action if diff_action < diff_login else diff_login
    should_log_out = diff > timeout_in_sec and not db_settings.keep_logged_in
    db_user.update_last_action()

    transaction.commit()
    return should_log_out


def refresh_public_nickname(user):
    """
    Creates and sets a random public nick for the given user

    :param user: User
    :return: the new nickname as string
    """
    biglist = animallist + thingslist + foodlist

    first = moodlist[random.randint(0, len(moodlist) - 1)]
    second = biglist[random.randint(0, len(biglist) - 1)]
    nick = first + ' ' + second

    while DBDiscussionSession.query(User).filter_by(public_nickname=nick).first():
        first = moodlist[random.randint(0, len(moodlist) - 1)]
        second = biglist[random.randint(0, len(biglist) - 1)]
        nick = first + ' ' + second

    logger('UserHandler', 'refresh_public_nickname', user.public_nickname + ' -> ' + nick)
    user.set_public_nickname(nick)

    return nick


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


def is_user_admin(nickname):
    """
    Check, if the given uid has admin rights or is admin

    :param nickname: current user name
    :return: true, if user is admin, false otherwise
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).join(Group).first()
    logger('UserHandler', 'is_user_admin', 'main')
    return db_user and db_user.groups.name == 'admins'


def get_public_information_data(nickname, lang):
    """
    Fetch some public information about the user with given nickname

    :param nickname: User.public_nickname
    :param lang:
    :return: dict()
    """
    return_dict = dict()
    current_user = get_user_by_private_or_public_nickname(nickname)

    if current_user is None:
        return return_dict

    _tn = Translator(lang)

    # data for last 7 and 30 days
    labels_decision_7 = []
    labels_decision_30 = []
    labels_edit_30 = []
    labels_statement_30 = []

    data_decision_7 = []
    data_decision_30 = []
    data_edit_30 = []
    data_statement_30 = []

    return_dict['label1'] = _tn.get(_.decisionIndex7)
    return_dict['label2'] = _tn.get(_.decisionIndex30)
    return_dict['label3'] = _tn.get(_.statementIndex)
    return_dict['label4'] = _tn.get(_.editIndex)

    return_dict['labelinfo1'] = _tn.get(_.decisionIndex7Info)
    return_dict['labelinfo2'] = _tn.get(_.decisionIndex30Info)
    return_dict['labelinfo3'] = _tn.get(_.statementIndexInfo)
    return_dict['labelinfo4'] = _tn.get(_.editIndexInfo)

    for days_diff in range(30, -1, -1):
        date_begin  = date.today() - timedelta(days=days_diff)
        date_end    = date.today() - timedelta(days=(days_diff - 1))
        begin       = arrow.get(date_begin.strftime('%Y-%m-%d'), 'YYYY-MM-DD')
        end         = arrow.get(date_end.strftime('%Y-%m-%d'), 'YYYY-MM-DD')

        ts = python_datetime_pretty_print(date_begin, lang)
        labels_decision_30.append(ts)
        labels_statement_30.append(ts)
        labels_edit_30.append(ts)

        db_votes_statements = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.author_uid == current_user.uid,
                                                                                   VoteStatement.timestamp >= begin,
                                                                                   VoteStatement.timestamp < end)).all()
        db_votes_arguments = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == current_user.uid,
                                                                                 VoteArgument.timestamp >= begin,
                                                                                 VoteArgument.timestamp < end)).all()
        votes = len(db_votes_arguments) + len(db_votes_statements)
        data_decision_30.append(votes)
        if days_diff < 6:
            labels_decision_7.append(ts)
            data_decision_7.append(votes)

        statements, edits = get_textversions_of_user(nickname, lang, begin, end)
        data_statement_30.append(len(statements))
        data_edit_30.append(len(edits))

    return_dict['labels1'] = labels_decision_7
    return_dict['labels2'] = labels_decision_30
    return_dict['labels3'] = labels_statement_30
    return_dict['labels4'] = labels_edit_30
    return_dict['data1'] = data_decision_7
    return_dict['data2'] = data_decision_30
    return_dict['data3'] = data_statement_30
    return_dict['data4'] = data_edit_30

    return return_dict


def get_reviews_of(user, only_today):
    """

    :param user:
    :param only_today:
    :return:
    """
    db_edits = DBDiscussionSession.query(ReviewEdit).filter_by(detector_uid=user.uid)
    db_deletes = DBDiscussionSession.query(ReviewDelete).filter_by(detector_uid=user.uid)
    db_optimizations = DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=user.uid)

    if only_today:
        today       = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_edits = db_edits.filter(ReviewEdit.timestamp >= today)
        db_deletes = db_deletes.filter(ReviewDelete.timestamp >= today)
        db_optimizations = db_optimizations.filter(ReviewOptimization.timestamp >= today)

    db_edits = db_edits.all()
    db_deletes = db_deletes.all()
    db_optimizations = db_optimizations.all()

    return len(db_edits) + len(db_deletes) + len(db_optimizations)


def get_count_of_statements_of_user(user, only_edits, limit_on_today=False):
    """
    Returns the count of statements of the user

    :param user: User
    :param only_edits: Boolean
    :param limit_on_today: Boolean
    :return:
    """
    if not user:
        return 0

    edit_count      = 0
    statement_count = 0
    db_textversions = DBDiscussionSession.query(TextVersion).filter_by(author_uid=user.uid)
    if limit_on_today:
        today       = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_textversions = db_textversions.filter(TextVersion.timestamp >= today)
    db_textversions = db_textversions.all()

    for tv in db_textversions:
        db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=tv.statement_uid).first()
        if db_root_version.uid < tv.uid:
            edit_count += 1
        else:
            statement_count += 1

    return edit_count if only_edits else statement_count


def get_count_of_votes_of_user(user, limit_on_today=False):
    """
    Returns the count of votes of the user

    :param user: User
    :param limit_on_today: Boolean
    :return:
    """
    if not user:
        return 0

    db_arg_votes = DBDiscussionSession.query(VoteArgument).filter(VoteArgument.author_uid == user.uid)
    db_stat_votes = DBDiscussionSession.query(VoteStatement).filter(VoteStatement.author_uid == user.uid)

    if limit_on_today:
        today       = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_arg_votes = db_arg_votes.filter(VoteArgument.timestamp >= today)
        db_stat_votes = db_stat_votes.filter(VoteStatement.timestamp >= today)

    db_arg_votes = db_arg_votes.all()
    db_stat_votes = db_stat_votes.all()

    return len(db_arg_votes), len(db_stat_votes)


def get_textversions_of_user(public_nickname, lang, timestamp_after=None, timestamp_before=None):
    """
    Returns all textversions, were the user was author

    :param public_nickname: User.public_nickname
    :param lang: ui_locales
    :param timestamp_after: Arrow or None
    :param timestamp_before: Arrow or None
    :return:
    """
    statement_array = []
    edit_array = []

    db_user = get_user_by_private_or_public_nickname(public_nickname)

    if not db_user:
        logger('UserManagement', 'get_textversions_of_user', 'no user found', error=True)
        return statement_array, edit_array

    if not timestamp_after:
        timestamp_after = arrow.get('1970-01-01').format('YYYY-MM-DD')
    if not timestamp_before:
        timestamp_before = arrow.utcnow().replace(days=+1).format('YYYY-MM-DD')

    db_edits = DBDiscussionSession.query(TextVersion).filter(and_(TextVersion.author_uid == db_user.uid,
                                                                  TextVersion.timestamp >= timestamp_after,
                                                                  TextVersion.timestamp < timestamp_before)).all()

    logger('UserManagement', 'get_textversions_of_user', 'count of edits: ' + str(len(db_edits)))
    for edit in db_edits:
        db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=edit.statement_uid).first()
        edit_dict = dict()
        edit_dict['uid'] = str(edit.uid)
        edit_dict['statement_uid'] = str(edit.statement_uid)
        edit_dict['content'] = str(edit.content)
        edit_dict['timestamp'] = sql_timestamp_pretty_print(edit.timestamp, lang)
        if db_root_version.uid == edit.uid:
            statement_array.append(edit_dict)
        else:
            edit_array.append(edit_dict)

    return statement_array, edit_array


def get_votes_of_user(user, is_argument, lang):
    """

    :param user:
    :param is_argument:
    :param lang:
    :return:
    """
    return_array = []

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if not db_user:
        return return_array

    if is_argument:
        db_votes = DBDiscussionSession.query(VoteArgument).filter_by(author_uid=db_user.uid).all()
    else:
        db_votes = DBDiscussionSession.query(VoteStatement).filter_by(author_uid=db_user.uid).all()

    for vote in db_votes:
        vote_dict = dict()
        vote_dict['uid'] = str(vote.uid)
        vote_dict['timestamp'] = sql_timestamp_pretty_print(vote.timestamp, lang)
        vote_dict['is_up_vote'] = str(vote.is_up_vote)
        vote_dict['is_valid'] = str(vote.is_valid)
        if is_argument:
            vote_dict['argument_uid'] = str(vote.argument_uid)
            vote_dict['text'] = get_text_for_argument_uid(vote.argument_uid, lang)
        else:
            vote_dict['statement_uid'] = str(vote.statement_uid)
            vote_dict['text'] = get_text_for_statement_uid(vote.statement_uid)
        return_array.append(vote_dict)

    return return_array


def get_information_of(db_user, lang):
    """
    Returns public information of the given user

    :param db_user: User
    :param lang: ui_locales
    :return:
    """
    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    db_group = DBDiscussionSession.query(Group).get(db_user.group_uid)
    ret_dict = dict()
    ret_dict['public_nick'] = db_user.nickname if db_settings.should_show_public_nickname else db_user.public_nickname
    ret_dict['last_action'] = sql_timestamp_pretty_print(db_user.last_action, lang)
    ret_dict['last_login']  = sql_timestamp_pretty_print(db_user.last_login, lang)
    ret_dict['registered']  = sql_timestamp_pretty_print(db_user.registered, lang)
    ret_dict['group']       = db_group.name[0:1].upper() + db_group.name[1:-1]

    ret_dict['is_male']     = db_user.gender == 'm'
    ret_dict['is_female']   = db_user.gender == 'f'
    ret_dict['is_neutral']  = db_user.gender != 'm' and db_user.gender != 'f'

    arg_vote, stat_vote = get_count_of_votes_of_user(db_user, True)

    statements, edits                       = get_textversions_of_user(db_user.public_nickname, lang)
    ret_dict['statements_posted']           = len(statements)
    ret_dict['edits_done']                  = len(edits)
    ret_dict['discussion_arg_votes']        = arg_vote
    ret_dict['discussion_stat_votes']       = stat_vote
    ret_dict['avatar_url']                  = get_profile_picture(db_user, 120)
    ret_dict['discussion_stat_rep'], trash  = get_reputation_of(db_user.nickname)

    return ret_dict


def get_summary_of_today(nickname):
    """
    Returns summary of todays actions

    :param nickname: User.nickname
    :return: dict()
    """
    ret_dict = dict()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    if not db_user:
        return dict()

    arg_vote, stat_vote = get_count_of_votes_of_user(db_user, True)

    ret_dict['statements_posted']     = get_count_of_statements_of_user(db_user, False, True)
    ret_dict['edits_done']            = get_count_of_statements_of_user(db_user, True, True)
    ret_dict['discussion_arg_votes']  = arg_vote
    ret_dict['discussion_stat_votes'] = stat_vote
    ret_dict['statements_reported']   = get_reviews_of(db_user, True)

    return ret_dict


def change_password(user, old_pw, new_pw, confirm_pw, lang):
    """

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
        message = _t.get(_.oldPwdEmpty)  # 'The old password field is empty.'
        error = True
    # is the new password given?
    elif not new_pw:
        logger('UserHandler', 'change_password', 'new pwd is empty')
        message = _t.get(_.newPwdEmtpy)  # 'The new password field is empty.'
        error = True
    # is the confirmation password given?
    elif not confirm_pw:
        logger('UserHandler', 'change_password', 'confirm pwd is empty')
        message = _t.get(_.confPwdEmpty)  # 'The password confirmation field is empty.'
        error = True
    # is new password equals the confirmation?
    elif not new_pw == confirm_pw:
        logger('UserHandler', 'change_password', 'new pwds not equal')
        message = _t.get(_.newPwdNotEqual)  # 'The new passwords are not equal'
        error = True
    # is new old password equals the new one?
    elif old_pw == new_pw:
        logger('UserHandler', 'change_password', 'pwds are the same')
        message = _t.get(_.pwdsSame)  # 'The new and old password are the same'
        error = True
    else:
        # is the old password valid?
        if not user.validate_password(old_pw):
            logger('UserHandler', 'change_password', 'old password is wrong')
            message = _t.get(_.oldPwdWrong)  # 'Your old password is wrong.'
            error = True
        else:
            hashed_pw = password_handler.get_hashed_password(new_pw)

            # set the hashed one
            user.password = hashed_pw
            DBDiscussionSession.add(user)
            transaction.commit()

            logger('UserHandler', 'change_password', 'password was changed')
            message = _t.get(_.pwdChanged)  # 'Your password was changed'
            success = True

    return message, error, success


def create_new_user(request, firstname, lastname, email, nickname, password, gender, db_group_uid, ui_locales):
    """

    :param request:
    :param firstname:
    :param lastname:
    :param email:
    :param nickname:
    :param password:
    :param gender:
    :param db_group_uid:
    :param ui_locales:
    :return:
    """
    success = ''
    info = ''

    _t = Translator(ui_locales)
    # creating a new user with hashed password
    logger('UserManagement', 'create_new_user', 'Adding user ' + nickname)
    hashed_password = password_handler.get_hashed_password(password)
    newuser = User(firstname=firstname,
                   surname=lastname,
                   email=email,
                   nickname=nickname,
                   password=hashed_password,
                   gender=gender,
                   group_uid=db_group_uid)
    DBDiscussionSession.add(newuser)
    transaction.commit()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    settings = Settings(author_uid=db_user.uid,
                        send_mails=True,
                        send_notifications=True,
                        should_show_public_nickname=True)
    DBDiscussionSession.add(settings)
    transaction.commit()

    # sanity check, whether the user exists
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        logger('UserManagement', 'create_new_user', 'New data was added with uid ' + str(db_user.uid))
        success = _t.get(_.accountWasAdded).format(nickname)

        # sending an email
        subject = _t.get(_.accountRegistration)
        body = _t.get(_.accountWasRegistered).format('"' + nickname + '"', email)
        email_helper.send_mail(request, subject, body, email, ui_locales)
        send_welcome_notification(db_user.uid)

    else:
        logger('UserManagement', 'create_new_user', 'New data was not added')
        info = _t.get(_.accoutErrorTryLateOrContant)

    return success, info
