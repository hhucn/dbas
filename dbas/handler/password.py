"""
Class for handling passwords.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
import random

import bcrypt
import transaction
from pyramid_mailer import Mailer
from sqlalchemy import func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Language
from dbas.handler.email import send_mail
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
def get_rnd_passwd(pw_len: int = 10) -> str:
    """
    Generates a password with the length of 10 out of ([a-z][A-Z][+-*/#!*?])+

    :param pw_len:
    :return:
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    upperalphabet = alphabet.upper()
    symbols = '+-*/#!*?'
    pwlist = []

    for i in range(pw_len // 3):
        pwlist.append(alphabet[random.randrange(len(alphabet))])
        pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
        pwlist.append(str(random.randrange(10)))
    for i in range(pw_len - len(pwlist)):
        pwlist.append(alphabet[random.randrange(len(symbols))])

    random.shuffle(pwlist)
    pwstring = ''.join(pwlist)

    return pwstring


def get_hashed_password(password: str):
    """
    Returns hashed password

    :param password: String
    :return: String
    """
    # hashpw returns bytes. they have to be decoded in order to be stored as 'text' in the db
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode("utf-8")


def request_password(email: str, mailer: Mailer, _tn: Translator):
    """
    Create new hashed password and send mail..

    :param email: Mail-address which should be queried
    :param mailer: pyramid Mailer
    :param _tn: Translator
    :return: dict with info about mailing
    """

    db_user = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    if not db_user:
        LOG.debug("Mail unknown")
        return {
            'success': False,
            'message': _tn.get(_.emailUnknown)
        }

    rnd_pwd = get_rnd_passwd()
    hashed_pwd = get_hashed_password(rnd_pwd)

    # set the hashed one
    db_user.password = hashed_pwd
    DBDiscussionSession.add(db_user)
    transaction.commit()

    db_language = DBDiscussionSession.query(Language).get(db_user.settings.lang_uid)

    body = _tn.get(_.nicknameIs) + db_user.nickname + '\n'
    body += _tn.get(_.newPwdIs) + rnd_pwd + '\n\n'
    body += _tn.get(_.newPwdInfo)
    subject = _tn.get(_.dbasPwdRequest)
    success, success_message, message = send_mail(mailer, subject, body, email, db_language.ui_locales)

    return {
        'success': success,
        'message': success_message
    }
