from dbas.logger import logger
import requests

client_key = '6LdktxgUAAAAAHEyj-oKPWc1hYEXwt2diquujz-I'
server_key = '6LdktxgUAAAAAHLIXI_YAkCIIoUqsBjTLTzVeJ8x'


def validate_recaptcha(recaptcha):
    """
    Validates googles recaptcha

    :param recaptcha: Recaptcha
    :return:
    """
    logger('Recaptcha', 'validate_recaptcha', 'recaptcha ' + str(recaptcha))
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': server_key,
                                                                                   'response': recaptcha})
        json = r.json()
    except:
        logger('Recaptcha', 'validate_recaptcha', 'Unexpected error', error=True)
        return False, True

    logger('Recaptcha', 'validate_recaptcha', 'answer ' + str(json))
    error = False

    if 'error-codes' in json:
        if 'missing-input-secret' in json['error-codes']:
            logger('Recaptcha', 'validate_recaptcha', 'The secret parameter is missing.', error=True)
            error = True
        if 'invalid-input-secret' in json['error-codes']:
            logger('Recaptcha', 'validate_recaptcha', 'The secret parameter is invalid or malformed.', error=True)
            error = True
        if 'missing-input-response' in json['error-codes']:
            logger('Recaptcha', 'validate_recaptcha', 'The response parameter is missing.', error=True)
            error = True
        if 'invalid-input-response' in json['error-codes']:
            logger('Recaptcha', 'validate_recaptcha', 'The response parameter is invalid or malformed.', error=True)
            error = True

    return json['success'], error