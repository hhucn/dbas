from splinter import Browser

class WebTests():

	def __init__(self, browser):
		self.browserStyle = browser

	def runAllTests(self):
		"""
		Just runs every test
		"""

		# server check
		if not self.__checkForServer(self.browserStyle):
			return


		testCount = 4
		success = 0

		success += self.__testIndex(self.browserStyle)
		success += self.__testLogin(self.browserStyle)
		success += self.__testStartDiscussionButton(self.browserStyle)
		success += self.__testContactFormular(self.browserStyle)

		print("====================================================")
		print("Failed " + str(testCount-success) + " out of " + str(testCount))

	def __checkForPresentText(self, browser, text, message):
		"""
		Checks whether given text is presented in the browser
		:param browser: current browser
		:param text: text for the check
		:param message: for pint on console
		:return: true if text is present else false
		"""
		if browser.is_text_present(text):
			print("    SUCCESS: " + message)
			return True
		else:
			print("    FAILED: " + message)
			return False

	def __checkForServer(self, browser):
		"""
		Checks whether the server if online
		:param browser: current browser
		:return: true when the server is on, false otherwise
		"""
		b = Browser(self.browserStyle)
		try:
			b.visit('http://localhost:4284/')
			b.quit
			return True
		except ConnectionResetError:
			print("Server is offline")
			b.quit()
			return False


	def __testIndex(self, browser):
		"""
		Checks index page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start testIndex:")
		b = Browser(browser)
		b.visit('http://localhost:4284/')
		txt = 'This novel discussions software will help you to discuss'
		msg = 'testing index page'
		success = self.__checkForPresentText(b, txt, msg)
		b.quit()
		print("")
		return 1 if success else 0

	def __testLogin(self, browser):
		"""
		Checks login
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start testLogin:")
		b = Browser(browser)
		b.visit('http://localhost:4284/login')

		b.fill('nickname', 'admin')
		b.fill('password', 'admin')

		button = b.find_by_name('form.login.submitted')
		button.click()

		txt = 'The current discussion is about'
		msg = 'testing login function'
		success = self.__checkForPresentText(b, txt, msg)
		b.quit()
		print("")
		return 1 if success else 0

	def __testStartDiscussionButton(self, browser):
		"""
		Checks the start discussion button after login
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start testStartDiscussionButton:")
		b = Browser(browser)
		b.visit('http://localhost:4284/login')

		b.fill('nickname', 'admin')
		b.fill('password', 'admin')

		button1 = b.find_by_name('form.login.submitted')
		button1.click()

		button2 = b.find_by_id('get-positions')
		button2.click()

		txt = 'These are the current statements'
		msg = 'testing start discussion button function'
		success = self.__checkForPresentText(b, txt, msg)
		b.quit()
		print("")
		return 1 if success else 0

	def __testContactFormular(self, browser):
		"""
		Checks every form on the contact page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __testContactFormular:")
		b = Browser(browser)
		b.visit('http://localhost:4284/contact')

		form = ['',
				'name',
				'mail',
				'content',
				'spam']

		content = ['',
					'some_name',
					'some_mail@gmx.de',
					'some_content',
					'some_spam']

		txt = ['name is empty',
				'e-mail is empty',
				'content is empty',
				'anti-spam message is empty or wrong',
				'anti-spam message is empty or wrong']

		msg = ['testing contact formular for empty name',
				'testing contact formular for empty e-mail',
				'testing contact formular for empty content',
				'testing contact formular for empty anti-spam',
				'testing contact formular for wrong anti-spam']

		success = True
		for i in range(0, len(txt)):
			# special cases
			if i>0:
				b.fill(form[i], content[i])
			if i==4:
				b.fill(form[3], content[3])
			b.find_by_name('form.contact.submitted').click()
			success = success and self.__checkForPresentText(b, txt[i], msg[i])

		b.quit()
		print("")
		return 1 if success else 0


browserStyle = 'firefox'
webtests = WebTests(browserStyle)
try:
	webtests.runAllTests()
except ConnectionResetError as e:
	print("Server is offline")