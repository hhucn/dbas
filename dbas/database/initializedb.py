#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import transaction

from dbas.user_management import PasswordHandler
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.discussion_model import User, Argument, Statement, TextVersion, \
	PremiseGroup, Premise, Group, Issue, Notification, Settings
from dbas.database.news_model import News
from dbas.database.api_model import KeywordMapper
from dbas.database import DiscussionBase, NewsBase, APIBase, DBDiscussionSession, DBNewsSession, DBAPISession

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)


def main_discussion(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	discussion_engine = engine_from_config(settings, 'sqlalchemy-discussion.')
	DBDiscussionSession.configure(bind=discussion_engine)
	DiscussionBase.metadata.create_all(discussion_engine)

	with transaction.manager:
		setup_discussion_database()
		transaction.commit()


def main_news(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	news_engine = engine_from_config(settings, 'sqlalchemy-news.')
	DBNewsSession.configure(bind=news_engine)
	NewsBase.metadata.create_all(news_engine)

	with transaction.manager:
		setup_news_db()
		transaction.commit()


def main_api(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	api_engine = engine_from_config(settings, 'sqlalchemy-api.')
	DBAPISession.configure(bind=api_engine)
	APIBase.metadata.create_all(api_engine)

	with transaction.manager:
		setup_api_db()
		transaction.commit()


def setup_api_db():
	# adding data
	mapping1 = KeywordMapper(url='http://localhost:4284/discuss/cat-or-dog', keyword='Cat', issue_uid=1)
	mapping2 = KeywordMapper(url='http://localhost:4284/discuss/cat-or-dog', keyword='Dog', issue_uid=1)
	DBAPISession.add_all([mapping1, mapping2])
	DBAPISession.flush()

def setup_news_db():
	news01 = News(title='Anonymous users after vacation',
				  date='24.09.2015',
				  author='Tobias Krauthoff',
				  news='After two and a half week of vacation we have a new feature. The discussion is now available for anonymous ' +
				       'users, therefore everyone can participate, but only registered users can make and edit statements.')
	news02 = News(title='Vacation done',
				  date='23.09.2015',
				  author='Tobias Krauthoff',
				  news='After two and a half weeks of vacation a new feature was done. Hence anonymous users can participate, the ' +
				       'discussion is open for all, but commiting end editing statements is for registeres users only.')
	news03 = News(title='New URL-Schemes',
				  date='01.09.2015',
				  author='Tobias Krauthoff',
				  news='Now D-BAS has unique urls for the discussion, therefore these urls can be shared.')
	news04 = News(title='Long time, no see!',
				  date='31.08.2015',
				  author='Tobias Krauthoff',
				  news='In the mean time we have developed a new, better, more logically data structure. Additionally the navigation ' +
				       'was refreshed.')
	news05 = News(title='i18n/l10n',
				  date='28.07.2015',
				  author='Tobias Krauthoff',
				  news='Internationalization is now working :)')
	news06 = News(title='i18n',
				  date='22.07.2015',
				  author='Tobias Krauthoff',
				  news='Still working on i18n-problems of chameleon templates due to lingua. If this is fixed, i18n of jQuery will ' +
				       'happen. Afterwards l10n will take place.')
	news07 = News(title='Design & Research',
				  date='13.07.2015',
				  author='Tobias Krauthoff',
				  news='D-BAS is still under construction. Meanwhile the index page was recreated and we are improving our algorithm for ' +
				       'the guided view mode. Next to this we are inventing a bunch of metrics for measuring the quality of discussion ' +
				       'in several software programs.')
	news08 = News(title='Session Management / CSRF',
				  date='25.06.2015',
				  author='Tobias Krauthoff',
				  news='D-BAS is no able to manage a session as well as it has protection against CSRF.')
	news09 = News(title='Edit/Changelog',
				  date='24.06.2015',
				  author='Tobias Krauthoff',
				  news='Now, each user can edit positions and arguments. All changes will be saved and can be watched. Future work is ' +
				       'the chance to edit the relations between positions.')
	news10 = News(title='Simple Navigation was improved',
				  date='19.06.2015',
				  author='Tobias Krauthoff',
				  news='Because the first kind of navigation was finished recently, D-BAS is now dynamically. That means, that each user ' +
				       'can add positions and arguments on his own.<br><i>Open issues</i> are i18n, a framework for JS-tests as well as ' +
				       'the content of the popups.')
	news11 = News(title='Simple Navigation ready',
				  date='09.06.2015',
				  author='Tobias Krauthoff',
				  news='First beta of D-BAS navigation is now ready. Within this kind the user will be permantly confronted with ' +
				       'arguments, which have a attack relation to the current selected argument/position. For an justification the user ' +
				       'can select out of all arguments, which have a attack relation to the \'attacking\' argument. Unfortunately the ' +
				       'support-relation are currently useless except for the justification for the position at start.')
	news12 = News(title='Workshop',
				  date='27.05.2015',
				  author='Tobias Krauthoff',
				  news='Today: A new workshop at the O.A.S.E. :)')
	news13 = News(title='Admin Interface',
				  date='29.05.2015',
				  author='Tobias Krauthoff',
				  news='Everything is growing, we have now a little admin interface and a navigation for the discussion is finshed, ' +
				       'but this is very basic and simple')
	news14 = News(title='Sharing',
				  date='27.05.2015',
				  author='Tobias Krauthoff',
				  news='Every news can now be shared via FB, G+, Twitter and Mail. Not very important, but in some kind it is...')
	news15 = News(title='Tests and JS',
				  date='26.05.2015',
				  author='Tobias Krauthoff',
				  news='Front-end tests with Splinter are now finished. They are great and easy to manage. Additionally I\'am working ' +
				       'on JS, so we can navigate in a static graph. Next to this, the I18N is waiting...')
	news16 = News(title='JS Starts',
				  date='18.05.2015',
				  author='Tobias Krauthoff',
				  news='Today started the funny part about the dialog based part, embedded in the content page.')
	news18 = News(title='No I18N + L10N',
				  date='18.05.2015',
				  author='Tobias Krauthoff',
				  news='Interationalization and localization is much more diffult than described by the pyramid. This has something todo ' +
				       'with Chameleon 2, Lingua and Babel, so this feature has to wait.')
	news19 = News(title='I18N + L10N',
				  date='12.05.2015',
				  author='Tobias Krauthoff',
				  news='D-BAS, now with internationalization and translation.')
	news20 = News(title='Settings',
				  date='10.05.2015',
				  author='Tobias Krauthoff',
				  news='New part of the website is finished: a settings page for every user.')
	news21 = News(title='About the Workshop in Karlsruhe',
				  date='09.05.2015',
				  author='Tobias Krauthoff',
				  news='The workshop was very interesting. We have had very interesting talks and got much great feedback vom Jun.-Prof. ' +
				       'Dr. Betz and Mr. Voigt. A repetition will be planed for the middle of july.')
	news22 = News(title='Workshop in Karlsruhe',
				  date='07.05.2015',
				  author='Tobias Krauthoff',
				  news='The working group \'functionality\' will drive to Karlsruhe for a workshop with Jun.-Prof. Dr. Betz as well as ' +
				       'with C. Voigt until 08.05.2015. Our main topics will be the measurement of quality of discussions and the design of ' +
				       'online-participation. I think, this will be very interesting!')
	news23 = News(title='System will be build up',
				  date='01.05.2015',
				  author='Tobias Krauthoff',
				  news='Currently I am working a lot at the system. This work includes:<br><ul><li>frontend-design with CSS and ' +
				       'jQuery</li><li>backend-development with pything</li><li>development of unit- and integration tests</li><li>a ' +
				       'database scheme</li><li>validating and deserializing data with ' +
				       '<a href="http://docs.pylonsproject.org/projects/colander/en/latest/">Colander</a></li><li>translating string ' +
				       'with <a href="http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html#localization-deployment-settings">internationalization</a></li></ul>')
	news24 = News(title='First set of tests',
				  date='06.05.2015',
				  author='Tobias Krauthoff',
				  news='Finished first set of unit- and integration tests for the database and frontend.')
	news25 = News(title='Page is growing',
				  date='05.05.2015',
				  author='Tobias Krauthoff',
				  news='The contact page is now working as well as the password-request option.')
	news26 = News(title='First mockup',
				  date='01.05.2015',
				  author='Tobias Krauthoff',
				  news='The webpage has now a contact, login and register site.')
	news27 = News(title='Start',
				  date='14.04.2015',
				  author='Tobias Krauthoff',
				  news='I\'ve started with the Prototype.')
	news28 = News(title='First steps',
				  date='01.12.2014',
				  author='Tobias Krauthoff',
				  news='I\'ve started with with my PhD.')
	news29 = News(title='New logic for inserting',
				  date='14.10.2015',
				  author='Tobias Krauthoff',
				  news='Logic for inserting statements was redone. Everytime, where the user can add information via a textarea, '
				       'only the area is visible, which is logically correct. Therefore the decisions are based on argumentations theory.')
	news30 = News(title='Different topics',
				  date='15.10.2015',
				  author='Tobias Krauthoff',
				  news='Since today we can switch between different topics :) Unfortunately this feature is not really tested ;-)')
	news31 = News(title='Stable release',
				  date='10.11.2015',
				  author='Tobias Krauthoff',
				  news='After two weeks of debugging, a first and stable version is online. Now we can start with the interessing things!')
	news32 = News(title='Design Update',
				  date='11.11.2015',
				  author='Tobias Krauthoff',
				  news='Today we released a new material-oriented design. Enjoy it!')
	news33 = News(title='Improved Bootstrapping',
				  date='16.11.2015',
				  author='Tobias Krauthoff',
				  news='Bootstraping is one of the main challenges in discussion. Therefore we have a two-step process for this task!')
	news34 = News(title='Breadcrumbs',
				  date='24.11.2015',
				  author='Tobias Krauthoff',
				  news='Now we have a breadcrumbs with shortcuts for every step in our discussion. This feature will be im improved soon!')
	news35 = News(title='Logic improvements',
				  date='01.12.2015',
				  author='Tobias Krauthoff',
				  news='Every week we try to improve the look and feel of the discussions navigation. Sometimes just a few words are '
				       'edited, but on other day the logic itself gets an update. So keep on testing :)')
	news36 = News(title='Piwik',
				  date='08.12.2015',
				  author='Tobias Krauthoff',
				  news='Today Piwik was installed. It will help to improve the services of D-BAS!')
	news37 = News(title='Happy new Year',
				  date='01.01.2016',
				  author='Tobias Krauthoff',
				  news='Frohes Neues Jahr ... Bonne Annee ... Happy New Year ... Feliz Ano Nuevo ... Feliz Ano Novo')
	news38 = News(title='Island View and Pictures',
				  date='06.01.2016',
				  author='Tobias Krauthoff',
				  news='DBAS will be more personal and results driven. Therefore the new release has profile pictures for '
				       'everyone. They are powered by gravatar and are based on a md5-hash of the users email. Next to this '
				       'a new view was published - the island view. Do not be shy and try it in discussions ;-) Last '
				       'improvement just collects the attacks and supports for arguments...this is needed for our next big '
				       'thing :) Stay tuned!')
	news39 = News(title='Refactoring',
				  date='27.01.2016',
				  author='Tobias Krauthoff',
				  news='DBAS refactored the last two weeks. During this time, a lot of JavaScript was removed. Therefore '
				       'DBAS uses Chameleon with TAL in the Pyramid-Framework. So DBAS will be more stable and faster. '
				       'The next period all functions will be tested and recovered.')
	news40 = News(title='API',
				  date='29.01.2016',
				  author='Tobias Krauthoff',
				  news='Now DBAS has a API. Just replace the "discuss"-tag in your url with api to get your current steps raw data.')
	news41 = News(title='Voting Model',
				  date='05.01.2016',
				  author='Tobias Krauthoff',
				  news='Currently we are improving out model of voting for arguments as well as statements. Therefore we are working'
				       'together with our colleage out of the theoretical computer science...because DBAS datastructure can be '
				       'formalized to be compatible with frameworks of Dung.')
	news42 = News(title='Premisegroups',
				  date='09.02.2016',
				  author='Tobias Krauthoff',
				  news='Now we have a mechanism for unclear statements. For example the user enters "I want something because '
				       'A and B". The we do not know, whether A and B must hold at the same time, or if she wants something '
				       'when A or B holds.')
	news43 = News(title='Notification System',
				  date='16.02.2016',
				  author='Tobias Krauthoff',
				  news='Yesterday we have develope a minimal notification system. This system could send information to every author, '
				       'if one of their statement was edited. More features are comming soon')
	news_array = [news01, news02, news03, news04, news05, news06, news07, news08, news09, news10,
	              news11, news12, news13, news14, news15, news16, news29, news18, news19, news20,
	              news21, news22, news23, news24, news25, news26, news27, news28, news30, news31,
	              news32, news33, news34, news35, news36, news37, news38, news39, news40, news41,
	              news42, news43]
	DBNewsSession.add_all(news_array[::-1])
	DBNewsSession.flush()


def setup_discussion_database():
	# adding our main issue
	issue1 = Issue(title='Cat or Dog', info='Your familiy argues about whether to buy a cat or dog as pet. Now your opinion matters!')
	issue2 = Issue(title='Town cuts spending', info='Our town needs to cut spending. Please discuss ideas how this should be done.')
	issue3 = Issue(title='Make the world better', info='How can we make this world a better place?')
	DBDiscussionSession.add_all([issue1, issue2, issue3])
	DBDiscussionSession.flush()

	# adding groups
	group0 = Group(name='admins')
	group1 = Group(name='authors')
	group2 = Group(name='editors')
	group3 = Group(name='users')
	DBDiscussionSession.add_all([group0, group1, group2, group3])
	DBDiscussionSession.flush()

	# adding some dummy users
	pwhandler = PasswordHandler()
	pw0 = pwhandler.get_hashed_password('QMuxpuPXwehmhm2m93#I;)QX§u4qjqoiwhebakb)(4hkblkb(hnzUIQWEGgalksd')
	pw1 = pwhandler.get_hashed_password('admin')
	pw2 = pwhandler.get_hashed_password('tobias')
	pw3 = pwhandler.get_hashed_password('martin')
	pw4 = pwhandler.get_hashed_password('kalman')
	pw5 = pwhandler.get_hashed_password('mladen')
	pw6 = pwhandler.get_hashed_password('drtobias')
	pw7 = pwhandler.get_hashed_password('michael')
	pw8 = pwhandler.get_hashed_password('gregor')
	pw9 = pwhandler.get_hashed_password('christian')
	pw10 = pwhandler.get_hashed_password('alexander')
	pw11 = pwhandler.get_hashed_password('raphael')
	user0 = User(firstname='anonymous', surname='anonymous', nickname='anonymous', email='', password=pw0, group=group3.uid, gender='m')
	user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas.hhu@gmail.com', password=pw1, group=group0.uid, gender='m')
	user2 = User(firstname='Tobias', surname='Krauthoff', nickname='tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2, group=group1.uid, gender='m')
	user3 = User(firstname='Martin', surname='Mauve', nickname='martin', email='mauve@cs.uni-duesseldorf', password=pw3, group=group2.uid, gender='m')
	user4 = User(firstname='Kalman', surname='Graffi', nickname='kalman', email='graffi@cs.uni-duesseldorf.de', password=pw4, group=group2.uid, gender='m')
	user5 = User(firstname='Mladen', surname='Topic', nickname='mladen', email='mladen.topic@hhu.de', password=pw5, group=group2.uid, gender='m')
	user6 = User(firstname='Tobias', surname='Escher', nickname='drtobias', email='tobias.escher@hhu.de', password=pw6, group=group2.uid, gender='m')
	user7 = User(firstname='Michael', surname='Baurmann', nickname='michael', email='baurmann@hhu.de', password=pw7, group=group2.uid, gender='m')
	user8 = User(firstname='Gregor', surname='Betz', nickname='gregor', email='gregor.betz@kit.edu', password=pw8, group=group2.uid, gender='m')
	user9 = User(firstname='Christian', surname='Meter', nickname='christian', email='meter@cs.uni-duesseldorf.de', password=pw9, group=group2.uid, gender='m')
	user10 = User(firstname='Alexander', surname='Schneider', nickname='alexander', email='aschneider@cs.uni-duesseldorf.de', password=pw10, group=group2.uid, gender='m')
	user11 = User(firstname='Raphael', surname='Bialon', nickname='raphael', email='bialon@cs.uni-duesseldorf.de', password=pw11, group=group2.uid, gender='m')
	DBDiscussionSession.add_all([user0, user1, user2, user3, user4, user5, user6, user7, user8, user9, user10, user11])
	DBDiscussionSession.flush()

	# adding settings
	settings0 = Settings(author_uid=user0.uid, send_mails=True, send_notifications=True)
	settings1 = Settings(author_uid=user1.uid, send_mails=True, send_notifications=True)
	settings2 = Settings(author_uid=user2.uid, send_mails=True, send_notifications=True)
	settings3 = Settings(author_uid=user3.uid, send_mails=True, send_notifications=True)
	settings4 = Settings(author_uid=user4.uid, send_mails=True, send_notifications=True)
	settings5 = Settings(author_uid=user5.uid, send_mails=True, send_notifications=True)
	settings6 = Settings(author_uid=user6.uid, send_mails=True, send_notifications=True)
	settings7 = Settings(author_uid=user7.uid, send_mails=True, send_notifications=True)
	settings8 = Settings(author_uid=user8.uid, send_mails=True, send_notifications=True)
	settings9 = Settings(author_uid=user9.uid, send_mails=True, send_notifications=True)
	settings10 = Settings(author_uid=user10.uid, send_mails=True, send_notifications=True)
	settings11 = Settings(author_uid=user11.uid, send_mails=True, send_notifications=True)
	DBDiscussionSession.add_all([settings0, settings1, settings2, settings3, settings4, settings5, settings6, settings7,
	                             settings8, settings9, settings10, settings11])
	DBDiscussionSession.flush()

	# Adding welcome notifications
	notification0 = Notification(from_author_uid=user1.uid, to_author_uid=user2.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification1 = Notification(from_author_uid=user1.uid, to_author_uid=user3.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification2 = Notification(from_author_uid=user1.uid, to_author_uid=user4.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification3 = Notification(from_author_uid=user1.uid, to_author_uid=user5.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification4 = Notification(from_author_uid=user1.uid, to_author_uid=user6.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification5 = Notification(from_author_uid=user1.uid, to_author_uid=user7.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification6 = Notification(from_author_uid=user1.uid, to_author_uid=user8.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification7 = Notification(from_author_uid=user1.uid, to_author_uid=user9.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification8 = Notification(from_author_uid=user1.uid, to_author_uid=user10.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	notification9 = Notification(from_author_uid=user1.uid, to_author_uid=user11.uid, topic='Welcome', content='Welcome to the novel dialog-based argumentation system...')
	DBDiscussionSession.add_all([notification0, notification1, notification2, notification3, notification4,
	                             notification5, notification6, notification7, notification8, notification9])
	DBDiscussionSession.flush()

	# Adding all textversions
	textversion1 = TextVersion(content="We should get a cat.", author=user2.uid)
	textversion2 = TextVersion(content="We should get a dog.", author=user2.uid)
	textversion3 = TextVersion(content="We could get both, a cat and a dog.", author=user2.uid)
	textversion4 = TextVersion(content="Cats are very independent.", author=user2.uid)
	textversion5 = TextVersion(content="Cats are capricious.", author=user2.uid)
	textversion6 = TextVersion(content="Dogs can act as watch dogs.", author=user2.uid)
	textversion7 = TextVersion(content="You have to take the dog for a walk every day, which is tedious.", author=user2.uid)
	textversion8 = TextVersion(content="We have no use for a watch dog.", author=user2.uid)
	textversion9 = TextVersion(content="Going for a walk with the dog every day is good for social interaction and physical exercise.", author=user2.uid)
	textversion10 = TextVersion(content="It would be no problem.", author=user2.uid)
	textversion11 = TextVersion(content="A cat and a dog will generally not get along well.", author=user2.uid)
	textversion12 = TextVersion(content="We do not have enough money for two pets.", author=user2.uid)
	textversion13 = TextVersion(content="A dog costs taxes and will be more expensive than a cat.", author=user2.uid)
	textversion14 = TextVersion(content="Cats are fluffy.", author=user2.uid)
	textversion15 = TextVersion(content="Cats are small.", author=user2.uid)
	textversion16 = TextVersion(content="Fluffy animals losing much hair and I'm allergic to animal hair.", author=user2.uid)
	textversion17 = TextVersion(content="You could use a automatic vacuum cleaner.", author=user2.uid)
	textversion18 = TextVersion(content="Cats ancestors are animals in wildlife, who are hunting alone and not in groups.", author=user2.uid)
	textversion19 = TextVersion(content="This is not true for overbred races.", author=user2.uid)
	textversion20 = TextVersion(content="This lies in their the natural conditions.", author=user2.uid)
	textversion21 = TextVersion(content="The purpose of a pet is to have something to take care of.", author=user2.uid)
	textversion22 = TextVersion(content="Several cats of friends of mine are real as*holes.", author=user2.uid)
	textversion23 = TextVersion(content="The fact, that cats are capricious, is based on the cats race.", author=user2.uid)
	textversion24 = TextVersion(content="Not every cat is capricious.", author=user2.uid)
	textversion25 = TextVersion(content="This is based on the cats race and a little bit on the breeding.", author=user2.uid)
	textversion26 = TextVersion(content="Next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on.", author=user2.uid)
	textversion27 = TextVersion(content="The equipment for running costs of cats and dogs are nearly the same.", author=user2.uid)
	textversion29 = TextVersion(content="This is just a claim without any justification.", author=user2.uid)
	textversion30 = TextVersion(content="In Germany you have to pay for your second dog even more taxes!", author=user2.uid)
	textversion31 = TextVersion(content="It is important, that pets are small and fluffy!", author=user2.uid)
	textversion32 = TextVersion(content="Cats are little, sweet and innocent cuddle toys.", author=user2.uid)
	textversion33 = TextVersion(content="Do you have ever seen a sphinx cat or savannah cats?", author=user2.uid)
	textversion34 = TextVersion(content="This is for debugging, so that A29 exists with S34 attacks A12", author=user2.uid)
	textversion35 = TextVersion(content="This is for debugging, so that A30 exists with S35 attacks A13", author=user2.uid)
	textversion36 = TextVersion(content="This is for debugging, so that A31 exists with S36 attacks A14", author=user2.uid)
	textversion37 = TextVersion(content="This is for debugging, so that A32 exists with S37 attacks A15", author=user2.uid)
	textversion38 = TextVersion(content="This is for debugging, so that A33 exists with S38 attacks A16", author=user2.uid)
	textversion39 = TextVersion(content="This is for debugging, so that A34 exists with S39 attacks A17", author=user2.uid)
	textversion40 = TextVersion(content="This is for debugging, so that A35 exists with S40 attacks A18", author=user2.uid)
	textversion41 = TextVersion(content="This is for debugging, so that A36 exists with S41 attacks A19", author=user2.uid)
	textversion42 = TextVersion(content="This is for debugging, so that A37 exists with S42 attacks A20", author=user2.uid)
	textversion43 = TextVersion(content="This is for debugging, so that A38 exists with S43 attacks A21", author=user2.uid)
	textversion44 = TextVersion(content="This is for debugging, so that A39 exists with S44 attacks A22", author=user2.uid)
	textversion45 = TextVersion(content="This is for debugging, so that A40 exists with S45 attacks A23", author=user2.uid)
	textversion46 = TextVersion(content="This is for debugging, so that A41 exists with S46 attacks A24", author=user2.uid)
	textversion47 = TextVersion(content="This is for debugging, so that A42 exists with S47 attacks A25", author=user2.uid)
	textversion48 = TextVersion(content="This is for debugging, so that A43 exists with S48 attacks A26", author=user2.uid)
	textversion49 = TextVersion(content="This is for debugging, so that A44 exists with S49 attacks A27", author=user2.uid)
	textversion50 = TextVersion(content="This is for debugging, so that A45 exists with S50 attacks A28", author=user2.uid)
	textversion51 = TextVersion(content="This is for debugging, so that A46 exists with S51 supports A12", author=user2.uid)
	textversion52 = TextVersion(content="This is for debugging, so that A47 exists with S52 supports A13", author=user2.uid)
	textversion53 = TextVersion(content="This is for debugging, so that A48 exists with S53 supports A14", author=user2.uid)
	textversion54 = TextVersion(content="This is for debugging, so that A49 exists with S54 supports A15", author=user2.uid)
	textversion55 = TextVersion(content="This is for debugging, so that A50 exists with S55 supports A16", author=user2.uid)
	textversion56 = TextVersion(content="This is for debugging, so that A51 exists with S56 supports A17", author=user2.uid)
	textversion57 = TextVersion(content="This is for debugging, so that A52 exists with S57 supports A18", author=user2.uid)
	textversion58 = TextVersion(content="This is for debugging, so that A53 exists with S58 supports A19", author=user2.uid)
	textversion59 = TextVersion(content="This is for debugging, so that A54 exists with S59 supports A20", author=user2.uid)
	textversion60 = TextVersion(content="This is for debugging, so that A55 exists with S60 supports A21", author=user2.uid)
	textversion61 = TextVersion(content="This is for debugging, so that A56 exists with S61 supports A22", author=user2.uid)
	textversion62 = TextVersion(content="This is for debugging, so that A57 exists with S62 supports A23", author=user2.uid)
	textversion63 = TextVersion(content="This is for debugging, so that A58 exists with S63 supports A24", author=user2.uid)
	textversion64 = TextVersion(content="This is for debugging, so that A59 exists with S64 supports A25", author=user2.uid)
	textversion65 = TextVersion(content="This is for debugging, so that A60 exists with S65 supports A26", author=user2.uid)
	textversion66 = TextVersion(content="This is for debugging, so that A61 exists with S66 supports A27", author=user2.uid)
	textversion67 = TextVersion(content="This is for debugging, so that A62 exists with S67 supports A28", author=user2.uid)
	textversion68 = TextVersion(content="For debugging argument 63. Thus this attacks 'Fluffy animals losing much hai[...]'", author=user2.uid)
	textversion69 = TextVersion(content="For debugging argument 64. Thus this attacks 'You could use a automatic vacu[...]'", author=user2.uid)
	textversion70 = TextVersion(content="For debugging argument 65. Thus this attacks 'Cats ancestors are animals in [...]'", author=user2.uid)
	textversion71 = TextVersion(content="Even overbred races can be taught.", author=user2.uid)
	textversion72 = TextVersion(content="For debugging argument 67. Thus this attacks 'This lies in their the natural[...]'", author=user2.uid)
	textversion73 = TextVersion(content="Several pets are nice to have and you do not have to take much care of them, for example turtles or cats, which are living outside.", author=user2.uid)
	textversion74 = TextVersion(content="For debugging argument 69. Thus this attacks 'Several cats of friends of min[...]'", author=user2.uid)
	textversion75 = TextVersion(content="For debugging argument 70. Thus this attacks 'This fact is based on the cats[...]'", author=user2.uid)
	textversion76 = TextVersion(content="For debugging argument 71. Thus this attacks 'All cats of my friends are cap[...]'", author=user2.uid)
	textversion77 = TextVersion(content="For debugging argument 72. Thus this attacks 'This is based on the cats race[...]'", author=user2.uid)
	textversion78 = TextVersion(content="For debugging argument 73. Thus this attacks 'Next to the taxes you will nee[...]'", author=user2.uid)
	textversion79 = TextVersion(content="For debugging argument 74. Thus this attacks 'The equipment for running cost[...]'", author=user2.uid)
	textversion80 = TextVersion(content="For debugging argument 75. Thus this attacks 'This is just a claim without a[...]'", author=user2.uid)
	textversion81 = TextVersion(content="For debugging argument 76. Thus this attacks 'In Germany you have to pay for[...]'", author=user2.uid)
	textversion82 = TextVersion(content="For debugging argument 77. Thus this attacks 'It is important, that pets are[...]'", author=user2.uid)
	textversion83 = TextVersion(content="For debugging argument 78. Thus this attacks 'Cats are little, sweet and inn[...]'", author=user2.uid)
	textversion84 = TextVersion(content="For debugging argument 79. Thus this attacks 'Do you have ever seen a sphinx[...]'", author=user2.uid)
	textversion85 = TextVersion(content="For debugging argument 80. Thus this supports 'Fluffy animals losing much hai[...]'", author=user2.uid)
	textversion86 = TextVersion(content="For debugging argument 81. Thus this supports 'You could use a automatic vacu[...]'", author=user2.uid)
	textversion87 = TextVersion(content="For debugging argument 82. Thus this supports 'Cats ancestors are animals in [...]'", author=user2.uid)
	textversion88 = TextVersion(content="For debugging argument 83. Thus this supports 'This is not true for overbred [...]'", author=user2.uid)
	textversion89 = TextVersion(content="For debugging argument 84. Thus this supports 'This lies in their the natural[...]'", author=user2.uid)
	textversion90 = TextVersion(content="For debugging argument 85. Thus this supports 'The purpose of a pet is to hav[...]'", author=user2.uid)
	textversion91 = TextVersion(content="For debugging argument 86. Thus this supports 'Several cats of friends of min[...]'", author=user2.uid)
	textversion92 = TextVersion(content="For debugging argument 87. Thus this supports 'This fact is based on the cats[...]'", author=user2.uid)
	textversion93 = TextVersion(content="For debugging argument 88. Thus this supports 'All cats of my friends are cap[...]'", author=user2.uid)
	textversion94 = TextVersion(content="For debugging argument 89. Thus this supports 'This is based on the cats race[...]'", author=user2.uid)
	textversion95 = TextVersion(content="For debugging argument 90. Thus this supports 'Next to the taxes you will nee[...]'", author=user2.uid)
	textversion96 = TextVersion(content="For debugging argument 91. Thus this supports 'The equipment for running cost[...]'", author=user2.uid)
	textversion97 = TextVersion(content="For debugging argument 92. Thus this supports 'This is just a claim without a[...]'", author=user2.uid)
	textversion98 = TextVersion(content="For debugging argument 93. Thus this supports 'In Germany you have to pay for[...]'", author=user2.uid)
	textversion99 = TextVersion(content="For debugging argument 94. Thus this supports 'It is important, that pets are[...]'", author=user2.uid)
	textversion100 = TextVersion(content="For debugging argument 95. Thus this supports 'Cats are little, sweet and inn[...]'", author=user2.uid)
	textversion101 = TextVersion(content="For debugging argument 96. Thus this supports 'Do you have ever seen a sphinx[...]'", author=user2.uid)

	textversion102 = TextVersion(content="We should shut down university park.", author=user2.uid)
	textversion103 = TextVersion(content="Shutting down university park will save 100.000$ a year.", author=user2.uid)
	textversion104 = TextVersion(content="Criminals use university park to sell drugs.", author=user2.uid)
	textversion105 = TextVersion(content="We should not give in to criminals.", author=user2.uid)
	textversion106 = TextVersion(content="We should close public swimming pools.", author=user2.uid)
	textversion107 = TextVersion(content="The mayor should increase the taxes", author=user2.uid)
	textversion108 = TextVersion(content="The number of police patrols should be increased.", author=user2.uid)

	textversion109 = TextVersion(content="It is much work to take care of both animals.", author=user2.uid)

	DBDiscussionSession.add_all([textversion1, textversion2, textversion3, textversion4, textversion5, textversion6, textversion7,
	                             textversion8, textversion9, textversion10, textversion11, textversion12, textversion13, textversion14,
	                             textversion15, textversion16, textversion17, textversion18, textversion19, textversion20, textversion21,
	                             textversion22, textversion23, textversion24, textversion25, textversion26, textversion27, textversion29,
	                             textversion30, textversion31, textversion32, textversion33, textversion34, textversion35, textversion36,
	                             textversion37, textversion38, textversion39, textversion40, textversion41, textversion42, textversion43,
	                             textversion44, textversion45, textversion46, textversion47, textversion48, textversion49, textversion50,
	                             textversion51, textversion52, textversion53, textversion54, textversion55, textversion56, textversion57,
	                             textversion58, textversion59, textversion60, textversion61, textversion62, textversion63, textversion64,
	                             textversion65, textversion66, textversion67, textversion68, textversion69, textversion70, textversion71,
	                             textversion72, textversion73, textversion74, textversion75, textversion76, textversion77, textversion78,
	                             textversion79, textversion80, textversion81, textversion82, textversion83, textversion84, textversion85,
	                             textversion86, textversion87, textversion88, textversion89, textversion90, textversion91, textversion92,
	                             textversion93, textversion94, textversion95, textversion96, textversion97, textversion98, textversion99,
	                             textversion100, textversion101, textversion102, textversion103, textversion104, textversion105,
	                             textversion106, textversion107, textversion108, textversion109])
	DBDiscussionSession.flush()

	# adding all statements
	statement1 = Statement(textversion=textversion1.uid, is_startpoint=True, issue=issue1.uid)
	statement2 = Statement(textversion=textversion2.uid, is_startpoint=True, issue=issue1.uid)
	statement3 = Statement(textversion=textversion3.uid, is_startpoint=True, issue=issue1.uid)
	statement4 = Statement(textversion=textversion4.uid, is_startpoint=False, issue=issue1.uid)
	statement5 = Statement(textversion=textversion5.uid, is_startpoint=False, issue=issue1.uid)
	statement6 = Statement(textversion=textversion6.uid, is_startpoint=False, issue=issue1.uid)
	statement7 = Statement(textversion=textversion7.uid, is_startpoint=False, issue=issue1.uid)
	statement8 = Statement(textversion=textversion8.uid, is_startpoint=False, issue=issue1.uid)
	statement9 = Statement(textversion=textversion9.uid, is_startpoint=False, issue=issue1.uid)
	statement10 = Statement(textversion=textversion10.uid, is_startpoint=False, issue=issue1.uid)
	statement11 = Statement(textversion=textversion11.uid, is_startpoint=False, issue=issue1.uid)
	statement12 = Statement(textversion=textversion12.uid, is_startpoint=False, issue=issue1.uid)
	statement13 = Statement(textversion=textversion13.uid, is_startpoint=False, issue=issue1.uid)
	statement14 = Statement(textversion=textversion14.uid, is_startpoint=False, issue=issue1.uid)
	statement15 = Statement(textversion=textversion15.uid, is_startpoint=False, issue=issue1.uid)
	statement16 = Statement(textversion=textversion16.uid, is_startpoint=False, issue=issue1.uid)
	statement17 = Statement(textversion=textversion17.uid, is_startpoint=False, issue=issue1.uid)
	statement18 = Statement(textversion=textversion18.uid, is_startpoint=False, issue=issue1.uid)
	statement19 = Statement(textversion=textversion19.uid, is_startpoint=False, issue=issue1.uid)
	statement20 = Statement(textversion=textversion20.uid, is_startpoint=False, issue=issue1.uid)
	statement21 = Statement(textversion=textversion21.uid, is_startpoint=False, issue=issue1.uid)
	statement22 = Statement(textversion=textversion22.uid, is_startpoint=False, issue=issue1.uid)
	statement23 = Statement(textversion=textversion23.uid, is_startpoint=False, issue=issue1.uid)
	statement24 = Statement(textversion=textversion24.uid, is_startpoint=False, issue=issue1.uid)
	statement25 = Statement(textversion=textversion25.uid, is_startpoint=False, issue=issue1.uid)
	statement26 = Statement(textversion=textversion26.uid, is_startpoint=False, issue=issue1.uid)
	statement27 = Statement(textversion=textversion27.uid, is_startpoint=False, issue=issue1.uid)
	statement29 = Statement(textversion=textversion29.uid, is_startpoint=False, issue=issue1.uid)
	statement30 = Statement(textversion=textversion30.uid, is_startpoint=False, issue=issue1.uid)
	statement31 = Statement(textversion=textversion31.uid, is_startpoint=False, issue=issue1.uid)
	statement32 = Statement(textversion=textversion32.uid, is_startpoint=False, issue=issue1.uid)
	statement33 = Statement(textversion=textversion33.uid, is_startpoint=False, issue=issue1.uid)
	statement34 = Statement(textversion=textversion34.uid, is_startpoint=False, issue=issue1.uid)
	statement35 = Statement(textversion=textversion35.uid, is_startpoint=False, issue=issue1.uid)
	statement36 = Statement(textversion=textversion36.uid, is_startpoint=False, issue=issue1.uid)
	statement37 = Statement(textversion=textversion37.uid, is_startpoint=False, issue=issue1.uid)
	statement38 = Statement(textversion=textversion38.uid, is_startpoint=False, issue=issue1.uid)
	statement39 = Statement(textversion=textversion39.uid, is_startpoint=False, issue=issue1.uid)
	statement40 = Statement(textversion=textversion40.uid, is_startpoint=False, issue=issue1.uid)
	statement41 = Statement(textversion=textversion41.uid, is_startpoint=False, issue=issue1.uid)
	statement42 = Statement(textversion=textversion42.uid, is_startpoint=False, issue=issue1.uid)
	statement43 = Statement(textversion=textversion43.uid, is_startpoint=False, issue=issue1.uid)
	statement44 = Statement(textversion=textversion44.uid, is_startpoint=False, issue=issue1.uid)
	statement45 = Statement(textversion=textversion45.uid, is_startpoint=False, issue=issue1.uid)
	statement46 = Statement(textversion=textversion46.uid, is_startpoint=False, issue=issue1.uid)
	statement47 = Statement(textversion=textversion47.uid, is_startpoint=False, issue=issue1.uid)
	statement48 = Statement(textversion=textversion48.uid, is_startpoint=False, issue=issue1.uid)
	statement49 = Statement(textversion=textversion49.uid, is_startpoint=False, issue=issue1.uid)
	statement50 = Statement(textversion=textversion50.uid, is_startpoint=False, issue=issue1.uid)
	statement51 = Statement(textversion=textversion51.uid, is_startpoint=False, issue=issue1.uid)
	statement52 = Statement(textversion=textversion52.uid, is_startpoint=False, issue=issue1.uid)
	statement53 = Statement(textversion=textversion53.uid, is_startpoint=False, issue=issue1.uid)
	statement54 = Statement(textversion=textversion54.uid, is_startpoint=False, issue=issue1.uid)
	statement55 = Statement(textversion=textversion55.uid, is_startpoint=False, issue=issue1.uid)
	statement56 = Statement(textversion=textversion56.uid, is_startpoint=False, issue=issue1.uid)
	statement57 = Statement(textversion=textversion57.uid, is_startpoint=False, issue=issue1.uid)
	statement58 = Statement(textversion=textversion58.uid, is_startpoint=False, issue=issue1.uid)
	statement59 = Statement(textversion=textversion59.uid, is_startpoint=False, issue=issue1.uid)
	statement60 = Statement(textversion=textversion60.uid, is_startpoint=False, issue=issue1.uid)
	statement61 = Statement(textversion=textversion61.uid, is_startpoint=False, issue=issue1.uid)
	statement62 = Statement(textversion=textversion62.uid, is_startpoint=False, issue=issue1.uid)
	statement63 = Statement(textversion=textversion63.uid, is_startpoint=False, issue=issue1.uid)
	statement64 = Statement(textversion=textversion64.uid, is_startpoint=False, issue=issue1.uid)
	statement65 = Statement(textversion=textversion65.uid, is_startpoint=False, issue=issue1.uid)
	statement66 = Statement(textversion=textversion66.uid, is_startpoint=False, issue=issue1.uid)
	statement67 = Statement(textversion=textversion67.uid, is_startpoint=False, issue=issue1.uid)
	statement68 = Statement(textversion=textversion68.uid, is_startpoint=False, issue=issue1.uid)
	statement69 = Statement(textversion=textversion69.uid, is_startpoint=False, issue=issue1.uid)
	statement70 = Statement(textversion=textversion70.uid, is_startpoint=False, issue=issue1.uid)
	statement71 = Statement(textversion=textversion71.uid, is_startpoint=False, issue=issue1.uid)
	statement72 = Statement(textversion=textversion72.uid, is_startpoint=False, issue=issue1.uid)
	statement73 = Statement(textversion=textversion73.uid, is_startpoint=False, issue=issue1.uid)
	statement74 = Statement(textversion=textversion74.uid, is_startpoint=False, issue=issue1.uid)
	statement75 = Statement(textversion=textversion75.uid, is_startpoint=False, issue=issue1.uid)
	statement76 = Statement(textversion=textversion76.uid, is_startpoint=False, issue=issue1.uid)
	statement77 = Statement(textversion=textversion77.uid, is_startpoint=False, issue=issue1.uid)
	statement78 = Statement(textversion=textversion78.uid, is_startpoint=False, issue=issue1.uid)
	statement79 = Statement(textversion=textversion79.uid, is_startpoint=False, issue=issue1.uid)
	statement80 = Statement(textversion=textversion80.uid, is_startpoint=False, issue=issue1.uid)
	statement81 = Statement(textversion=textversion81.uid, is_startpoint=False, issue=issue1.uid)
	statement82 = Statement(textversion=textversion82.uid, is_startpoint=False, issue=issue1.uid)
	statement83 = Statement(textversion=textversion83.uid, is_startpoint=False, issue=issue1.uid)
	statement84 = Statement(textversion=textversion84.uid, is_startpoint=False, issue=issue1.uid)
	statement85 = Statement(textversion=textversion85.uid, is_startpoint=False, issue=issue1.uid)
	statement86 = Statement(textversion=textversion86.uid, is_startpoint=False, issue=issue1.uid)
	statement87 = Statement(textversion=textversion87.uid, is_startpoint=False, issue=issue1.uid)
	statement88 = Statement(textversion=textversion88.uid, is_startpoint=False, issue=issue1.uid)
	statement89 = Statement(textversion=textversion89.uid, is_startpoint=False, issue=issue1.uid)
	statement90 = Statement(textversion=textversion90.uid, is_startpoint=False, issue=issue1.uid)
	statement91 = Statement(textversion=textversion91.uid, is_startpoint=False, issue=issue1.uid)
	statement92 = Statement(textversion=textversion92.uid, is_startpoint=False, issue=issue1.uid)
	statement93 = Statement(textversion=textversion93.uid, is_startpoint=False, issue=issue1.uid)
	statement94 = Statement(textversion=textversion94.uid, is_startpoint=False, issue=issue1.uid)
	statement95 = Statement(textversion=textversion95.uid, is_startpoint=False, issue=issue1.uid)
	statement96 = Statement(textversion=textversion96.uid, is_startpoint=False, issue=issue1.uid)
	statement97 = Statement(textversion=textversion97.uid, is_startpoint=False, issue=issue1.uid)
	statement98 = Statement(textversion=textversion98.uid, is_startpoint=False, issue=issue1.uid)
	statement99 = Statement(textversion=textversion99.uid, is_startpoint=False, issue=issue1.uid)
	statement100 = Statement(textversion=textversion100.uid, is_startpoint=False, issue=issue1.uid)
	statement101 = Statement(textversion=textversion101.uid, is_startpoint=False, issue=issue1.uid)

	statement102 = Statement(textversion=textversion102.uid, is_startpoint=True, issue=issue2.uid)
	statement103 = Statement(textversion=textversion103.uid, is_startpoint=False, issue=issue2.uid)
	statement104 = Statement(textversion=textversion104.uid, is_startpoint=False, issue=issue2.uid)
	statement105 = Statement(textversion=textversion105.uid, is_startpoint=False, issue=issue2.uid)
	statement106 = Statement(textversion=textversion106.uid, is_startpoint=True, issue=issue2.uid)
	statement107 = Statement(textversion=textversion107.uid, is_startpoint=True, issue=issue2.uid)
	statement108 = Statement(textversion=textversion108.uid, is_startpoint=False, issue=issue2.uid)

	statement109 = Statement(textversion=textversion109.uid, is_startpoint=False, issue=issue1.uid)

	DBDiscussionSession.add_all([statement1, statement2, statement3, statement4, statement5, statement6, statement7, statement8,
	                             statement9, statement10, statement11, statement12, statement13, statement14, statement15, statement16,
	                             statement17, statement18, statement19, statement20, statement21, statement22, statement23, statement24,
	                             statement25, statement26, statement27, statement29, statement30, statement31, statement32, statement33,
	                             statement34, statement35, statement36, statement37, statement38, statement39, statement40, statement41,
	                             statement42, statement43, statement44, statement45, statement46, statement47, statement48, statement49,
	                             statement50, statement51, statement52, statement53, statement54, statement55, statement56, statement57,
	                             statement58, statement59, statement60, statement61, statement62, statement63, statement64, statement65,
	                             statement66, statement67, statement68, statement69, statement70, statement71, statement72, statement73,
	                             statement74, statement75, statement76, statement77, statement78, statement79, statement80, statement81,
	                             statement82, statement83, statement84, statement85, statement86, statement87, statement88, statement89,
	                             statement90, statement91, statement92, statement93, statement94, statement95, statement96, statement97,
	                             statement98, statement99, statement100, statement101, statement102, statement103, statement104,
	                             statement105, statement106, statement107, statement108, statement109])
	DBDiscussionSession.flush()

	# set statements
	textversion1.set_statement(statement1.uid)
	textversion2.set_statement(statement2.uid)
	textversion3.set_statement(statement3.uid)
	textversion4.set_statement(statement4.uid)
	textversion5.set_statement(statement5.uid)
	textversion6.set_statement(statement6.uid)
	textversion7.set_statement(statement7.uid)
	textversion8.set_statement(statement8.uid)
	textversion9.set_statement(statement9.uid)
	textversion10.set_statement(statement10.uid)
	textversion11.set_statement(statement11.uid)
	textversion12.set_statement(statement12.uid)
	textversion13.set_statement(statement13.uid)
	textversion14.set_statement(statement14.uid)
	textversion15.set_statement(statement15.uid)
	textversion16.set_statement(statement16.uid)
	textversion17.set_statement(statement17.uid)
	textversion18.set_statement(statement18.uid)
	textversion19.set_statement(statement19.uid)
	textversion20.set_statement(statement20.uid)
	textversion21.set_statement(statement21.uid)
	textversion22.set_statement(statement22.uid)
	textversion23.set_statement(statement23.uid)
	textversion24.set_statement(statement24.uid)
	textversion25.set_statement(statement25.uid)
	textversion26.set_statement(statement26.uid)
	textversion27.set_statement(statement27.uid)
	textversion29.set_statement(statement29.uid)
	textversion30.set_statement(statement30.uid)
	textversion31.set_statement(statement31.uid)
	textversion32.set_statement(statement32.uid)
	textversion33.set_statement(statement33.uid)
	textversion34.set_statement(statement34.uid)
	textversion35.set_statement(statement35.uid)
	textversion36.set_statement(statement36.uid)
	textversion37.set_statement(statement37.uid)
	textversion38.set_statement(statement38.uid)
	textversion39.set_statement(statement39.uid)
	textversion40.set_statement(statement40.uid)
	textversion41.set_statement(statement41.uid)
	textversion42.set_statement(statement42.uid)
	textversion43.set_statement(statement43.uid)
	textversion44.set_statement(statement44.uid)
	textversion45.set_statement(statement45.uid)
	textversion46.set_statement(statement46.uid)
	textversion47.set_statement(statement47.uid)
	textversion48.set_statement(statement48.uid)
	textversion49.set_statement(statement49.uid)
	textversion50.set_statement(statement50.uid)
	textversion51.set_statement(statement51.uid)
	textversion52.set_statement(statement52.uid)
	textversion53.set_statement(statement53.uid)
	textversion54.set_statement(statement54.uid)
	textversion55.set_statement(statement55.uid)
	textversion56.set_statement(statement56.uid)
	textversion57.set_statement(statement57.uid)
	textversion58.set_statement(statement58.uid)
	textversion59.set_statement(statement59.uid)
	textversion60.set_statement(statement60.uid)
	textversion61.set_statement(statement61.uid)
	textversion62.set_statement(statement62.uid)
	textversion63.set_statement(statement63.uid)
	textversion64.set_statement(statement64.uid)
	textversion65.set_statement(statement65.uid)
	textversion66.set_statement(statement66.uid)
	textversion67.set_statement(statement67.uid)
	textversion68.set_statement(statement68.uid)
	textversion69.set_statement(statement69.uid)
	textversion70.set_statement(statement70.uid)
	textversion71.set_statement(statement71.uid)
	textversion72.set_statement(statement72.uid)
	textversion73.set_statement(statement73.uid)
	textversion74.set_statement(statement74.uid)
	textversion75.set_statement(statement75.uid)
	textversion76.set_statement(statement76.uid)
	textversion77.set_statement(statement77.uid)
	textversion78.set_statement(statement78.uid)
	textversion79.set_statement(statement79.uid)
	textversion80.set_statement(statement80.uid)
	textversion81.set_statement(statement81.uid)
	textversion82.set_statement(statement82.uid)
	textversion83.set_statement(statement83.uid)
	textversion84.set_statement(statement84.uid)
	textversion85.set_statement(statement85.uid)
	textversion86.set_statement(statement86.uid)
	textversion87.set_statement(statement87.uid)
	textversion88.set_statement(statement88.uid)
	textversion89.set_statement(statement89.uid)
	textversion90.set_statement(statement90.uid)
	textversion91.set_statement(statement91.uid)
	textversion92.set_statement(statement92.uid)
	textversion93.set_statement(statement93.uid)
	textversion94.set_statement(statement94.uid)
	textversion95.set_statement(statement95.uid)
	textversion96.set_statement(statement96.uid)
	textversion97.set_statement(statement97.uid)
	textversion98.set_statement(statement98.uid)
	textversion99.set_statement(statement99.uid)
	textversion100.set_statement(statement100.uid)
	textversion101.set_statement(statement101.uid)

	textversion102.set_statement(statement102.uid)
	textversion103.set_statement(statement103.uid)
	textversion104.set_statement(statement104.uid)
	textversion105.set_statement(statement105.uid)
	textversion106.set_statement(statement106.uid)
	textversion107.set_statement(statement107.uid)
	textversion108.set_statement(statement108.uid)

	textversion109.set_statement(statement109.uid)

	DBDiscussionSession.flush()

	# adding all premisegroups
	premisegroup1 = PremiseGroup(author=user2.uid)
	premisegroup2 = PremiseGroup(author=user2.uid)
	premisegroup3 = PremiseGroup(author=user2.uid)
	premisegroup4 = PremiseGroup(author=user2.uid)
	premisegroup5 = PremiseGroup(author=user2.uid)
	premisegroup6 = PremiseGroup(author=user2.uid)
	premisegroup7 = PremiseGroup(author=user2.uid)
	premisegroup8 = PremiseGroup(author=user2.uid)
	premisegroup9 = PremiseGroup(author=user2.uid)
	premisegroup10 = PremiseGroup(author=user2.uid)
	premisegroup11 = PremiseGroup(author=user2.uid)
	premisegroup12 = PremiseGroup(author=user2.uid)
	premisegroup13 = PremiseGroup(author=user2.uid)
	premisegroup14 = PremiseGroup(author=user2.uid)
	premisegroup15 = PremiseGroup(author=user2.uid)
	premisegroup16 = PremiseGroup(author=user2.uid)
	premisegroup17 = PremiseGroup(author=user2.uid)
	premisegroup18 = PremiseGroup(author=user2.uid)
	premisegroup19 = PremiseGroup(author=user2.uid)
	premisegroup20 = PremiseGroup(author=user2.uid)
	premisegroup21 = PremiseGroup(author=user2.uid)
	premisegroup22 = PremiseGroup(author=user2.uid)
	premisegroup23 = PremiseGroup(author=user2.uid)
	premisegroup24 = PremiseGroup(author=user2.uid)
	premisegroup25 = PremiseGroup(author=user2.uid)
	premisegroup26 = PremiseGroup(author=user2.uid)
	premisegroup27 = PremiseGroup(author=user2.uid)
	premisegroup28 = PremiseGroup(author=user2.uid)
	premisegroup29 = PremiseGroup(author=user2.uid)
	premisegroup30 = PremiseGroup(author=user2.uid)
	premisegroup31 = PremiseGroup(author=user2.uid)
	premisegroup32 = PremiseGroup(author=user2.uid)
	premisegroup33 = PremiseGroup(author=user2.uid)
	premisegroup34 = PremiseGroup(author=user2.uid)
	premisegroup35 = PremiseGroup(author=user2.uid)
	premisegroup36 = PremiseGroup(author=user2.uid)
	premisegroup37 = PremiseGroup(author=user2.uid)
	premisegroup38 = PremiseGroup(author=user2.uid)
	premisegroup39 = PremiseGroup(author=user2.uid)
	premisegroup40 = PremiseGroup(author=user2.uid)
	premisegroup41 = PremiseGroup(author=user2.uid)
	premisegroup42 = PremiseGroup(author=user2.uid)
	premisegroup43 = PremiseGroup(author=user2.uid)
	premisegroup44 = PremiseGroup(author=user2.uid)
	premisegroup45 = PremiseGroup(author=user2.uid)
	premisegroup46 = PremiseGroup(author=user2.uid)
	premisegroup47 = PremiseGroup(author=user2.uid)
	premisegroup48 = PremiseGroup(author=user2.uid)
	premisegroup49 = PremiseGroup(author=user2.uid)
	premisegroup50 = PremiseGroup(author=user2.uid)
	premisegroup51 = PremiseGroup(author=user2.uid)
	premisegroup52 = PremiseGroup(author=user2.uid)
	premisegroup53 = PremiseGroup(author=user2.uid)
	premisegroup54 = PremiseGroup(author=user2.uid)
	premisegroup55 = PremiseGroup(author=user2.uid)
	premisegroup56 = PremiseGroup(author=user2.uid)
	premisegroup57 = PremiseGroup(author=user2.uid)
	premisegroup58 = PremiseGroup(author=user2.uid)
	premisegroup59 = PremiseGroup(author=user2.uid)
	premisegroup60 = PremiseGroup(author=user2.uid)
	premisegroup61 = PremiseGroup(author=user2.uid)
	premisegroup62 = PremiseGroup(author=user2.uid)
	premisegroup63 = PremiseGroup(author=user2.uid)
	premisegroup64 = PremiseGroup(author=user2.uid)
	premisegroup65 = PremiseGroup(author=user2.uid)
	premisegroup66 = PremiseGroup(author=user2.uid)
	premisegroup67 = PremiseGroup(author=user2.uid)
	premisegroup68 = PremiseGroup(author=user2.uid)
	premisegroup69 = PremiseGroup(author=user2.uid)
	premisegroup70 = PremiseGroup(author=user2.uid)
	premisegroup71 = PremiseGroup(author=user2.uid)
	premisegroup72 = PremiseGroup(author=user2.uid)
	premisegroup73 = PremiseGroup(author=user2.uid)
	premisegroup74 = PremiseGroup(author=user2.uid)
	premisegroup75 = PremiseGroup(author=user2.uid)
	premisegroup76 = PremiseGroup(author=user2.uid)
	premisegroup77 = PremiseGroup(author=user2.uid)
	premisegroup78 = PremiseGroup(author=user2.uid)
	premisegroup79 = PremiseGroup(author=user2.uid)
	premisegroup80 = PremiseGroup(author=user2.uid)
	premisegroup81 = PremiseGroup(author=user2.uid)
	premisegroup82 = PremiseGroup(author=user2.uid)
	premisegroup83 = PremiseGroup(author=user2.uid)
	premisegroup84 = PremiseGroup(author=user2.uid)
	premisegroup85 = PremiseGroup(author=user2.uid)
	premisegroup86 = PremiseGroup(author=user2.uid)
	premisegroup87 = PremiseGroup(author=user2.uid)
	premisegroup88 = PremiseGroup(author=user2.uid)
	premisegroup89 = PremiseGroup(author=user2.uid)
	premisegroup90 = PremiseGroup(author=user2.uid)
	premisegroup91 = PremiseGroup(author=user2.uid)
	premisegroup92 = PremiseGroup(author=user2.uid)
	premisegroup93 = PremiseGroup(author=user2.uid)
	premisegroup94 = PremiseGroup(author=user2.uid)
	premisegroup95 = PremiseGroup(author=user2.uid)
	premisegroup96 = PremiseGroup(author=user2.uid)

	premisegroup97 = PremiseGroup(author=user2.uid)
	premisegroup98 = PremiseGroup(author=user2.uid)
	premisegroup99 = PremiseGroup(author=user2.uid)
	premisegroup100 = PremiseGroup(author=user2.uid)
	premisegroup101 = PremiseGroup(author=user2.uid)
	premisegroup102 = PremiseGroup(author=user2.uid)
	premisegroup103 = PremiseGroup(author=user2.uid)

	premisegroup104 = PremiseGroup(author=user2.uid)

	DBDiscussionSession.add_all([premisegroup1, premisegroup2, premisegroup3, premisegroup4, premisegroup5, premisegroup6,
	                             premisegroup7, premisegroup8, premisegroup9, premisegroup10, premisegroup11, premisegroup12,
	                             premisegroup13, premisegroup14, premisegroup15, premisegroup16, premisegroup17, premisegroup18,
	                             premisegroup19, premisegroup20, premisegroup21, premisegroup22, premisegroup23, premisegroup24,
	                             premisegroup25, premisegroup26, premisegroup27, premisegroup28, premisegroup29, premisegroup30,
	                             premisegroup31, premisegroup32, premisegroup33, premisegroup34, premisegroup35, premisegroup36,
	                             premisegroup37, premisegroup38, premisegroup39, premisegroup40, premisegroup41, premisegroup42,
	                             premisegroup43, premisegroup44, premisegroup45, premisegroup46, premisegroup47, premisegroup48,
	                             premisegroup49, premisegroup50, premisegroup51, premisegroup52, premisegroup53, premisegroup54,
	                             premisegroup55, premisegroup56, premisegroup57, premisegroup58, premisegroup59, premisegroup60,
	                             premisegroup61, premisegroup62, premisegroup63, premisegroup64, premisegroup65, premisegroup66,
	                             premisegroup67, premisegroup68, premisegroup69, premisegroup70, premisegroup71, premisegroup72,
	                             premisegroup73, premisegroup74, premisegroup75, premisegroup76, premisegroup77, premisegroup78,
	                             premisegroup79, premisegroup80, premisegroup81, premisegroup82, premisegroup83, premisegroup84,
	                             premisegroup85, premisegroup86, premisegroup87, premisegroup88, premisegroup89, premisegroup90,
	                             premisegroup91, premisegroup92, premisegroup93, premisegroup94, premisegroup95, premisegroup96,
	                             premisegroup97, premisegroup98, premisegroup99, premisegroup100, premisegroup101, premisegroup102,
	                             premisegroup103, premisegroup104])
	DBDiscussionSession.flush()

	premise1 = Premise(premisesgroup=premisegroup1.uid, statement=statement4.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise2 = Premise(premisesgroup=premisegroup2.uid, statement=statement5.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise3 = Premise(premisesgroup=premisegroup3.uid, statement=statement6.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise4 = Premise(premisesgroup=premisegroup4.uid, statement=statement7.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise5 = Premise(premisesgroup=premisegroup5.uid, statement=statement8.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise6 = Premise(premisesgroup=premisegroup6.uid, statement=statement9.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise7 = Premise(premisesgroup=premisegroup7.uid, statement=statement10.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise8 = Premise(premisesgroup=premisegroup8.uid, statement=statement11.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise9 = Premise(premisesgroup=premisegroup9.uid, statement=statement12.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise10 = Premise(premisesgroup=premisegroup10.uid, statement=statement13.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise11 = Premise(premisesgroup=premisegroup11.uid, statement=statement14.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise12 = Premise(premisesgroup=premisegroup11.uid, statement=statement15.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise13 = Premise(premisesgroup=premisegroup12.uid, statement=statement16.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise14 = Premise(premisesgroup=premisegroup13.uid, statement=statement17.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise15 = Premise(premisesgroup=premisegroup14.uid, statement=statement18.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise16 = Premise(premisesgroup=premisegroup15.uid, statement=statement19.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise17 = Premise(premisesgroup=premisegroup16.uid, statement=statement20.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise18 = Premise(premisesgroup=premisegroup17.uid, statement=statement21.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise19 = Premise(premisesgroup=premisegroup18.uid, statement=statement22.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise20 = Premise(premisesgroup=premisegroup19.uid, statement=statement23.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise21 = Premise(premisesgroup=premisegroup20.uid, statement=statement24.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise22 = Premise(premisesgroup=premisegroup21.uid, statement=statement25.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise23 = Premise(premisesgroup=premisegroup22.uid, statement=statement26.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise24 = Premise(premisesgroup=premisegroup23.uid, statement=statement27.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise25 = Premise(premisesgroup=premisegroup24.uid, statement=statement29.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise26 = Premise(premisesgroup=premisegroup25.uid, statement=statement30.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise27 = Premise(premisesgroup=premisegroup26.uid, statement=statement31.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise28 = Premise(premisesgroup=premisegroup27.uid, statement=statement32.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise29 = Premise(premisesgroup=premisegroup28.uid, statement=statement33.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise30 = Premise(premisesgroup=premisegroup29.uid, statement=statement34.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise31 = Premise(premisesgroup=premisegroup30.uid, statement=statement35.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise32 = Premise(premisesgroup=premisegroup31.uid, statement=statement36.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise33 = Premise(premisesgroup=premisegroup32.uid, statement=statement37.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise34 = Premise(premisesgroup=premisegroup33.uid, statement=statement38.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise35 = Premise(premisesgroup=premisegroup34.uid, statement=statement39.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise36 = Premise(premisesgroup=premisegroup35.uid, statement=statement40.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise37 = Premise(premisesgroup=premisegroup36.uid, statement=statement41.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise38 = Premise(premisesgroup=premisegroup37.uid, statement=statement42.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise39 = Premise(premisesgroup=premisegroup38.uid, statement=statement43.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise40 = Premise(premisesgroup=premisegroup39.uid, statement=statement44.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise41 = Premise(premisesgroup=premisegroup40.uid, statement=statement45.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise42 = Premise(premisesgroup=premisegroup41.uid, statement=statement46.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise43 = Premise(premisesgroup=premisegroup42.uid, statement=statement47.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise44 = Premise(premisesgroup=premisegroup43.uid, statement=statement48.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise45 = Premise(premisesgroup=premisegroup44.uid, statement=statement49.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise46 = Premise(premisesgroup=premisegroup45.uid, statement=statement50.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise47 = Premise(premisesgroup=premisegroup46.uid, statement=statement51.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise48 = Premise(premisesgroup=premisegroup47.uid, statement=statement52.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise49 = Premise(premisesgroup=premisegroup48.uid, statement=statement53.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise50 = Premise(premisesgroup=premisegroup49.uid, statement=statement54.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise51 = Premise(premisesgroup=premisegroup50.uid, statement=statement55.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise52 = Premise(premisesgroup=premisegroup51.uid, statement=statement56.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise53 = Premise(premisesgroup=premisegroup52.uid, statement=statement57.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise54 = Premise(premisesgroup=premisegroup53.uid, statement=statement58.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise55 = Premise(premisesgroup=premisegroup54.uid, statement=statement59.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise56 = Premise(premisesgroup=premisegroup55.uid, statement=statement60.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise57 = Premise(premisesgroup=premisegroup56.uid, statement=statement61.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise58 = Premise(premisesgroup=premisegroup57.uid, statement=statement62.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise59 = Premise(premisesgroup=premisegroup58.uid, statement=statement63.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise60 = Premise(premisesgroup=premisegroup59.uid, statement=statement64.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise61 = Premise(premisesgroup=premisegroup60.uid, statement=statement65.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise62 = Premise(premisesgroup=premisegroup61.uid, statement=statement66.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise63 = Premise(premisesgroup=premisegroup62.uid, statement=statement67.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise64 = Premise(premisesgroup=premisegroup63.uid, statement=statement68.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise65 = Premise(premisesgroup=premisegroup64.uid, statement=statement69.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise66 = Premise(premisesgroup=premisegroup65.uid, statement=statement70.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise67 = Premise(premisesgroup=premisegroup66.uid, statement=statement71.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise68 = Premise(premisesgroup=premisegroup67.uid, statement=statement72.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise69 = Premise(premisesgroup=premisegroup68.uid, statement=statement73.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise70 = Premise(premisesgroup=premisegroup69.uid, statement=statement74.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise71 = Premise(premisesgroup=premisegroup70.uid, statement=statement75.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise72 = Premise(premisesgroup=premisegroup71.uid, statement=statement76.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise73 = Premise(premisesgroup=premisegroup72.uid, statement=statement77.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise74 = Premise(premisesgroup=premisegroup73.uid, statement=statement78.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise75 = Premise(premisesgroup=premisegroup74.uid, statement=statement79.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise76 = Premise(premisesgroup=premisegroup75.uid, statement=statement80.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise77 = Premise(premisesgroup=premisegroup76.uid, statement=statement81.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise78 = Premise(premisesgroup=premisegroup77.uid, statement=statement82.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise79 = Premise(premisesgroup=premisegroup78.uid, statement=statement83.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise80 = Premise(premisesgroup=premisegroup79.uid, statement=statement84.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise81 = Premise(premisesgroup=premisegroup80.uid, statement=statement85.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise82 = Premise(premisesgroup=premisegroup81.uid, statement=statement86.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise83 = Premise(premisesgroup=premisegroup82.uid, statement=statement87.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise84 = Premise(premisesgroup=premisegroup83.uid, statement=statement88.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise85 = Premise(premisesgroup=premisegroup84.uid, statement=statement89.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise86 = Premise(premisesgroup=premisegroup85.uid, statement=statement90.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise87 = Premise(premisesgroup=premisegroup86.uid, statement=statement91.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise88 = Premise(premisesgroup=premisegroup87.uid, statement=statement92.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise89 = Premise(premisesgroup=premisegroup88.uid, statement=statement93.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise90 = Premise(premisesgroup=premisegroup89.uid, statement=statement94.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise91 = Premise(premisesgroup=premisegroup90.uid, statement=statement95.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise92 = Premise(premisesgroup=premisegroup91.uid, statement=statement96.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise93 = Premise(premisesgroup=premisegroup92.uid, statement=statement97.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise94 = Premise(premisesgroup=premisegroup93.uid, statement=statement98.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise95 = Premise(premisesgroup=premisegroup94.uid, statement=statement99.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise96 = Premise(premisesgroup=premisegroup95.uid, statement=statement100.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise97 = Premise(premisesgroup=premisegroup96.uid, statement=statement101.uid, is_negated=False, author=user2.uid, issue=issue1.uid)

	premise98 = Premise(premisesgroup=premisegroup97.uid, statement=statement102.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise99 = Premise(premisesgroup=premisegroup98.uid, statement=statement103.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise100 = Premise(premisesgroup=premisegroup99.uid, statement=statement104.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise101 = Premise(premisesgroup=premisegroup100.uid, statement=statement105.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise102 = Premise(premisesgroup=premisegroup101.uid, statement=statement106.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise103 = Premise(premisesgroup=premisegroup102.uid, statement=statement107.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise104 = Premise(premisesgroup=premisegroup103.uid, statement=statement108.uid, is_negated=False, author=user2.uid, issue=issue2.uid)

	premise105 = Premise(premisesgroup=premisegroup104.uid, statement=statement109.uid, is_negated=False, author=user2.uid, issue=issue1.uid)

	DBDiscussionSession.add_all([premise1, premise2, premise3, premise4, premise5, premise6, premise7, premise8, premise9,
	                             premise10, premise11, premise12, premise13, premise14, premise15, premise16, premise17, premise18,
	                             premise19, premise20, premise21, premise22, premise23, premise24, premise25, premise26, premise27,
	                             premise28, premise29, premise30, premise31, premise32, premise33, premise34, premise35, premise36,
	                             premise37, premise38, premise39, premise40, premise41, premise42, premise43, premise44, premise45,
	                             premise46, premise47, premise48, premise49, premise50, premise51, premise52, premise53, premise54,
	                             premise55, premise56, premise57, premise58, premise59, premise60, premise61, premise62, premise63,
	                             premise64, premise65, premise66, premise67, premise68, premise69, premise70, premise71, premise72,
	                             premise73, premise74, premise75, premise76, premise77, premise78, premise79, premise80, premise81,
	                             premise82, premise83, premise84, premise85, premise86, premise87, premise88, premise89, premise90,
	                             premise91, premise92, premise93, premise94, premise95, premise96, premise97, premise98, premise99,
	                             premise100, premise101, premise102, premise103, premise104, premise105])
	DBDiscussionSession.flush()

	# adding all arguments and set the adjacency list
	argument1 = Argument(premisegroup=premisegroup1.uid, issupportive=True, author=user2.uid, conclusion=statement1.uid, issue=issue1.uid)
	argument2 = Argument(premisegroup=premisegroup2.uid, issupportive=False, author=user2.uid, conclusion=statement1.uid, issue=issue1.uid)
	argument3 = Argument(premisegroup=premisegroup3.uid, issupportive=True, author=user2.uid, conclusion=statement2.uid, issue=issue1.uid)
	argument4 = Argument(premisegroup=premisegroup4.uid, issupportive=False, author=user2.uid, conclusion=statement2.uid, issue=issue1.uid)
	argument5 = Argument(premisegroup=premisegroup5.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument6 = Argument(premisegroup=premisegroup6.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument7 = Argument(premisegroup=premisegroup7.uid, issupportive=True, author=user2.uid, conclusion=statement3.uid, issue=issue1.uid)
	argument8 = Argument(premisegroup=premisegroup8.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument9 = Argument(premisegroup=premisegroup9.uid, issupportive=False, author=user2.uid, conclusion=statement10.uid, issue=issue1.uid)
	argument10 = Argument(premisegroup=premisegroup10.uid, issupportive=True, author=user2.uid, conclusion=statement1.uid, issue=issue1.uid)
	argument11 = Argument(premisegroup=premisegroup11.uid, issupportive=True, author=user2.uid, conclusion=statement1.uid, issue=issue1.uid)
	argument12 = Argument(premisegroup=premisegroup12.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument13 = Argument(premisegroup=premisegroup13.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument14 = Argument(premisegroup=premisegroup14.uid, issupportive=True, author=user2.uid, conclusion=statement4.uid, issue=issue1.uid)
	argument15 = Argument(premisegroup=premisegroup15.uid, issupportive=False, author=user2.uid, conclusion=statement4.uid, issue=issue1.uid)
	argument16 = Argument(premisegroup=premisegroup16.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument17 = Argument(premisegroup=premisegroup17.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument18 = Argument(premisegroup=premisegroup18.uid, issupportive=True, author=user2.uid, conclusion=statement5.uid, issue=issue1.uid)
	argument19 = Argument(premisegroup=premisegroup19.uid, issupportive=False, author=user2.uid, conclusion=statement5.uid, issue=issue1.uid)
	argument20 = Argument(premisegroup=premisegroup20.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument21 = Argument(premisegroup=premisegroup21.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument22 = Argument(premisegroup=premisegroup22.uid, issupportive=False, author=user2.uid, conclusion=statement13.uid, issue=issue1.uid)
	argument23 = Argument(premisegroup=premisegroup23.uid, issupportive=True, author=user2.uid, conclusion=statement13.uid, issue=issue1.uid)
	argument24 = Argument(premisegroup=premisegroup24.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument25 = Argument(premisegroup=premisegroup25.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument26 = Argument(premisegroup=premisegroup26.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument27 = Argument(premisegroup=premisegroup27.uid, issupportive=True, author=user2.uid, conclusion=statement14.uid, issue=issue1.uid)
	argument28 = Argument(premisegroup=premisegroup27.uid, issupportive=True, author=user2.uid, conclusion=statement15.uid, issue=issue1.uid)
	# IMPORTANT: If the conclusion is an argument, check the counter!
	argument29 = Argument(premisegroup=premisegroup28.uid, issupportive=False, author=user2.uid, conclusion=statement14.uid, issue=issue1.uid)
	argument30 = Argument(premisegroup=premisegroup28.uid, issupportive=False, author=user2.uid, conclusion=statement15.uid, issue=issue1.uid)
	# IMPORTANT: If the conclusion is an argument, check the counter!
	argument31 = Argument(premisegroup=premisegroup29.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument32 = Argument(premisegroup=premisegroup30.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument33 = Argument(premisegroup=premisegroup31.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument34 = Argument(premisegroup=premisegroup32.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument35 = Argument(premisegroup=premisegroup33.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument36 = Argument(premisegroup=premisegroup34.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument37 = Argument(premisegroup=premisegroup35.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument38 = Argument(premisegroup=premisegroup36.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument39 = Argument(premisegroup=premisegroup37.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument40 = Argument(premisegroup=premisegroup38.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument41 = Argument(premisegroup=premisegroup39.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument42 = Argument(premisegroup=premisegroup40.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument43 = Argument(premisegroup=premisegroup41.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument44 = Argument(premisegroup=premisegroup42.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument45 = Argument(premisegroup=premisegroup43.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument46 = Argument(premisegroup=premisegroup44.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument47 = Argument(premisegroup=premisegroup45.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	argument48 = Argument(premisegroup=premisegroup46.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument49 = Argument(premisegroup=premisegroup47.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument50 = Argument(premisegroup=premisegroup48.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument51 = Argument(premisegroup=premisegroup49.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument52 = Argument(premisegroup=premisegroup50.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument53 = Argument(premisegroup=premisegroup51.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument54 = Argument(premisegroup=premisegroup52.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument55 = Argument(premisegroup=premisegroup53.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument56 = Argument(premisegroup=premisegroup54.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument57 = Argument(premisegroup=premisegroup55.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument58 = Argument(premisegroup=premisegroup56.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument59 = Argument(premisegroup=premisegroup57.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument60 = Argument(premisegroup=premisegroup58.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument61 = Argument(premisegroup=premisegroup59.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument62 = Argument(premisegroup=premisegroup60.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument63 = Argument(premisegroup=premisegroup61.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument64 = Argument(premisegroup=premisegroup62.uid, issupportive=True, author=user2.uid, issue=issue1.uid)
	argument65 = Argument(premisegroup=premisegroup63.uid, issupportive=False, author=user2.uid, conclusion=statement16.uid, issue=issue1.uid)
	argument66 = Argument(premisegroup=premisegroup64.uid, issupportive=False, author=user2.uid, conclusion=statement17.uid, issue=issue1.uid)
	argument67 = Argument(premisegroup=premisegroup65.uid, issupportive=False, author=user2.uid, conclusion=statement18.uid, issue=issue1.uid)
	argument68 = Argument(premisegroup=premisegroup66.uid, issupportive=False, author=user2.uid, conclusion=statement19.uid, issue=issue1.uid)
	argument69 = Argument(premisegroup=premisegroup67.uid, issupportive=False, author=user2.uid, conclusion=statement20.uid, issue=issue1.uid)
	argument70 = Argument(premisegroup=premisegroup68.uid, issupportive=False, author=user2.uid, conclusion=statement21.uid, issue=issue1.uid)
	argument71 = Argument(premisegroup=premisegroup69.uid, issupportive=False, author=user2.uid, conclusion=statement22.uid, issue=issue1.uid)
	argument72 = Argument(premisegroup=premisegroup70.uid, issupportive=False, author=user2.uid, conclusion=statement23.uid, issue=issue1.uid)
	argument73 = Argument(premisegroup=premisegroup71.uid, issupportive=False, author=user2.uid, conclusion=statement24.uid, issue=issue1.uid)
	argument74 = Argument(premisegroup=premisegroup72.uid, issupportive=False, author=user2.uid, conclusion=statement25.uid, issue=issue1.uid)
	argument75 = Argument(premisegroup=premisegroup73.uid, issupportive=False, author=user2.uid, conclusion=statement26.uid, issue=issue1.uid)
	argument76 = Argument(premisegroup=premisegroup74.uid, issupportive=False, author=user2.uid, conclusion=statement27.uid, issue=issue1.uid)
	argument77 = Argument(premisegroup=premisegroup75.uid, issupportive=False, author=user2.uid, conclusion=statement29.uid, issue=issue1.uid)
	argument78 = Argument(premisegroup=premisegroup76.uid, issupportive=False, author=user2.uid, conclusion=statement30.uid, issue=issue1.uid)
	argument79 = Argument(premisegroup=premisegroup77.uid, issupportive=False, author=user2.uid, conclusion=statement31.uid, issue=issue1.uid)
	argument80 = Argument(premisegroup=premisegroup78.uid, issupportive=False, author=user2.uid, conclusion=statement32.uid, issue=issue1.uid)
	argument81 = Argument(premisegroup=premisegroup79.uid, issupportive=False, author=user2.uid, conclusion=statement33.uid, issue=issue1.uid)
	argument82 = Argument(premisegroup=premisegroup80.uid, issupportive=True, author=user2.uid, conclusion=statement16.uid, issue=issue1.uid)
	argument83 = Argument(premisegroup=premisegroup81.uid, issupportive=True, author=user2.uid, conclusion=statement17.uid, issue=issue1.uid)
	argument84 = Argument(premisegroup=premisegroup82.uid, issupportive=True, author=user2.uid, conclusion=statement18.uid, issue=issue1.uid)
	argument85 = Argument(premisegroup=premisegroup83.uid, issupportive=True, author=user2.uid, conclusion=statement19.uid, issue=issue1.uid)
	argument86 = Argument(premisegroup=premisegroup84.uid, issupportive=True, author=user2.uid, conclusion=statement20.uid, issue=issue1.uid)
	argument87 = Argument(premisegroup=premisegroup85.uid, issupportive=True, author=user2.uid, conclusion=statement21.uid, issue=issue1.uid)
	argument88 = Argument(premisegroup=premisegroup86.uid, issupportive=True, author=user2.uid, conclusion=statement22.uid, issue=issue1.uid)
	argument89 = Argument(premisegroup=premisegroup87.uid, issupportive=True, author=user2.uid, conclusion=statement23.uid, issue=issue1.uid)
	argument90 = Argument(premisegroup=premisegroup88.uid, issupportive=True, author=user2.uid, conclusion=statement24.uid, issue=issue1.uid)
	argument91 = Argument(premisegroup=premisegroup89.uid, issupportive=True, author=user2.uid, conclusion=statement25.uid, issue=issue1.uid)
	argument92 = Argument(premisegroup=premisegroup90.uid, issupportive=True, author=user2.uid, conclusion=statement26.uid, issue=issue1.uid)
	argument93 = Argument(premisegroup=premisegroup91.uid, issupportive=True, author=user2.uid, conclusion=statement27.uid, issue=issue1.uid)
	argument94 = Argument(premisegroup=premisegroup92.uid, issupportive=True, author=user2.uid, conclusion=statement29.uid, issue=issue1.uid)
	argument95 = Argument(premisegroup=premisegroup93.uid, issupportive=True, author=user2.uid, conclusion=statement30.uid, issue=issue1.uid)
	argument96 = Argument(premisegroup=premisegroup94.uid, issupportive=True, author=user2.uid, conclusion=statement31.uid, issue=issue1.uid)
	argument97 = Argument(premisegroup=premisegroup95.uid, issupportive=True, author=user2.uid, conclusion=statement32.uid, issue=issue1.uid)
	argument98 = Argument(premisegroup=premisegroup96.uid, issupportive=True, author=user2.uid, conclusion=statement33.uid, issue=issue1.uid)

	argument99 = Argument(premisegroup=premisegroup98.uid, issupportive=True, author=user2.uid, conclusion=statement102.uid, issue=issue2.uid)
	argument100 = Argument(premisegroup=premisegroup99.uid, issupportive=True, author=user2.uid, conclusion=statement102.uid, issue=issue2.uid)
	argument101 = Argument(premisegroup=premisegroup100.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument102 = Argument(premisegroup=premisegroup103.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	# premise104 = Premise(premisesgroup=premisegroup103.uid, statement=statement108.uid,  isnegated=False, author=user2.uid,  issue=issue2.uid)

	argument105 = Argument(premisegroup=premisegroup104.uid, issupportive=False, author=user2.uid, conclusion=statement10.uid,
	                       issue=issue1.uid)

	DBDiscussionSession.add_all([argument1, argument2, argument3, argument4, argument5, argument6, argument7, argument8, argument9,
	                             argument10, argument11, argument12, argument13, argument14, argument15, argument16, argument17, argument18,
	                             argument19, argument20, argument21, argument22, argument23, argument24, argument25, argument26, argument27,
	                             argument28, argument29, argument30, argument31, argument32, argument33, argument34, argument35, argument36,
	                             argument37, argument38, argument39, argument40, argument41, argument42, argument43, argument44, argument45,
	                             argument46, argument47, argument48, argument49, argument50, argument51, argument52, argument53, argument54,
	                             argument55, argument56, argument57, argument58, argument59, argument60, argument61, argument62, argument63,
	                             argument64, argument65, argument66, argument67, argument68, argument69, argument70, argument71, argument72,
	                             argument73, argument74, argument75, argument76, argument77, argument78, argument79, argument80, argument81,
	                             argument82, argument83, argument84, argument85, argument86, argument87, argument88, argument89, argument90,
	                             argument91, argument92, argument93, argument94, argument95, argument96, argument97, argument98, argument99,
	                             argument100, argument101, argument102, argument105])
	DBDiscussionSession.flush()

	argument5.conclusions_argument(argument3.uid)
	argument6.conclusions_argument(argument4.uid)
	argument8.conclusions_argument(argument7.uid)
	argument12.conclusions_argument(argument11.uid)
	argument13.conclusions_argument(argument12.uid)
	argument16.conclusions_argument(argument1.uid)
	argument17.conclusions_argument(argument1.uid)
	argument20.conclusions_argument(argument2.uid)
	argument21.conclusions_argument(argument2.uid)
	argument24.conclusions_argument(argument10.uid)
	argument25.conclusions_argument(argument10.uid)
	argument26.conclusions_argument(argument11.uid)
	argument29.conclusions_argument(argument12.uid)
	argument30.conclusions_argument(argument13.uid)
	argument31.conclusions_argument(argument14.uid)
	argument32.conclusions_argument(argument15.uid)
	argument33.conclusions_argument(argument16.uid)
	argument34.conclusions_argument(argument17.uid)
	argument35.conclusions_argument(argument18.uid)
	argument36.conclusions_argument(argument19.uid)
	argument37.conclusions_argument(argument20.uid)
	argument38.conclusions_argument(argument21.uid)
	argument39.conclusions_argument(argument22.uid)
	argument40.conclusions_argument(argument23.uid)
	argument41.conclusions_argument(argument24.uid)
	argument42.conclusions_argument(argument25.uid)
	argument43.conclusions_argument(argument26.uid)
	argument44.conclusions_argument(argument27.uid)
	argument45.conclusions_argument(argument28.uid)
	argument46.conclusions_argument(argument12.uid)
	argument47.conclusions_argument(argument13.uid)
	argument48.conclusions_argument(argument14.uid)
	argument49.conclusions_argument(argument15.uid)
	argument50.conclusions_argument(argument16.uid)
	argument51.conclusions_argument(argument17.uid)
	argument52.conclusions_argument(argument18.uid)
	argument53.conclusions_argument(argument19.uid)
	argument54.conclusions_argument(argument20.uid)
	argument55.conclusions_argument(argument21.uid)
	argument56.conclusions_argument(argument22.uid)
	argument57.conclusions_argument(argument23.uid)
	argument58.conclusions_argument(argument24.uid)
	argument59.conclusions_argument(argument25.uid)
	argument60.conclusions_argument(argument26.uid)
	argument61.conclusions_argument(argument27.uid)
	argument62.conclusions_argument(argument28.uid)
	argument63.conclusions_argument(argument29.uid)
	argument64.conclusions_argument(argument30.uid)

	argument101.conclusions_argument(argument100.uid)
	argument102.conclusions_argument(argument101.uid)

	DBDiscussionSession.flush()
