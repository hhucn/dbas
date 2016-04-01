from splinter import Browser, exceptions
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException
import sys
import time

mainpage = 'http://localhost:4284/'


class Helper:

	@staticmethod
	def print_success(has_success, message):
		print("    " + ("SUCCESS" if has_success else "FAILED ") + ":  " + message)

	@staticmethod
	def login(browser, nickname, password, url):
		browser.visit(mainpage + 'ajax_user_login?user=' + nickname + '&password=' + password + '&keep_login=false&url=' + url)
		return browser

	@staticmethod
	def logout(browser):
		browser.visit(mainpage + 'ajax_user_logout')
		return browser

	@staticmethod
	def test_wrapper(name, testfunction, *args):
		"""
		Wrapper method
		:param name: of the test
		:param testfunction: the function itself
		:return: value of the testfunction on success, 0 otherwise
		"""
		try:
			returnValue = testfunction(*args)
			print('    --> SUCCESS' if returnValue == 1 else '    --> FAILED')
			print('')
			return returnValue
		except AttributeError as e1:
			print('    -> AttributeError occured in ' + name)
			print('       ' + str(e1))
			webtests.browser.quit()
			return 0
		except exceptions.ElementDoesNotExist as e2:
			print('    -> ElementDoesNotExist occured in ' + name)
			print('       ' + str(e2))
			webtests.browser.quit()
			return 0
		except IndexError as e3:
			print('    -> IndexError occured in ' + name)
			print('       ' + str(e3))
			webtests.browser.quit()
			return 0
		except ElementNotVisibleException as e4:
			print('    -> ElementNotVisibleException occured in ' + name)
			print('       ' + str(e4))
			webtests.browser.quit()
			return 0
		except WebDriverException as e5:
			print('    -> WebDriverException occured in ' + name)
			print('       ' + str(e5))
			webtests.browser.quit()
			return 0
		except:
			print('    -> Unexpected error: ' + str(sys.exc_info()[0]))
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
			print("====================================================")
			print("Exit gracefully!")
			return

		test_count = 7
		success = 0

		browserStyle = self.browserStyle
		start = time.time()
		# success += Helper.test_wrapper('test normal pages', self.__test_pages_when_not_logged_in, browserStyle)
		# success += Helper.test_wrapper('test login logout', self.__test_login_logout, browserStyle)
		# success += Helper.test_wrapper('test logged in pages', self.__test_pages_when_logged_in, browserStyle)
		# success += Helper.test_wrapper('test popups', self.__test_popups, browserStyle)
		# success += Helper.test_wrapper('test contact formular', self.__test_contact_formular, browserStyle)
		# success += Helper.test_wrapper('test language switch', self.__test_language_switch, browserStyle)
		success += Helper.test_wrapper('test discussion buttons', self.__test_discussion_buttons, browserStyle)
		success += Helper.test_wrapper('test demo discussion', self.__test_demo_discussion, browserStyle)
		end = time.time()
		diff = str(end - start)
		diff = diff[0:diff.index('.') + 3]
		print("====================================================")
		print("Failed " + str(test_count - success) + " out of " + str(test_count) + ' in ' + str(diff) + 's')

	def __check_for_server(self):
		"""
		Checks whether the server if online
		:return: true when the server is on, false otherwise
		"""
		b = Browser(self.browserStyle)
		self.browser = b
		try:
			print("Is server online?")
			b.visit(mainpage)
			success = Helper().check_for_present_text(b, 'part of the graduate school', 'check main page')
			b.quit()
			self.browser = None
			print(" -> SUCCESS" if success else " -> FAIL")
			print("")
			return success
		except ConnectionResetError:
			print(" -> FAIL")
			print("")
			b.quit()
			self.browser = None
			return False
		except ConnectionRefusedError:
			print(" -> FAIL")
			print("")
			b.quit()
			self.browser = None
			return False

	def __test_pages_when_not_logged_in(self, browser):
		"""
		Checks pages
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_pages_not_logged_in:")
		success = True
		b = Browser(browser)
		self.browser = b

		pages = [mainpage,
		         mainpage + 'contact',
		         mainpage + 'news',
		         mainpage + 'imprint',
		         mainpage + 'discuss',
		         mainpage + 'settings',
		         mainpage + 'notifications',
		         mainpage + 'admin']
		tests = ['main',
		         'contact',
		         'news',
		         'imprint',
		         'discuss',
		         'settings',
		         'notifications',
		         'admin']
		texts = ['part of the graduate school',
		         'Feel free to drop us a',
		         'Speech Bubbles System',
		         'Liability for content',
		         'The current discussion is about:',
		         'part of the graduate school',
		         'part of the graduate school',
		         '401']
		for index, p in enumerate(pages):
			b.visit(p)
			test = 'testing ' + tests[index] + ' page'
			success = success and Helper().check_for_present_text(b, texts[index], test)

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_login_logout(self, browser):
		"""

		:param browser:
		:return:
		"""
		success = True
		print("Starting __test_login_logout:")
		b = Browser(browser)
		self.browser = b

		b = Helper.login(b, 'tobias', 'wrongpassword', mainpage)
		test = 'testing wrong login'
		success = success and Helper().check_for_present_text(b, 'do not match', test)

		b = Helper.login(b, 'tobias', 'tobias', mainpage)
		test = 'testing right login'
		success = success and Helper().check_for_present_text(b, 'tobias', test)

		b = Helper.logout(b)
		test = 'testing logout'
		success = success and Helper().check_for_non_present_text(b, 'tobias', test)

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_pages_when_logged_in(self, browser):
		"""

		:param browser:
		:return:
		"""
		success = True
		print("Starting __test_pages_logged_in:")
		b = Browser(browser)
		self.browser = b
		b = Helper.login(b, 'tobias', 'tobias', mainpage)

		pages = [mainpage + 'settings',
		         mainpage + 'notifications',
		         mainpage + 'admin']
		tests = ['settings',
		         'notifications',
		         'admin']
		texts = ['Personal Information',
		         'Notification Board',
		         'Dashboard']
		for index, p in enumerate(pages):
			b.visit(p)
			test = 'testing ' + tests[index] + ' page'
			success = success and Helper().check_for_present_text(b, texts[index], test)

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
		b.visit(mainpage)

		# open author popup
		b.find_by_id('link_popup_author').click()
		success = Helper().check_for_present_text(b, 'About me', 'check for author text')
		close = b.find_by_name('popup_author_icon_close')
		close.click()

		time.sleep(0.5)

		# open licence popup
		b.find_by_id('link_popup_license').click()
		success = success and Helper().check_for_present_text(b, 'MIT', 'check for license text')
		close = b.find_by_name('popup_license_icon_close')
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

	def __test_language_switch(self, browser):
		"""
		Testing language switch
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_language_switch:")
		b = Browser(browser)
		self.browser = b
		h = Helper()

		b.visit(mainpage)
		success = h.check_for_present_text(b, 'part of the graduate', 'check englisch language')

		b.click_link_by_partial_text('Language')
		b.click_link_by_partial_text('Deutsch')
		success = success and h.check_for_present_text(b, 'Teil der Graduierten-Kollegs', 'check switch to german language')

		b.click_link_by_partial_text('Sprache')
		b.click_link_by_partial_text('English')
		success = success and h.check_for_present_text(b, 'part of the graduate', 'check switch back to englisch language')

		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_discussion_buttons(self, browser):
		"""
		Checks the discussions buttons
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_discussion_buttons:")
		success = True
		b = Browser(browser)
		self.browser = b
		h = Helper()
		b = h.login(b, 'tobias', 'tobias', mainpage + 'discussion')

		# check url popup
		b.find_by_id('share-url').click()
		success = h.check_for_present_text(b, 'Share your URL', 'check for share url popup')
		b.find_by_id('popup-url-sharing-long-url-button').click()
		success = success and h.check_for_present_text(b, mainpage + 'discussion', 'check for long url')
		b.find_by_id('popup-url-sharing-close-button').click()
		time.sleep(0.5)

		# check edit statement popup
		b.find_by_id('edit-statement').click()
		success = success and h.check_for_present_text(b, mainpage + 'Edit Statements / View Changelog', 'check for edit statements popup')
		b.find_by_id('popup-edit-statement-close').click()
		time.sleep(0.5)

		# check issue dropdown and switch issue
		b.find_by_id('issue-dropdown').click()
		success = success and h.check_for_present_text(b, mainpage + 'Cat or Dog', 'check for issue dropdown')
		success = success and h.check_for_present_text(b, mainpage + 'Change of discussion', 'check for topic list')
		b.find_by_id('confirm-dialog-checkbox-accept-btn').click()
		time.sleep(0.5)
		success = success and h.check_for_present_text(b, mainpage + 'Your familiy argues', 'check for switched issue')

		b.find_by_id('finish-button').click()
		success = success and h.check_for_present_text(b, mainpage + 'Thank you!', 'check for finish button')

		# click position
		success = success and h.check_for_present_text(b, mainpage + 'What is the initial position', 'check for first step in discussion')
		b.find_by_css('discussions-space-list input:first-child').click()
		success = success and h.check_for_present_text(b, mainpage + 'What do you think', 'check for second step in discussion')

		# restart
		b.find_by_id('discussion-restart-btn').click()
		success = success and h.check_for_present_text(b, mainpage + 'What is the initial position', 'check for restart')

		b = h.logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_demo_discussion(self, browser):
		"""
		Checks the discussion
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print("Starting __test_demo_discussion:")
		success = True
		b = Browser(browser)
		self.browser = b
		h = Helper()
		b = h.login(b, 'tobias', 'tobias', mainpage + 'discussion')

		b = h.logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0


browserStyle = 'firefox'
webtests = WebTests(browserStyle)
try:
	webtests.run_all_tests()
except ConnectionResetError as e:
	print("  Server is offline")
