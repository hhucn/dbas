import unittest

class UrlManagerTests(unittest.TestCase):

    def _getTargetClass(self):
        from dbas.url_manager import UrlManager
        return UrlManager

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_init(self):
        url1 = self._makeOne(application_url = 'application_url',
                             slug = '',
                             for_api = True,
                             history = '')
        url2 = self._makeOne(application_url = 'application_url/',
                             slug = 'cat-or-dog',
                             for_api = False,
                             history = 'Abc123/()')

        self.assertEqual(url1.url, 'application_url/')
        self.assertEqual(url2.url, 'application_url/')

        self.assertEqual(url1.discussion_url, 'application_url/discuss/')

        self.assertEquals(url1.api_url, 'api/')

        self.assertEqual(url1.slug, '')
        self.assertEqual(url2.slug, 'cat-or-dog')

        self.assertEqual(url1.for_api, True)
        self.assertEqual(url2.for_api, False)

        self.assertEquals(url1.history, '')
        self.assertEquals(url2.history, 'Abc123/()')

        self.assertEqual(url1.__init__('application_url/'), None);


    def test_get_404(self):
        url = self._makeOne('application_url')

        responseArrayTrue = url.get_404(params = ['discuss', '123', '.(%', 'A1('],
                                        is_param_error = True)
        self.assertEqual(responseArrayTrue, 'application_url/404/discuss/123/.(%/A1(?param_error=true')

        responseArrayFalse = url.get_404(params = ['discuss', '123', '.(%', 'A1('],
                                         is_param_error = False)
        self.assertEqual(responseArrayFalse, 'application_url/404/discuss/123/.(%/A1(')

        responseQuestionMarkTrue = url.get_404(params = ['?discuss'],
                                               is_param_error = True)
        self.assertEqual(responseQuestionMarkTrue, 'application_url/404/?discuss&param_error=true')

        responseQuestionMarkFalse = url.get_404(params = ['?discuss'],
                                                is_param_error = False)
        self.assertEqual(responseQuestionMarkFalse, 'application_url/404/?discuss')

        responseEmptyTrue = url.get_404(params = ['discuss','','123'],
                                        is_param_error = True)
        self.assertEqual(responseEmptyTrue, 'application_url/404/discuss/123?param_error=true')

        responseEmptyFalse = url.get_404(params = ['discuss','','123'],
                                         is_param_error = False)
        self.assertEqual(responseEmptyFalse, 'application_url/404/discuss/123')

