"""
Validate database-related models and objects.
"""

from admin.lib import table_mapper
from dbas.database import DBDiscussionSession
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.lib import add_error, escape_if_string


def valid_table_name(request):
    """

    :param request:
    :return:
    """
    table_name = escape_if_string(request.json_body, 'table')
    if table_name and table_name.lower() in table_mapper:
        request.validated['table'] = table_name
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid table name', _tn.get(_.invalidTableName))
        return False


def valid_database_model(keyword, model):
    def valid_model(request):
        uid = request.json_body.get(keyword)
        db_something = DBDiscussionSession.query(model).get(uid) if is_integer(uid) and model else None
        if db_something:
            request.validated['db_model'] = db_something
            return True
        else:
            add_error(request, 'Database has no row {} of {}'.format(uid, model))
            return False

    return valid_model
