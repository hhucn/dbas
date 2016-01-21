import logging

log = logging.getLogger(__name__)

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

def logger(who, when, what):
	"""
	Log for the console and logfile on disk. Logged format: [who.upper()] when <what>
	:param who: which class
	:param when: which method
	:param what: what mesage
	:return: None
	"""
	if who == '-':
		log.debug('[' + who.upper() + '] ' + when + ' <' + what + '>')