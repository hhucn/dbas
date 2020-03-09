"""
Handler for user-accounts
"""
import logging
import random
import uuid
from datetime import date, timedelta
from typing import Tuple, List, Dict, Union, Any, Optional

import arrow
from arrow.arrow import Arrow
from pyramid_mailer import Mailer

import dbas.handler.password as password_handler
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, ClickedStatement, ClickedArgument, TextVersion, Settings, \
    ReviewEdit, ReviewDelete, ReviewOptimization, get_now, sql_timestamp_pretty_print, MarkedArgument, \
    MarkedStatement, ReviewDuplicate, StatementReference, SeenStatement, SeenArgument, PremiseGroup, \
    Premise, History, Message, ReviewEditValue, ReviewMerge, ReviewSplit, LastReviewerDelete, LastReviewerDuplicate, \
    LastReviewerEdit, LastReviewerOptimization, \
    LastReviewerSplit, LastReviewerMerge, ReputationHistory, ReviewCanceled, RevokedContent, RevokedContentHistory, \
    Issue, Argument, Language
from dbas.handler.email import send_mail
from dbas.handler.notification import send_welcome_notification
from dbas.handler.opinion import get_user_with_same_opinion_for_argument, \
    get_user_with_same_opinion_for_statements, get_user_with_opinions_for_attitude, \
    get_user_with_same_opinion_for_premisegroups_of_args, get_user_and_opinions_for_argument
from dbas.lib import pretty_print_timestamp, get_text_for_argument_uid, \
    get_profile_picture, nick_of_anonymous_user
from dbas.review.reputation import get_reputation_of
from dbas.strings.keywords import Keywords
from dbas.strings.lib import start_with_capital
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)
values = ['firstname', 'surname', 'email', 'nickname', 'password', 'gender']
oauth_values = ['firstname', 'lastname', 'email', 'nickname', 'gender']

# from https://moodlist.net/
MOODS = ['Accepted', 'Accomplished', 'Aggravated', 'Alone', 'Amused', 'Angry', 'Annoyed', 'Anxious', 'Apathetic',
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
# $.each($($('table')[3]).find('tbody td:first-child'), function(){if ($(this).text().length > 2 ) list += ', ' +
# '"' + $(this).text().replace(' (list) ', ') + '"'});
ANIMALS = ['Aardvark', 'Albatross', 'Alligator', 'Alpaca', 'Ant', 'Anteater', 'Antelope', 'Ape', 'Armadillo',
           'Badger', 'Barracuda', 'Bat', 'Bear', 'Beaver', 'Bee', 'Bird', 'Bison', 'Boar', 'Buffalo', 'Butterfly',
           'Camel', 'Caribou', 'Cassowary', 'Cat', 'Caterpillar', 'Cattle', 'Chamois', 'Cheetah', 'Chicken',
           'Chimpanzee', 'Chinchilla', 'Chough', 'Coati', 'Cobra', 'Cockroach', 'Cod', 'Cormorant', 'Coyote',
           'Crab', 'Crane', 'Crocodile', 'Crow', 'Curlew', 'Deer', 'Dinosaur', 'Dog', 'Dolphin', 'Donkey',
           'Dotterel',
           'Dove', 'Dragonfly', 'Duck', 'Dugong', 'Dunlin', 'Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant',
           'Elephant Seal', 'Elk', 'Emu Falcon', 'Ferret', 'Finch', 'Fish', 'Flamingo', 'Fly', 'Fox', 'FrogGaur',
           'Gazelle', 'Gerbil', 'Giant Panda', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goosander', 'Goose',
           'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Guinea Pig', 'Gull ', 'Hamster', 'Hare',
           'Hawk',
           'Hedgehog', 'Heron', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Hummingbird', 'Hyena', 'Ibex',
           'Ibis', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Kangaroo', 'Kinkajou', 'Koala', 'Komodo Dragon',
           'Kouprey', 'Kudu', 'Lapwing', 'Lark', 'Lemur', 'Leopard', 'Lion', 'Llama', 'Lobster', 'Locust', 'Loris',
           'Louse', 'Lyrebird Magpie', 'Mallard', 'Mammoth', 'Manatee', 'Mandrill', 'Mink', 'Mole', 'Mongoose',
           'Monkey', 'Moose', 'Mouse', 'Mosquito', 'Narwhal', 'Newt', 'Nightingale', 'Octopus', 'Okapi', 'Opossum',
           'Ostrich',
           'Otter', 'Owl', 'Oyster', 'Panther', 'Parrot', 'Partridge', 'Peafowl', 'Pelican', 'Penguin', 'Pheasant',
           'Pig', 'Pigeon', 'Polar Bear', 'Porcupine', 'Porpoise', 'Quelea', 'Quetzal', 'Rabbit', 'Raccoon', 'Rat',
           'Raven', 'Red Deer', 'Red Panda', 'Reindeer', 'Rhinoceros', 'RookSalamander', 'Salmon', 'Sand Dollar',
           'Sandpiper', 'Sardine', 'Sea Lion', 'Sea Urchin', 'Seahorse', 'Seal', 'Shark', 'Sheep', 'Shrew', 'Skunk',
           'Sloth', 'Snail', 'Snake ', 'Spider', 'Squirrel', 'Starling', 'Swan', 'Tapir', 'Tarsier', 'Termite',
           'Tiger',
           'Toad', 'Turkey', 'Turtle', 'Walrus', 'Wasp', 'Water Buffalo', 'Weasel', 'Whale', 'Wolf', 'Wolverine',
           'Wombat', 'Yak', 'Zebra', 'Baboon', 'Eagle']

# http://www.manythings.org/vocabulary/lists/l/words.php?f=ogden-picturable
THINGS = ['Angle', 'Ant', 'Apple', 'Arch', 'Arm', 'Army', 'Baby', 'Bag', 'Ball', 'Band', 'Basin', 'Basket',
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
FOODS = ['Acorn Squash', 'Adobo', 'Aioli', 'Alfredo Sauce', 'Almond Paste', 'Amaretto', 'Ancho Chile Peppers',
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


def should_log_out(timeout: int, user: User) -> bool:
    """
    Returns a boolean stating that the user should be logged out when its True, and False otherwise.

    :param timeout: A timeout in seconds.
    :param user: The User that should be checked for a possible log-out
    :return: Boolean
    """
    if not user or user.nickname == nick_of_anonymous_user:
        return False

    # check difference of
    diff_action: timedelta = get_now() - user.last_action
    diff_login: timedelta = get_now() - user.last_login
    diff_action: int = diff_action.seconds + diff_action.days * 24 * 60 * 60
    diff_login: int = diff_login.seconds + diff_login.days * 24 * 60 * 60

    diff = diff_action if diff_action < diff_login else diff_login
    log_out = diff > timeout and not user.settings.keep_logged_in

    return log_out


def _random_nickname() -> str:
    name_parts = ANIMALS + THINGS + FOODS
    adjective = random.choice(MOODS)
    noun = random.choice(name_parts)
    return adjective + ' ' + noun


def refresh_public_nickname(user: User) -> str:
    """
    Creates and sets a random public nick for the given user

    :param user: The user whose nickname shall be refreshed.
    :return: The new nickname as string
    """
    nick = _random_nickname()
    while DBDiscussionSession.query(User).filter_by(public_nickname=nick).first():
        nick = _random_nickname()

    LOG.debug("User %s -> %s", user.public_nickname, nick)
    user.set_public_nickname(nick)

    return nick


def _labels_for_historical_data(days: int, lang: str) -> List[str]:
    """
    Return a list of dates that can be used as labels for public data points regarding a user.

    :param days: Labels for last x days.
    :param lang: The language of the labels.
    :return: A list containing the labels for every of the last `days`.
    """
    labels = []
    for days_diff in range(days, -1, -1):
        date_begin = date.today() - timedelta(days=days_diff)
        timestamp = pretty_print_timestamp(date_begin, lang)
        labels.append(timestamp)
    return labels


def _time_range_list(days: int) -> List[Tuple[Arrow, Arrow]]:
    """
    Return a list of Tuples containing begin and end dates needed to query the database.

    :param days: Number of days back, where the range is starting.
    :return: Returns a List of Arrow Tuples.
    """
    time_range = []
    for days_diff in range(days, -1, -1):
        date_begin = date.today() - timedelta(days=days_diff)
        date_end = date.today() - timedelta(days=days_diff - 1)
        begin = arrow.get(date_begin.strftime('%Y-%m-%d'), 'YYYY-MM-DD')
        end = arrow.get(date_end.strftime('%Y-%m-%d'), 'YYYY-MM-DD')
        time_range.append((begin, end))

    return time_range


def _historical_user_data_for_decisions(user: User, days: int) -> List:
    """
    Return public data regarding the clicked Statements for a certain user

    :param days: The number of days ending with today for which the data shall be procured.
    :param user: The user for which the data shall be procured.
    :return: A Tuple containing the labels and the data points.
    """
    data = []
    for begin, end in _time_range_list(days):
        db_clicks_statements = DBDiscussionSession.query(ClickedStatement).filter(
            ClickedStatement.author_uid == user.uid,
            ClickedStatement.timestamp >= begin,
            ClickedStatement.timestamp < end).all()
        db_clicks_arguments = DBDiscussionSession.query(ClickedArgument).filter(
            ClickedArgument.author_uid == user.uid,
            ClickedArgument.timestamp >= begin,
            ClickedArgument.timestamp < end).all()
        clicks = len(db_clicks_statements) + len(db_clicks_arguments)
        data.append(clicks)

    return data


def _historical_user_data_for_statements_edits(user: User, days: int, lang: str) -> Tuple[List, List]:
    """
    Return the public historical data regarding statements and edits of a certain user.

    :param user: The user for which the data shall be procured.
    :param days: The number of days the data should date back.
    :param lang: The language in which the data shall be presented.
    :return: A tuple with two lists containing the data regarding statements and edits.
    """
    statement_data = []
    edit_data = []
    for begin, end in _time_range_list(days):
        get_tv_dict = get_textversions(user, lang, begin, end)
        statement_data.append(len(get_tv_dict.get('statements', [])))
        edit_data.append(len(get_tv_dict.get('edits', [])))

    return statement_data, edit_data


def get_public_data(user_id: int, lang: str) -> Dict[str, List]:
    """
    Fetch public information about the user with given id

    :param user_id: Id of the user for which public information shall be fetched
    :param lang: Language of information
    :return: A dictionary representing the information. All values are Lists.
    """
    return_dict = dict()
    db_user = DBDiscussionSession.query(User).get(user_id)

    if db_user is None and user_id != 1:
        LOG.debug("Could not fetch public information. User is unknown.")
        return return_dict

    LOG.debug("Fetching public information for user: %s", db_user.nickname)

    _tn = Translator(lang)

    return_dict['label1'] = _tn.get(Keywords.decisionIndex7)
    return_dict['label2'] = _tn.get(Keywords.decisionIndex30)
    return_dict['label3'] = _tn.get(Keywords.statementIndex)
    return_dict['label4'] = _tn.get(Keywords.editIndex)

    if user_id == 1:
        return _special_public_data(return_dict, lang)

    labels_decision_30 = labels_statement_30 = labels_edit_30 = _labels_for_historical_data(30, lang)
    data_statement_30, data_edit_30 = _historical_user_data_for_statements_edits(db_user, 30, lang)

    return_dict['labels1'] = _labels_for_historical_data(7, lang)
    return_dict['labels2'] = labels_decision_30
    return_dict['labels3'] = labels_statement_30
    return_dict['labels4'] = labels_edit_30
    return_dict['data1'] = _historical_user_data_for_decisions(db_user, 7)
    return_dict['data2'] = _historical_user_data_for_decisions(db_user, 30)
    return_dict['data3'] = data_statement_30
    return_dict['data4'] = data_edit_30

    return return_dict


def _special_public_data(rdict: Dict, lang: str) -> Dict[str, List]:
    """
    Return mock public data for anonymous User.

    :param rdict: The dictionary which shall be filled.
    :param lang: The language in which the dictionary is provided.
    :return: Mock public statistics in a dictionary.
    """
    rdict['labels1'] = [pretty_print_timestamp(date.today() - timedelta(days=dd), lang) for dd in range(7, -1, -1)]
    rdict['labels2'] = [pretty_print_timestamp(date.today() - timedelta(days=dd), lang) for dd in range(30, -1, -1)]
    rdict['labels3'] = rdict['labels2']
    rdict['labels4'] = rdict['labels2']
    rdict['data1'] = [9000.1] * 7
    rdict['data2'] = [9000.1] * 30
    rdict['data3'] = rdict['data2']
    rdict['data4'] = rdict['data2']
    return rdict


def number_of_reviews(user: User, only_today: bool) -> int:
    """
    Returns the number of reviews made by the user.

    :param user: The user whose reviews should be counted.
    :param only_today: True if only the reviews of the current date shall be counted.
    :return: Number of reviews.
    """
    since = arrow.utcnow() if only_today else arrow.get(0)
    since_timestamp = since.format('YYYY-MM-DD')

    num_edits = DBDiscussionSession.query(ReviewEdit).filter(
        ReviewEdit.detector_uid == user.uid,
        ReviewEdit.timestamp >= since_timestamp).count()
    num_deletes = DBDiscussionSession.query(ReviewDelete).filter(
        ReviewDelete.detector_uid == user.uid,
        ReviewDelete.timestamp >= since_timestamp).count()
    num_optimizations = DBDiscussionSession.query(ReviewOptimization).filter(
        ReviewOptimization.detector_uid == user.uid,
        ReviewOptimization.timestamp >= since_timestamp).count()
    num_duplicates = DBDiscussionSession.query(ReviewDuplicate).filter(
        ReviewDuplicate.detector_uid == user.uid,
        ReviewOptimization.timestamp >= since_timestamp).count()

    return num_edits + num_deletes + num_optimizations + num_duplicates


def _get_count_of_statements(user: User, only_today: bool = False) -> Tuple[int, int]:
    """
    Returns the number of statements and edits a user made.

    :param user: The user which should be queried.
    :param only_today: Indicates, whether only the data of the current day shall be counted.
    :return: A Tuple containing the number of edits and statements.
    """
    edit_count = 0
    statement_count = 0
    texts = DBDiscussionSession.query(TextVersion).filter_by(author_uid=user.uid)

    if only_today:
        today = arrow.utcnow().format('YYYY-MM-DD')
        texts = texts.filter(TextVersion.timestamp >= today)
    texts = texts.all()

    for text in texts:
        original_text = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=text.statement_uid).first()
        if original_text.uid < text.uid:
            edit_count += 1
        else:
            statement_count += 1

    return edit_count, statement_count


def get_statement_count_of(db_user: User, only_today: bool = False) -> int:
    """
    Returns the number of statements a user made.

    :param db_user: The user which should be queried.
    :param only_today: Indicates, whether only the data of the current day shall be counted.
    :return: The number of statements.
    """
    _, statement_count = _get_count_of_statements(db_user, only_today)
    return statement_count


def get_edit_count_of(db_user: User, only_today: bool = False) -> int:
    """
    Returns the number of edits a user made.

    :param db_user: The user which should be queried.
    :param only_today: Indicates, whether only the data of the current day shall be counted.
    :return: The number of edits.
    """
    edit_count, _ = _get_count_of_statements(db_user, only_today)
    return edit_count


def get_mark_count_of(user: User, only_today: bool = False) -> Tuple[int, int]:
    """
    Returns the count of marked arguments and statements of the specific user.

    :param user: The user whose arguments are counted.
    :param only_today: True if only the marked arguments of the current day shall be counted.
    :return: A tuple containing the count of marked arguments and marked statements.
    """
    if not user:
        return 0, 0

    marked_arguments = DBDiscussionSession.query(MarkedArgument).filter(MarkedArgument.author_uid == user.uid)
    marked_statements = DBDiscussionSession.query(MarkedStatement).filter(MarkedStatement.author_uid == user.uid)

    if only_today:
        today = arrow.utcnow().format('YYYY-MM-DD')
        marked_arguments = marked_arguments.filter(MarkedArgument.timestamp >= today)
        marked_statements = marked_statements.filter(MarkedStatement.timestamp >= today)

    return marked_arguments.count(), marked_statements.count()


def get_click_count_of(user: User, only_today: bool = False) -> Tuple[int, int]:
    """
    Returns the count of clicked arguments and clicked statements the user made.

    :param user: The user whose clicks are counted.
    :param only_today: True if only the clicks of the current day shall be counted.
    :return: A Tuple containing the number of clicked arguments and clicked statements.
    """
    if not user:
        return 0, 0

    clicked_arguments = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == user.uid)
    clicked_statements = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.author_uid == user.uid)

    if only_today:
        today = arrow.utcnow().format('YYYY-MM-DD')
        clicked_arguments = clicked_arguments.filter(ClickedArgument.timestamp >= today)
        clicked_statements = clicked_statements.filter(ClickedStatement.timestamp >= today)

    return clicked_arguments.count(), clicked_statements.count()


def get_textversions(user: User, lang: str, timestamp_after: Arrow = None, timestamp_before: Arrow = None) -> \
        Dict[str, List[Dict[str, str]]]:
    """
    Returns all textversions, were the user is the author.

    :param user: The user who is author of desired textversion objects.
    :param lang: The language in which the results shall be delivered.
    :param timestamp_after: Set a date if results should only include objects created after the date.
    :param timestamp_before: Set a date if results should only include objects created before the date.
    :return: Return a dict with all statements and edits that use a textversion where the user is author.
    """
    statements = []
    edits = []

    if not timestamp_after:
        timestamp_after = arrow.get('1970-01-01').format('YYYY-MM-DD')
    if not timestamp_before:
        timestamp_before = arrow.utcnow().replace(days=+1).format('YYYY-MM-DD')

    textversions = DBDiscussionSession.query(TextVersion).filter(TextVersion.author_uid == user.uid,
                                                                 TextVersion.timestamp >= timestamp_after,
                                                                 TextVersion.timestamp < timestamp_before).all()

    for textversion in textversions:
        db_root_version = DBDiscussionSession.query(TextVersion).filter_by(
            statement_uid=textversion.statement_uid).first()
        edit_dict = dict()
        edit_dict['uid'] = str(textversion.uid)
        edit_dict['statement_uid'] = str(textversion.statement_uid)
        edit_dict['content'] = str(textversion.content)
        edit_dict['timestamp'] = sql_timestamp_pretty_print(textversion.timestamp, lang)
        if db_root_version.uid == textversion.uid:
            statements.append(edit_dict)
        else:
            edits.append(edit_dict)

    return {
        'statements': statements,
        'edits': edits
    }


def get_marked_arguments(user: User, lang: str) -> List[Dict[str, Any]]:
    """
    Get all marked arguments of the user.

    :param user: The user whose marked arguments you want to query.
    :param lang: The language in which the answer shall be returned.
    :return: A list of dictionaries representing arguments
    """
    marked_arguments = DBDiscussionSession.query(MarkedArgument).filter_by(author_uid=user.uid).all()
    return [_marked_element_to_dict(marked_argument, lang) for marked_argument in marked_arguments]


def get_marked_statements(user: User, lang: str) -> List[Dict[str, Any]]:
    """
    Get all marked statements of the user.

    :param user: The user whose marked statements you want to query.
    :param lang: The language in which the answer shall be returned.
    :return: A list of dictionaries representing arguments
    """
    marked_statements = DBDiscussionSession.query(MarkedStatement).filter_by(author_uid=user.uid).all()
    return [_marked_element_to_dict(marked_statement, lang) for marked_statement in marked_statements]


def _marked_element_to_dict(marked_object: Union[MarkedArgument, MarkedStatement], lang: str) -> Dict[str, Any]:
    """
    Transform a given MarkedArgument or MarkedStatement object into a dictionary representation.

    :param marked_object: The MarkedArgument or MarkedStatement which shall be transformed.
    :param lang: The language in which the answer shall be returned.
    :return: A dictionary representing a MarkedArgument / MarkedStatement.
    """
    dict_representation = marked_object.to_dict()
    if type(marked_object) is MarkedArgument:
        return dict_representation.update({'content': get_text_for_argument_uid(marked_object.argument_uid, lang)})
    else:
        return dict_representation.update({'content': marked_object.statement.get_text()})


def get_clicked_statements(user: User, lang: str) -> List[Dict[str, Any]]:
    """
    Return all statements that the user clicked.

    :param user: The user for which the clicked statements shall be acquired.
    :param lang: Language that the answer shall be delivered in.
    :return: A list of dictionaries representing the clicked statements.
    """
    return [clicked_statement.to_dict(lang) for clicked_statement in user.clicked_statements]


def get_clicked_arguments(user: User, lang: str) -> List[Dict[str, Any]]:
    """
    Return all arguments that the user clicked.

    :param user: The user for which the clicked arguments shall be acquired.
    :param lang: Language that the answer shall be delivered in.
    :return: A list of dictionaries representing the clicked arguments.
    """
    return [_clicked_argument_to_dict(clicked_argument, lang) for clicked_argument in user.clicked_arguments]


def _clicked_argument_to_dict(clicked_argument: ClickedArgument, lang: str) -> Dict[str, Any]:
    """
    Transforms a single ClickedArgument object into a dictionary representation of itself.

    :param clicked_argument: The object that shall be transformed.
    :param lang: Language that the answer shall be delivered in.
    :return: A dictionary representing `clicked_argument`.
    """

    return {'uid': clicked_argument.uid,
            'timestamp': sql_timestamp_pretty_print(clicked_argument.timestamp, lang),
            'is_up_vote': clicked_argument.is_up_vote,
            'is_valid': clicked_argument.is_valid,
            'argument_uid': clicked_argument.argument_uid,
            'content': get_text_for_argument_uid(clicked_argument.argument_uid, lang)}


def get_information_of(user: User, lang: str) -> Dict[str, Any]:
    """
    Returns public information of the given user.

    :param user: User whose information is queried.
    :param lang: Language-string representing language of the answer.
    :return: A dictionary containing the public information.
    """
    if user.nickname == nick_of_anonymous_user:
        return _get_special_infos(lang)
    ret_dict = dict()
    ret_dict['public_nick'] = user.global_nickname
    ret_dict['last_action'] = sql_timestamp_pretty_print(user.last_action, lang)
    ret_dict['last_login'] = sql_timestamp_pretty_print(user.last_login, lang)
    ret_dict['registered'] = sql_timestamp_pretty_print(user.registered, lang)
    ret_dict['group'] = start_with_capital(user.group.name)

    ret_dict['is_male'] = user.gender == 'm'
    ret_dict['is_female'] = user.gender == 'f'
    ret_dict['is_neutral'] = user.gender != 'm' and user.gender != 'f'

    arg_votes, stat_votes = get_mark_count_of(user, False)
    db_reviews_duplicate = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=user.uid).all()
    db_reviews_edit = DBDiscussionSession.query(ReviewEdit).filter_by(detector_uid=user.uid).all()
    db_reviews_delete = DBDiscussionSession.query(ReviewDelete).filter_by(detector_uid=user.uid).all()
    db_reviews_optimization = DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=user.uid).all()
    db_reviews = db_reviews_duplicate + db_reviews_edit + db_reviews_delete + db_reviews_optimization

    get_tv_dict = get_textversions(user, lang)
    ret_dict['statements_posted'] = len(get_tv_dict.get('statements', []))
    ret_dict['edits_done'] = len(get_tv_dict.get('edits', []))
    ret_dict['reviews_proposed'] = len(db_reviews)
    ret_dict['discussion_arg_votes'] = arg_votes
    ret_dict['discussion_stat_votes'] = stat_votes
    ret_dict['avatar_url'] = get_profile_picture(user, 120)
    ret_dict['discussion_stat_rep'], _ = get_reputation_of(user)

    return ret_dict


def _get_special_infos(lang: str) -> Dict[str, Any]:
    return {
        'public_nick': 'Son Goku',
        'last_action': sql_timestamp_pretty_print(get_now(), lang),
        'last_login': sql_timestamp_pretty_print(get_now(), lang),
        'registered': sql_timestamp_pretty_print(get_now(), lang),
        'group': 'Saiyajin',
        'is_male': True,
        'is_female': False,
        'is_neutral': False,
        'statements_posted': '>9000',
        'edits_done': '>9000',
        'reviews_proposed': '>9000',
        'discussion_arg_votes': '>9000',
        'discussion_stat_votes': '>9000',
        'avatar_url': '/static/images/goku.jpg',
        'discussion_stat_rep': '>9000',
    }


def get_summary_of_today(db_user: User) -> dict:
    """
    Returns summary of today's actions

    :param db_user: Contains parameters for the user concerned
    :return: dict()
    """
    if not db_user:
        return {}

    arg_votes, stat_votes = get_mark_count_of(db_user, True)
    arg_clicks, stat_clicks = get_click_count_of(db_user, True)
    reputation, tmp = get_reputation_of(db_user, True)
    timestamp = arrow.utcnow().to('Europe/Berlin')
    timestamp.format('DD.MM.')

    ret_dict = {
        'firstname': db_user.firstname,
        'statements_posted': get_statement_count_of(db_user, True),
        'edits_done': get_edit_count_of(db_user, True),
        'discussion_arg_votes': arg_votes,
        'discussion_stat_votes': stat_votes,
        'discussion_arg_clicks': arg_clicks,
        'discussion_stat_clicks': stat_clicks,
        'statements_reported': number_of_reviews(db_user, True),
        'reputation_collected': reputation
    }
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
    LOG.debug("Entering change_password")
    _t = Translator(lang)

    success = False

    # is the old password given?
    if not old_pw:
        LOG.debug("Old pwd is empty")
        message = _t.get(Keywords.oldPwdEmpty)  # 'The old password field is empty.'
    # is the new password given?
    elif not new_pw:
        LOG.debug("New pwd is empty")
        message = _t.get(Keywords.newPwdEmtpy)  # 'The new password field is empty.'
    # is the confirmation password given?
    elif not confirm_pw:
        LOG.debug("Confirm pwd is empty")
        message = _t.get(Keywords.confPwdEmpty)  # 'The password confirmation field is empty.'
    # is new password equals the confirmation?
    elif not new_pw == confirm_pw:
        LOG.debug("New pwds not equal")
        message = _t.get(Keywords.newPwdNotEqual)  # 'The new passwords are not equal'
    # is new old password equals the new one?
    elif old_pw == new_pw:
        LOG.debug("Pwds are the same")
        message = _t.get(Keywords.pwdsSame)  # 'The new and old password are the same'
    else:
        # is the old password valid?
        if not user.validate_password(old_pw):
            LOG.debug("Old password is wrong")
            message = _t.get(Keywords.oldPwdWrong)  # 'Your old password is wrong.'
        else:
            user.change_password(new_pw)

            LOG.debug("Password was changed")
            message = _t.get(Keywords.pwdChanged)  # 'Your password was changed'
            success = True

    return message, success


def __create_new_user(user_info: Dict[str, Any], ui_locales: str, oauth_provider: Optional[str] = None,
                      oauth_provider_id: Optional[str] = None) -> Tuple[str, str, User]:
    """
    Create a new user.

    :param user_info: A dictionary containing information about the desired user.
    :param ui_locales: Language which shall be used for messaging.
    :param oauth_provider: If applicable: Which oauth-provider is referring the user.
    :param oauth_provider_id: If applicable: The ID of the oauth-provider.
    :return: Returns a tuple containing a success message, a information message and the freshly created user.
    """
    success = ''
    info = ''

    _tn = Translator(ui_locales)
    language = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
    # creating a new user_info with hashed password
    LOG.debug("Adding user_info for %s", user_info['nickname'])
    hashed_password = password_handler.get_hashed_password(user_info['password'])
    new_user = User(firstname=user_info['firstname'],
                    surname=user_info['lastname'],
                    email=user_info['email'],
                    nickname=user_info['nickname'],
                    password=hashed_password,
                    gender=user_info['gender'],
                    group=user_info['db_group'],
                    oauth_provider=oauth_provider,
                    oauth_provider_id=oauth_provider_id)
    DBDiscussionSession.add(new_user)
    settings = Settings(user=new_user,
                        send_mails=False,
                        send_notifications=True,
                        should_show_public_nickname=True,
                        language=language)
    DBDiscussionSession.add(settings)

    if new_user:
        LOG.debug("New data was added with uid %s", new_user.uid)
        success = _tn.get(Keywords.accountWasAdded).format(user_info['nickname'])
    else:
        LOG.debug("New data was not added")
        info = _tn.get(Keywords.accoutErrorTryLateOrContant)

    return success, info, new_user


def set_new_user(mailer: Mailer, user_data: Dict[str, Any], password: str, _tn: Translator) -> Dict[str, Any]:
    """
    Public interface for creating a new user.

    :param mailer: The mailer used to send Emails to the new user.
    :param user_data: Dictionary containing user information.
    :param password: The desired password to be set. (un-hashed)
    :param _tn: The translator object to be used for messaging.
    :return: A dictionary containing whether the operation was a success, an optional error message and the newly
        created user if the transaction was successful.
    """
    # copy the dict to not change the mutable structure
    temporary_user = dict(user_data)
    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()

    # does the group exists?
    if not db_group:
        LOG.debug("Internal error occurred")
        return {'success': False, 'error': _tn.get(Keywords.errorTryLateOrContant), 'user': None}

    if DBDiscussionSession.query(User).filter(User.nickname == temporary_user['nickname']).first():
        LOG.debug("User already exists")
        return {'success': False, 'error': _tn.get(Keywords.nickIsTaken), 'user': None}

    temporary_user['password'] = password
    temporary_user['db_group'] = db_group

    success, info, db_new_user = __create_new_user(temporary_user, _tn.get_lang())

    if db_new_user:
        # sending an email and message
        subject = _tn.get(Keywords.accountRegistration)
        body = _tn.get(Keywords.accountWasRegistered).format(temporary_user['firstname'], temporary_user['lastname'],
                                                             temporary_user['email'])
        send_mail(mailer, subject, body, temporary_user['email'], _tn.get_lang())
        send_welcome_notification(db_new_user.uid, _tn)

        LOG.debug("Set new user in db")
        return {'success': success, 'error': '', 'user': db_new_user}

    LOG.debug("New user not found in db")
    return {
        'success': False,
        'error': _tn.get(Keywords.errorTryLateOrContant),
        'user': None
    }


def set_new_oauth_user(user_data: Dict[str, Any], oauth_id: str, provider: str, _tn: Translator) -> Dict[str, Any]:
    """
    Create a new user for an oauth provider.

    :param user_data: Dictionary containing user information.
    :param oauth_id: The user id at his oauth-provider.
    :param provider: The oauth provider.
    :param _tn: A Translator object.
    :return: A dictionary containing whether the operation was a success, an optional error message and the newly
        created user if the transaction was successful.
    """
    temporary_user = dict(user_data)
    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()

    # does the group exists?
    if not db_group:
        LOG.debug("Internal error occurred")
        return {'success': False, 'error': _tn.get(Keywords.errorTryLateOrContant), 'user': None}

    # sanity check
    db_user = DBDiscussionSession.query(User).filter(User.oauth_provider == str(provider),
                                                     User.oauth_provider_id == str(oauth_id)).first()
    # login of oauth user
    if db_user:
        LOG.debug("User already exists. They will login")
        return {'success': True, 'error': '', 'user': db_user}

    # sanity check
    db_user = DBDiscussionSession.query(User).filter_by(nickname=temporary_user['nickname']).first()
    if db_user:
        LOG.debug("User already exists")
        return {'success': False, 'error': _tn.get(Keywords.nickIsTaken), 'user': None}

    temporary_user['password'] = str(uuid.uuid4().hex)
    temporary_user['db_group'] = db_group

    success, info, db_new_user = __create_new_user(temporary_user, _tn.get_lang(), oauth_provider=provider,
                                                   oauth_provider_id=oauth_id)

    if db_new_user:
        LOG.debug("Set new user in db")
        return {'success': success, 'error': '', 'user': db_new_user}

    LOG.debug("New user not found in db")

    return {
        'success': False,
        'error': _tn.get(Keywords.errorTryLateOrContant),
        'user': None
    }


def get_users_with_same_opinion(uids: List[int], app_url: str, path: str, db_user: User, is_argument: bool,
                                is_attitude: bool, is_reaction: bool, is_position: bool, db_lang: Language) -> Dict:
    """
    Based on current discussion step information about other users will be given

    :param uids: IDs of statements or argument for the information request
    :param app_url: url of the application
    :param path: current path of the user
    :param db_user: User
    :param is_argument: boolean, whether the request is for an argument
    :param is_attitude: boolean, whether the request is during the attitude step
    :param is_reaction: boolean, whether the request is during the attitude step
    :param is_position: boolean, whether the request is for a position
    :param db_lang: Language
    :return: prepared collection with information about other users with the same opinion or an error
    """
    prepared_dict = dict()

    if is_argument and is_reaction:
        prepared_dict = get_user_and_opinions_for_argument(uids[0], db_user, db_lang.ui_locales, app_url, path)
    elif is_argument and not is_reaction:
        prepared_dict = get_user_with_same_opinion_for_argument(uids, db_user, db_lang.ui_locales, app_url)
    elif is_position:
        prepared_dict = get_user_with_same_opinion_for_statements(uids, True, db_user, db_lang.ui_locales, app_url)
    elif is_attitude:
        prepared_dict = get_user_with_opinions_for_attitude(uids[0], db_user, db_lang.ui_locales, app_url)
    elif not is_attitude:
        prepared_dict = get_user_with_same_opinion_for_premisegroups_of_args(uids, db_user, db_lang.ui_locales, app_url)
    prepared_dict['info'] = ''

    return prepared_dict


def delete(user: User) -> None:
    """
    Delete the user and all data connected to them.

    :param user: The user which gets deleted.
    :return: Returns nothing, this function is one big side-effect.
    """
    anonym_uid = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first().uid

    # authors
    authors = DBDiscussionSession.query(Issue).filter_by(author_uid=user.uid).all()
    authors += DBDiscussionSession.query(TextVersion).filter_by(author_uid=user.uid).all()
    authors += DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=user.uid).all()
    authors += DBDiscussionSession.query(Premise).filter_by(author_uid=user.uid).all()
    authors += DBDiscussionSession.query(Argument).filter_by(author_uid=user.uid).all()
    authors += DBDiscussionSession.query(ReviewCanceled).filter_by(author_uid=user.uid).all()
    authors += DBDiscussionSession.query(RevokedContent).filter_by(author_uid=user.uid).all()
    for element in authors:
        element.author_uid = anonym_uid

    # reviews without ReviewSplitValues and ReviewMergeValues
    review_edit = DBDiscussionSession.query(ReviewEdit).filter_by(detector_uid=user.uid).all()
    review_edit_value = DBDiscussionSession.query(ReviewEditValue).filter(
        ReviewEditValue.review_edit_uid.in_([r.uid for r in review_edit])).all()
    reviews = DBDiscussionSession.query(ReviewDelete).filter_by(detector_uid=user.uid).all()
    reviews += DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=user.uid).all()
    reviews += DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=user.uid).all()
    reviews += DBDiscussionSession.query(ReviewMerge).filter_by(detector_uid=user.uid).all()
    reviews += DBDiscussionSession.query(ReviewSplit).filter_by(detector_uid=user.uid).all()
    for element in reviews + review_edit + review_edit_value:
        element.detector_uid = anonym_uid

    # last reviewed elements
    last_reviewers = DBDiscussionSession.query(LastReviewerDelete).filter_by(reviewer_uid=user.uid).all()
    last_reviewers += DBDiscussionSession.query(LastReviewerDuplicate).filter_by(reviewer_uid=user.uid).all()
    last_reviewers += DBDiscussionSession.query(LastReviewerEdit).filter_by(reviewer_uid=user.uid).all()
    last_reviewers += DBDiscussionSession.query(LastReviewerOptimization).filter_by(reviewer_uid=user.uid).all()
    last_reviewers += DBDiscussionSession.query(LastReviewerSplit).filter_by(reviewer_uid=user.uid).all()
    last_reviewers += DBDiscussionSession.query(LastReviewerMerge).filter_by(reviewer_uid=user.uid).all()
    for element in last_reviewers:
        element.reviewer_uid = anonym_uid

    # revoked content
    rev_cntnt_hisy_old = DBDiscussionSession.query(RevokedContentHistory).filter_by(old_author_uid=user.uid).all()
    rev_cntnt_hisy_new = DBDiscussionSession.query(RevokedContentHistory).filter_by(new_author_uid=user.uid).all()
    for element in rev_cntnt_hisy_old:
        element.old_author_uid = anonym_uid
    for element in rev_cntnt_hisy_new:
        element.new_author_uid = anonym_uid

    DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=user.uid).delete()
    DBDiscussionSession.query(SeenStatement).filter_by(user_uid=user.uid).delete()
    DBDiscussionSession.query(SeenArgument).filter_by(user_uid=user.uid).delete()
    DBDiscussionSession.query(History).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(Settings).filter_by(user=user).delete()
    DBDiscussionSession.query(StatementReference).filter_by(author=user).delete()
    DBDiscussionSession.query(ClickedArgument).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(MarkedArgument).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(MarkedStatement).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(Message).filter_by(from_author_uid=user.uid).delete()
    DBDiscussionSession.query(Message).filter_by(to_author_uid=user.uid).delete()
    DBDiscussionSession.query(User).filter_by(uid=user.uid).delete()


def get_list_of_admins() -> List[User]:
    """
    Returns a list of users which are members of the admin group. If this list is empty, D-BAS is configured wrongly.

    :return: A List of Users. Every user belongs to the 'admin' group.
    """
    db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
    db_admins = DBDiscussionSession.query(User).filter_by(group_uid=db_admin_group.uid).all()
    return db_admins
