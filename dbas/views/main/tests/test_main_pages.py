import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.views.main.rendered import imprint, news, privacy, experiment, index, faq, docs, health


class MainImprintViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = imprint(request)
        verify_dictionary_of_view(response)


class MainFieldexperimentViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = experiment(request)
        verify_dictionary_of_view(response)


class MainNewsViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = news(request)
        verify_dictionary_of_view(response)


class MainPrivacyViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = privacy(request)
        verify_dictionary_of_view(response)


class MainPageViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = index(request)
        verify_dictionary_of_view(response)


class MainFaqViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = faq(request)
        verify_dictionary_of_view(response)


class MainDocsViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = docs(request)
        verify_dictionary_of_view(response)


class MainHealthViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = health(request)
        self.assertEqual(200, response.status_code)
