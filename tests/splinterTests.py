from splinter import Browser, exceptions


class Helper:

	def print_success(self, has_success, message):
		print("    " + ("SUCCESS" if has_success else "FAILED") + ":  " + message)

	def login(self, browser, nickname, password):
		browser.visit('http://localhost:4284/login')

		browser.fill('nickname', nickname)
		browser.fill('password', password)

		button = browser.find_by_name('form.login.submitted')
		button.click()

		return browser

	def logout(self, browser):
		browser.visit('http://localhost:4284/logout')
		button = browser.find_by_id('homebutton')
		button.click()
		return browser

	def test_wrapper(self, name, testfunction):
		"""
		Wrapper method
		:param name: of the test
		:param testfunction: the function itself
		:return: value of the testfunction on success, 0 otherwise
		"""
		try:
			returnValue = testfunction
			print("    --> SUCCESS" if returnValue == 1 else "    --> FAILED")
			print("")
			return returnValue
		except AttributeError as e1:
			print("  Some AttributeError occured in " + name + ": " + str(e1))
			webtests.browser.quit()
			return 0
		except exceptions.ElementDoesNotExist as e2:
			print("  Some ElementDoesNotExist occured in " + name + ": " + str(e2))
			webtests.browser.quit()
			return 0
		except IndexError as e3:
			print("  Some IndexError occured in " + name + ": " + str(e3))
			webtests.browser.quit()
			return 0

	def check_for_present_text(self, browser, text, message):
		"""
		Checks whether given text is presented in the browser
		:param browser: current browser
		:param text: text for the check
		:param message: for pint on console
		:return: true if text is present else false
		"""
		if browser.is_text_present(text):
			self.print_success(True, message)
			return True
		else:
			self.print_success(False, message)
			return False

	def check_for_non_present_text(self, browser, text, message):
		"""
		Checks whether given text is not presented in the browser
		:param browser: current browser
		:param text: text for the check
		:param message: for pint on console
		:return: true if text is present else false
		"""
		if not browser.is_text_present(text):
			self.print_success(True, message)
			return True
		else:
			self.print_success(False, message)
			return False


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

		test_count = 9
		success = 0
		
		h = Helper()
		browserStyle = self.browserStyle
		success += h.test_wrapper('text index', self.__test_index(browserStyle))
		success += h.test_wrapper('test popups', self.__test_popups(browserStyle))
		success += h.test_wrapper('test contact formular', self.__test_contact_formular(browserStyle))
		success += h.test_wrapper('test sharing news', self.__test_sharing_news(browserStyle))
		success += h.test_wrapper('test login', self.__test_login(browserStyle))
		success += h.test_wrapper('test logout', self.__test_logout(browserStyle))
		success += h.test_wrapper('test logout', self.__test_sign_up(browserStyle))
		success += h.test_wrapper('test settings', self.__test_settings(browserStyle))
		success += h.test_wrapper('test start discussion button', self.__test_start_discussion(browserStyle))
		success += h.test_wrapper('test admin list all users', self.__test_list_all_users(browserStyle))
		# todo: more testscases

		print("====================================================")
		print("Failed " + str(test_count-success) + " out of " + str(test_count))

	def __check_for_server(self):
		"""
		Checks whether the server if online
		:return: true when the server is on, false otherwise
		"""
		b = Browser(self.browserStyle)
		self.browser = b
		try:
			print("Is server online?")
			b.visit('http://localhost:4284/')
			b.quit()
			self.browser = None
			print("  SUCCESS")
			print("")
			return True
		except ConnectionResetError:
			print("  FAIL")
			print("")
			b.quit()
			self.browser = None
			return False
		except ConnectionRefusedError:
			print("  FAIL")
			print("")
			b.quit()
			self.browser = None
			return False

	def __test_index(self, browser):
		"""
		Checks index page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_index:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/')
		txt = 'This novel discussions software will help you to discuss'
		msg = 'testing index page'
		success = Helper().check_for_present_text(b, txt, msg)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_popups(self, browser):
		"""
		Checks ???
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_popups:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/')

		# open author popup
		toggle = b.find_by_name('show-more-toggle').first
		toggle.click()
		b.click_link_by_partial_text('Author')
		success = Helper().check_for_present_text(b, 'About me', 'check for author text')
		close = b.find_by_name('popup_author_icon_close')
		close.click()

		# open licence popup
		toggle = b.find_by_name('show-more-toggle').first
		toggle.click()
		b.click_link_by_partial_text('Licence')
		success &= success and Helper().check_for_present_text(b, 'MIT', 'check for licence text')
		close = b.find_by_name('popup_licence_icon_close')
		close.click()

		# open privacy policy popup
		toggle = b.find_by_name('show-more-toggle').first
		toggle.click()
		b.click_link_by_partial_text('Privacy Policy')
		success &= success and Helper().check_for_present_text(b, 'Policy', 'check for policy text')
		close = b.find_by_name('popup_privacy_icon_close')
		close.click()

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_contact_formular(self, browser):
		"""
		Checks every form on the contact page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_contact_formular:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/contact')

		form = ['', 'name', 'mail', 'content', 'spam']
		content = ['', 'some_name', 'some_mail@gmx.de', 'some_content', 'some_spam']
		txt = ['name is empty', 'e-mail is empty', 'content is empty', 'anti-spam message is empty or wrong', 'anti-spam message is empty or wrong']
		prefix = 'testing contact formular for '
		msg = [prefix + 'empty name', prefix + 'empty e-mail', prefix + 'empty content', prefix + 'empty anti-spam', prefix + 'wrong anti-spam']

		success = True
		for i in range(0, len(txt)):
			# special cases
			if i > 0:
				b.fill(form[i], content[i])
			if i == 4:
				b.fill(form[3], content[3])
			b.find_by_name('form.contact.submitted').click()
			success = success and Helper().check_for_present_text(b, txt[i], msg[i])

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_sharing_news(self, browser):
		"""
		Checks the sharing buttons on the news page
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_sharing_news:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/news')

		success1 = not b.find_by_css('.share-mail').visible
		success1 = success1 and (not b.find_by_css('.share-google').visible)
		success1 = success1 and (not b.find_by_css('.share-facebook').visible)
		success1 = success1 and (not b.find_by_css('.share-twitter').visible)

		Helper().print_success(success1, "testing whether news sharing icons are not visible")

		b.find_by_css('.share-icon').mouse_over()

		success2 = b.find_by_css('.share-mail').visible
		success2 = success2 and b.find_by_css('.share-google').visible
		success2 = success2 and b.find_by_css('.share-facebook').visible
		success2 = success2 and b.find_by_css('.share-twitter').visible

		Helper().print_success(success2, "testing whether news sharing icons are visible on mouseover")

		b.quit()
		self.browser = None
		return 1 if (success1 and success2) else 0

	def __test_login(self, browser):
		"""
		Checks login
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_login:")
		b = Browser(browser)
		self.browser = b
		b = Helper().login(b, 'admin', 'admin')

		txt = 'The current discussion is about'
		msg = 'testing login function'
		success = Helper().check_for_present_text(b, txt, msg)

		Helper().logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_logout(self, browser):
		"""
		Checks logout after a login
		:param browser:
		:return:
		"""
		print("Starting __test_logout:")
		b = Browser(browser)
		self.browser = b

		b = Helper().login(b, 'admin', 'admin')
		txt = 'The current discussion is about'
		msg = 'testing login'
		success = Helper().check_for_present_text(b, txt, msg)

		b.visit('http://localhost:4284/logout')
		button = b.find_by_id('homebutton')
		button.click()

		txt = "Let's go"
		msg = 'testing logout'
		success &= Helper().check_for_non_present_text(b, txt, msg)

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_sign_up(self, browser):
		"""
		Testing signup
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_sign_up:")
		b = Browser(browser)
		self.browser = b
		b.visit('http://localhost:4284/login')

		h = Helper()
		b.click_link_by_partial_text('Sign Up')
		success = h.check_for_present_text(b, 'Sign Up For Free', 'check for sign up form')

		button = b.find_by_name('form.registration.submitted')
		button.click()

		success &= h.check_for_present_text(b, 'E-Mail is not valid', 'check for wrong email on empty form')

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_settings(self, browser):
		"""
		Settings test
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("__test_settings:")
		b = Browser(browser)
		self.browser = b

		b = Helper().login(b, 'admin', 'admin')
		toggle = b.find_by_name('user-options-toggle').first
		toggle.click()

		b.click_link_by_partial_text('Settings')

		txt = 'dbas@cs.uni-duesseldorf.de'
		msg = 'testing information about the user'
		h = Helper()
		success = h.check_for_present_text(b, txt, msg)

		button = b.find_by_id('request-track')
		button.click()
		txt1 = 'UID'
		txt2 = 'No data was tracked'
		msg1 = 'testing tracked decisions by UID'
		msg2 = 'testing tracked decisions by no tracked data'
		success &= (h.check_for_present_text(b, txt1, msg1) or h.check_for_present_text(b, txt2, msg2))

		Helper().logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_start_discussion(self, browser):
		"""
		Checks the start discussion button after login
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_start_discussion_button:")
		b = Browser(browser)
		self.browser = b
		b = Helper().login(b, 'admin', 'admin')

		button = b.find_by_id('start-discussion')
		button.click()

		# start discussion
		txt = 'These are the current statements'
		msg = 'testing start discussion button function'
		success = Helper().check_for_present_text(b, txt, msg)

		# there should be no error
		txt = 'Please select a statement!'
		msg ='testing no error message displayed'
		success &= Helper().check_for_non_present_text(b, txt, msg)

		# add statement container should not be there
		txt = 'Please insert a new position'
		msg ='testing for non display statement container'
		success &= Helper().check_for_non_present_text(b, txt, msg)

		# check for error, when nothing was clicked
		button = b.find_by_id('send-answer')
		button.click()
		txt = 'Please select a statement!'
		msg ='testing error message displayed'
		success &= Helper().check_for_present_text(b, txt, msg)

		# choose last radio button
		b.choose('radioButtonGroup', 'Adding a new position.')

		# add statement container should be there
		txt = 'Please insert a new position'
		msg ='testing for non display statement container'
		success &= Helper().check_for_present_text(b, txt, msg)

		Helper().logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_list_all_users(self, browser):
		"""
		Tests the listing and hiding of all users
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_list_all_users:")
		b = Browser(browser)
		self.browser = b

		b = Helper().login(b, 'admin', 'admin')

		button = b.find_by_id('list-all-users')
		button.click()

		txt = 'dbas@cs.uni-duesseldorf.de'
		msg = 'testing list all users'
		success = Helper().check_for_present_text(b, txt, msg)

		button.click()
		msg = 'testing hiding all users'
		success &= Helper().check_for_non_present_text(b, txt, msg)

		Helper().logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_dummy(self, browser):
		"""
		Dummy Test
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_dummy:")
		b = Browser(browser)
		self.browser = b
		b = Helper().login(b, 'admin', 'admin')

		success = True

		Helper().logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0


browserStyle = 'firefox'
webtests = WebTests(browserStyle)
try:
	webtests.run_all_tests()
except ConnectionResetError as e:
	print("  Server is offline")
