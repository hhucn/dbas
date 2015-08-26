import logging

log = logging.getLogger(__name__)

def logger(who, when, what):
	log.debug('[' + who.upper() + '] ' + when + ' <' + what + '>')