from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class Translator(object):
	# TODO THIS

	def __init__(self, lang):
		"""

		:param lang: current language
		:return:
		"""
		self.lang = lang

		self.attack = 'attack'
		self.support = 'support'
		self.premise = 'premise'
		self.because = 'because'
		self.doesNotHoldBecause = 'doesNotHoldBecause'
		self.moreAbout = 'moreAbout'
		self.undermine1 = 'undermine1'
		self.undermine2 = 'undermine2'
		self.support1 = 'support1'
		self.support2 = 'support2'
		self.undercut1 = 'undercut1'
		self.undercut2 = 'undercut2'
		self.overbid1 = 'overbid1'
		self.overbid2 = 'overbid2'
		self.rebut1 = 'rebut1'
		self.rebut2 = 'rebut2'
		self.oldPwdEmpty = 'oldPwdEmpty'
		self.newPwdEmtpy = 'newPwdEmtpy'
		self.confPwdEmpty = 'confPwdEmpty'
		self.newPwdNotEqual = 'newPwdNotEqual'
		self.pwdsSame = 'pwdsSame'
		self.oldPwdWrong = 'oldPwdWrong'
		self.pwdChanged = 'pwdChanged'
		self.emptyName = 'emptyName'
		self.emptyEmail = 'emptyEmail'
		self.emtpyContent = 'emtpyContent'
		self.maliciousAntiSpam = 'maliciousAntiSpam'
		self.nonValidCSRF = 'nonValidCSRF'
		self.name = 'name'
		self.mail = 'mail'
		self.phone = 'phone'
		self.message = 'message'
		self.pwdNotEqual = 'pwdNotEqual'
		self.nickIsTaken = 'nickIsTaken'
		self.mailIsTaken = 'mailIsTaken'
		self.mailNotValid = 'mailNotValid'
		self.errorTryLateOrContant = 'errorTryLateOrContant'
		self.accountWasAdded = 'accountWasAdded'
		self.accountWasRegistered = 'accountWasRegistered'
		self.accoutErrorTryLateOrContant = 'accoutErrorTryLateOrContant'
		self.nicknameIs = 'nicknameIs'
		self.newPwdIs = 'newPwdIs'
		self.dbasPwdRequest = 'dbasPwdRequest'
		self.emailBodyText = 'emailBodyText'
		self.emailWasSent = 'emailWasSent'
		self.emailWasNotSent = 'emailWasNotSent'
		self.antispamquestion = 'antispamquestion'
		self.signs = 'signs'

		self.en_dict = self.setUpEnDict()
		self.de_dict = self.setUpDeDict()

	def setUpEnDict(self):
		"""

		:return: dictionary for the english language
		"""
		logger('Translator', 'setUpEnDict', 'def')

		en_lang = {}
		en_lang[self.attack]                       = 'You disagreed with'
		en_lang[self.support]                      = 'You agreed with'
		en_lang[self.premise]                      = 'Premise'
		en_lang[self.because]                      = 'because'
		en_lang[self.doesNotHoldBecause]           = 'does not hold because'
		en_lang[self.moreAbout]                    = 'More about'
		en_lang[self.undermine1]                   = 'It is false that'
		en_lang[self.undermine2]                   = ''
		en_lang[self.support1]                     = ''
		en_lang[self.support2]                     = ''
		en_lang[self.undercut1]                    = 'It is false that'
		en_lang[self.undercut2]                    = 'and this is no good counter-argument'
		en_lang[self.overbid1]                     = 'It is false that'
		en_lang[self.overbid2]                     = 'and this is a good counter-argument'
		en_lang[self.rebut1]                       = 'It is right that'
		en_lang[self.rebut2]                       = ', but I have a better statement'
		en_lang[self.oldPwdEmpty]                  = 'Old password field is empty.'
		en_lang[self.newPwdEmtpy]                  = 'New password field is empty.'
		en_lang[self.confPwdEmpty]                 = 'Password confirmation field is empty.'
		en_lang[self.newPwdNotEqual]               = 'New passwords are not equal'
		en_lang[self.pwdsSame]                     = 'New and old password are the same'
		en_lang[self.oldPwdWrong]                  = 'Your old password is wrong.'
		en_lang[self.pwdChanged]                   = 'Your password was changed'
		en_lang[self.emptyName]                    = 'Your name is empty!'
		en_lang[self.emptyEmail]                   = 'Your e-mail is empty!'
		en_lang[self.emtpyContent]                 = 'Your content is empty!'
		en_lang[self.maliciousAntiSpam]            = 'Your anti-spam message is empty or wrong!'
		en_lang[self.nonValidCSRF]                 = 'CSRF-Token is not valid'
		en_lang[self.name]                         = 'Name'
		en_lang[self.mail]                         = 'Mail'
		en_lang[self.phone]                        = 'Phone'
		en_lang[self.message]                      = 'Message'
		en_lang[self.pwdNotEqual]                  = 'Passwords are not equal'
		en_lang[self.nickIsTaken]                  = 'Nickname is taken'
		en_lang[self.mailIsTaken]                  = 'E-Mail is taken'
		en_lang[self.mailNotValid]                 = 'E-Mail is not valid'
		en_lang[self.errorTryLateOrContant]        = 'An error occured, please try again later or contact the author'
		en_lang[self.accountWasAdded]              = 'Your account was added and you are now able to login.'
		en_lang[self.accountWasRegistered]         = 'Your account was successfully registered for this e-mail.'
		en_lang[self.accoutErrorTryLateOrContant]  = 'Your account with the nick could not be added. Please try again or contact the author.'
		en_lang[self.nicknameIs]                   = 'Your nickname is: '
		en_lang[self.newPwdIs]                     = 'Your new password is: '
		en_lang[self.dbasPwdRequest]               = 'D-BAS Password Request'
		en_lang[self.emailBodyText] = "This is an automatically generated mail by the D-BAS System.\n" + \
				"For contact please write an mail to krauthoff@cs.uni-duesseldorf.de\n" + \
				"This system is part of a doctoral thesis and currently in an alpha-phase."
		en_lang[self.emailWasSent]                 = 'E-Mail was sent.'
		en_lang[self.emailWasNotSent]              = 'E-Mail was not sent.'
		en_lang[self.antispamquestion]             = 'What is'
		en_lang[self.signs]                        = ['+','*','/','-']
		en_lang['0']                               = 'zero'
		en_lang['1']                               = 'one'
		en_lang['2']                               = 'two'
		en_lang['3']                               = 'three'
		en_lang['4']                               = 'four'
		en_lang['5']                               = 'five'
		en_lang['6']                               = 'six'
		en_lang['7']                               = 'seven'
		en_lang['8']                               = 'eight'
		en_lang['9']                               = 'nine'
		en_lang['+']                               = 'plus'
		en_lang['-']                               = 'minus'
		en_lang['*']                               = 'multiply with'
		en_lang['/']                               = 'divided by'

		logger('Translator', 'setUpEnDict', 'length ' + str(len(en_lang)))
		return en_lang

	def setUpDeDict(self):
		"""

		:return: dictionary for the german language
		"""
		logger('Translator', 'setUpDeDict', 'def')
		de_lang = {}
		de_lang[self.attack]                       = 'Sie lehnen ab, dass'
		de_lang[self.support]                      = 'Sie akzeptieren'
		de_lang[self.premise]                      = 'Prämisse'
		de_lang[self.because]                      = 'weil'
		de_lang[self.doesNotHoldBecause]           = 'gilt nicht, weil'
		de_lang[self.moreAbout]                    = 'Mehr über'
		de_lang[self.undermine1]                   = 'Es ist falsch, dass'
		de_lang[self.undermine2]                   = ''
		de_lang[self.support1]                     = 'Es ist richtig, dass'
		de_lang[self.support2]                     = ''
		de_lang[self.undercut1]                    = 'Es ist falsch, dass'
		de_lang[self.undercut2]                    = 'und das ist ein schlechter Konter'
		de_lang[self.overbid1]                     = 'Es ist falsch, dass'
		de_lang[self.overbid2]                     = 'und das ist ein guter Konter'
		de_lang[self.rebut1]                       = 'Es ist richtig, dass'
		de_lang[self.rebut2]                       = ', aber ich habe etwas besseres'
		de_lang[self.oldPwdEmpty]                  = 'Altes Passwortfeld ist leer.'
		de_lang[self.newPwdEmtpy]                  = 'Neues Passwortfeld ist leer.'
		de_lang[self.confPwdEmpty]                 = 'Bestätigungs-Passwordfeld ist leer.'
		de_lang[self.newPwdNotEqual]               = 'Password und Bestätigung stimmen nicht überein.'
		de_lang[self.pwdsSame]                     = 'Altes und neues Passwort sind identisch.'
		de_lang[self.oldPwdWrong]                  = 'Ihr altes Passwort ist falsch.'
		de_lang[self.pwdChanged]                   = 'Ihr Passwort würde geändert.'
		de_lang[self.emptyName]                    = 'Ihr Name ist leer!'
		de_lang[self.emptyEmail]                   = 'Ihre E-Mail ist leer!'
		de_lang[self.emtpyContent]                 = 'Ihr Inhalt ist leer!'
		de_lang[self.maliciousAntiSpam]            = 'Ihr Anti-Spam-Nachricht ist leer oder falsch!'
		de_lang[self.nonValidCSRF]                 = 'CSRF-Token ist nicht valide'
		de_lang[self.name]                         = 'Name'
		de_lang[self.mail]                         = 'Mail'
		de_lang[self.phone]                        = 'Telefon'
		de_lang[self.message]                      = 'Nachricht'
		de_lang[self.pwdNotEqual]                  = 'Passwörter sind nicht gleich.'
		de_lang[self.nickIsTaken]                  = 'Nickname ist schon vergeben.'
		de_lang[self.mailIsTaken]                  = 'E-Mail ist schon vergeben.'
		de_lang[self.mailNotValid]                 = 'E-Mail ist nicht gültig.'
		de_lang[self.errorTryLateOrContant]        = 'Leider ist ein Fehler aufgetreten, bitte versuchen Sie später erneut oder ' \
		                                          'kontaktieren Sie uns.'
		de_lang[self.accountWasAdded]              = 'Ihr Account wurde angelegt. Sie können sich nun anmelden.'
		de_lang[self.accountWasRegistered]         = 'Ihr Account wurde erfolgreich für die genannte E-Mail registiert.'
		de_lang[self.accoutErrorTryLateOrContant]  = 'Ihr Account konnte nicht angelegt werden, bitte versuchen Sie später erneut oder ' \
		                                          'kontaktieren Sie uns.'
		de_lang[self.nicknameIs]                   = 'Ihr Nickname lautet: '
		de_lang[self.newPwdIs]                     = 'Ihr Passwort lautet: '
		de_lang[self.dbasPwdRequest]               = 'D-BAS Passwort Nachfrage'
		de_lang[self.emailBodyText] = 'Dies ist eine automatisch generierte E-Mail von D-BAS.\n' + \
				'Für Kontakt können Sie gerne eine E-Mail an krauthoff@cs.uni-duesseldorf.de verfassen.\n' + \
				'Dieses System ist Teil einer Promotion und noch in der Testphase.'
		de_lang[self.emailWasSent]                 = 'E-Mail wurde gesendet.'
		de_lang[self.emailWasNotSent]              = 'E-Mail wurde nicht gesendet.'
		de_lang[self.antispamquestion]             = 'Was ist'
		de_lang[self.signs]                        = ['+','*','/','-']
		de_lang['0']                               = 'null'
		de_lang['1']                               = 'eins'
		de_lang['2']                               = 'zwei'
		de_lang['3']                               = 'drei'
		de_lang['4']                               = 'vier'
		de_lang['5']                               = 'fünf'
		de_lang['6']                               = 'sechs'
		de_lang['7']                               = 'sieben'
		de_lang['8']                               = 'acht'
		de_lang['9']                               = 'neun'
		de_lang['+']                               = 'plus'
		de_lang['-']                               = 'minus'
		de_lang['*']                               = 'mal'
		de_lang['/']                               = 'durch'


		logger('Translator', 'setUpDeDict', 'length ' + str(len(de_lang)))
		return de_lang


	def get(self, id):
		"""
		Returns an localized string
		:param id: string identifier
		:return: string
		"""
		logger('Translator', 'get', 'id: ' + id + ', lang: ' + self.lang)
		if self.lang == 'de' and id in self.de_dict:
			logger('Translator', 'get', 'return de: ' + str(self.de_dict[id]))
			return self.de_dict[id]

		elif self.lang == 'en' and id in self.en_dict:
			logger('Translator', 'get', 'return en: ' + str(self.en_dict[id]))
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