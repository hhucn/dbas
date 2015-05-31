from splinter import Browser, exceptions

class WebTests:
	browser = None

	def __init__(self, browser):
		self.browserStyle = browser

	def run_all_tests(self):
		"""
		Just runs every test
		"""

		# server check
		if not self.__check_for_server():
			return

		test_count = 6
		success = 0

		tmp = self.browserStyle
		success += self.__test_wrapper('text index', self.__test_index(tmp))
		success += self.__test_wrapper('test index', self.__test_index(tmp))
		success += self.__test_wrapper('test login', self.__test_login(tmp))
		success += self.__test_wrapper('test start discussion button', self.__test_start_discussion_button(tmp))
		success += self.__test_wrapper('test contact formular', self.__test_contact_formular(tmp))
		success += self.__test_wrapper('test sharing news', self.__test_sharing_news(tmp))
		success += self.__test_wrapper('test popups', self.__test_popups(tmp))
		# todo: more testscases

		print("====================================================")
		print("Failed " + str(test_count-success) + " out of " + str(test_count))

	def __test_wrapper(self, name, testfunction):
		"""

		:param name:
		:param testfunction:
		:return:
		"""
		try:
			return testfunction
		except AttributeError as e1:
			print("  Some AttributeError occured in " + name + ": " + str(e1))
			webtests.browser.quit()
			return False
		except exceptions.ElementDoesNotExist as e2:
			print("  Some ElementDoesNotExist occured in " + name + ": " + str(e2))
			webtests.browser.quit()
			return False

	def __check_for_present_text(self, browser, text, message):
		"""
		Checks whether given text is presented in the browser
		:param browser: current browser
		:param text: text for the check
		:param message: for pint on console
		:return: true if text is present else false
		"""
		if browser.is_text_present(text):
			self.__print_success(True, message)
			return True
		else:
			self.__print_success(False, message)
			return False

	def __print_success(self, hasSuccess, message):
		print("    " + ("SUCCESS" if hasSuccess else "FAILED") + ": " + message)

	def __check_for_server(self):
		"""
		Checks whether the server if online
		:return: true when the server is on, false otherwise
		"""
		b = Browser(self.browserStyle)
		self.browser = b
		try:
			b.visit('http://localhost:4284/')
			b.quit()
			self.browser = None
			return True
		except ConnectionResetError:
			print("Server is offline")
			b.quit()
			self.browser = None
			return False

	def __test_index(self, browser):
		"""
		Checks index page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __test_index:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/')
		txt = 'This novel discussions software will help you to discuss'
		msg = 'testing index page'
		success = self.__check_for_present_text(b, txt, msg)
		b.quit()
		self.browser = None
		print("")
		return 1 if success else 0

	def __test_login(self, browser):
		"""
		Checks login
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __test_login:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/login')

		b.fill('nickname', 'admin')
		b.fill('password', 'admin')

		button = b.find_by_name('form.login.submitted')
		button.click()

		txt = 'The current discussion is about'
		msg = 'testing login function'
		success = self.__check_for_present_text(b, txt, msg)
		b.quit()
		self.browser = None
		print("")
		return 1 if success else 0

	def __test_start_discussion_button(self, browser):
		"""
		Checks the start discussion button after login
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __test_start_discussion_button:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/login')

		b.fill('nickname', 'admin')
		b.fill('password', 'admin')

		button1 = b.find_by_name('form.login.submitted')
		button1.click()

		button2 = b.find_by_id('start-discussion')
		button2.click()

		txt = 'These are the current statements'
		msg = 'testing start discussion button function'
		success = self.__check_for_present_text(b, txt, msg)
		b.quit()
		self.browser = None
		print("")
		return 1 if success else 0

	def __test_contact_formular(self, browser):
		"""
		Checks every form on the contact page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __test_contact_formular:")
		b = Browser(browser)
		self.browser = b
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
			success = success and self.__check_for_present_text(b, txt[i], msg[i])

		b.quit()
		self.browser = None
		print("")
		return 1 if success else 0

	def __test_sharing_news(self, browser):
		"""
		Checks the sharing buttons on the news page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __test_sharing_news:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/news')

		success1 = not b.find_by_css('.share-mail').visible
		success1 = success1 and (not b.find_by_css('.share-google').visible)
		success1 = success1 and (not b.find_by_css('.share-facebook').visible)
		success1 = success1 and (not b.find_by_css('.share-twitter').visible)

		self.__print_success(success1, "testing whether news sharing icons are not visible")

		b.find_by_css('.share-icon').mouse_over()

		success2 = b.find_by_css('.share-mail').visible
		success2 = success2 and b.find_by_css('.share-google').visible
		success2 = success2 and b.find_by_css('.share-facebook').visible
		success2 = success2 and b.find_by_css('.share-twitter').visible

		self.__print_success(success2, "testing whether news sharing icons are visible on mouseover")

		b.quit()
		self.browser = None
		print("")
		return 1 if (success1 and success2) else 0

	def __test_popups(self, browser):
		"""
		Checks ???
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Start __test_popups:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/')

		success = False
		# # open author popup
		# b.find_by_xpath("//a[@class='dropdown-toggle']/a[text()='Author']").click()
		# success = sucess or self.__check_for_present_text(b, 'About me', 'check for author text')
		# close = b.find_by_id('popup_author_btn_close')
		# close.click()

		# # open licence popup
		# b.find_by_xpath("//select[@class='dropdown-toggle']/option[text()='Licence']").click()
		# success = success and self.__check_for_present_text(b, 'MIT', 'check for licence text')
		# close = b.find_by_id('popup_licence_btn_close')
		# close.click()

		# # open privacy policy popup
		# b.find_by_xpath("//select[@class='dropdown-toggle']/option[text()='Privacy Policy']").click()
		# success = success and self.__check_for_present_text(b, 'Policy', 'check for policy text')
		# close = b.find_by_id('popup_licence_btn_close')
		# close.click()

		self.__print_success(success, "testing popups")

		b.quit()
		self.browser = None
		print("")
		return 1 if success else 0

browserStyle = 'firefox'
webtests = WebTests(browserStyle)
try:
	webtests.run_all_tests()
except ConnectionResetError as e:
	print("  Server is offline")
