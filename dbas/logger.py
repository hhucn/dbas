import logging

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


def logger(who, when, what, info=False, warn=False, error=False, debug=True):
	"""
	Log for the console and logfile on disk. Logged format: [who.upper()] when <what>
	:param who: which class
	:param when: which method
	:param what: what mesage
	:return: None
	:param info: Boolean, default False
	:param warn: Boolean, default False
	:param error: Boolean, default False
	:param debug: Boolean, default True
	:return:
	"""
	logger = logging.getLogger(__name__)
	if info:
		logger.info('[' + who.upper() + '] ' + when + ': ' + what)
	elif warn:
		logger.warn('[' + who.upper() + '] ' + when + ': ' + what)
	elif error:
		logger.error('[' + who.upper() + '] ' + when + ': ' + what)
	else:
		logger.debug('[' + who.upper() + '] ' + when + ': ' + what)

