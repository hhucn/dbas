import unittest

import os

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config

from dbas import DBDiscussionSession

dir_name = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
settings = appconfig('config:' + os.path.join(dir_name, 'development.ini'))


class OpinionHandlerTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.opinion_handler import OpinionHandler
        return OpinionHandler

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_init(self):
        opinion = self._makeOne(lang='en',
                                nickname='nickname',
                                mainpage='url')

        self.assertEqual(opinion.lang, 'en')

        self.assertEqual(opinion.nickname, 'nickname')

        self.assertEqual(opinion.mainpage, 'url')

    def test_get_user_and_opinions_for_argument(self):
        opinion = self._makeOne(lang='de',
                                nickname='nickname',
                                mainpage='url')

        DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

        response = {'opinions':
                        {'undercut':
                             {'users':
                                  [{'vote_timestamp': 'vor 11 Tagen',
                                    'nickname': 'Tired Spider',
                                    'public_profile_url': 'url/user/Tired Spider',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/6bb2517d60e42794c67dc9202609008c?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 16 Tagen',
                                    'nickname': 'Sleepy Brush',
                                    'public_profile_url': 'url/user/Sleepy Brush',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/252f24a5f958193a68311ad70919da5f?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Complacent Cobra',
                                    'public_profile_url': 'url/user/Complacent Cobra',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/11981c123398ab1eaff878279c794744?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 21 Tagen',
                                    'nickname': 'Nora',
                                    'public_profile_url': 'url/user/Nora',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/b5dbbdffaff9c480417ad04e9d38558e?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 14 Tagen',
                                    'nickname': 'Jutta',
                                    'public_profile_url': 'url/user/Jutta',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/396f78530243343aec83ce45d3cf1c91?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 21 Tagen',
                                    'nickname': 'Friedrich',
                                    'public_profile_url': 'url/user/Friedrich',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/fa558317029c93b968888b4cee4736ae?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 17 Tagen',
                                    'nickname': 'Sybille',
                                    'public_profile_url': 'url/user/Sybille',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/101ef3e619bf541eba001124b15ed2b1?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 20 Tagen',
                                    'nickname': 'Torben',
                                    'public_profile_url': 'url/user/Torben',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/e019a629612a4c83dfae6059e451e354?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Crazy Line',
                                    'public_profile_url': 'url/user/Crazy Line',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/e6bea3c722b1a93ace3e22b30c7ac12a?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Hanne',
                                    'public_profile_url': 'url/user/Hanne',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/56e991f77a510cc4f5060c6e60180809?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Helga',
                                    'public_profile_url': 'url/user/Helga',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/6cede182f7fe60919dd82dc41da895e0?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Ingeburg',
                                    'public_profile_url': 'url/user/Ingeburg',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/acc2b70dd800decf22733fcffa0c4459?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 14 Tagen',
                                    'nickname': 'High Scissors',
                                    'public_profile_url': 'url/user/High Scissors',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/b931a0310425e0132204cc5d8fc1821a?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 10 Tagen',
                                    'nickname': 'Pascal',
                                    'public_profile_url': 'url/user/Pascal',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/550abbbf1af0cabd75b5d1b501e9ef29?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Full Throat',
                                    'public_profile_url': 'url/user/Full Throat',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/e81099a3753f8f85def6b72f28880b89?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 18 Tagen',
                                    'nickname': 'Melancholy Barracuda',
                                    'public_profile_url': 'url/user/Melancholy Barracuda',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/749aacba83440880ef0185dcd5c28b11?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 7 Tagen',
                                    'nickname': 'Elly',
                                    'public_profile_url': 'url/user/Elly',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/a1e69580847a6ce87e0354217e693641?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Thorsten',
                                    'public_profile_url': 'url/user/Thorsten',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/da84d4011af0412744d79e647f34c1aa?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor einem Monat',
                                    'nickname': 'Excited Crane',
                                    'public_profile_url': 'url/user/Excited Crane',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/9d08e4dc3ef6c4618e9b2ea6300c8baf?s=80&d=wavatar'},
                                   {'vote_timestamp': 'vor 10 Tagen',
                                    'nickname': 'Aayden',
                                    'public_profile_url': 'url/user/Aayden',
                                    'avatar_url': 'https://secure.gravatar.com/avatar/3d99cde69c2c37b2c46ea2e9ccd92d48?s=80&d=wavatar'}],
                              'text': 'Ja, ich akzeptiere, dass it is much work to take care of both animals, aber ich glaube nicht, dass es ein gutes Argument dagegen ist, dass ich akzeptiere, dass Cats are very independent, weil Cats ancestors are animals in wildlife, who are hunting alone and not in groups.',
                              'message': '20 weitere Teilnehmer/innen mit dieser Meinung.'},
                         'undermine': {'users': [],
                                       'text': 'Nein, ich lehne ab, dass  it is much work to take care of both animals.',
                                       'message': ''},
                         'support': {'users': [{'vote_timestamp': 'vor 15 Tagen',
                                                'nickname': 'Bitchy Berry',
                                                'public_profile_url': 'url/user/Bitchy Berry',
                                                'avatar_url': 'https://secure.gravatar.com/avatar/ce80438b2ab6e75c5f6f05304d02de7c?s=80&d=wavatar'},
                                               {'vote_timestamp': 'vor einem Monat',
                                                'nickname': 'Thorsten',
                                                'public_profile_url': 'url/user/Thorsten',
                                                'avatar_url': 'https://secure.gravatar.com/avatar/da84d4011af0412744d79e647f34c1aa?s=80&d=wavatar'},
                                               {'vote_timestamp': 'vor einem Monat',
                                                'nickname': 'Indifferent Moon',
                                                'public_profile_url': 'url/user/Indifferent Moon',
                                                'avatar_url': 'https://secure.gravatar.com/avatar/1ce0c053f3bed03eb3be63ec0f77f06a?s=80&d=wavatar'},
                                               {'vote_timestamp': 'vor 9 Tagen',
                                                'nickname': 'Sybille',
                                                'public_profile_url': 'url/user/Sybille',
                                                'avatar_url': 'https://secure.gravatar.com/avatar/101ef3e619bf541eba001124b15ed2b1?s=80&d=wavatar'}],
                                     'text': 'Ja, ich akzeptiere, dass  it is much work to take care of both animals.',
                                     'message': '4 weitere Teilnehmer/innen mit dieser Meinung.'},
                         'rebut': {'users': [{'vote_timestamp': 'vor 13 Tagen',
                                              'nickname': 'High Scissors',
                                              'public_profile_url': 'url/user/High Scissors',
                                              'avatar_url': 'https://secure.gravatar.com/avatar/b931a0310425e0132204cc5d8fc1821a?s=80&d=wavatar'},
                                             {'vote_timestamp': 'vor 24 Tagen',
                                              'nickname': 'Torben',
                                              'public_profile_url': 'url/user/Torben',
                                              'avatar_url': 'https://secure.gravatar.com/avatar/e019a629612a4c83dfae6059e451e354?s=80&d=wavatar'},
                                             {'vote_timestamp': 'vor 8 Tagen',
                                              'nickname': 'Crazy Line',
                                              'public_profile_url': 'url/user/Crazy Line',
                                              'avatar_url': 'https://secure.gravatar.com/avatar/e6bea3c722b1a93ace3e22b30c7ac12a?s=80&d=wavatar'},
                                             {'vote_timestamp': 'vor einem Monat',
                                              'nickname': 'Bitchy Berry',
                                              'public_profile_url': 'url/user/Bitchy Berry',
                                              'avatar_url': 'https://secure.gravatar.com/avatar/ce80438b2ab6e75c5f6f05304d02de7c?s=80&d=wavatar'}],
                                   'text': 'Ja, ich akzeptiere, dass it is much work to take care of both animals und ich akzeptiere, dass es ein Argument dagegen ist, dass ich akzeptiere, dass Cats are very independent, weil Cats ancestors are animals in wildlife, who are hunting alone and not in groups. Jedoch habe ich ein viel stärkeres Argument dafür, dass cats are very independent.',
                                   'message': '4 weitere Teilnehmer/innen mit dieser Meinung.'}},
                    'title': 'Reaktionen zu: Ich akzeptiere, dass The city should reduce the number of street festivals, weil Reducing the number of street festivals can save up to $50.000 a year'}

        self.assertEqual(opinion.get_user_and_opinions_for_argument([31, 30]), response)
