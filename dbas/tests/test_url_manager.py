import unittest


class UrlManagerTests(unittest.TestCase):
    @staticmethod
    def __get_target_class():
        from dbas.url_manager import UrlManager
        return UrlManager

    def __make_one(self, *args, **kw):
        return self.__get_target_class()(*args, **kw)

    def test_init(self):
        url1 = self.__make_one(application_url='application_url',
                               slug='',
                               for_api=True,
                               history='')
        url2 = self.__make_one(application_url='application_url/',
                               slug='cat-or-dog',
                               for_api=False,
                               history='attitude/35')
        # Test whether backslash is added, if application_url does not end with it.
        self.assertEqual(url1.url, 'application_url/')
        # Test whether empty String is added, if application_url ends with backslash.
        self.assertEqual(url2.url, 'application_url/')

        # Test if 'discuss/' is attached in discussion_url.
        self.assertEqual(url1.discussion_url, 'application_url/discuss/')

        # Test if 'api/' is assigned to variable 'api_url'.
        self.assertEqual(url1.api_url, 'api/')

        # Test empty string.
        self.assertEqual(url1.slug, '')
        # Test string.
        self.assertEqual(url2.slug, 'cat-or-dog')

        # Verify variable 'for_api' is assigned to expected boolean value.
        self.assertEqual(url1.for_api, True)
        self.assertEqual(url2.for_api, False)

        # Test empty string.
        self.assertEqual(url1.history, '')
        # Test string.
        self.assertEqual(url2.history, 'attitude/35')

        # Test whether 'None' is returned.
        self.assertEqual(url1.__init__('application_url/'), None)

    def test_get_url(self):
        url1 = self.__make_one(application_url='application_url',
                               for_api=True)
        url2 = self.__make_one(application_url='application_url',
                               for_api=False)

        response_for_api_true = url1.get_url(path='discuss')
        # Verify that, if 'for_api' is 'True', the path is returned.
        self.assertEqual(response_for_api_true, 'discuss')

        response_for_api_false = url2.get_url(path='discuss')
        # Verify that, if 'for_api' is 'False', the path with the 'application_url' as prefix is returned.
        self.assertEqual(response_for_api_false, 'application_url/discuss')

    def test_get_404(self):
        url = self.__make_one('application_url')

        response_array_true = url.get_404(params=['discuss', '123', '.(%', 'A1('],
                                          is_param_error=True)
        # If an element of array 'params' is not empty:
        # verify that, if there is no character '?' in array 'params' and value of 'is_param_error' is 'True',
        # the elements are put together to an url, separated with backslash and '?param_error=true' is attached in url.
        self.assertEqual(response_array_true, 'application_url/404/discuss/123/.(%/A1(?param_error=true')

        response_array_false = url.get_404(params=['discuss', '123', '.(%', 'A1('],
                                           is_param_error=False)
        # Verify that, if there is no character '?' in array 'params' and value of 'is_param_error' is 'False', the url
        # is returned.
        self.assertEqual(response_array_false, 'application_url/404/discuss/123/.(%/A1(')

        response_question_mark_true = url.get_404(params=['?discuss'],
                                                  is_param_error=True)
        # Verify that, if there is a character '?' in array 'params' and value of 'is_param_error' is 'True',
        # '&param_error=true' is attached in url.
        self.assertEqual(response_question_mark_true, 'application_url/404/?discuss&param_error=true')

        response_question_mark_false = url.get_404(params=['?discuss'],
                                                   is_param_error=False)
        # Verify that, if there is a character '?' in array 'params' and value of 'is_param_error' is 'False', the url
        # is returned.
        self.assertEqual(response_question_mark_false, 'application_url/404/?discuss')

        response_empty_true = url.get_404(params=['discuss', '', '123'],
                                          is_param_error=True)
        # Verify that if an element of array 'params' is empty and value of 'is_param_error' is 'True',
        # there is no backslash between empty element and next element, '?param_error=true' is attached in url.
        self.assertEqual(response_empty_true, 'application_url/404/discuss/123?param_error=true')

        response_empty_false = url.get_404(params=['discuss', '', '123'],
                                           is_param_error=False)
        # Verify that if an element of array 'params' is empty and value of 'is_param_error' is 'False',
        # there is no backslash between empty element and next element.
        self.assertEqual(response_empty_false, 'application_url/404/discuss/123')

    def test_get_slug_url(self):
        url = self.__make_one(application_url='application_url',
                              slug='cat-or-dog')

        response_as_location_href_true = url.get_slug_url(as_location_href=True)
        # Verify that, if 'as_location_href' is 'True', 'discussion_url/slug' with 'location.href=' as prefix is
        # returned.
        self.assertEqual(response_as_location_href_true, 'location.href="application_url/discuss/cat-or-dog"')

        response_as_location_href_false = url.get_slug_url(as_location_href=False)
        # Verify that, if 'as_location_href' is 'False', 'discussion_url/slug' is returned.
        self.assertEqual(response_as_location_href_false, 'application_url/discuss/cat-or-dog')

    def test_get_url_for_statement_attitude(self):
        url = self.__make_one(application_url='application_url',
                              slug='cat-or-dog')

        response_string_true = url.get_url_for_statement_attitude(as_location_href=True,
                                                                  statement_uid=123)
        # Verify that, if 'as_location_href' is 'True' and 'statement_uid' is not empty,
        # '{discussion_url}/{slug}/attitude/{statement_uid}' with 'location.href=' as prefix is returned.
        self.assertEqual(response_string_true, 'location.href="application_url/discuss/cat-or-dog/attitude/123"')

        response_empty_string_false = url.get_url_for_statement_attitude(as_location_href=False,
                                                                         statement_uid='')
        # Verify that, if 'as_location_href' is 'False' and 'statement_uid' is empty,
        # '{discussion_url}/{slug}/attitude/' is returned.
        self.assertEqual(response_empty_string_false, 'application_url/discuss/cat-or-dog/attitude/')

        response_negative_uid_true = url.get_url_for_statement_attitude(as_location_href=True,
                                                                        statement_uid=-123)
        self.assertEqual(response_negative_uid_true, 'location.href="application_url/discuss/cat-or-dog/attitude/-123"')

    def test_get_url_for_justifying_statement(self):
        url = self.__make_one(application_url='application_url',
                              slug='cat-or-dog')

        response_string_true = url.get_url_for_justifying_statement(as_location_href=True,
                                                                    statement_uid=123,
                                                                    mode='t')
        # Verify that, if 'as_location_href' is 'True', 'statement_uid' and 'mode' are not empty,
        # 'location.href="{discussion_url}/{slug}/justify/{statement_or_arg_id}/{mode}"' is returned.
        self.assertEqual(response_string_true, 'location.href="application_url/discuss/cat-or-dog/justify/123/t"')

        response_empty_string_false = url.get_url_for_justifying_statement(as_location_href=False,
                                                                           statement_uid='',
                                                                           mode='')
        # Verify that, if 'as_location_href' is 'False', 'statement_uid' and 'mode' are empty,
        # '{discussion_url}/{slug}/justify//' is returned.
        self.assertEqual(response_empty_string_false, 'application_url/discuss/cat-or-dog/justify//')

    def test_get_url_for_justifying_argument(self):
        url = self.__make_one(application_url='application_url',
                              slug='cat-or-dog')

        response_no_additional_id_true = url.get_url_for_justifying_argument(as_location_href=True,
                                                                             argument_uid=123,
                                                                             mode='t',
                                                                             attitude='attitude',
                                                                             additional_id=-1)
        # Verify that, if 'additional_id' is '-1' and 'as_location_href' is 'True',
        # 'location.href="{discussion_url}/{slug}/justify/{argument_uid}/{mode}/{attitude}"' is returned.
        self.assertEqual(response_no_additional_id_true,
                         'location.href="application_url/discuss/cat-or-dog/justify/123/t/attitude"')

        response_additional_id_false = url.get_url_for_justifying_argument(as_location_href=False,
                                                                           argument_uid=123,
                                                                           mode='t',
                                                                           attitude='attitude',
                                                                           additional_id=30)
        # Verify that, if 'additional_id' is not equal '-1' and 'as_location_href' is 'False',
        # '{discussion_url}/{slug}/justify/{argument_uid}/{mode}/{attitude}/{attitude_uid}"' is returned.
        self.assertEqual(response_additional_id_false, 'application_url/discuss/cat-or-dog/justify/123/t/attitude/30')

    def test_get_url_for_reaction_on_argument(self):
        url = self.__make_one(application_url='application_url',
                              slug='cat-or-dog')

        response_as_location_href_true = url.get_url_for_reaction_on_argument(as_location_href=True,
                                                                              argument_uid=123,
                                                                              mode='rebut',
                                                                              confrontation_argument=35)
        # Verify that, if 'as_location_href' is 'True',
        # 'location.href="{discussion_url}/{slug}/reaction/{argument_uid}/{mode}/{confrontation_argument}"' is returned.
        self.assertEqual(response_as_location_href_true,
                         'location.href="application_url/discuss/cat-or-dog/reaction/123/rebut/35"')

        response_as_location_href_false = url.get_url_for_reaction_on_argument(as_location_href=False,
                                                                               argument_uid=0,
                                                                               mode='undercut',
                                                                               confrontation_argument=0)
        # Verify that, if 'as_location_href' is 'False',
        # '{discussion_url}/{slug}/reaction/{argument_uid}/{mode}/{confrontation_argument}' is returned.
        self.assertEqual(response_as_location_href_false, 'application_url/discuss/cat-or-dog/finish/0')

    def test_get_url_for_choosing_premisegroup(self):
        url = self.__make_one(application_url='application_url',
                              slug='cat-or-dog')

        response_true = url.get_url_for_choosing_premisegroup(as_location_href=True,
                                                              is_argument=True,
                                                              is_supportive=True,
                                                              statement_or_argument_id=20,
                                                              pgroup_id_list=[1, 2, 3])
        # Verify that, if 'as_location_href', 'is_argument', 'is_supportive' are 'True' and length of array
        # 'pgroup_id_list' is greater than 0, the url 'location.href="{discussion-url}/{slug}/choose/{is_argument}/{
        # is_supportive}/{statement_or_argument_id}"' and the elements of array 'pgroup_id_list' are put together,
        # separated with backslash, and are attached in url.
        self.assertEqual(response_true, 'location.href="application_url/discuss/cat-or-dog/choose/t/t/20/1/2/3"')

        response_false = url.get_url_for_choosing_premisegroup(as_location_href=False,
                                                               is_argument=False,
                                                               is_supportive=False,
                                                               statement_or_argument_id=20,
                                                               pgroup_id_list='')
        # Verify that, if 'as_location_href', 'is_argument', 'is_supportive' are 'False' and length of array
        # 'pgroup_id_list' is equal 0, '{discussion-url}/{slug}/choose/{is_argument}/{is_supportive}/{
        # statement_or_argument_id}' is returned.
        self.assertEqual(response_false, 'application_url/discuss/cat-or-dog/choose/f/f/20')

    def test_get_url_for_new_argument(self):
        url1 = self.__make_one(application_url='application_url',
                               for_api=True,
                               slug='cat-or-dog',
                               history='attitude/4')
        url2 = self.__make_one(application_url='application_url',
                               for_api=False,
                               slug='cat-or-dog',
                               history='attitude/4')

        api = 'api/cat-or-dog/finish/10?history=attitude/4'
        dbas = 'location.href="application_url/discuss/cat-or-dog/finish/10?history=attitude/4"'

        self.assertEqual(api, url1.get_url_for_new_argument([10], True))
        self.assertEqual(dbas, url2.get_url_for_new_argument([10], True))
