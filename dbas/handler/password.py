"""
Class for handling passwords.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

import transaction
from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy import func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Settings, Language
from dbas.helper.email import send_mail
from dbas.helper.language import get_language_from_cookie
from dbas.lib import escape_string
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
def get_rnd_passwd():
    """
    Generates a password with the length of 10 out of ([a-z][A-Z][+-*/#!*?])+

    :return: String
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    upperalphabet = alphabet.upper()
    symbols = '+-*/#!*?'
    pw_len = 8
    pwlist = []

    for i in range(pw_len // 3):
        pwlist.append(alphabet[random.randrange(len(alphabet))])
        pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
        pwlist.append(str(random.randrange(10)))
    for i in range(pw_len - len(pwlist)):
        pwlist.append(alphabet[random.randrange(len(alphabet))])

    pwlist.append(symbols[random.randrange(len(symbols))])
    pwlist.append(symbols[random.randrange(len(symbols))])

    random.shuffle(pwlist)
    pwstring = ''.join(pwlist)

    return pwstring


def get_hashed_password(password):
    """
    Returns hashed password

    :param password: String
    :return: String
    """
    manager = BCRYPTPasswordManager()
    return manager.encode(password)


def request_password(request):
    """
    Request for a new password

    :param request: current webserver request
    :param ui_locales: Language.ui_locales
    :return: Success-, Error-, Info-String
    """
    success = ''
    error = ''
    info = ''
    ui_locales = request.params['lang'] if 'lang' in request.params else get_language_from_cookie(request)

    _t = Translator(ui_locales)
    email = escape_string(request.params['email'])
    db_user = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()

    # does the user exists?
    if db_user:
        # get password and hashed password
        pwd = get_rnd_passwd()
        hashedpwd = get_hashed_password(pwd)

        # set the hashed one
        db_user.password = hashedpwd
        DBDiscussionSession.add(db_user)
        transaction.commit()

        db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
        db_language = DBDiscussionSession.query(Language).get(db_settings.lang_uid)

        body = _t.get(_.nicknameIs) + db_user.nickname + '\n'
        body += _t.get(_.newPwdIs) + pwd + '\n\n'
        body += _t.get(_.newPwdInfo)
        subject = _t.get(_.dbasPwdRequest)
        reg_success, message = send_mail(request, subject, body, email, db_language.ui_locales)

        if reg_success:
            success = message
        else:
            error = message
    else:
        logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
        info = _t.get(_.emailUnknown)

    return success, error, info
