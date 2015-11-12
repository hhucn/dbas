from .logger import logger

class Translator(object):

	def __init__(self, lang):
		"""

		:param lang: current language
		:return:
		"""
		self.en_dict = self.setUpEnDict()
		self.de_dict = self.setUpDeDict()
		self.lang = lang

	def setUpEnDict(self):
		"""

		:return:
		"""
		logger('Translator', 'setUpEnDict', 'def')

		en_lang = {}

		en_lang['oldPwdEmpty']                  = 'Old password field is empty.'
		en_lang['newPwdEmtpy']                  = 'New password field is empty.'
		en_lang['confPwdEmpty']                 = 'Password confirmation field is empty.'
		en_lang['newPwdNotEqual']               = 'New passwords are not equal'
		en_lang['pwdsSame']                     = 'New and old password are the same'
		en_lang['oldPwdWrong']                  = 'Your old password is wrong.'
		en_lang['pwdChanged']                   = 'Your password was changed'

		en_lang['emptyName']                    = 'Your name is empty!'
		en_lang['emptyEmail']                   = 'Your e-mail is empty!'
		en_lang['emtpyContent']                 = 'Your content is empty!'
		en_lang['maliciousAntiSpam']            = 'Your anti-spam message is empty or wrong!'
		en_lang['nonValidCSRF']                 = 'CSRF-Token is not valid'
		en_lang['name']                         = 'Name'
		en_lang['mail']                         = 'Mail'
		en_lang['phone']                        = 'Phone'
		en_lang['message']                      = 'Message'

		en_lang['pwdNotEqual']                  = 'Passwords are not equal'
		en_lang['nickIsTaken']                  = 'Nickname is taken'
		en_lang['mailIsTaken']                  = 'E-Mail is taken'
		en_lang['mailNotValid']                 = 'E-Mail is not valid'
		en_lang['errorTryLateOrContant']        = 'An error occured, please try again later or contact the author'
		en_lang['accountWasAdded']              = 'Your account was added and you are now able to login.'
		en_lang['accountWasRegistered']         = 'Your account was successfully registered for this e-mail.'
		en_lang['accoutErrorTryLateOrContant']  = 'Your account with the nick could not be added. Please try again or contact the author.'

		en_lang['nicknameIs']                   = 'Your nickname is: '
		en_lang['newPwdIs']                     = 'Your new password is: '
		en_lang['dbasPwdRequest']               = 'D-BAS Password Request'

		en_lang['emailBodyText'] = "This is an automatically generated mail by the D-BAS System.\n" + \
				"For contact please write an mail to krauthoff@cs.uni-duesseldorf.de\n" + \
				"This system is part of a doctoral thesis and currently in an alpha-phase."

		en_lang['emailWasSent']                 = 'E-Mail was sent.'
		en_lang['emailWasNotSent']              = 'E-Mail was not sent.'

		logger('Translator', 'setUpEnDict', 'length ' + str(len(en_lang)))
		return en_lang

	def setUpDeDict(self):
		"""

		:return:
		"""
		logger('Translator', 'setUpDeDict', 'def')

		de_lang = {}

		de_lang['oldPwdEmpty']                  = 'Altes Passwortfeld ist leer.'
		de_lang['newPwdEmtpy']                  = 'Neues Passwortfeld ist leer.'
		de_lang['confPwdEmpty']                 = 'Bestätigungs-Passwordfeld ist leer.'
		de_lang['newPwdNotEqual']               = 'Password und Bestätigung stimmen nicht überein.'
		de_lang['pwdsSame']                     = 'Altes und neues Passwort sind identisch.'
		de_lang['oldPwdWrong']                  = 'Ihr altes Passwort ist falsch.'
		de_lang['pwdChanged']                   = 'Ihr Passwort würde geändert.'

		de_lang['emptyName']                    = 'Ihr Name ist leer!'
		de_lang['emptyEmail']                   = 'Ihre E-Mail ist leer!'
		de_lang['emtpyContent']                 = 'Ihr Inhalt ist leer!'
		de_lang['maliciousAntiSpam']            = 'Ihr Anti-Spam-Nachricht ist leer oder falsch!'
		de_lang['nonValidCSRF']                 = 'CSRF-Token ist nicht valide'
		de_lang['name']                         = 'Name'
		de_lang['mail']                         = 'Mail'
		de_lang['phone']                        = 'Telefon'
		de_lang['message']                      = 'Nachricht'

		de_lang['pwdNotEqual']                  = 'Passwörter sind nicht gleich.'
		de_lang['nickIsTaken']                  = 'Nickname ist schon vergeben.'
		de_lang['mailIsTaken']                  = 'E-Mail ist schon vergeben.'
		de_lang['mailNotValid']                 = 'E-Mail ist nicht gültig.'
		de_lang['errorTryLateOrContant']        = 'Leider ist ein Fehler aufgetreten, bitte versuchen Sie später erneut oder ' \
		                                          'kontaktieren Sie uns.'
		de_lang['accountWasAdded']              = 'Ihr Account wurde angelegt. Sie können sich nun anmelden.'
		de_lang['accountWasRegistered']         = 'Ihr Account wurde erfolgreich für die genannte E-Mail registiert.'
		de_lang['accoutErrorTryLateOrContant']  = 'Ihr Account konnte nicht angelegt werden, bitte versuchen Sie später erneut oder ' \
		                                          'kontaktieren Sie uns.'

		de_lang['nicknameIs']                   = 'Ihr Nickname lautet: '
		de_lang['newPwdIs']                     = 'Ihr Passwort lautet: '
		de_lang['dbasPwdRequest']               = 'D-BAS Password Nachfrage'

		de_lang['emailBodyText'] = 'Dies ist eine automatisch generierte E-Mail von D-BAS.\n' + \
				'Für Kontakt können Sie gerne eine E-Mail an krauthoff@cs.uni-duesseldorf.de verfassen.\n' + \
				'Dieses System ist Teil einer Promotion und noch in der Testphase.'

		de_lang['emailWasSent']                 = 'E-Mail wurde gesendet.'
		de_lang['emailWasNotSent']              = 'E-Mail wurde nicht gesendet.'


		logger('Translator', 'setUpDeDict', 'length ' + str(len(de_lang)))
		return de_lang


	def get(self, id):
		"""

		:param id:
		:return:
		"""
		logger('Translator', 'get', 'id: ' + id + ', lang: ' + self.lang)
		if self.lang == 'de' and id in self.de_dict:
			logger('Translator', 'get', 'return de: ' + self.de_dict[id])
			return self.de_dict[id]

		elif self.lang == 'en' and id in self.en_dict:
			logger('Translator', 'get', 'return en: ' + self.en_dict[id])
			return self.en_dict[id]

		elif self.lang == 'de' and id not in self.de_dict:
			logger('Translator', 'get', 'unknown id for german dict')
			return 'unbekannter identifier im deutschen Wörterbuch'

		elif self.lang == 'en' and id not in self.en_dict:
			logger('Translator', 'get', 'unknown id for englisch dict')
			return 'unknown identifier in the englisch dictionary'

		else:
			logger('Translator', 'get', 'unknown lang')
			return 'unknown language: ' + self.lang