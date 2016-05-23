"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


import random
from cryptacular.bcrypt import BCRYPTPasswordManager


# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
def get_rnd_passwd():
	"""
	Generates a password with the length of 10 out of ([a-z][A-Z][+-*/#!*?])+
	:return: new secure password
	"""
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	upperalphabet = alphabet.upper()
	symbols = '+-*/#!*?'
	pw_len = 10
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
	Returns encrypted password

	:param password: String
	:return: String
	"""
	manager = BCRYPTPasswordManager()
	return manager.encode(password)
