"""
Core validation class for validators.
"""
import logging
from typing import Tuple, List, Callable, Optional

from cornice import Errors
from cornice.util import json_error
from pyramid.request import Request

from dbas.validators.lib import add_error

LOG = logging.getLogger(__name__)


def spec_keyword_in_json_body(*keywords: Tuple[type, str, Callable[[any], bool]]):
    def valid_keywords(request: Request, **_kwargs):
        error_occured = False
        for (ktype, keyword, predicate) in keywords:
            value = request.json_body.get(keyword)
            if value is not None and predicate(value, ktype):
                request.validated[keyword] = value
            elif value is None:
                add_error(request, 'Parameter {} is missing in body'.format(keyword))
                error_occured = True
            else:
                add_error(request,
                          'Parameter {} failed spec. Value: {}.'.format(keyword, value))
                error_occured = True
        return not error_occured

    return valid_keywords


def has_keywords_in_json_path(*keywords: Tuple[str, type]):
    """
    Verify that specified keywords exist in the request.json_body.

    :param keywords: tuple of the field's name and its expected type.
    :return:
    """
    validator_keywords = [[ktype, keyword, lambda v, k: isinstance(v, k)] for [keyword, ktype] in keywords]
    return spec_keyword_in_json_body(*validator_keywords)


def has_keywords_in_path(*keywords: Tuple[str, type], location='matchdict'):
    """
    Verify that specified keywords exist in the request object.

    :param keywords: tuple of keys and their expected types in request
    :param location: specify dictionary in request object, where the data is stored
    :return:
    """

    def valid_keywords(request: Request, **_kwargs):
        error_occured = False
        for (keyword, ktype) in keywords:
            request_attribute: dict = getattr(request, location)
            value = request_attribute.get(keyword)
            if value is not None and isinstance(value, ktype):
                request.validated[keyword] = value
            elif value is not None:
                if ktype in [int, float]:
                    try:
                        request.validated[keyword] = ktype(value)
                        continue
                    except ValueError:
                        pass
                elif ktype is bool and value.lower() in ['true', 'false']:
                    request.validated[keyword] = value.lower() == 'true'
                    continue

                add_error(request, 'Parameter {} has wrong type'.format(keyword),
                          '{} is {}, expected {}'.format(keyword, type(value), ktype))
                error_occured = True
            else:
                add_error(request, 'Parameter {} is missing in {}'.format(keyword, location))
                error_occured = True
        return not error_occured

    return valid_keywords


def has_maybe_keywords(*keywords):
    """
    Check if parameter exists. If not, provide fallback value.

    :param keywords: 3-tuple of keys, their expected types in request.json_body and a default value
    :return:
    """

    def valid_keywords(request):
        error_occured = False
        for (keyword, ktype, kdefault) in keywords:
            value = request.json_body.get(keyword)
            if value is not None and isinstance(value, ktype):
                request.validated[keyword] = value
            elif value is None:
                request.validated[keyword] = kdefault
            else:
                add_error(request, 'Parameter {} has wrong type'.format(keyword),
                          '{} is {}, expected {}'.format(keyword, type(keyword), ktype))
                error_occured = True
        return not error_occured

    return valid_keywords


class validate(object):
    """
    Applies all validators to this function.
    If one of the validators adds an error, the function will not be called.
    In this situation a response is given with a json body, containing all errors from all validators.

    Decorate a function like this

    .. code-block:: python

        @validate(validators=(check_for_user, check_for_issue, )
        def my_view(request)
    """

    def __init__(self, *validators: List[Callable[[Request], Optional[bool]]]):
        self.validators: List[Callable[[Request], Optional[bool]]] = validators

    def __call__(self, func: Callable[[Request], dict]):
        def inner(request: Request):
            if not hasattr(request, 'validated'):
                setattr(request, 'validated', {})
            if not hasattr(request, 'errors'):
                setattr(request, 'errors', Errors())
            if not hasattr(request, 'info'):
                setattr(request, 'info', {})

            for validator in self.validators:
                validator(request=request)

            if len(request.errors) > 0:
                return json_error(request)
            return func(request)

        return inner
