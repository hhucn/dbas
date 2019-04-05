import logging
import os

import ldap

from dbas.strings.keywords import Keywords as _

LOG = logging.getLogger(__name__)


def verify_ldap_user_data(nickname, password, _tn):
    """
    Tries to authenticate the user with nickname and password

    :param nickname: users nickname for LDAP
    :param password: users password for LDAP
    :param _tn: Translator
    :return: [firstname, lastname, gender, email] on success else None
    """
    try:
        server = os.environ.get('HHU_LDAP_SERVER', None)
        base = os.environ.get('HHU_LDAP_BASE', None)
        scope = os.environ.get('HHU_LDAP_ACCOUNT_SCOPE', None)
        filterf = os.environ.get('HHU_LDAP_ACCOUNT_FILTER', None)
        firstname = os.environ.get('HHU_LDAP_ACCOUNT_FIRSTNAME', None)
        lastname = os.environ.get('HHU_LDAP_ACCOUNT_LAST', None)
        title = os.environ.get('HHU_LDAP_ACCOUNT_TITLE', None)
        email = os.environ.get('HHU_LDAP_ACCOUNT_EMAIL', None)

        if any(el is None for el in [server, base, scope, filterf, firstname, lastname, title, email]):
            LOG.debug("Environment Keys are None")
            return {'error': _tn.get(_.internalKeyError) + ' ' + _tn.get(_.pleaseTryAgainLaterOrContactUs)}

        server = server.replace('\'', '')
        base = base.replace('\'', '')
        scope = scope.replace('\'', '')
        filterf = filterf.replace('\'', '')
        firstname = firstname.replace('\'', '')
        lastname = lastname.replace('\'', '')
        title = title.replace('\'', '')
        email = email.replace('\'', '')

        LOG.debug("Using LDAP server: '%s')", server)
        ldaps = ldap.initialize(server)
        ldaps.set_option(ldap.OPT_NETWORK_TIMEOUT, 5.0)
        LOG.debug(
            "search for user {nickname}{scope} with filter {filterf} on {base}".format(nickname=nickname, scope=scope,
                                                                                       filterf=filterf, base=base))
        ldaps.simple_bind_s(nickname + scope, password)
        result = ldaps.search_s(base, ldap.SCOPE_SUBTREE, filterf.format(nickname=nickname),
                                attrlist=[firstname, lastname, title, email])

        if not result:
            LOG.debug("ldap user {nickname} not allowed by {filterf}".format(nickname=nickname, filterf=filterf))
            data = {
                'error': "Leider ist es dir nicht erlaubt, dich einzuloggen. Wenn du meinst, das ist falsch, dann melde dich bei uns!"
            }  # TODO translate
            return data

        user = result[0][1]

        firstname = user[firstname][0].decode('utf-8')
        lastname = user[lastname][0].decode('utf-8')
        title = user[title][0].decode('utf-8')
        gender = 'm' if 'Herr' in title else 'f' if 'Frau' in title else 'n'
        email = user[email][0].decode('utf-8')
        LOG.debug("success")

        data = {
            'firstname': firstname,
            'lastname': lastname,
            'gender': gender,
            'email': email,
            'error': False
        }
        return data

    except ldap.INVALID_CREDENTIALS as e:
        LOG.debug("ldap credetial error: %s", e)
        data = {'error': _tn.get(_.userPasswordNotMatch)}
        return data

    except ldap.SERVER_DOWN as e:
        LOG.debug("can't reach server within 5s: %s", e)
        data = {'error': _tn.get(_.serviceNotAvailable) + '. ' + _tn.get(_.pleaseTryAgainLaterOrContactUs)}
        return data

    except ldap.OPERATIONS_ERROR as e:
        LOG.debug("OPERATIONS_ERROR: %s", e)
        data = {'error': _tn.get(_.userPasswordNotMatch)}
        return data
