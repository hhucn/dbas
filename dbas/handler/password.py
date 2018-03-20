"""
Class for handling passwords.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

import transaction
from cryptacular.bcrypt import BCRYPTPasswordManager
from pyramid_mailer import Mailer
from sqlalchemy import func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Language
from dbas.handler.email import send_mail
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


def request_password(email: str, mailer: Mailer, _tn: Translator):
    """
    Create new hashed password and send mail..

    :param email: Mail-address which should be queried
    :param mailer: pyramid Mailer
    :param _tn: Translator
    :return: dict with info about mailing
    """
    success = ''
    error = ''
    info = ''

    db_user = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    if db_user:
        pwd = get_rnd_passwd()
        hashedpwd = get_hashed_password(pwd)

        # set the hashed one
        db_user.password = hashedpwd
        DBDiscussionSession.add(db_user)
        transaction.commit()

        db_language = DBDiscussionSession.query(Language).get(db_user.settings.lang_uid)

        body = _tn.get(_.nicknameIs) + db_user.nickname + '\n'
        body += _tn.get(_.newPwdIs) + pwd + '\n\n'
        body += _tn.get(_.newPwdInfo)
        subject = _tn.get(_.dbasPwdRequest)
        reg_success, message = send_mail(mailer, subject, body, email, db_language.ui_locales)

        if reg_success:
            success = message
        else:
            error = message
    else:
        logger('user_password_request', 'Mail unknown')
        info = _tn.get(_.emailUnknown)
    return {'success': success, 'error': error, 'info': info}
