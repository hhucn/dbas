"""
Utility functions for tests, which are used in multiple namespaces.
"""
from cornice import Errors
from pyramid.testing import DummyRequest
from pyramid_mailer.mailer import DummyMailer


def construct_dummy_request(json_body=None) -> DummyRequest:
    """
    Creates a Dummy-Request. Optionally takes a json_body, which can directly be injected into the request.

    :param json_body: dict
    :return: DummyRequest
    :rtype: DummyRequest
    """
    if json_body is None:
        json_body = dict()
    return DummyRequest(json_body=json_body, validated={}, errors=Errors(), mailer=DummyMailer,
                        cookies={'_LOCALE_': 'en'})
