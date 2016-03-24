import logging
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


def logger(who, when, what, warn=False, error=False, debug=False):
	"""
	Log for the console and logfile on disk. Logged format: [who.upper()] when <what>
	:param who: which class
	:param when: which method
	:param what: what mesage
	:return: None
	:param warn: Boolean, default False
	:param error: Boolean, default False
	:param debug: Boolean, default False
	:return:
	"""
	info = not(warn or error or debug)

	logger = logging.getLogger(__name__)
	if info:
		logger.info('[' + who.upper() + '] ' + when + ': ' + what)
	if warn:
		logger.warn('[' + who.upper() + '] ' + when + ': ' + what)
	if error:
		logger.error('[' + who.upper() + '] ' + when + ': ' + what)
	if debug:
		logger.debug('[' + who.upper() + '] ' + when + ': ' + what)
