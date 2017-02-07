from dbas.logger import logger


def verify_ldap_user_data(request, nickname, password):
    """

    :param nickname:
    :param password:
    :return:
    """
    import ldap

    try:
        r = request.registry.settings
        server = r['settings:ldap:server']
        base = r['settings:ldap:base']
        scope = r['settings:ldap:account.scope']
        filter = r['settings:ldap:account.filter']
        firstname = r['settings:ldap:account.firstname']
        lastname = r['settings:ldap:account.lastname']
        title = r['settings:ldap:account.title']
        email = r['settings:ldap:account.email']
        logger('ViewHelper', 'verify_ldap_user_data', 'parsed data')

        logger('ViewHelper', 'verify_ldap_user_data', 'ldap.initialize(\'' + server + '\')')
        l = ldap.initialize(server)
        l.set_option(ldap.OPT_NETWORK_TIMEOUT, 5.0)
        logger('ViewHelper', 'verify_ldap_user_data', 'simple_bind_s(\'' + nickname + scope + '\', \'***\')')
        l.simple_bind_s(nickname + scope, password)
        logger('ViewHelper', 'verify_ldap_user_data',
               'l.search_s(' + base + ', ldap.SCOPE_SUBTREE, (\'' + filter + '=' + nickname + '\'))[0][1]')
        user = l.search_s(base, ldap.SCOPE_SUBTREE, (filter + '=' + nickname))[0][1]

        firstname = user[firstname][0].decode('utf-8')
        lastname = user[lastname][0].decode('utf-8')
        title = user[title][0].decode('utf-8')
        gender = 'm' if 'Herr' in title else 'f' if 'Frau' in title else 'n'
        email = user[email][0].decode('utf-8')
        logger('ViewHelper', 'verify_ldap_user_data', 'success')

        return [firstname, lastname, gender, email]

    except ldap.INVALID_CREDENTIALS as e:
        logger('ViewHelper', 'verify_ldap_user_data', 'ldap credential error: ' + str(e))
        return None

    except ldap.SERVER_DOWN as e:
        logger('ViewHelper', 'verify_ldap_user_data', 'can\'t reach server within 5s: ' + str(e))
        return None

    except ldap.OPERATIONS_ERROR as e:
        logger('ViewHelper', 'verify_ldap_user_data', 'OPERATIONS_ERROR: ' + str(e))
        return None
