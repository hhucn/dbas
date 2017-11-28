"""
Handler for user-accounts

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import random
from datetime import date, timedelta

import arrow
import transaction
from pyramid_mailer import get_mailer
from sqlalchemy import and_

import dbas.handler.password as password_handler
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, ClickedStatement, ClickedArgument, TextVersion, Settings, \
    ReviewEdit, ReviewDelete, ReviewOptimization, get_now, sql_timestamp_pretty_print, MarkedArgument, MarkedStatement, \
    ReviewDuplicate
from dbas.handler.email import send_mail
from dbas.handler.notification import send_welcome_notification
from dbas.handler.opinion import get_user_with_same_opinion_for_argument, \
    get_user_with_same_opinion_for_statements, get_user_with_opinions_for_attitude, \
    get_user_with_same_opinion_for_premisegroups, get_user_and_opinions_for_argument
from dbas.lib import python_datetime_pretty_print, get_text_for_argument_uid, \
    get_text_for_statement_uid, get_user_by_private_or_public_nickname, get_profile_picture
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

values = ['firstname', 'surname', 'email', 'nickname', 'password', 'gender']
oauth_values = ['firstname', 'lastname', 'email', 'nickname', 'gender']

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
# list = ';
# $.each($($('table')[3]).find('tbody td:first-child'), function(){if ($(this).text().length > 2 ) list += ', ' + '"' + $(this).text().replace(' (list) ', ') + '"'});
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
    logger('User', 'update_last_action', 'main')
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

    logger('User', 'refresh_public_nickname', user.public_nickname + ' -> ' + nick)
    user.set_public_nickname(nick)

    return nick


def is_in_group(nickname, groupname):
    """
    Returns boolean if the user is in the group

    :param nickname: User.nickname
    :param groupname: Group.name
    :return: Boolean
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).join(Group).first()
    logger('User', 'is user in: ' + groupname, 'main')
    return db_user and db_user.groups.name == groupname


def is_admin(nickname):
    """
    Check, if the given uid has admin rights or is admin

    :param nickname: current user name
    :return: true, if user is admin, false otherwise
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).join(Group).first()
    logger('User', 'is_admin', 'main')
    return db_user and db_user.groups.name == 'admins'


def get_public_data(nickname, lang):
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
        date_begin = date.today() - timedelta(days=days_diff)
        date_end = date.today() - timedelta(days=days_diff - 1)
        begin = arrow.get(date_begin.strftime('%Y-%m-%d'), 'YYYY-MM-DD')
        end = arrow.get(date_end.strftime('%Y-%m-%d'), 'YYYY-MM-DD')

        ts = python_datetime_pretty_print(date_begin, lang)
        labels_decision_30.append(ts)
        labels_statement_30.append(ts)
        labels_edit_30.append(ts)

        db_votes_statements = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == current_user.uid,
                                                                                      ClickedStatement.timestamp >= begin,
                                                                                      ClickedStatement.timestamp < end)).all()
        db_votes_arguments = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == current_user.uid,
                                                                                    ClickedArgument.timestamp >= begin,
                                                                                    ClickedArgument.timestamp < end)).all()
        votes = len(db_votes_arguments) + len(db_votes_statements)
        data_decision_30.append(votes)
        if days_diff < 6:
            labels_decision_7.append(ts)
            data_decision_7.append(votes)

        statements, edits = get_textversions(nickname, lang, begin, end)
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
    Returns the sum of all reviews of the given user

    :param user: User
    :param only_today: Boolean
    :return: Int
    """
    db_edits = DBDiscussionSession.query(ReviewEdit).filter_by(detector_uid=user.uid)
    db_deletes = DBDiscussionSession.query(ReviewDelete).filter_by(detector_uid=user.uid)
    db_optimizations = DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=user.uid)
    db_duplicates = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=user.uid)

    if only_today:
        today = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_edits = db_edits.filter(ReviewEdit.timestamp >= today)
        db_deletes = db_deletes.filter(ReviewDelete.timestamp >= today)
        db_optimizations = db_optimizations.filter(ReviewOptimization.timestamp >= today)
        db_duplicates = DBDiscussionSession.query(ReviewDuplicate).filter(ReviewOptimization.timestamp >= today)

    db_edits = db_edits.all()
    db_deletes = db_deletes.all()
    db_optimizations = db_optimizations.all()
    db_duplicates = db_duplicates.all()

    return len(db_edits) + len(db_deletes) + len(db_optimizations) + len(db_duplicates)


def get_count_of_statements(user, only_edits, limit_on_today=False):
    """
    Returns the count of statements of the user

    :param user: User
    :param only_edits: Boolean
    :param limit_on_today: Boolean
    :return: Int
    """
    if not user:
        return 0

    edit_count = 0
    statement_count = 0
    db_textversions = DBDiscussionSession.query(TextVersion).filter_by(author_uid=user.uid)
    if limit_on_today:
        today = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_textversions = db_textversions.filter(TextVersion.timestamp >= today)
    db_textversions = db_textversions.all()

    for tv in db_textversions:
        db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=tv.statement_uid).first()  # TODO #432
        if db_root_version.uid < tv.uid:
            edit_count += 1
        else:
            statement_count += 1

    return edit_count if only_edits else statement_count


def get_count_of_votes_of_user(user, limit_on_today=False):
    """
    Returns the count of marked ones of the user

    :param user: User
    :param limit_on_today: Boolean
    :return: Int, Int
    """
    if not user:
        return 0

    db_arg = DBDiscussionSession.query(MarkedArgument).filter(ClickedArgument.author_uid == user.uid)
    db_stat = DBDiscussionSession.query(MarkedStatement).filter(ClickedStatement.author_uid == user.uid)

    if limit_on_today:
        today = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_arg = db_arg.filter(MarkedArgument.timestamp >= today)
        db_stat = db_stat.filter(MarkedStatement.timestamp >= today)

    db_arg = db_arg.all()
    db_stat = db_stat.all()

    return len(db_arg), len(db_stat)


def get_count_of_clicks(user, limit_on_today=False):
    """
    Returns the count of clicks of the user

    :param user: User
    :param limit_on_today: Boolean
    :return: Int, Int
    """
    if not user:
        return 0

    db_arg = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == user.uid)
    db_stat = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.author_uid == user.uid)

    if limit_on_today:
        today = arrow.utcnow().to('Europe/Berlin').format('YYYY-MM-DD')
        db_arg = db_arg.filter(ClickedArgument.timestamp >= today)
        db_stat = db_stat.filter(ClickedStatement.timestamp >= today)

    db_arg = db_arg.all()
    db_stat = db_stat.all()

    return len(db_arg), len(db_stat)


def get_textversions(public_nickname, lang, timestamp_after=None, timestamp_before=None):
    """
    Returns all textversions, were the user was author

    :param public_nickname: User.public_nickname
    :param lang: ui_locales
    :param timestamp_after: Arrow or None
    :param timestamp_before: Arrow or None
    :return: [{},...], [{},...]
    """
    statement_array = []
    edit_array = []

    db_user = get_user_by_private_or_public_nickname(public_nickname)

    if not db_user:
        logger('User', 'get_textversions', 'no user found', error=True)
        return statement_array, edit_array

    if not timestamp_after:
        timestamp_after = arrow.get('1970-01-01').format('YYYY-MM-DD')
    if not timestamp_before:
        timestamp_before = arrow.utcnow().replace(days=+1).format('YYYY-MM-DD')

    db_edits = DBDiscussionSession.query(TextVersion).filter(and_(TextVersion.author_uid == db_user.uid,
                                                                  TextVersion.timestamp >= timestamp_after,
                                                                  TextVersion.timestamp < timestamp_before)).all()

    logger('User', 'get_textversions', 'count of edits: ' + str(len(db_edits)))
    for edit in db_edits:
        db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=edit.statement_uid).first()  # TODO #432
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


def get_marked_elements_of_user(user, is_argument, lang):
    """
    Get all marked arguments/statements of the user

    :param user: User
    :param is_argument: Boolean
    :param lang: uid_locales
    :return: [{},...]
    """
    return_array = []

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if not db_user:
        return return_array

    if is_argument:
        db_votes = DBDiscussionSession.query(MarkedArgument).filter_by(author_uid=db_user.uid).all()
    else:
        db_votes = DBDiscussionSession.query(MarkedStatement).filter_by(author_uid=db_user.uid).all()

    for vote in db_votes:
        vote_dict = dict()
        vote_dict['uid'] = str(vote.uid)
        vote_dict['timestamp'] = sql_timestamp_pretty_print(vote.timestamp, lang)
        if is_argument:
            vote_dict['argument_uid'] = str(vote.argument_uid)
            vote_dict['content'] = get_text_for_argument_uid(vote.argument_uid, lang)
        else:
            vote_dict['statement_uid'] = str(vote.statement_uid)
            vote_dict['content'] = get_text_for_statement_uid(vote.statement_uid)
        return_array.append(vote_dict)

    return return_array


def get_arg_clicks_of_user(user, lang):
    return get_clicks_of_user(user, True, lang)


def get_stmt_clicks_of_user(user, lang):
    return get_clicks_of_user(user, False, lang)


def get_clicks_of_user(user, is_argument, lang):
    """
    Returs array with all clicks done by the user

    :param user: user.nickname
    :param is_argument: Boolean
    :param lang: ui_locales
    :return: [{},...]
    """
    return_array = []

    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if not db_user:
        return return_array

    if is_argument:
        db_votes = DBDiscussionSession.query(ClickedArgument).filter_by(author_uid=db_user.uid).all()
    else:
        db_votes = DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=db_user.uid).all()

    for vote in db_votes:
        vote_dict = dict()
        vote_dict['uid'] = str(vote.uid)
        vote_dict['timestamp'] = sql_timestamp_pretty_print(vote.timestamp, lang)
        vote_dict['is_up_vote'] = str(vote.is_up_vote)
        vote_dict['is_valid'] = str(vote.is_valid)
        if is_argument:
            vote_dict['argument_uid'] = str(vote.argument_uid)
            vote_dict['content'] = get_text_for_argument_uid(vote.argument_uid, lang)
        else:
            vote_dict['statement_uid'] = str(vote.statement_uid)
            vote_dict['content'] = get_text_for_statement_uid(vote.statement_uid)
        return_array.append(vote_dict)

    return return_array


def get_information_of(db_user, lang):
    """
    Returns public information of the given user

    :param db_user: User
    :param lang: ui_locales
    :return: dict()
    """
    db_group = DBDiscussionSession.query(Group).get(db_user.group_uid)
    ret_dict = dict()
    ret_dict['public_nick'] = db_user.get_global_nickname()
    ret_dict['last_action'] = sql_timestamp_pretty_print(db_user.last_action, lang)
    ret_dict['last_login'] = sql_timestamp_pretty_print(db_user.last_login, lang)
    ret_dict['registered'] = sql_timestamp_pretty_print(db_user.registered, lang)
    ret_dict['group'] = db_group.name[0:1].upper() + db_group.name[1:-1]

    ret_dict['is_male'] = db_user.gender == 'm'
    ret_dict['is_female'] = db_user.gender == 'f'
    ret_dict['is_neutral'] = db_user.gender != 'm' and db_user.gender != 'f'

    arg_vote, stat_vote = get_count_of_votes_of_user(db_user, False)
    db_reviews_duplicate = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=db_user.uid).all()
    db_reviews_edit = DBDiscussionSession.query(ReviewEdit).filter_by(detector_uid=db_user.uid).all()
    db_reviews_delete = DBDiscussionSession.query(ReviewDelete).filter_by(detector_uid=db_user.uid).all()
    db_reviews_optimization = DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=db_user.uid).all()
    db_reviews = db_reviews_duplicate + db_reviews_edit + db_reviews_delete + db_reviews_optimization

    statements, edits = get_textversions(db_user.public_nickname, lang)
    ret_dict['statements_posted'] = len(statements)
    ret_dict['edits_done'] = len(edits)
    ret_dict['reviews_proposed'] = len(db_reviews)
    ret_dict['discussion_arg_votes'] = arg_vote
    ret_dict['discussion_stat_votes'] = stat_vote
    ret_dict['avatar_url'] = get_profile_picture(db_user, 120)
    ret_dict['discussion_stat_rep'], trash = get_reputation_of(db_user.nickname)

    return ret_dict


def get_summary_of_today(nickname, lang):
    """
    Returns summary of todays actions

    :param nickname: User.nickname
    :param lang: ui_locales
    :return: dict()
    """
    ret_dict = dict()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    if not db_user:
        return dict()

    arg_vote, stat_vote = get_count_of_votes_of_user(db_user, True)
    arg_clicks, stat_clicks = get_count_of_clicks(db_user, True)
    reputation, tmp = get_reputation_of(nickname, True)
    timestamp = arrow.utcnow().to('Europe/Berlin')

    ret_dict['firstname'] = db_user.firstname
    ret_dict['date'] = timestamp.format('YYYY-MM-DD') if lang == 'en' else timestamp.format('DD.MM.')
    ret_dict['statements_posted'] = get_count_of_statements(db_user, False, True)
    ret_dict['edits_done'] = get_count_of_statements(db_user, True, True)
    ret_dict['discussion_arg_votes'] = arg_vote
    ret_dict['discussion_stat_votes'] = stat_vote
    ret_dict['discussion_arg_clicks'] = arg_clicks
    ret_dict['discussion_stat_clicks'] = stat_clicks
    ret_dict['statements_reported'] = get_reviews_of(db_user, True)
    ret_dict['reputation_colltected'] = reputation

    return ret_dict


def change_password(user, old_pw, new_pw, confirm_pw, lang):
    """
    Change password of given user

    :param user: current database user
    :param old_pw: old received password
    :param new_pw: new received password
    :param confirm_pw: confirmation of the password
    :param lang: current language
    :return: an message and boolean for error and success
    """
    logger('User', 'change_password', 'def')
    _t = Translator(lang)

    success = False

    # is the old password given?
    if not old_pw:
        logger('User', 'change_password', 'old pwd is empty')
        message = _t.get(_.oldPwdEmpty)  # 'The old password field is empty.'
    # is the new password given?
    elif not new_pw:
        logger('User', 'change_password', 'new pwd is empty')
        message = _t.get(_.newPwdEmtpy)  # 'The new password field is empty.'
    # is the confirmation password given?
    elif not confirm_pw:
        logger('User', 'change_password', 'confirm pwd is empty')
        message = _t.get(_.confPwdEmpty)  # 'The password confirmation field is empty.'
    # is new password equals the confirmation?
    elif not new_pw == confirm_pw:
        logger('User', 'change_password', 'new pwds not equal')
        message = _t.get(_.newPwdNotEqual)  # 'The new passwords are not equal'
    # is new old password equals the new one?
    elif old_pw == new_pw:
        logger('User', 'change_password', 'pwds are the same')
        message = _t.get(_.pwdsSame)  # 'The new and old password are the same'
    else:
        # is the old password valid?
        if not user.validate_password(old_pw):
            logger('User', 'change_password', 'old password is wrong')
            message = _t.get(_.oldPwdWrong)  # 'Your old password is wrong.'
        else:
            hashed_pw = password_handler.get_hashed_password(new_pw)

            # set the hashed one
            user.password = hashed_pw
            DBDiscussionSession.add(user)
            transaction.commit()

            logger('User', 'change_password', 'password was changed')
            message = _t.get(_.pwdChanged)  # 'Your password was changed'
            success = True

    return message, success


def __create_new_user(firstname, lastname, email, nickname, password, gender, db_group_uid, ui_locales,
                      oauth_provider='', oauth_provider_id=''):
    """
    Insert a new user row

    :param firstname: String
    :param lastname: String
    :param email: String
    :param nickname: String
    :param password: String
    :param gender: String
    :param db_group_uid: Group.uid
    :param ui_locales: Language.ui_locales
    :param oauth_provider: String
    :param oauth_provider_id: String
    :return: String, String, User
    """
    success = ''
    info = ''

    _t = Translator(ui_locales)
    # creating a new user with hashed password
    logger('User', '__create_new_user', 'Adding user ' + nickname)
    hashed_password = password_handler.get_hashed_password(password)
    newuser = User(firstname=firstname,
                   surname=lastname,
                   email=email,
                   nickname=nickname,
                   password=hashed_password,
                   gender=gender,
                   group_uid=db_group_uid,
                   oauth_provider=oauth_provider,
                   oauth_provider_id=oauth_provider_id)
    DBDiscussionSession.add(newuser)
    transaction.commit()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    settings = Settings(author_uid=db_user.uid,
                        send_mails=False,
                        send_notifications=True,
                        should_show_public_nickname=True)
    DBDiscussionSession.add(settings)
    transaction.commit()

    # sanity check, whether the user exists
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        logger('User', '__create_new_user', 'New data was added with uid ' + str(db_user.uid))
        success = _t.get(_.accountWasAdded).format(nickname)

    else:
        logger('User', '__create_new_user', 'New data was not added')
        info = _t.get(_.accoutErrorTryLateOrContant)

    return success, info, db_user


def set_new_user(request, firstname, lastname, nickname, gender, email, password, _tn):
    """
    Let's create a new user

    :param request: current request of web server
    :param firstname: String
    :param lastname: String
    :param nickname: String
    :param gender: String
    :param email: String
    :param password: String
    :param _tn: Translaator
    :return: Boolean, msg
    """
    # getting the authors group
    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()

    # does the group exists?
    if not db_group:
        logger('User', 'set_new_user', 'Internal error occured')
        return {'success': False, 'error': _tn.get(_.errorTryLateOrContant), 'user': None}

    # sanity check
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        logger('User', 'set_new_user', 'User already exists')
        return {'success': False, 'error': _tn.get(_.nickIsTaken), 'user': None}

    success, info, db_new_user = __create_new_user(firstname, lastname, email, nickname, password, gender,
                                                   db_group.uid, _tn.get_lang())

    if db_new_user:
        # sending an email and message
        subject = _tn.get(_.accountRegistration)
        body = _tn.get(_.accountWasRegistered).format(firstname, lastname, email)
        send_mail(get_mailer(request), subject, body, email, _tn.get_lang())
        send_welcome_notification(db_new_user.uid, _tn)

        logger('User', 'set_new_user', 'set new user in db')
        return {'success': success, 'error': '', 'user': db_new_user}

    logger('User', 'set_new_user', 'new user not found in db')
    return {
        'success': False,
        'error': _tn.get(_.errorTryLateOrContant),
        'user': None
    }


def set_new_oauth_user(firstname, lastname, nickname, email, gender, password, id, provider, _tn):
    """
    Let's create a new user

    :param firstname: String
    :param lastname: String
    :param nickname: String
    :param email: String
    :param gender: String
    :param password: String
    :param id: String
    :param provider: String
    :param _tn: Translaator
    :return: Boolean, msg
    """
    # getting the authors group
    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()

    # does the group exists?
    if not db_group:
        logger('User', 'set_new_oauth_user', 'Internal error occured')
        return {'success': False, 'error': _tn.get(_.errorTryLateOrContant), 'user': None}

    # sanity check
    db_user = DBDiscussionSession.query(User).filter(User.oauth_provider == str(provider),
                                                     User.oauth_provider_id == str(id)).first()
    # login of oauth user
    if db_user:
        logger('User', 'set_new_oauth_user', 'User already exists, she will login')
        return {'success': True, 'error': '', 'user': db_user}

    # sanity check
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        logger('User', 'set_new_oauth_user', 'User already exists')
        return {'success': False, 'error': _tn.get(_.nickIsTaken), 'user': None}

    success, info, db_new_user = __create_new_user(firstname, lastname, email, nickname, password, gender,
                                                   db_group.uid, _tn.get_lang(), oauth_provider=provider,
                                                   oauth_provider_id=id)

    if db_new_user:
        logger('User', 'set_new_oauth_user', 'set new user in db')
        return {'success': success, 'error': '', 'user': db_new_user}

    logger('User', 'set_new_oauth_user', 'new user not found in db')

    return {
        'success': False,
        'error': _tn.get(_.errorTryLateOrContant),
        'user': None
    }


def get_users_with_same_opinion(uids, application_url, path, nickname, is_argument, is_attitude, is_reaction,
                                is_position, ui_locales) -> dict:
    """
    Based on current discussion step information about other users will be given

    :param uids: IDs of statements or argument for the information request
    :param application_url: url of the application
    :param path: current path of the user
    :param nickname: users nickname
    :param is_argument: boolean, if the request is for an argument
    :param is_attitude: boolean, if the request is during the attitude step
    :param is_reaction: boolean, if the request is during the attitude step
    :param is_position: boolean, if the request is for a position
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: prepared collection with information about other users with the same opinion or an error
    """
    prepared_dict = dict()
    _tn = Translator(ui_locales)

    if is_argument and is_reaction:
        uids = json.loads(uids)
        prepared_dict = get_user_and_opinions_for_argument(uids, nickname, ui_locales, application_url, path)
    elif is_argument and not is_reaction:
        prepared_dict = get_user_with_same_opinion_for_argument(uids, nickname, ui_locales, application_url)
    elif is_position:
        uids = json.loads(uids)
        uids = uids if isinstance(uids, list) else [uids]
        prepared_dict = get_user_with_same_opinion_for_statements(uids, True, nickname, ui_locales, application_url)
    elif is_attitude:
            prepared_dict = get_user_with_opinions_for_attitude(uids, nickname, ui_locales, application_url)
    elif not is_attitude:
        uids = json.loads(uids)
        uids = uids if isinstance(uids, list) else [uids]
        prepared_dict = get_user_with_same_opinion_for_premisegroups(uids, nickname, ui_locales, application_url)
    prepared_dict['info'] = _tn.get(_.otherParticipantsDontHaveOpinionForThisStatement) if len(uids) == 0 else ''
    prepared_dict['error'] = ''

    return prepared_dict
