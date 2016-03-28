#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import transaction

from dbas.user_management import PasswordHandler
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.discussion_model import User, Argument, Statement, TextVersion, PremiseGroup, Premise, Group, Issue,\
	Notification, Settings, VoteArgument, VoteStatement, Bubble, Breadcrumb, StatementReferences
from dbas.database.news_model import News
from dbas.database import DiscussionBase, NewsBase, DBDiscussionSession, DBNewsSession

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
		user2 = setup_up_users()
		setup_discussion_database(user2)
		transaction.commit()


def main_discussion_reload(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	discussion_engine = engine_from_config(settings, 'sqlalchemy-discussion.')
	DBDiscussionSession.configure(bind=discussion_engine)
	DiscussionBase.metadata.create_all(discussion_engine)

	with transaction.manager:
		drop_in_discussion_database()
		user2 = DBDiscussionSession.query(User).filter_by(nickname = 'tobias').first()
		setup_discussion_database(user2)
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
				  news='D-BAS will be more personal and results driven. Therefore the new release has profile pictures for '
				       'everyone. They are powered by gravatar and are based on a md5-hash of the users email. Next to this '
				       'a new view was published - the island view. Do not be shy and try it in discussions ;-) Last '
				       'improvement just collects the attacks and supports for arguments...this is needed for our next big '
				       'thing :) Stay tuned!')
	news39 = News(title='Refactoring',
				  date='27.01.2016',
				  author='Tobias Krauthoff',
				  news='D-BAS refactored the last two weeks. During this time, a lot of JavaScript was removed. Therefore '
				       'D-BAS uses Chameleon with TAL in the Pyramid-Framework. So D-BAS will be more stable and faster. '
				       'The next period all functions will be tested and recovered.')
	news40 = News(title='API',
				  date='29.01.2016',
				  author='Tobias Krauthoff',
				  news='Now D-BAS has a API. Just replace the "discuss"-tag in your url with api to get your current steps raw data.')
	news41 = News(title='Voting Model',
				  date='05.01.2016',
				  author='Tobias Krauthoff',
				  news='Currently we are improving out model of voting for arguments as well as statements. Therefore we are working'
				       'together with our colleage out of the theoretical computer science...because D-BAS datastructure can be '
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
				       'if one of their statement was edited. More features are comming soon!')
	news44 = News(title='Speech Bubbles System',
				  date='02.03.2016',
				  author='Tobias Krauthoff',
				  news='After one week of testing, we released a new minor version of D-BAS. Instead of the text presentation,'
				       'we will use chat-like style :) Come on and try it! Additionally anonymous users will have a history now!')
	news_array = [news01, news02, news03, news04, news05, news06, news07, news08, news09, news10,
	              news11, news12, news13, news14, news15, news16, news29, news18, news19, news20,
	              news21, news22, news23, news24, news25, news26, news27, news28, news30, news31,
	              news32, news33, news34, news35, news36, news37, news38, news39, news40, news41,
	              news42, news43, news44]
	DBNewsSession.add_all(news_array[::-1])
	DBNewsSession.flush()


def drop_in_discussion_database():
	"""

	:return:
	"""
	DBDiscussionSession.query(VoteArgument).delete()
	DBDiscussionSession.query(VoteStatement).delete()
	DBDiscussionSession.query(Bubble).delete()
	DBDiscussionSession.query(Breadcrumb).delete()
	DBDiscussionSession.query(Notification).delete()
	DBDiscussionSession.query(StatementReferences).delete()
	DBDiscussionSession.query(Argument).delete()
	DBDiscussionSession.query(Premise).delete()
	DBDiscussionSession.query(PremiseGroup).delete()
	DBDiscussionSession.query(Statement).delete()
	DBDiscussionSession.query(TextVersion).delete()
	DBDiscussionSession.query(Issue).delete()


def setup_up_users():
	# adding groups
	group0 = Group(name='admins')
	group1 = Group(name='authors')
	group2 = Group(name='users')
	DBDiscussionSession.add_all([group0, group1, group2])
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
	user0 = User(firstname='anonymous', surname='anonymous', nickname='anonymous', email='', password=pw0, group=group0.uid, gender='m')
	user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas.hhu@gmail.com', password=pw1, group=group0.uid, gender='m')
	user2 = User(firstname='Tobias', surname='Krauthoff', nickname='tobias', email='krauthoff@cs.uni-duesseldorf.de', password=pw2, group=group0.uid, gender='m')
	user3 = User(firstname='Martin', surname='Mauve', nickname='martin', email='mauve@cs.uni-duesseldorf', password=pw3, group=group0.uid, gender='m')
	user4 = User(firstname='Kalman', surname='Graffi', nickname='kalman', email='graffi@cs.uni-duesseldorf.de', password=pw4, group=group1.uid, gender='m')
	user5 = User(firstname='Mladen', surname='Topic', nickname='mladen', email='mladen.topic@hhu.de', password=pw5, group=group1.uid, gender='m')
	user6 = User(firstname='Tobias', surname='Escher', nickname='drtobias', email='tobias.escher@hhu.de', password=pw6, group=group1.uid, gender='m')
	user7 = User(firstname='Michael', surname='Baurmann', nickname='michael', email='baurmann@hhu.de', password=pw7, group=group1.uid, gender='m')
	user8 = User(firstname='Gregor', surname='Betz', nickname='gregor', email='gregor.betz@kit.edu', password=pw8, group=group1.uid, gender='m')
	user9 = User(firstname='Christian', surname='Meter', nickname='christian', email='meter@cs.uni-duesseldorf.de', password=pw9, group=group0.uid, gender='m')
	user10 = User(firstname='Alexander', surname='Schneider', nickname='alexander', email='aschneider@cs.uni-duesseldorf.de', password=pw10, group=group1.uid, gender='m')
	DBDiscussionSession.add_all([user0, user1, user2, user3, user4, user5, user6, user7, user8, user9, user10])
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
	DBDiscussionSession.add_all([settings0, settings1, settings2, settings3, settings4, settings5, settings6, settings7])
	DBDiscussionSession.add_all([settings8, settings9])
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
	DBDiscussionSession.add_all([notification0, notification1, notification2, notification3, notification4])
	DBDiscussionSession.add_all([notification5, notification6, notification7, notification8])
	DBDiscussionSession.flush()

	return user2


def setup_discussion_database(user2):
	# adding our main issue
	issue1 = Issue(title='Cat or Dog', info='Your familiy argues about whether to buy a cat or dog as pet. Now your opinion matters!', author_uid=user2.uid)
	issue2 = Issue(title='Town has to cut spending ', info='Our town needs to cut spending. Please discuss ideas how this should be done.', author_uid=user2.uid)
	issue3 = Issue(title='Make the world better', info='How can we make this world a better place?', author_uid=user2.uid)
	issue4 = Issue(title='Reducing workload of the secretary', info='With wich measures can we reduce the workload of our secretaries?', author_uid=user2.uid)
	DBDiscussionSession.add_all([issue2, issue1])
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
	textversion34 = TextVersion(content="Even overbred races can be taught.", author=user2.uid)
	textversion35 = TextVersion(content="Several pets are nice to have and you do not have to take much care of them, for example turtles or cats, which are living outside.", author=user2.uid)
	textversion36 = TextVersion(content="It is much work to take care of both animals.", author=user2.uid)
	textversion101 = TextVersion(content="The major should increase the taxes.", author=user2.uid)
	textversion102 = TextVersion(content="We should shut down university park.", author=user2.uid)
	textversion103 = TextVersion(content="We should close public swimming pools.", author=user2.uid)
	# textversion104 = TextVersion(content="The major should start an e-participation process for the participatory budgeting.", author=user2.uid)
	textversion105 = TextVersion(content="This is a good idea, because we have more money then to solve other problems.", author=user2.uid)
	textversion106 = TextVersion(content="Not every problem can be solved with money.", author=user2.uid)
	textversion107 = TextVersion(content="Then we will have more money to expand out pedestrian zone", author=user2.uid)
	textversion108 = TextVersion(content="Our city will get more attractive for shopping.", author=user2.uid)
	textversion109 = TextVersion(content="This fights problems, but not the causes.", author=user2.uid)
	textversion110 = TextVersion(content="At some point we have to start. Where to start, if not here?", author=user2.uid)
	textversion111 = TextVersion(content="Money does not solve problems of our society.", author=user2.uid)
	textversion112 = TextVersion(content="Criminals use university park to sell drugs.", author=user2.uid)
	textversion113 = TextVersion(content="Shutting down university park will save 100.000$ a year.", author=user2.uid)
	textversion114 = TextVersion(content="We should not give in to criminals.", author=user2.uid)
	textversion115 = TextVersion(content="The number of police patrols has been increased recently.", author=user2.uid)
	textversion116 = TextVersion(content="This is the only park in our city.", author=user2.uid)
	textversion117 = TextVersion(content="There are many parks in neighbouring towns.", author=user2.uid)
	textversion118 = TextVersion(content="The city is planing a new park in the upcoming month.", author=user2.uid)
	textversion119 = TextVersion(content="Parks are highly important for our climate.", author=user2.uid)
	textversion120 = TextVersion(content="Our swimming pool are very old and would need many resaurations. This is too expensive.", author=user2.uid)
	textversion121 = TextVersion(content="Schools need the swimming pools for their sports lessons.", author=user2.uid)
	textversion122 = TextVersion(content="The rate of non-swimmers is too high.", author=user2.uid)
	textversion123 = TextVersion(content="The police cannot patrol in the park for 24/7.", author=user2.uid)

	DBDiscussionSession.add_all([textversion1, textversion2, textversion3, textversion4, textversion5, textversion6])
	DBDiscussionSession.add_all([textversion7, textversion8, textversion9, textversion10, textversion11, textversion12])
	DBDiscussionSession.add_all([textversion13, textversion14, textversion15, textversion16, textversion17, textversion18])
	DBDiscussionSession.add_all([textversion19, textversion20, textversion21, textversion22, textversion23, textversion24])
	DBDiscussionSession.add_all([textversion25, textversion26, textversion27, textversion29, textversion30, textversion31])
	DBDiscussionSession.add_all([textversion32, textversion33, textversion34, textversion35, textversion36])
	DBDiscussionSession.add_all([textversion101, textversion102, textversion103, textversion105])
	DBDiscussionSession.add_all([textversion106, textversion107, textversion108, textversion109, textversion110])
	DBDiscussionSession.add_all([textversion111, textversion112, textversion113, textversion114, textversion115])
	DBDiscussionSession.add_all([textversion116, textversion117, textversion118, textversion119, textversion120])
	DBDiscussionSession.add_all([textversion121, textversion122, textversion123])
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
	statement101 = Statement(textversion=textversion101.uid, is_startpoint=True, issue=issue2.uid)
	statement102 = Statement(textversion=textversion102.uid, is_startpoint=True, issue=issue2.uid)
	statement103 = Statement(textversion=textversion103.uid, is_startpoint=True, issue=issue2.uid)
	# statement104 = Statement(textversion=textversion104.uid, is_startpoint=True, issue=issue2.uid)
	statement105 = Statement(textversion=textversion105.uid, is_startpoint=False, issue=issue2.uid)
	statement106 = Statement(textversion=textversion106.uid, is_startpoint=False, issue=issue2.uid)
	statement107 = Statement(textversion=textversion107.uid, is_startpoint=False, issue=issue2.uid)
	statement108 = Statement(textversion=textversion108.uid, is_startpoint=False, issue=issue2.uid)
	statement109 = Statement(textversion=textversion109.uid, is_startpoint=False, issue=issue2.uid)
	statement110 = Statement(textversion=textversion110.uid, is_startpoint=False, issue=issue2.uid)
	statement111 = Statement(textversion=textversion111.uid, is_startpoint=False, issue=issue2.uid)
	statement112 = Statement(textversion=textversion112.uid, is_startpoint=False, issue=issue2.uid)
	statement113 = Statement(textversion=textversion113.uid, is_startpoint=False, issue=issue2.uid)
	statement114 = Statement(textversion=textversion114.uid, is_startpoint=False, issue=issue2.uid)
	statement115 = Statement(textversion=textversion115.uid, is_startpoint=False, issue=issue2.uid)
	statement116 = Statement(textversion=textversion116.uid, is_startpoint=False, issue=issue2.uid)
	statement117 = Statement(textversion=textversion117.uid, is_startpoint=False, issue=issue2.uid)
	statement118 = Statement(textversion=textversion118.uid, is_startpoint=False, issue=issue2.uid)
	statement119 = Statement(textversion=textversion119.uid, is_startpoint=False, issue=issue2.uid)
	statement120 = Statement(textversion=textversion120.uid, is_startpoint=False, issue=issue2.uid)
	statement121 = Statement(textversion=textversion121.uid, is_startpoint=False, issue=issue2.uid)
	statement122 = Statement(textversion=textversion122.uid, is_startpoint=False, issue=issue2.uid)
	statement123 = Statement(textversion=textversion123.uid, is_startpoint=False, issue=issue2.uid)

	DBDiscussionSession.add_all([statement1, statement2, statement3, statement4, statement5, statement6, statement7])
	DBDiscussionSession.add_all([statement8, statement9, statement10, statement11, statement12, statement13, statement14])
	DBDiscussionSession.add_all([statement15, statement16, statement17, statement18, statement19, statement20, statement21])
	DBDiscussionSession.add_all([statement22, statement23, statement24, statement25, statement26, statement27, statement29])
	DBDiscussionSession.add_all([statement30, statement31, statement32, statement33, statement34, statement35, statement36])
	DBDiscussionSession.add_all([statement101, statement102, statement103, statement105, statement106])
	DBDiscussionSession.add_all([statement107, statement108, statement109, statement110, statement111, statement112])
	DBDiscussionSession.add_all([statement113, statement114, statement115, statement116, statement117, statement118])
	DBDiscussionSession.add_all([statement119, statement120, statement121, statement122, statement123])
	DBDiscussionSession.flush()

	# set statements
	# textversion1.set_statement(statement1.uid)
	# textversion2.set_statement(statement2.uid)
	# textversion3.set_statement(statement3.uid)
	# textversion4.set_statement(statement4.uid)
	# textversion5.set_statement(statement5.uid)
	# textversion6.set_statement(statement6.uid)
	# textversion7.set_statement(statement7.uid)
	# textversion8.set_statement(statement8.uid)
	# textversion9.set_statement(statement9.uid)
	# textversion10.set_statement(statement10.uid)
	# textversion11.set_statement(statement11.uid)
	# textversion12.set_statement(statement12.uid)
	# textversion13.set_statement(statement13.uid)
	# textversion14.set_statement(statement14.uid)
	# textversion15.set_statement(statement15.uid)
	# textversion16.set_statement(statement16.uid)
	# textversion17.set_statement(statement17.uid)
	# textversion18.set_statement(statement18.uid)
	# textversion19.set_statement(statement19.uid)
	# textversion20.set_statement(statement20.uid)
	# textversion21.set_statement(statement21.uid)
	# textversion22.set_statement(statement22.uid)
	# textversion23.set_statement(statement23.uid)
	# textversion24.set_statement(statement24.uid)
	# textversion25.set_statement(statement25.uid)
	# textversion26.set_statement(statement26.uid)
	# textversion27.set_statement(statement27.uid)
	# textversion29.set_statement(statement29.uid)
	# textversion30.set_statement(statement30.uid)
	# textversion31.set_statement(statement31.uid)
	# textversion32.set_statement(statement32.uid)
	# textversion33.set_statement(statement33.uid)
	# textversion34.set_statement(statement34.uid)
	# textversion35.set_statement(statement35.uid)
	# textversion36.set_statement(statement36.uid)
	# textversion101.set_statement(statement101.uid)
	# textversion102.set_statement(statement102.uid)
	# textversion103.set_statement(statement103.uid)
	# # textversion104.set_statement(statement104.uid)
	# textversion105.set_statement(statement105.uid)
	# textversion106.set_statement(statement106.uid)
	# textversion107.set_statement(statement107.uid)
	# textversion108.set_statement(statement108.uid)
	# textversion109.set_statement(statement109.uid)
	# textversion110.set_statement(statement110.uid)
	# textversion111.set_statement(statement111.uid)
	# textversion112.set_statement(statement112.uid)
	# textversion113.set_statement(statement113.uid)
	# textversion114.set_statement(statement114.uid)
	# textversion115.set_statement(statement115.uid)
	# textversion116.set_statement(statement116.uid)
	# textversion117.set_statement(statement117.uid)
	# textversion118.set_statement(statement118.uid)
	# textversion119.set_statement(statement119.uid)
	# textversion120.set_statement(statement120.uid)
	# textversion121.set_statement(statement121.uid)
	# textversion122.set_statement(statement122.uid)
	# textversion123.set_statement(statement123.uid)

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
	premisegroup105 = PremiseGroup(author=user2.uid)
	premisegroup106 = PremiseGroup(author=user2.uid)
	premisegroup107 = PremiseGroup(author=user2.uid)
	premisegroup108 = PremiseGroup(author=user2.uid)
	premisegroup109 = PremiseGroup(author=user2.uid)
	premisegroup110 = PremiseGroup(author=user2.uid)
	premisegroup111 = PremiseGroup(author=user2.uid)
	premisegroup112 = PremiseGroup(author=user2.uid)
	premisegroup113 = PremiseGroup(author=user2.uid)
	premisegroup114 = PremiseGroup(author=user2.uid)
	premisegroup115 = PremiseGroup(author=user2.uid)
	premisegroup116 = PremiseGroup(author=user2.uid)
	premisegroup117 = PremiseGroup(author=user2.uid)
	premisegroup118 = PremiseGroup(author=user2.uid)
	premisegroup119 = PremiseGroup(author=user2.uid)
	premisegroup120 = PremiseGroup(author=user2.uid)
	premisegroup121 = PremiseGroup(author=user2.uid)
	premisegroup122 = PremiseGroup(author=user2.uid)
	premisegroup123 = PremiseGroup(author=user2.uid)

	DBDiscussionSession.add_all([premisegroup1, premisegroup2, premisegroup3, premisegroup4, premisegroup5, premisegroup6])
	DBDiscussionSession.add_all([premisegroup7, premisegroup8, premisegroup9, premisegroup10, premisegroup11, premisegroup12])
	DBDiscussionSession.add_all([premisegroup13, premisegroup14, premisegroup15, premisegroup16, premisegroup17, premisegroup18])
	DBDiscussionSession.add_all([premisegroup19, premisegroup20, premisegroup21, premisegroup22, premisegroup23, premisegroup24])
	DBDiscussionSession.add_all([premisegroup25, premisegroup26, premisegroup27, premisegroup28, premisegroup29])
	DBDiscussionSession.add_all([premisegroup105, premisegroup106, premisegroup107, premisegroup108, premisegroup109])
	DBDiscussionSession.add_all([premisegroup110, premisegroup111, premisegroup112, premisegroup113, premisegroup114])
	DBDiscussionSession.add_all([premisegroup115, premisegroup116, premisegroup117, premisegroup118, premisegroup119])
	DBDiscussionSession.add_all([premisegroup120, premisegroup121, premisegroup122, premisegroup123])
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
	premise30 = Premise(premisesgroup=premisegroup29.uid, statement=statement36.uid, is_negated=False, author=user2.uid, issue=issue1.uid)
	premise105 = Premise(premisesgroup=premisegroup105.uid, statement=statement105.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise106 = Premise(premisesgroup=premisegroup106.uid, statement=statement106.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise107 = Premise(premisesgroup=premisegroup107.uid, statement=statement107.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise108 = Premise(premisesgroup=premisegroup108.uid, statement=statement108.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise109 = Premise(premisesgroup=premisegroup109.uid, statement=statement109.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise110 = Premise(premisesgroup=premisegroup110.uid, statement=statement110.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise111 = Premise(premisesgroup=premisegroup111.uid, statement=statement111.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise112 = Premise(premisesgroup=premisegroup112.uid, statement=statement112.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise113 = Premise(premisesgroup=premisegroup113.uid, statement=statement113.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise114 = Premise(premisesgroup=premisegroup114.uid, statement=statement114.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise115 = Premise(premisesgroup=premisegroup115.uid, statement=statement115.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise116 = Premise(premisesgroup=premisegroup116.uid, statement=statement116.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise117 = Premise(premisesgroup=premisegroup117.uid, statement=statement117.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise118 = Premise(premisesgroup=premisegroup118.uid, statement=statement118.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise119 = Premise(premisesgroup=premisegroup119.uid, statement=statement119.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise120 = Premise(premisesgroup=premisegroup120.uid, statement=statement120.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise121 = Premise(premisesgroup=premisegroup121.uid, statement=statement121.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise122 = Premise(premisesgroup=premisegroup122.uid, statement=statement122.uid, is_negated=False, author=user2.uid, issue=issue2.uid)
	premise123 = Premise(premisesgroup=premisegroup123.uid, statement=statement123.uid, is_negated=False, author=user2.uid, issue=issue2.uid)

	DBDiscussionSession.add_all([premise1, premise2, premise3, premise4, premise5, premise6, premise7, premise8, premise9])
	DBDiscussionSession.add_all([premise10, premise11, premise12, premise13, premise14, premise15, premise16, premise17])
	DBDiscussionSession.add_all([premise18, premise19, premise20, premise21, premise22, premise23, premise24, premise25])
	DBDiscussionSession.add_all([premise26, premise27, premise28, premise29, premise30])
	DBDiscussionSession.add_all([premise105, premise106, premise107, premise108, premise109, premise110, premise111])
	DBDiscussionSession.add_all([premise112, premise113, premise114, premise115, premise116, premise117, premise118])
	DBDiscussionSession.add_all([premise119, premise120, premise121, premise122, premise123])
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
	argument29 = Argument(premisegroup=premisegroup28.uid, issupportive=False, author=user2.uid, conclusion=statement14.uid, issue=issue1.uid)
	argument30 = Argument(premisegroup=premisegroup28.uid, issupportive=False, author=user2.uid, conclusion=statement15.uid, issue=issue1.uid)
	argument31 = Argument(premisegroup=premisegroup29.uid, issupportive=False, author=user2.uid, issue=issue1.uid)
	####
	argument101 = Argument(premisegroup=premisegroup105.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement101.uid)
	argument102 = Argument(premisegroup=premisegroup106.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument103 = Argument(premisegroup=premisegroup107.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement105.uid)
	argument104 = Argument(premisegroup=premisegroup108.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement107.uid)
	argument105 = Argument(premisegroup=premisegroup109.uid, issupportive=False, author=user2.uid, issue=issue2.uid, conclusion=statement101.uid)
	argument106 = Argument(premisegroup=premisegroup110.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument107 = Argument(premisegroup=premisegroup111.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument108 = Argument(premisegroup=premisegroup112.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement102.uid)
	argument109 = Argument(premisegroup=premisegroup113.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement112.uid)
	argument110 = Argument(premisegroup=premisegroup115.uid, issupportive=False, author=user2.uid, issue=issue2.uid, conclusion=statement112.uid)
	argument111 = Argument(premisegroup=premisegroup114.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument112 = Argument(premisegroup=premisegroup116.uid, issupportive=False, author=user2.uid, issue=issue2.uid, conclusion=statement102.uid)
	argument113 = Argument(premisegroup=premisegroup117.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument114 = Argument(premisegroup=premisegroup118.uid, issupportive=False, author=user2.uid, issue=issue2.uid, conclusion=statement116.uid)
	argument115 = Argument(premisegroup=premisegroup119.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement116.uid)
	argument116 = Argument(premisegroup=premisegroup120.uid, issupportive=True, author=user2.uid, issue=issue2.uid, conclusion=statement103.uid)
	argument117 = Argument(premisegroup=premisegroup121.uid, issupportive=False, author=user2.uid, issue=issue2.uid)
	argument118 = Argument(premisegroup=premisegroup122.uid, issupportive=False, author=user2.uid, issue=issue2.uid, conclusion=statement103.uid)
	argument119 = Argument(premisegroup=premisegroup123.uid, issupportive=False, author=user2.uid, issue=issue2.uid, conclusion=statement115.uid)

	DBDiscussionSession.add_all([argument1, argument2, argument3, argument4, argument5, argument6, argument7, argument8])
	DBDiscussionSession.add_all([argument9, argument10, argument11, argument12, argument13, argument14, argument15])
	DBDiscussionSession.add_all([argument16, argument17, argument18, argument19, argument20, argument21, argument22])
	DBDiscussionSession.add_all([argument23, argument24, argument25, argument26, argument27, argument28, argument29])
	DBDiscussionSession.add_all([argument30, argument31])
	DBDiscussionSession.add_all([argument101, argument102, argument103, argument104, argument105, argument106, argument107])
	DBDiscussionSession.add_all([argument108, argument109, argument110, argument111, argument112, argument113, argument114])
	DBDiscussionSession.add_all([argument115, argument116, argument117, argument118, argument119])
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
	argument31.conclusions_argument(argument14.uid)
	argument102.conclusions_argument(argument101.uid)
	argument106.conclusions_argument(argument105.uid)
	argument107.conclusions_argument(argument105.uid)
	argument111.conclusions_argument(argument110.uid)
	argument113.conclusions_argument(argument112.uid)
	argument117.conclusions_argument(argument116.uid)
	DBDiscussionSession.flush()
