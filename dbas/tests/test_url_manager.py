import unittest

from dbas.url_manager import UrlManager


class UrlManagerTests(unittest.TestCase):

    def test_get_404(self):
        inst = UrlManager('application_url')

        responseArrayTrue = inst.get_404(['discuss', '123', '.(%', 'A1('], True)
        self.assertEqual(responseArrayTrue, 'application_url/404/discuss/123/.(%/A1(?param_error=true')

        responseArrayFalse = inst.get_404(['discuss', '123', '.(%', 'A1('], False)
        self.assertEqual(responseArrayFalse, 'application_url/404/discuss/123/.(%/A1(')

        responseQuestionMarkTrue = inst.get_404(['?discuss'], True)
        self.assertEqual(responseQuestionMarkTrue, 'application_url/404/?discuss&param_error=true')

        responseQuestionMarkFalse = inst.get_404(['?discuss'], False)
        self.assertEqual(responseQuestionMarkFalse, 'application_url/404/?discuss')

        responseEmptyTrue = inst.get_404(['discuss','','123'], True)
        self.assertEqual(responseEmptyTrue, 'application_url/404/discuss/123?param_error=true')

        responseEmptyFalse = inst.get_404(['discuss','','123'], False)
        self.assertEqual(responseEmptyFalse, 'application_url/404/discuss/123')

