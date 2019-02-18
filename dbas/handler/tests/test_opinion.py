from dbas.handler.opinion import get_user_and_opinions_for_argument, get_user_with_same_opinion_for_statements, \
    get_user_with_same_opinion_for_premisegroups_of_args, get_user_with_same_opinion_for_argument, \
    get_user_with_opinions_for_attitude
from dbas.tests.utils import TestCaseWithConfig


class OpinionHandlerTests(TestCaseWithConfig):
    def test_get_user_and_opinions_for_argument(self):
        lang = 'en'
        main_page = 'url'

        for uid in [11, 12, 13]:
            response = get_user_and_opinions_for_argument(argument_uid=uid,
                                                          db_user=self.user_tobi,
                                                          lang=lang,
                                                          main_page=main_page,
                                                          path='')
            self.verify_structure_of_statement_premisegroup_argument_dictionary(response)

    def test_get_user_with_same_opinion_for_statements(self):
        lang = 'en'
        main_page = 'url'

        for uid in [1, 2, 3]:
            response = get_user_with_same_opinion_for_statements(statement_uids=[uid],
                                                                 is_supportive=True,
                                                                 db_user=self.user_tobi,
                                                                 lang=lang,
                                                                 main_page=main_page)
            self.verify_structure_of_statement_premisegroup_argument_dictionary(response)

    def test_get_user_with_same_opinion_for_premisegroups(self):
        lang = 'en'
        main_page = 'url'

        for uid in [1, 2, 61, 62]:
            response = get_user_with_same_opinion_for_premisegroups_of_args(argument_uids=[uid],
                                                                            db_user=self.user_tobi,
                                                                            lang=lang,
                                                                            main_page=main_page)
            self.verify_structure_of_statement_premisegroup_argument_dictionary(response)

    def test_get_user_with_same_opinion_for_argument(self):
        lang = 'en'
        main_page = 'url'

        # correct argument id
        response_correct_id = get_user_with_same_opinion_for_argument(argument_uid=1, db_user=self.user_tobi,
                                                                      lang=lang, main_page=main_page)
        self.verify_structure_of_user_dictionary_for_argument(response_correct_id)

        response_correct_id2 = get_user_with_same_opinion_for_argument(argument_uid=62, db_user=self.user_tobi,
                                                                       lang=lang, main_page=main_page)
        self.verify_structure_of_user_dictionary_for_argument(response_correct_id2)

        # wrong id
        response_wrong_id = get_user_with_same_opinion_for_argument(argument_uid=0, db_user=self.user_tobi,
                                                                    lang=lang, main_page=main_page)
        map(lambda x: self.assertEqual(x, None), response_wrong_id.items())

        response_wrong_id2 = get_user_with_same_opinion_for_argument(argument_uid=None, db_user=self.user_tobi,
                                                                     lang=lang, main_page=main_page)
        map(lambda x: self.assertEqual(x, None), response_wrong_id2.items())

    def test_get_user_with_opinions_for_attitude(self):
        lang = 'en'
        main_page = 'url'

        # correct statement id
        response_correct_id = get_user_with_opinions_for_attitude(statement_uid=1, db_user=self.user_tobi,
                                                                  lang=lang, main_page=main_page)
        self.verify_structure_of_attitude_dictionary(response_correct_id)
        response_correct_id2 = get_user_with_opinions_for_attitude(statement_uid=74, db_user=self.user_tobi,
                                                                   lang=lang, main_page=main_page)
        self.verify_structure_of_attitude_dictionary(response_correct_id2)

        # wrong id
        response_wrong_id = get_user_with_opinions_for_attitude(statement_uid=0, db_user=self.user_tobi, lang=lang,
                                                                main_page=main_page)
        self.assertEqual(response_wrong_id['text'], None)
        response_wrong_id2 = get_user_with_opinions_for_attitude(statement_uid=None, db_user=self.user_tobi,
                                                                 lang=lang, main_page=main_page)
        self.assertEqual(response_wrong_id2['text'], None)

    def test_verify_text_includes_point_of_view(self):
        lang = 'en'
        main_page = 'url'
        path = 'http://0.0.0.0:4284/discuss/cat-or-dog/reaction/2/undermine/16?history=attitude/2-justify/2/agree'

        response = get_user_and_opinions_for_argument(argument_uid=11,
                                                      db_user=self.user_tobi,
                                                      lang=lang,
                                                      main_page=main_page,
                                                      path=path)
        self.assertTrue("my point of view" in response["opinions"][3]["text"])
        for opinion in response["opinions"]:
            self.assertFalse(">reason<" in opinion["text"])

    def test_verify_text_generation_handling_dontknow(self):
        lang = 'en'
        main_page = 'url'
        path = 'https://dbas.cs.uni-duesseldorf.de/discuss/town-has-to-cut-spending/justify/127/dontknow?history=/attitude/11'

        response = get_user_and_opinions_for_argument(argument_uid=11,
                                                      db_user=self.user_tobi,
                                                      lang=lang,
                                                      main_page=main_page,
                                                      path=path)
        self.assertTrue(">reason<" in response["opinions"][2]["text"])
        for opinion in response["opinions"]:
            self.assertFalse("my point of view" in opinion["text"])

    def verify_structure_of_argument_dictionary(self, response):
        # test structure of dictionary

        self.assertIn('opinions', response)
        self.assertIn('title', response)

        # test structure of ...
        # ... value of key 'opinions'
        undermine = 0
        support = 1
        undercut = 2
        rebut = 3

        # ... value of key 'attack_type' in 'opinions'
        self.assertIn('users', response['opinions'][undermine])
        self.assertIn('message', response['opinions'][support])
        self.assertIn('text', response['opinions'][undercut])
        self.assertIn('seen_by', response['opinions'][rebut])

        # wrong structure
        self.assertNotIn('', response)
        self.assertNotIn('opinion', response)

        return True

    def verify_structure_of_statement_premisegroup_argument_dictionary(self, response):
        self.assertIn('opinions', response)
        self.assertIn('title', response)

        # test structure of ...
        # ... value of key 'opinions'
        self.assertIn('text', response['opinions'][0])
        self.assertIn('message', response['opinions'][0])
        self.assertIn('users', response['opinions'][0])
        self.assertIn('seen_by', response['opinions'][0])

        # ... value of key 'users' in 'opinions'
        if len(response['opinions'][0]['users']) > 0:
            self.assertIn('nickname', response['opinions'][0]['users'][0])

        # wrong structure
        self.assertNotIn('', response)
        self.assertNotIn('uid', response)

    def verify_structure_of_user_dictionary_for_argument(self, response):
        self.assertIn('opinions', response)
        self.assertIn('title', response)

        # test structure of ...
        # ... value of key 'opinions'
        self.assertIn('uid', response['opinions'])
        self.assertIn('text', response['opinions'])
        self.assertIn('message', response['opinions'])
        self.assertIn('users', response['opinions'])

        # wrong structure
        self.assertNotIn('', response)
        self.assertNotIn('uid', response)

    def verify_structure_of_attitude_dictionary(self, response):
        # correct structure
        self.assertIn('text', response)
        self.assertIn('agree', response)
        self.assertIn('disagree', response)
        self.assertIn('users', response['agree'])
        self.assertIn('text', response['agree'])
        self.assertIn('users', response['disagree'])
        self.assertIn('text', response['disagree'])
        self.assertIn('title', response)
        self.assertIn('seen_by', response)

        # wrong structure
        self.assertNotIn('', response)
        self.assertNotIn('text ', response)
