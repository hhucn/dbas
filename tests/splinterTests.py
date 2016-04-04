from splinter import Browser, exceptions
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException
import time

mainpage = 'http://localhost:4284/'
testcounter = 0
waittime = 0.3


class Helper:

	@staticmethod
	def print_success(has_success, message):
		print('    ' + ('SUCCESS' if has_success else 'FAILED') + ':  ' + message)

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
			global testcounter
			testcounter += 1
			ret_val = testfunction(*args)
			print('    --> SUCCESS' if ret_val == 1 else '    --> FAILED')
			print('')
			return ret_val
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
		except Exception as e6:
			print('    -> Unexpected error in ' + name)
			print('       ' + str(e6))
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
		self.browser_style = browser

	def run_all_tests(self):
		"""
		Just runs every test
		"""

		# server check
		if not self.__check_for_server():
			print('====================================================')
			print('Exit gracefully!')
			return

		success_counter = 0

		start = time.time()
		success_counter += Helper.test_wrapper('test normal pages', self.__test_pages_when_not_logged_in, self.browser_style)
		success_counter += Helper.test_wrapper('test login logout', self.__test_login_logout, self.browser_style)
		success_counter += Helper.test_wrapper('test logged in pages', self.__test_pages_when_logged_in, self.browser_style)
		success_counter += Helper.test_wrapper('test popups', self.__test_popups, self.browser_style)
		success_counter += Helper.test_wrapper('test contact formular', self.__test_contact_formular, self.browser_style)
		success_counter += Helper.test_wrapper('test language switch', self.__test_language_switch, self.browser_style)
		success_counter += Helper.test_wrapper('test discussion buttons', self.__test_discussion_buttons, self.browser_style)
		success_counter += Helper.test_wrapper('test demo discussion', self.__test_demo_discussion, self.browser_style)
		success_counter += Helper.test_wrapper('test demo discussion', self.__test_functions_while_discussion, self.browser_style)
		end = time.time()
		diff = str(end - start)
		diff = diff[0:diff.index('.') + 3]
		print('====================================================')
		print('Failed ' + str(testcounter - success_counter) + ' out of ' + str(testcounter) + ' in ' + str(diff) + 's')

	def __check_for_server(self):
		"""
		Checks whether the server if online
		:return: true when the server is on, false otherwise
		"""
		b = Browser(self.browser_style)
		self.browser = b
		try:
			print('Is server online?')
			b.visit(mainpage)
			success = Helper().check_for_present_text(b, 'part of the graduate school', 'check main page')
			b.quit()
			self.browser = None
			print('    --> SUCCESS' if success else '    --> FAIL')
			print('')
			return success
		except ConnectionResetError:
			print('    --> FAIL')
			print('')
			b.quit()
			self.browser = None
			return False
		except ConnectionRefusedError:
			print('    --> FAIL')
			print('')
			b.quit()
			self.browser = None
			return False

	def __test_pages_when_not_logged_in(self, browser):
		"""
		Checks pages
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print('Starting tests for pages_not_logged_in:')
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
		print('Starting tests for login_logout:')
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
		print('Starting tests for pages_logged_in:')
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
		print('Starting tests for popups:')
		b = Browser(browser)
		self.browser = b
		b.visit(mainpage)

		# open author popup
		b.find_by_id('link_popup_author').click()
		success = Helper().check_for_present_text(b, 'About me', 'check for author text')
		close = b.find_by_name('popup_author_icon_close')
		close.click()

		time.sleep(waittime)

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
		print('Starting tests for contact_formular:')
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
		print('Starting tests for language_switch:')
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
		print('Starting tests for discussion_buttons:')
		b = Browser(browser)
		self.browser = b
		success = True
		h = Helper()
		b = h.login(b, 'tobias', 'tobias', mainpage + 'discussion')

		# check url popup
		b.find_by_id('share-url').click()
		success = success and h.check_for_present_text(b, 'Share your URL', 'check for share url popup')
		b.find_by_id('popup-url-sharing-long-url-button').click()
		success = success and h.check_for_present_text(b, 'discussion', 'check for long url')
		b.find_by_id('popup-url-sharing-close').click()
		time.sleep(waittime)

		# check edit statement popup
		b.find_by_id('edit-statement').click()
		success = success and h.check_for_present_text(b, 'Edit Statements / View Changelog', 'check for edit statements popup')
		b.find_by_id('popup-edit-statement-close').click()
		time.sleep(waittime)

		# check issue dropdown and switch issue
		b.find_by_id('issue-dropdown').click()
		success = success and h.check_for_present_text(b, 'Cat or Dog', 'check for issue dropdown')
		b.find_by_css('.dropdown-menu li.enabled').click()
		success = success and h.check_for_present_text(b, 'Change of discussion', 'check for topic list')
		b.find_by_id('confirm-dialog-checkbox-accept-btn').click()
		time.sleep(waittime)
		success = success and h.check_for_present_text(b, 'Your familiy argues', 'check for switched issue')

		# check finish
		b.find_by_id('finish-button').click()
		success = success and h.check_for_present_text(b, 'Thank you!', 'check for finish button')

		# go back
		b.find_by_id('back-to-discuss-button').click()

		# click position
		success = success and h.check_for_present_text(b, 'What is the initial position', 'check for first step in discussion')
		b.find_by_css('#discussions-space-list li:first-child input').click()
		success = success and h.check_for_present_text(b, 'What do you think', 'check for second step in discussion')

		# restart
		b.find_by_id('discussion-restart-btn').click()
		success = success and h.check_for_present_text(b, 'What is the initial position', 'check for restart')

		b = h.logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_demo_discussion(self, browser):
		"""
		Checks the demo of the discussion. Simple walkthrough.
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print('Starting tests for demo_discussion:')
		success = True
		b = Browser(browser)
		self.browser = b
		h = Helper()
		b = h.login(b, 'tobias', 'tobias', mainpage + 'discussion')

		# position
		success = success and h.check_for_present_text(b, 'initial ', 'check for position')
		b.find_by_id('item_37').click()
		time.sleep(waittime)

		# attitude
		success = success and h.check_for_present_text(b, 'What do you think', 'check for attitude')
		b.find_by_css('#discussions-space-list li:first-child input').click()
		time.sleep(waittime)

		# premise
		success = success and h.check_for_present_text(b, 'most important reason', 'check for premise')
		b.find_by_css('#discussions-space-list li:first-child input').click()
		time.sleep(waittime)

		# confrontation
		success = success and h.check_for_present_text(b, 'Other participants', 'check for confrontatation')
		b.find_by_css('#discussions-space-list li:first-child input').click()
		time.sleep(waittime)

		# justification
		tmp1 = h.check_for_present_text(b, 'most important reason', 'check for justification 1')
		tmp2 = h.check_for_present_text(b, 'Let me enter my reason!', 'check for justification 2')
		success = success and (tmp1 or tmp2)

		# go back
		b.find_by_id('discussion-restart-btn').click()
		success = success and h.check_for_present_text(b, 'initial ', 'check for position again')

		b = h.logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0

	def __test_functions_while_discussion(self, browser):
		"""
		Checks different functions in the discussion like adding one premise, premisegroups and so one
		:param browser: current browser
		:return: 1 if success else 0
		"""
		print('Starting tests for functions_while_discussion:')
		success = True
		b = Browser(browser)
		self.browser = b
		h = Helper()
		b = h.login(b, 'tobias', 'tobias', mainpage + 'discussion')

		# new position
		b.find_by_css('#discussions-space-list li:last-child input').click()
		success = success and h.check_for_present_text(b, 'What is your idea? ', 'check for new position field')
		position = 'some new position ' + str(time.time())
		b.find_by_id('add-statement-container-main-input').fill(position)
		b.find_by_id('send-new-statement').click()
		time.sleep(waittime)

		# attitude
		success = success and h.check_for_present_text(b, 'What do you think about some new position', 'check for attitude')
		b.find_by_css('#discussions-space-list li:first-child input').click()
		time.sleep(waittime)

		# new premise
		success = success and h.check_for_present_text(b, 'Let me enter my reason', 'check for new window premise')
		b.find_by_id('add-premise-container-main-input').fill('some new reason')
		b.find_by_id('send-new-premise').click()
		time.sleep(waittime)

		# confrontation
		success = success and h.check_for_present_text(b, position[1:] + ' because some new reason', 'check for new argument')
		success = success and h.check_for_present_text(b, 'Other participants do not have any counter', 'check that no confrontation exists')
		success = success and h.check_for_present_text(b, 'The discussion ends here', 'check for end text')

		# go back to first premise
		b.find_by_css('#dialog-speech-bubbles-space .triangle-r:first-child a span').click()
		time.sleep(waittime)
		b.find_by_css('#discussions-space-list li:last-child input').click()
		time.sleep(waittime)
		# add new premise
		success = success and h.check_for_present_text(b, 'Let me enter my reason', 'check for new premise window again')
		b.find_by_id('add-premise-container-main-input').fill('some new reason 1 and some new reason 2')
		# add another input field
		b.find_by_css('.icon-add-premise').click()
		time.sleep(waittime)
		b.find_by_id('send-new-premise').click()
		time.sleep(waittime)

		# check for pgroup poup
		success = success and h.check_for_present_text(b, 'We need your help', 'check for pgroup popup')
		b.find_by_id('insert_more_arguments_0').click()
		time.sleep(waittime)
		b.find_by_id('popup-set-premisegroups-send-button').click()
		time.sleep(waittime)

		# check choosing
		success = success and h.check_for_present_text(b, 'multiple reasons', 'check options for choosing ')
		success = success and h.check_for_present_text(b, 'some new reason 1', 'check options for choosing answer 1')
		success = success and h.check_for_present_text(b, 'some new reason 2', 'check options for choosing answer 2')

		b = h.logout(b)
		b.quit()
		self.browser = None
		return 1 if success else 0


browserStyle = 'firefox'
webtests = WebTests(browserStyle)
try:
	webtests.run_all_tests()
except ConnectionResetError as e:
	print('  Server is offline')
