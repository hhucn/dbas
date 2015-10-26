import os
import sys
import transaction

from dbas.user_management import PasswordHandler
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from dbas.database.discussion_model import User, Argument, Statement, TextValue, TextVersion, \
	PremisseGroup, Premisse, Group, Relation, Issue
from dbas.database.news_model import News
from dbas.database import DiscussionBase, NewsBase, DBDiscussionSession, DBNewsSession


def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n'
		  '(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)


def main(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)

	discussionEngine = engine_from_config(settings, 'sqlalchemy-discussion.')
	DBDiscussionSession.configure(bind=discussionEngine)
	DiscussionBase.metadata.create_all(discussionEngine)

	newsEngine = engine_from_config(settings, 'sqlalchemy-news.')
	DBNewsSession.configure(bind=newsEngine)
	NewsBase.metadata.create_all(newsEngine)

	with transaction.manager:
		setupDiscussionDatabase()
		transaction.commit()
		setupNewsDatabase()
		transaction.commit()

def setupNewsDatabase():
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
	news10 = News(title='imple Navigation was improved',
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
				  news='I\'ve started with the Prototype')
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

	news_array = [news01, news02, news03, news04, news05, news06, news07, news08, news09, news10, news11, news12, news13, news14,
	              news15, news16, news29, news18, news19, news20, news21, news22, news23, news24, news25, news26, news27, news28,
	              news30]
	DBNewsSession.add_all(news_array[::-1])
	DBNewsSession.flush()

def setupDiscussionDatabase():
	# adding our main issue
	issue1 = Issue(text='Your familiy argues about whether to buy a cat or dog as pet. Now your opinion matters!')
	issue2 = Issue(text='Our town needs to cut spending. Please discuss ideas how this should be done.')
	DBDiscussionSession.add_all([issue1, issue2])
	DBDiscussionSession.flush()

	# adding groups
	group0 = Group(name='admins')
	group1 = Group(name='authors')
	group2 = Group(name='editors')
	group3 = Group(name='users')
	DBDiscussionSession.add_all([group0, group1, group2, group3])
	DBDiscussionSession.flush()

	# adding relation
	relation0 = Relation(name='undermine')
	relation1 = Relation(name='support')
	relation2 = Relation(name='undercut')
	relation3 = Relation(name='overbid')
	relation4 = Relation(name='rebut')
	DBDiscussionSession.add_all([relation0, relation1, relation2, relation3, relation4])
	DBDiscussionSession.flush()

	# adding some dummy users
	pwHandler = PasswordHandler()
	pw0 = pwHandler.get_hashed_password('QMuxpuPXwehmhm2m93#I;)QX§u4qjqoiwhebakb)(4hkblkb(hnzUIQWEGgalksd')
	pw1 = pwHandler.get_hashed_password('admin')
	pw2 = pwHandler.get_hashed_password('tobias')
	pw3 = pwHandler.get_hashed_password('martin')
	pw4 = pwHandler.get_hashed_password('kalman')
	pw5 = pwHandler.get_hashed_password('mladen')
	pw6 = pwHandler.get_hashed_password('drtobias')
	pw7 = pwHandler.get_hashed_password('michael')
	pw8 = pwHandler.get_hashed_password('gregor')
	pw9 = pwHandler.get_hashed_password('christian')
	pw10 = pwHandler.get_hashed_password('alexander')
	user0 = User(firstname='anonymous', surname='anonymous', nickname='anonymous', email='',password=pw0, group=group3.uid, gender='m')
	user1 = User(firstname='admin', surname='admin', nickname='admin', email='dbas.hhu@gmail.com',password=pw1, group=group0.uid, gender='m')
	user2 = User(firstname='Tobias', surname='Krauthoff', nickname='tobias', email='krauthoff@cs.uni-duesseldorf.de',password=pw2, group=group1.uid, gender='m')
	user3 = User(firstname='Martin', surname='Mauve', nickname='martin', email='mauve@cs.uni-duesseldorf',password=pw3, group=group2.uid, gender='m')
	user4 = User(firstname='Kalman', surname='Graffi', nickname='kalman', email='graffi@cs.uni-duesseldorf.de',password=pw4, group=group2.uid, gender='m')
	user5 = User(firstname='Mladen', surname='Topic', nickname='mladen', email='mladen.topic@hhu.de',password=pw5, group=group2.uid, gender='m')
	user6 = User(firstname='Tobias', surname='Escher', nickname='drtobias', email='tobias.escher@hhu.de',password=pw6, group=group2.uid, gender='m')
	user7 = User(firstname='Michael', surname='Baurmann', nickname='michael', email='baurmann@hhu.de',password=pw7, group=group2.uid, gender='m')
	user8 = User(firstname='Gregor', surname='Betz', nickname='gregor', email='gregor.betz@kit.edu',password=pw8, group=group2.uid, gender='m')
	user9 = User(firstname='Christian', surname='Meter', nickname='christian', email='christian.meter@uni-duesseldorf.de', password=pw9, group=group2.uid, gender='m')
	user10 = User(firstname='Alexander', surname='Schneider', nickname='alexander', email='alexander.schneider@uni-duesseldorf.de', password=pw10, group=group2.uid, gender='m')
	DBDiscussionSession.add_all([user0, user1, user2, user3, user4, user5, user6, user7, user8, user9, user10])
	DBDiscussionSession.flush()

	#Adding all textversions
	textversion1 = TextVersion(content="We should get a cat.", author=user2.uid, weight=0)
	textversion2 = TextVersion(content="We should get a dog.", author=user2.uid, weight=0)
	textversion3 = TextVersion(content="We could get both, a cat and a dog.", author=user2.uid, weight=0)
	textversion4 = TextVersion(content="Cats are very independent.", author=user2.uid, weight=0)
	textversion5 = TextVersion(content="Cats are capricious.", author=user2.uid, weight=0)
	textversion6 = TextVersion(content="Dogs can act as watch dogs.", author=user2.uid, weight=0)
	textversion7 = TextVersion(content="You have to take the dog for a walk every day, which is tedious.", author=user2.uid, weight=0)
	textversion8 = TextVersion(content="We have no use for a watch dog.", author=user2.uid, weight=0)
	textversion9 = TextVersion(content="Going for a walk with the dog every day is good for social interaction and physical exercise.", author=user2.uid, weight=0)
	textversion10 = TextVersion(content="It would be no problem to get both a cat and a dog.", author=user2.uid, weight=0)
	textversion11 = TextVersion(content="A cat and a dog will generally not get along well.", author=user2.uid, weight=0)
	textversion12 = TextVersion(content="We do not have enough money for two pets.", author=user2.uid, weight=0)
	textversion13 = TextVersion(content="A dog costs taxes and will be more expensive than a cat.", author=user2.uid, weight=0)
	textversion14 = TextVersion(content="Cats are fluffy.", author=user2.uid, weight=0)
	textversion15 = TextVersion(content="Cats are small.", author=user2.uid, weight=0)
	textversion16 = TextVersion(content="Fluffy animals losing much hair and I'm allergic to animal hair.", author=user2.uid, weight=0)
	textversion17 = TextVersion(content="You could use a automatic vacuum cleaner.", author=user2.uid, weight=0)
	textversion18 = TextVersion(content="Cats ancestors are animals in wildlife, who are hunting alone and not in groups.", author=user2.uid, weight=0)
	textversion19 = TextVersion(content="This is not true for overbred races.", author=user2.uid, weight=0)
	textversion20 = TextVersion(content="This lies in their the natural conditions.", author=user2.uid, weight=0)
	textversion21 = TextVersion(content="The purpose of a pet is to have something to take care of.", author=user2.uid, weight=0)
	textversion22 = TextVersion(content="Several cats of friends of mine are real as*holes.", author=user2.uid, weight=0)
	textversion23 = TextVersion(content="The fact, that cats are capricious, is based on the cats race.", author=user2.uid, weight=0)
	textversion24 = TextVersion(content="All cats of my friends are capricious.", author=user2.uid, weight=0)
	textversion25 = TextVersion(content="This is based on the cats race and a little bit on the breeding.", author=user2.uid, weight=0)
	textversion26 = TextVersion(content="Next to the taxes you will need equipment like a dog lead, anti-flea-spray, and so on.", author=user2.uid, weight=0)
	textversion27 = TextVersion(content="The equipment for running costs of cats and dogs are nearly the same.", author=user2.uid, weight=0)
	textversion29 = TextVersion(content="This is just a claim without any justification.", author=user2.uid, weight=0)
	textversion30 = TextVersion(content="In Germany you have to pay for your second dog even more taxes!", author=user2.uid, weight=0)
	textversion31 = TextVersion(content="It is important, that pets are small and fluffy!", author=user2.uid, weight=0)
	textversion32 = TextVersion(content="Cats are little, sweet and innocent cuddle toys.", author=user2.uid, weight=0)
	textversion33 = TextVersion(content="Do you have ever seen a sphinx cat or savannah cats?", author=user2.uid, weight=0)
	textversion34 = TextVersion(content="This is for debugging, so that A29 exists with S34 attacks A12", author=user2.uid, weight=0)
	textversion35 = TextVersion(content="This is for debugging, so that A30 exists with S35 attacks A13", author=user2.uid, weight=0)
	textversion36 = TextVersion(content="This is for debugging, so that A31 exists with S36 attacks A14", author=user2.uid, weight=0)
	textversion37 = TextVersion(content="This is for debugging, so that A32 exists with S37 attacks A15", author=user2.uid, weight=0)
	textversion38 = TextVersion(content="This is for debugging, so that A33 exists with S38 attacks A16", author=user2.uid, weight=0)
	textversion39 = TextVersion(content="This is for debugging, so that A34 exists with S39 attacks A17", author=user2.uid, weight=0)
	textversion40 = TextVersion(content="This is for debugging, so that A35 exists with S40 attacks A18", author=user2.uid, weight=0)
	textversion41 = TextVersion(content="This is for debugging, so that A36 exists with S41 attacks A19", author=user2.uid, weight=0)
	textversion42 = TextVersion(content="This is for debugging, so that A37 exists with S42 attacks A20", author=user2.uid, weight=0)
	textversion43 = TextVersion(content="This is for debugging, so that A38 exists with S43 attacks A21", author=user2.uid, weight=0)
	textversion44 = TextVersion(content="This is for debugging, so that A39 exists with S44 attacks A22", author=user2.uid, weight=0)
	textversion45 = TextVersion(content="This is for debugging, so that A40 exists with S45 attacks A23", author=user2.uid, weight=0)
	textversion46 = TextVersion(content="This is for debugging, so that A41 exists with S46 attacks A24", author=user2.uid, weight=0)
	textversion47 = TextVersion(content="This is for debugging, so that A42 exists with S47 attacks A25", author=user2.uid, weight=0)
	textversion48 = TextVersion(content="This is for debugging, so that A43 exists with S48 attacks A26", author=user2.uid, weight=0)
	textversion49 = TextVersion(content="This is for debugging, so that A44 exists with S49 attacks A27", author=user2.uid, weight=0)
	textversion50 = TextVersion(content="This is for debugging, so that A45 exists with S50 attacks A28", author=user2.uid, weight=0)
	textversion51 = TextVersion(content="This is for debugging, so that A46 exists with S51 supports A12", author=user2.uid, weight=0)
	textversion52 = TextVersion(content="This is for debugging, so that A47 exists with S52 supports A13", author=user2.uid, weight=0)
	textversion53 = TextVersion(content="This is for debugging, so that A48 exists with S53 supports A14", author=user2.uid, weight=0)
	textversion54 = TextVersion(content="This is for debugging, so that A49 exists with S54 supports A15", author=user2.uid, weight=0)
	textversion55 = TextVersion(content="This is for debugging, so that A50 exists with S55 supports A16", author=user2.uid, weight=0)
	textversion56 = TextVersion(content="This is for debugging, so that A51 exists with S56 supports A17", author=user2.uid, weight=0)
	textversion57 = TextVersion(content="This is for debugging, so that A52 exists with S57 supports A18", author=user2.uid, weight=0)
	textversion58 = TextVersion(content="This is for debugging, so that A53 exists with S58 supports A19", author=user2.uid, weight=0)
	textversion59 = TextVersion(content="This is for debugging, so that A54 exists with S59 supports A20", author=user2.uid, weight=0)
	textversion60 = TextVersion(content="This is for debugging, so that A55 exists with S60 supports A21", author=user2.uid, weight=0)
	textversion61 = TextVersion(content="This is for debugging, so that A56 exists with S61 supports A22", author=user2.uid, weight=0)
	textversion62 = TextVersion(content="This is for debugging, so that A57 exists with S62 supports A23", author=user2.uid, weight=0)
	textversion63 = TextVersion(content="This is for debugging, so that A58 exists with S63 supports A24", author=user2.uid, weight=0)
	textversion64 = TextVersion(content="This is for debugging, so that A59 exists with S64 supports A25", author=user2.uid, weight=0)
	textversion65 = TextVersion(content="This is for debugging, so that A60 exists with S65 supports A26", author=user2.uid, weight=0)
	textversion66 = TextVersion(content="This is for debugging, so that A61 exists with S66 supports A27", author=user2.uid, weight=0)
	textversion67 = TextVersion(content="This is for debugging, so that A62 exists with S67 supports A28", author=user2.uid, weight=0)
	textversion68 = TextVersion(content="For debugging argument 63. Thus this attacks 'Fluffy animals losing much hai[...]'", author=user2.uid, weight=0)
	textversion69 = TextVersion(content="For debugging argument 64. Thus this attacks 'You could use a automatic vacu[...]'", author=user2.uid, weight=0)
	textversion70 = TextVersion(content="For debugging argument 65. Thus this attacks 'Cats ancestors are animals in [...]'", author=user2.uid, weight=0)
	textversion71 = TextVersion(content="Even overbred races can be taught.", author=user2.uid, weight=0)
	textversion72 = TextVersion(content="For debugging argument 67. Thus this attacks 'This lies in their the natural[...]'", author=user2.uid, weight=0)
	textversion73 = TextVersion(content="Several pets are nice to have and you do not have to take much care of them, for example turtles or cats, which are living outside.", author=user2.uid, weight=0)
	textversion74 = TextVersion(content="For debugging argument 69. Thus this attacks 'Several cats of friends of min[...]'", author=user2.uid, weight=0)
	textversion75 = TextVersion(content="For debugging argument 70. Thus this attacks 'This fact is based on the cats[...]'", author=user2.uid, weight=0)
	textversion76 = TextVersion(content="For debugging argument 71. Thus this attacks 'All cats of my friends are cap[...]'", author=user2.uid, weight=0)
	textversion77 = TextVersion(content="For debugging argument 72. Thus this attacks 'This is based on the cats race[...]'", author=user2.uid, weight=0)
	textversion78 = TextVersion(content="For debugging argument 73. Thus this attacks 'Next to the taxes you will nee[...]'", author=user2.uid, weight=0)
	textversion79 = TextVersion(content="For debugging argument 74. Thus this attacks 'The equipment for running cost[...]'", author=user2.uid, weight=0)
	textversion80 = TextVersion(content="For debugging argument 75. Thus this attacks 'This is just a claim without a[...]'", author=user2.uid, weight=0)
	textversion81 = TextVersion(content="For debugging argument 76. Thus this attacks 'In Germany you have to pay for[...]'", author=user2.uid, weight=0)
	textversion82 = TextVersion(content="For debugging argument 77. Thus this attacks 'It is important, that pets are[...]'", author=user2.uid, weight=0)
	textversion83 = TextVersion(content="For debugging argument 78. Thus this attacks 'Cats are little, sweet and inn[...]'", author=user2.uid, weight=0)
	textversion84 = TextVersion(content="For debugging argument 79. Thus this attacks 'Do you have ever seen a sphinx[...]'", author=user2.uid, weight=0)
	textversion85 = TextVersion(content="For debugging argument 80. Thus this supports 'Fluffy animals losing much hai[...]'", author=user2.uid, weight=0)
	textversion86 = TextVersion(content="For debugging argument 81. Thus this supports 'You could use a automatic vacu[...]'", author=user2.uid, weight=0)
	textversion87 = TextVersion(content="For debugging argument 82. Thus this supports 'Cats ancestors are animals in [...]'", author=user2.uid, weight=0)
	textversion88 = TextVersion(content="For debugging argument 83. Thus this supports 'This is not true for overbred [...]'", author=user2.uid, weight=0)
	textversion89 = TextVersion(content="For debugging argument 84. Thus this supports 'This lies in their the natural[...]'", author=user2.uid, weight=0)
	textversion90 = TextVersion(content="For debugging argument 85. Thus this supports 'The purpose of a pet is to hav[...]'", author=user2.uid, weight=0)
	textversion91 = TextVersion(content="For debugging argument 86. Thus this supports 'Several cats of friends of min[...]'", author=user2.uid, weight=0)
	textversion92 = TextVersion(content="For debugging argument 87. Thus this supports 'This fact is based on the cats[...]'", author=user2.uid, weight=0)
	textversion93 = TextVersion(content="For debugging argument 88. Thus this supports 'All cats of my friends are cap[...]'", author=user2.uid, weight=0)
	textversion94 = TextVersion(content="For debugging argument 89. Thus this supports 'This is based on the cats race[...]'", author=user2.uid, weight=0)
	textversion95 = TextVersion(content="For debugging argument 90. Thus this supports 'Next to the taxes you will nee[...]'", author=user2.uid, weight=0)
	textversion96 = TextVersion(content="For debugging argument 91. Thus this supports 'The equipment for running cost[...]'", author=user2.uid, weight=0)
	textversion97 = TextVersion(content="For debugging argument 92. Thus this supports 'This is just a claim without a[...]'", author=user2.uid, weight=0)
	textversion98 = TextVersion(content="For debugging argument 93. Thus this supports 'In Germany you have to pay for[...]'", author=user2.uid, weight=0)
	textversion99 = TextVersion(content="For debugging argument 94. Thus this supports 'It is important, that pets are[...]'", author=user2.uid, weight=0)
	textversion100 = TextVersion(content="For debugging argument 95. Thus this supports 'Cats are little, sweet and inn[...]'", author=user2.uid, weight=0)
	textversion101 = TextVersion(content="For debugging argument 96. Thus this supports 'Do you have ever seen a sphinx[...]'", author=user2.uid, weight=0)

	textversion102 = TextVersion(content="We should shut down university park.", author=user2.uid, weight=0)
	textversion103 = TextVersion(content="Shutting down university park will save 100.000$ a year.", author=user2.uid, weight=0)
	textversion104 = TextVersion(content="Criminals use university park to sell drugs.", author=user2.uid, weight=0)
	textversion105 = TextVersion(content="We should not give in to criminals.", author=user2.uid, weight=0)
	textversion106 = TextVersion(content="We should close public swimming pools.", author=user2.uid, weight=0)
	textversion107 = TextVersion(content="The mayor should increase the taxes", author=user2.uid, weight=0)
	textversion108 = TextVersion(content="The number of police patrols should be increased.", author=user2.uid, weight=0)

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
	                             textversion106, textversion107, textversion108] )
	DBDiscussionSession.flush()

	#Adding all textvalues
	textvalue1 = TextValue(textversion=textversion1.uid)
	textvalue2 = TextValue(textversion=textversion2.uid)
	textvalue3 = TextValue(textversion=textversion3.uid)
	textvalue4 = TextValue(textversion=textversion4.uid)
	textvalue5 = TextValue(textversion=textversion5.uid)
	textvalue6 = TextValue(textversion=textversion6.uid)
	textvalue7 = TextValue(textversion=textversion7.uid)
	textvalue8 = TextValue(textversion=textversion8.uid)
	textvalue9 = TextValue(textversion=textversion9.uid)
	textvalue10 = TextValue(textversion=textversion10.uid)
	textvalue11 = TextValue(textversion=textversion11.uid)
	textvalue12 = TextValue(textversion=textversion12.uid)
	textvalue13 = TextValue(textversion=textversion13.uid)
	textvalue14 = TextValue(textversion=textversion14.uid)
	textvalue15 = TextValue(textversion=textversion15.uid)
	textvalue16 = TextValue(textversion=textversion16.uid)
	textvalue17 = TextValue(textversion=textversion17.uid)
	textvalue18 = TextValue(textversion=textversion18.uid)
	textvalue19 = TextValue(textversion=textversion19.uid)
	textvalue20 = TextValue(textversion=textversion20.uid)
	textvalue21 = TextValue(textversion=textversion21.uid)
	textvalue22 = TextValue(textversion=textversion22.uid)
	textvalue23 = TextValue(textversion=textversion23.uid)
	textvalue24 = TextValue(textversion=textversion24.uid)
	textvalue25 = TextValue(textversion=textversion25.uid)
	textvalue26 = TextValue(textversion=textversion26.uid)
	textvalue27 = TextValue(textversion=textversion27.uid)
	textvalue29 = TextValue(textversion=textversion29.uid)
	textvalue30 = TextValue(textversion=textversion30.uid)
	textvalue31 = TextValue(textversion=textversion31.uid)
	textvalue32 = TextValue(textversion=textversion32.uid)
	textvalue33 = TextValue(textversion=textversion33.uid)
	textvalue34 = TextValue(textversion=textversion34.uid)
	textvalue35 = TextValue(textversion=textversion35.uid)
	textvalue36 = TextValue(textversion=textversion36.uid)
	textvalue37 = TextValue(textversion=textversion37.uid)
	textvalue38 = TextValue(textversion=textversion38.uid)
	textvalue39 = TextValue(textversion=textversion39.uid)
	textvalue40 = TextValue(textversion=textversion40.uid)
	textvalue41 = TextValue(textversion=textversion41.uid)
	textvalue42 = TextValue(textversion=textversion42.uid)
	textvalue43 = TextValue(textversion=textversion43.uid)
	textvalue44 = TextValue(textversion=textversion44.uid)
	textvalue45 = TextValue(textversion=textversion45.uid)
	textvalue46 = TextValue(textversion=textversion46.uid)
	textvalue47 = TextValue(textversion=textversion47.uid)
	textvalue48 = TextValue(textversion=textversion48.uid)
	textvalue49 = TextValue(textversion=textversion49.uid)
	textvalue50 = TextValue(textversion=textversion50.uid)
	textvalue51 = TextValue(textversion=textversion51.uid)
	textvalue52 = TextValue(textversion=textversion52.uid)
	textvalue53 = TextValue(textversion=textversion53.uid)
	textvalue54 = TextValue(textversion=textversion54.uid)
	textvalue55 = TextValue(textversion=textversion55.uid)
	textvalue56 = TextValue(textversion=textversion56.uid)
	textvalue57 = TextValue(textversion=textversion57.uid)
	textvalue58 = TextValue(textversion=textversion58.uid)
	textvalue59 = TextValue(textversion=textversion59.uid)
	textvalue60 = TextValue(textversion=textversion60.uid)
	textvalue61 = TextValue(textversion=textversion61.uid)
	textvalue62 = TextValue(textversion=textversion62.uid)
	textvalue63 = TextValue(textversion=textversion63.uid)
	textvalue64 = TextValue(textversion=textversion64.uid)
	textvalue65 = TextValue(textversion=textversion65.uid)
	textvalue66 = TextValue(textversion=textversion66.uid)
	textvalue67 = TextValue(textversion=textversion67.uid)
	textvalue68 = TextValue(textversion=textversion68.uid)
	textvalue69 = TextValue(textversion=textversion69.uid)
	textvalue70 = TextValue(textversion=textversion70.uid)
	textvalue71 = TextValue(textversion=textversion71.uid)
	textvalue72 = TextValue(textversion=textversion72.uid)
	textvalue73 = TextValue(textversion=textversion73.uid)
	textvalue74 = TextValue(textversion=textversion74.uid)
	textvalue75 = TextValue(textversion=textversion75.uid)
	textvalue76 = TextValue(textversion=textversion76.uid)
	textvalue77 = TextValue(textversion=textversion77.uid)
	textvalue78 = TextValue(textversion=textversion78.uid)
	textvalue79 = TextValue(textversion=textversion79.uid)
	textvalue80 = TextValue(textversion=textversion80.uid)
	textvalue81 = TextValue(textversion=textversion81.uid)
	textvalue82 = TextValue(textversion=textversion82.uid)
	textvalue83 = TextValue(textversion=textversion83.uid)
	textvalue84 = TextValue(textversion=textversion84.uid)
	textvalue85 = TextValue(textversion=textversion85.uid)
	textvalue86 = TextValue(textversion=textversion86.uid)
	textvalue87 = TextValue(textversion=textversion87.uid)
	textvalue88 = TextValue(textversion=textversion88.uid)
	textvalue89 = TextValue(textversion=textversion89.uid)
	textvalue90 = TextValue(textversion=textversion90.uid)
	textvalue91 = TextValue(textversion=textversion91.uid)
	textvalue92 = TextValue(textversion=textversion92.uid)
	textvalue93 = TextValue(textversion=textversion93.uid)
	textvalue94 = TextValue(textversion=textversion94.uid)
	textvalue95 = TextValue(textversion=textversion95.uid)
	textvalue96 = TextValue(textversion=textversion96.uid)
	textvalue97 = TextValue(textversion=textversion97.uid)
	textvalue98 = TextValue(textversion=textversion98.uid)
	textvalue99 = TextValue(textversion=textversion99.uid)
	textvalue100 = TextValue(textversion=textversion100.uid)
	textvalue101 = TextValue(textversion=textversion101.uid)

	textvalue102 = TextValue(textversion=textversion102.uid)
	textvalue103 = TextValue(textversion=textversion103.uid)
	textvalue104 = TextValue(textversion=textversion104.uid)
	textvalue105 = TextValue(textversion=textversion105.uid)
	textvalue106 = TextValue(textversion=textversion106.uid)
	textvalue107 = TextValue(textversion=textversion107.uid)
	textvalue108 = TextValue(textversion=textversion108.uid)

	DBDiscussionSession.add_all([textvalue1, textvalue2, textvalue3, textvalue4, textvalue5, textvalue6, textvalue7, textvalue8,
	                             textvalue9, textvalue10, textvalue11, textvalue12, textvalue13, textvalue14, textvalue15, textvalue16,
	                             textvalue17, textvalue18, textvalue19, textvalue20, textvalue21, textvalue22, textvalue23, textvalue24,
	                             textvalue25, textvalue26, textvalue27, textvalue29, textvalue30, textvalue31, textvalue32, textvalue33,
	                             textvalue34, textvalue35, textvalue36, textvalue37, textvalue38, textvalue39, textvalue40, textvalue41,
	                             textvalue42, textvalue43, textvalue44, textvalue45, textvalue46, textvalue47, textvalue48, textvalue49,
	                             textvalue50, textvalue51, textvalue52, textvalue53, textvalue54, textvalue55, textvalue56, textvalue57,
	                             textvalue58, textvalue59, textvalue60, textvalue61, textvalue62, textvalue63, textvalue64, textvalue65,
	                             textvalue66, textvalue67, textvalue68, textvalue69, textvalue70, textvalue71, textvalue72, textvalue73,
	                             textvalue74, textvalue75, textvalue76, textvalue77, textvalue78, textvalue79, textvalue80, textvalue81,
	                             textvalue82, textvalue83, textvalue84, textvalue85, textvalue86, textvalue87, textvalue88, textvalue89,
	                             textvalue90, textvalue91, textvalue92, textvalue93, textvalue94, textvalue95, textvalue96, textvalue97,
	                             textvalue98, textvalue99, textvalue100, textvalue101, textvalue102, textvalue103, textvalue104,
	                             textvalue105, textvalue106, textvalue107, textvalue108])
	DBDiscussionSession.flush()

	#Set textvalues of the textversions
	textversion1.set_textvalue(textvalue1.uid)
	textversion2.set_textvalue(textvalue2.uid)
	textversion3.set_textvalue(textvalue3.uid)
	textversion4.set_textvalue(textvalue4.uid)
	textversion5.set_textvalue(textvalue5.uid)
	textversion6.set_textvalue(textvalue6.uid)
	textversion7.set_textvalue(textvalue7.uid)
	textversion8.set_textvalue(textvalue8.uid)
	textversion9.set_textvalue(textvalue9.uid)
	textversion10.set_textvalue(textvalue10.uid)
	textversion11.set_textvalue(textvalue11.uid)
	textversion12.set_textvalue(textvalue12.uid)
	textversion13.set_textvalue(textvalue13.uid)
	textversion14.set_textvalue(textvalue14.uid)
	textversion15.set_textvalue(textvalue15.uid)
	textversion16.set_textvalue(textvalue16.uid)
	textversion17.set_textvalue(textvalue17.uid)
	textversion18.set_textvalue(textvalue18.uid)
	textversion19.set_textvalue(textvalue19.uid)
	textversion20.set_textvalue(textvalue20.uid)
	textversion21.set_textvalue(textvalue21.uid)
	textversion22.set_textvalue(textvalue22.uid)
	textversion23.set_textvalue(textvalue23.uid)
	textversion24.set_textvalue(textvalue24.uid)
	textversion25.set_textvalue(textvalue25.uid)
	textversion26.set_textvalue(textvalue26.uid)
	textversion27.set_textvalue(textvalue27.uid)
	textversion29.set_textvalue(textvalue29.uid)
	textversion30.set_textvalue(textvalue30.uid)
	textversion31.set_textvalue(textvalue31.uid)
	textversion32.set_textvalue(textvalue32.uid)
	textversion33.set_textvalue(textvalue33.uid)
	textversion34.set_textvalue(textvalue34.uid)
	textversion35.set_textvalue(textvalue35.uid)
	textversion36.set_textvalue(textvalue36.uid)
	textversion37.set_textvalue(textvalue37.uid)
	textversion38.set_textvalue(textvalue38.uid)
	textversion39.set_textvalue(textvalue39.uid)
	textversion40.set_textvalue(textvalue40.uid)
	textversion41.set_textvalue(textvalue41.uid)
	textversion42.set_textvalue(textvalue42.uid)
	textversion43.set_textvalue(textvalue43.uid)
	textversion44.set_textvalue(textvalue44.uid)
	textversion45.set_textvalue(textvalue45.uid)
	textversion46.set_textvalue(textvalue46.uid)
	textversion47.set_textvalue(textvalue47.uid)
	textversion48.set_textvalue(textvalue48.uid)
	textversion49.set_textvalue(textvalue49.uid)
	textversion50.set_textvalue(textvalue50.uid)
	textversion51.set_textvalue(textvalue51.uid)
	textversion52.set_textvalue(textvalue52.uid)
	textversion53.set_textvalue(textvalue53.uid)
	textversion54.set_textvalue(textvalue54.uid)
	textversion55.set_textvalue(textvalue55.uid)
	textversion56.set_textvalue(textvalue56.uid)
	textversion57.set_textvalue(textvalue57.uid)
	textversion58.set_textvalue(textvalue58.uid)
	textversion59.set_textvalue(textvalue59.uid)
	textversion60.set_textvalue(textvalue60.uid)
	textversion61.set_textvalue(textvalue61.uid)
	textversion62.set_textvalue(textvalue62.uid)
	textversion63.set_textvalue(textvalue63.uid)
	textversion64.set_textvalue(textvalue64.uid)
	textversion65.set_textvalue(textvalue65.uid)
	textversion66.set_textvalue(textvalue66.uid)
	textversion67.set_textvalue(textvalue67.uid)
	textversion68.set_textvalue(textvalue68.uid)
	textversion69.set_textvalue(textvalue69.uid)
	textversion70.set_textvalue(textvalue70.uid)
	textversion71.set_textvalue(textvalue71.uid)
	textversion72.set_textvalue(textvalue72.uid)
	textversion73.set_textvalue(textvalue73.uid)
	textversion74.set_textvalue(textvalue74.uid)
	textversion75.set_textvalue(textvalue75.uid)
	textversion76.set_textvalue(textvalue76.uid)
	textversion77.set_textvalue(textvalue77.uid)
	textversion78.set_textvalue(textvalue78.uid)
	textversion79.set_textvalue(textvalue79.uid)
	textversion80.set_textvalue(textvalue80.uid)
	textversion81.set_textvalue(textvalue81.uid)
	textversion82.set_textvalue(textvalue82.uid)
	textversion83.set_textvalue(textvalue83.uid)
	textversion84.set_textvalue(textvalue84.uid)
	textversion85.set_textvalue(textvalue85.uid)
	textversion86.set_textvalue(textvalue86.uid)
	textversion87.set_textvalue(textvalue87.uid)
	textversion88.set_textvalue(textvalue88.uid)
	textversion89.set_textvalue(textvalue89.uid)
	textversion90.set_textvalue(textvalue90.uid)
	textversion91.set_textvalue(textvalue91.uid)
	textversion92.set_textvalue(textvalue92.uid)
	textversion93.set_textvalue(textvalue93.uid)
	textversion94.set_textvalue(textvalue94.uid)
	textversion95.set_textvalue(textvalue95.uid)
	textversion96.set_textvalue(textvalue96.uid)
	textversion97.set_textvalue(textvalue97.uid)
	textversion98.set_textvalue(textvalue98.uid)
	textversion99.set_textvalue(textvalue99.uid)
	textversion100.set_textvalue(textvalue100.uid)
	textversion101.set_textvalue(textvalue101.uid)

	textversion102.set_textvalue(textvalue102.uid)
	textversion103.set_textvalue(textvalue103.uid)
	textversion104.set_textvalue(textvalue104.uid)
	textversion105.set_textvalue(textvalue105.uid)
	textversion106.set_textvalue(textvalue106.uid)
	textversion107.set_textvalue(textvalue107.uid)
	textversion108.set_textvalue(textvalue108.uid)
	DBDiscussionSession.flush()

	#Adding all statements
	statement1 = Statement(text=textvalue1.uid, isstartpoint=True, issue=issue1.uid)
	statement2 = Statement(text=textvalue2.uid, isstartpoint=True, issue=issue1.uid)
	statement3 = Statement(text=textvalue3.uid, isstartpoint=True, issue=issue1.uid)
	statement4 = Statement(text=textvalue4.uid, isstartpoint=False, issue=issue1.uid)
	statement5 = Statement(text=textvalue5.uid, isstartpoint=False, issue=issue1.uid)
	statement6 = Statement(text=textvalue6.uid, isstartpoint=False, issue=issue1.uid)
	statement7 = Statement(text=textvalue7.uid, isstartpoint=False, issue=issue1.uid)
	statement8 = Statement(text=textvalue8.uid, isstartpoint=False, issue=issue1.uid)
	statement9 = Statement(text=textvalue9.uid, isstartpoint=False, issue=issue1.uid)
	statement10 = Statement(text=textvalue10.uid, isstartpoint=False, issue=issue1.uid)
	statement11 = Statement(text=textvalue11.uid, isstartpoint=False, issue=issue1.uid)
	statement12 = Statement(text=textvalue12.uid, isstartpoint=False, issue=issue1.uid)
	statement13 = Statement(text=textvalue13.uid, isstartpoint=False, issue=issue1.uid)
	statement14 = Statement(text=textvalue14.uid, isstartpoint=False, issue=issue1.uid)
	statement15 = Statement(text=textvalue15.uid, isstartpoint=False, issue=issue1.uid)
	statement16 = Statement(text=textvalue16.uid, isstartpoint=False, issue=issue1.uid)
	statement17 = Statement(text=textvalue17.uid, isstartpoint=False, issue=issue1.uid)
	statement18 = Statement(text=textvalue18.uid, isstartpoint=False, issue=issue1.uid)
	statement19 = Statement(text=textvalue19.uid, isstartpoint=False, issue=issue1.uid)
	statement20 = Statement(text=textvalue20.uid, isstartpoint=False, issue=issue1.uid)
	statement21 = Statement(text=textvalue21.uid, isstartpoint=False, issue=issue1.uid)
	statement22 = Statement(text=textvalue22.uid, isstartpoint=False, issue=issue1.uid)
	statement23 = Statement(text=textvalue23.uid, isstartpoint=False, issue=issue1.uid)
	statement24 = Statement(text=textvalue24.uid, isstartpoint=False, issue=issue1.uid)
	statement25 = Statement(text=textvalue25.uid, isstartpoint=False, issue=issue1.uid)
	statement26 = Statement(text=textvalue26.uid, isstartpoint=False, issue=issue1.uid)
	statement27 = Statement(text=textvalue27.uid, isstartpoint=False, issue=issue1.uid)
	statement29 = Statement(text=textvalue29.uid, isstartpoint=False, issue=issue1.uid)
	statement30 = Statement(text=textvalue30.uid, isstartpoint=False, issue=issue1.uid)
	statement31 = Statement(text=textvalue31.uid, isstartpoint=False, issue=issue1.uid)
	statement32 = Statement(text=textvalue32.uid, isstartpoint=False, issue=issue1.uid)
	statement33 = Statement(text=textvalue33.uid, isstartpoint=False, issue=issue1.uid)
	statement34 = Statement(text=textvalue34.uid, isstartpoint=False, issue=issue1.uid)
	statement35 = Statement(text=textvalue35.uid, isstartpoint=False, issue=issue1.uid)
	statement36 = Statement(text=textvalue36.uid, isstartpoint=False, issue=issue1.uid)
	statement37 = Statement(text=textvalue37.uid, isstartpoint=False, issue=issue1.uid)
	statement38 = Statement(text=textvalue38.uid, isstartpoint=False, issue=issue1.uid)
	statement39 = Statement(text=textvalue39.uid, isstartpoint=False, issue=issue1.uid)
	statement40 = Statement(text=textvalue40.uid, isstartpoint=False, issue=issue1.uid)
	statement41 = Statement(text=textvalue41.uid, isstartpoint=False, issue=issue1.uid)
	statement42 = Statement(text=textvalue42.uid, isstartpoint=False, issue=issue1.uid)
	statement43 = Statement(text=textvalue43.uid, isstartpoint=False, issue=issue1.uid)
	statement44 = Statement(text=textvalue44.uid, isstartpoint=False, issue=issue1.uid)
	statement45 = Statement(text=textvalue45.uid, isstartpoint=False, issue=issue1.uid)
	statement46 = Statement(text=textvalue46.uid, isstartpoint=False, issue=issue1.uid)
	statement47 = Statement(text=textvalue47.uid, isstartpoint=False, issue=issue1.uid)
	statement48 = Statement(text=textvalue48.uid, isstartpoint=False, issue=issue1.uid)
	statement49 = Statement(text=textvalue49.uid, isstartpoint=False, issue=issue1.uid)
	statement50 = Statement(text=textvalue50.uid, isstartpoint=False, issue=issue1.uid)
	statement51 = Statement(text=textvalue51.uid, isstartpoint=False, issue=issue1.uid)
	statement52 = Statement(text=textvalue52.uid, isstartpoint=False, issue=issue1.uid)
	statement53 = Statement(text=textvalue53.uid, isstartpoint=False, issue=issue1.uid)
	statement54 = Statement(text=textvalue54.uid, isstartpoint=False, issue=issue1.uid)
	statement55 = Statement(text=textvalue55.uid, isstartpoint=False, issue=issue1.uid)
	statement56 = Statement(text=textvalue56.uid, isstartpoint=False, issue=issue1.uid)
	statement57 = Statement(text=textvalue57.uid, isstartpoint=False, issue=issue1.uid)
	statement58 = Statement(text=textvalue58.uid, isstartpoint=False, issue=issue1.uid)
	statement59 = Statement(text=textvalue59.uid, isstartpoint=False, issue=issue1.uid)
	statement60 = Statement(text=textvalue60.uid, isstartpoint=False, issue=issue1.uid)
	statement61 = Statement(text=textvalue61.uid, isstartpoint=False, issue=issue1.uid)
	statement62 = Statement(text=textvalue62.uid, isstartpoint=False, issue=issue1.uid)
	statement63 = Statement(text=textvalue63.uid, isstartpoint=False, issue=issue1.uid)
	statement64 = Statement(text=textvalue64.uid, isstartpoint=False, issue=issue1.uid)
	statement65 = Statement(text=textvalue65.uid, isstartpoint=False, issue=issue1.uid)
	statement66 = Statement(text=textvalue66.uid, isstartpoint=False, issue=issue1.uid)
	statement67 = Statement(text=textvalue67.uid, isstartpoint=False, issue=issue1.uid)
	statement68 = Statement(text=textvalue68.uid, isstartpoint=False, issue=issue1.uid)
	statement69 = Statement(text=textvalue69.uid, isstartpoint=False, issue=issue1.uid)
	statement70 = Statement(text=textvalue70.uid, isstartpoint=False, issue=issue1.uid)
	statement71 = Statement(text=textvalue71.uid, isstartpoint=False, issue=issue1.uid)
	statement72 = Statement(text=textvalue72.uid, isstartpoint=False, issue=issue1.uid)
	statement73 = Statement(text=textvalue73.uid, isstartpoint=False, issue=issue1.uid)
	statement74 = Statement(text=textvalue74.uid, isstartpoint=False, issue=issue1.uid)
	statement75 = Statement(text=textvalue75.uid, isstartpoint=False, issue=issue1.uid)
	statement76 = Statement(text=textvalue76.uid, isstartpoint=False, issue=issue1.uid)
	statement77 = Statement(text=textvalue77.uid, isstartpoint=False, issue=issue1.uid)
	statement78 = Statement(text=textvalue78.uid, isstartpoint=False, issue=issue1.uid)
	statement79 = Statement(text=textvalue79.uid, isstartpoint=False, issue=issue1.uid)
	statement80 = Statement(text=textvalue80.uid, isstartpoint=False, issue=issue1.uid)
	statement81 = Statement(text=textvalue81.uid, isstartpoint=False, issue=issue1.uid)
	statement82 = Statement(text=textvalue82.uid, isstartpoint=False, issue=issue1.uid)
	statement83 = Statement(text=textvalue83.uid, isstartpoint=False, issue=issue1.uid)
	statement84 = Statement(text=textvalue84.uid, isstartpoint=False, issue=issue1.uid)
	statement85 = Statement(text=textvalue85.uid, isstartpoint=False, issue=issue1.uid)
	statement86 = Statement(text=textvalue86.uid, isstartpoint=False, issue=issue1.uid)
	statement87 = Statement(text=textvalue87.uid, isstartpoint=False, issue=issue1.uid)
	statement88 = Statement(text=textvalue88.uid, isstartpoint=False, issue=issue1.uid)
	statement89 = Statement(text=textvalue89.uid, isstartpoint=False, issue=issue1.uid)
	statement90 = Statement(text=textvalue90.uid, isstartpoint=False, issue=issue1.uid)
	statement91 = Statement(text=textvalue91.uid, isstartpoint=False, issue=issue1.uid)
	statement92 = Statement(text=textvalue92.uid, isstartpoint=False, issue=issue1.uid)
	statement93 = Statement(text=textvalue93.uid, isstartpoint=False, issue=issue1.uid)
	statement94 = Statement(text=textvalue94.uid, isstartpoint=False, issue=issue1.uid)
	statement95 = Statement(text=textvalue95.uid, isstartpoint=False, issue=issue1.uid)
	statement96 = Statement(text=textvalue96.uid, isstartpoint=False, issue=issue1.uid)
	statement97 = Statement(text=textvalue97.uid, isstartpoint=False, issue=issue1.uid)
	statement98 = Statement(text=textvalue98.uid, isstartpoint=False, issue=issue1.uid)
	statement99 = Statement(text=textvalue99.uid, isstartpoint=False, issue=issue1.uid)
	statement100 = Statement(text=textvalue100.uid, isstartpoint=False, issue=issue1.uid)
	statement101 = Statement(text=textvalue101.uid, isstartpoint=False, issue=issue1.uid)

	statement102 = Statement(text=textvalue102.uid, isstartpoint=True, issue=issue2.uid)
	statement103 = Statement(text=textvalue103.uid, isstartpoint=False, issue=issue2.uid)
	statement104 = Statement(text=textvalue104.uid, isstartpoint=False, issue=issue2.uid)
	statement105 = Statement(text=textvalue105.uid, isstartpoint=False, issue=issue2.uid)
	statement106 = Statement(text=textvalue106.uid, isstartpoint=True, issue=issue2.uid)
	statement107 = Statement(text=textvalue107.uid, isstartpoint=True, issue=issue2.uid)
	statement108 = Statement(text=textvalue108.uid, isstartpoint=False, issue=issue2.uid)

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
	                             statement105, statement106, statement107, statement108])
	DBDiscussionSession.flush()

	#Adding all premissegroups
	premissegroup1 = PremisseGroup(author=user2.uid)
	premissegroup2 = PremisseGroup(author=user2.uid)
	premissegroup3 = PremisseGroup(author=user2.uid)
	premissegroup4 = PremisseGroup(author=user2.uid)
	premissegroup5 = PremisseGroup(author=user2.uid)
	premissegroup6 = PremisseGroup(author=user2.uid)
	premissegroup7 = PremisseGroup(author=user2.uid)
	premissegroup8 = PremisseGroup(author=user2.uid)
	premissegroup9 = PremisseGroup(author=user2.uid)
	premissegroup10 = PremisseGroup(author=user2.uid)
	premissegroup11 = PremisseGroup(author=user2.uid)
	premissegroup12 = PremisseGroup(author=user2.uid)
	premissegroup13 = PremisseGroup(author=user2.uid)
	premissegroup14 = PremisseGroup(author=user2.uid)
	premissegroup15 = PremisseGroup(author=user2.uid)
	premissegroup16 = PremisseGroup(author=user2.uid)
	premissegroup17 = PremisseGroup(author=user2.uid)
	premissegroup18 = PremisseGroup(author=user2.uid)
	premissegroup19 = PremisseGroup(author=user2.uid)
	premissegroup20 = PremisseGroup(author=user2.uid)
	premissegroup21 = PremisseGroup(author=user2.uid)
	premissegroup22 = PremisseGroup(author=user2.uid)
	premissegroup23 = PremisseGroup(author=user2.uid)
	premissegroup24 = PremisseGroup(author=user2.uid)
	premissegroup25 = PremisseGroup(author=user2.uid)
	premissegroup26 = PremisseGroup(author=user2.uid)
	premissegroup27 = PremisseGroup(author=user2.uid)
	premissegroup28 = PremisseGroup(author=user2.uid)
	premissegroup29 = PremisseGroup(author=user2.uid)
	premissegroup30 = PremisseGroup(author=user2.uid)
	premissegroup31 = PremisseGroup(author=user2.uid)
	premissegroup32 = PremisseGroup(author=user2.uid)
	premissegroup33 = PremisseGroup(author=user2.uid)
	premissegroup34 = PremisseGroup(author=user2.uid)
	premissegroup35 = PremisseGroup(author=user2.uid)
	premissegroup36 = PremisseGroup(author=user2.uid)
	premissegroup37 = PremisseGroup(author=user2.uid)
	premissegroup38 = PremisseGroup(author=user2.uid)
	premissegroup39 = PremisseGroup(author=user2.uid)
	premissegroup40 = PremisseGroup(author=user2.uid)
	premissegroup41 = PremisseGroup(author=user2.uid)
	premissegroup42 = PremisseGroup(author=user2.uid)
	premissegroup43 = PremisseGroup(author=user2.uid)
	premissegroup44 = PremisseGroup(author=user2.uid)
	premissegroup45 = PremisseGroup(author=user2.uid)
	premissegroup46 = PremisseGroup(author=user2.uid)
	premissegroup47 = PremisseGroup(author=user2.uid)
	premissegroup48 = PremisseGroup(author=user2.uid)
	premissegroup49 = PremisseGroup(author=user2.uid)
	premissegroup50 = PremisseGroup(author=user2.uid)
	premissegroup51 = PremisseGroup(author=user2.uid)
	premissegroup52 = PremisseGroup(author=user2.uid)
	premissegroup53 = PremisseGroup(author=user2.uid)
	premissegroup54 = PremisseGroup(author=user2.uid)
	premissegroup55 = PremisseGroup(author=user2.uid)
	premissegroup56 = PremisseGroup(author=user2.uid)
	premissegroup57 = PremisseGroup(author=user2.uid)
	premissegroup58 = PremisseGroup(author=user2.uid)
	premissegroup59 = PremisseGroup(author=user2.uid)
	premissegroup60 = PremisseGroup(author=user2.uid)
	premissegroup61 = PremisseGroup(author=user2.uid)
	premissegroup62 = PremisseGroup(author=user2.uid)
	premissegroup63 = PremisseGroup(author=user2.uid)
	premissegroup64 = PremisseGroup(author=user2.uid)
	premissegroup65 = PremisseGroup(author=user2.uid)
	premissegroup66 = PremisseGroup(author=user2.uid)
	premissegroup67 = PremisseGroup(author=user2.uid)
	premissegroup68 = PremisseGroup(author=user2.uid)
	premissegroup69 = PremisseGroup(author=user2.uid)
	premissegroup70 = PremisseGroup(author=user2.uid)
	premissegroup71 = PremisseGroup(author=user2.uid)
	premissegroup72 = PremisseGroup(author=user2.uid)
	premissegroup73 = PremisseGroup(author=user2.uid)
	premissegroup74 = PremisseGroup(author=user2.uid)
	premissegroup75 = PremisseGroup(author=user2.uid)
	premissegroup76 = PremisseGroup(author=user2.uid)
	premissegroup77 = PremisseGroup(author=user2.uid)
	premissegroup78 = PremisseGroup(author=user2.uid)
	premissegroup79 = PremisseGroup(author=user2.uid)
	premissegroup80 = PremisseGroup(author=user2.uid)
	premissegroup81 = PremisseGroup(author=user2.uid)
	premissegroup82 = PremisseGroup(author=user2.uid)
	premissegroup83 = PremisseGroup(author=user2.uid)
	premissegroup84 = PremisseGroup(author=user2.uid)
	premissegroup85 = PremisseGroup(author=user2.uid)
	premissegroup86 = PremisseGroup(author=user2.uid)
	premissegroup87 = PremisseGroup(author=user2.uid)
	premissegroup88 = PremisseGroup(author=user2.uid)
	premissegroup89 = PremisseGroup(author=user2.uid)
	premissegroup90 = PremisseGroup(author=user2.uid)
	premissegroup91 = PremisseGroup(author=user2.uid)
	premissegroup92 = PremisseGroup(author=user2.uid)
	premissegroup93 = PremisseGroup(author=user2.uid)
	premissegroup94 = PremisseGroup(author=user2.uid)
	premissegroup95 = PremisseGroup(author=user2.uid)
	premissegroup96 = PremisseGroup(author=user2.uid)

	premissegroup97 = PremisseGroup(author=user2.uid)
	premissegroup98 = PremisseGroup(author=user2.uid)
	premissegroup99 = PremisseGroup(author=user2.uid)
	premissegroup100 = PremisseGroup(author=user2.uid)
	premissegroup101 = PremisseGroup(author=user2.uid)
	premissegroup102 = PremisseGroup(author=user2.uid)
	premissegroup103 = PremisseGroup(author=user2.uid)

	DBDiscussionSession.add_all([premissegroup1, premissegroup2, premissegroup3, premissegroup4, premissegroup5, premissegroup6,
	                             premissegroup7, premissegroup8, premissegroup9, premissegroup10, premissegroup11, premissegroup12,
	                             premissegroup13, premissegroup14, premissegroup15, premissegroup16, premissegroup17, premissegroup18,
	                             premissegroup19, premissegroup20, premissegroup21, premissegroup22, premissegroup23, premissegroup24,
	                             premissegroup25, premissegroup26, premissegroup27, premissegroup28, premissegroup29, premissegroup30,
	                             premissegroup31, premissegroup32, premissegroup33, premissegroup34, premissegroup35, premissegroup36,
	                             premissegroup37, premissegroup38, premissegroup39, premissegroup40, premissegroup41, premissegroup42,
	                             premissegroup43, premissegroup44, premissegroup45, premissegroup46, premissegroup47, premissegroup48,
	                             premissegroup49, premissegroup50, premissegroup51, premissegroup52, premissegroup53, premissegroup54,
	                             premissegroup55, premissegroup56, premissegroup57, premissegroup58, premissegroup59, premissegroup60,
	                             premissegroup61, premissegroup62, premissegroup63, premissegroup64, premissegroup65, premissegroup66,
	                             premissegroup67, premissegroup68, premissegroup69, premissegroup70, premissegroup71, premissegroup72,
	                             premissegroup73, premissegroup74, premissegroup75, premissegroup76, premissegroup77, premissegroup78,
	                             premissegroup79, premissegroup80, premissegroup81, premissegroup82, premissegroup83, premissegroup84,
	                             premissegroup85, premissegroup86, premissegroup87, premissegroup88, premissegroup89, premissegroup90,
	                             premissegroup91, premissegroup92, premissegroup93, premissegroup94, premissegroup95, premissegroup96,
	                             premissegroup97, premissegroup98, premissegroup99, premissegroup100, premissegroup101, premissegroup102,
	                             premissegroup103])
	DBDiscussionSession.flush()

	premisse1 = Premisse(premissesgroup=premissegroup1.uid, statement=statement4.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse2 = Premisse(premissesgroup=premissegroup2.uid, statement=statement5.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse3 = Premisse(premissesgroup=premissegroup3.uid, statement=statement6.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse4 = Premisse(premissesgroup=premissegroup4.uid, statement=statement7.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse5 = Premisse(premissesgroup=premissegroup5.uid, statement=statement8.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse6 = Premisse(premissesgroup=premissegroup6.uid, statement=statement9.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse7 = Premisse(premissesgroup=premissegroup7.uid, statement=statement10.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse8 = Premisse(premissesgroup=premissegroup8.uid, statement=statement11.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse9 = Premisse(premissesgroup=premissegroup9.uid, statement=statement12.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse10 = Premisse(premissesgroup=premissegroup10.uid, statement=statement13.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse11 = Premisse(premissesgroup=premissegroup11.uid, statement=statement14.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse12 = Premisse(premissesgroup=premissegroup11.uid, statement=statement15.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse13 = Premisse(premissesgroup=premissegroup12.uid, statement=statement16.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse14 = Premisse(premissesgroup=premissegroup13.uid, statement=statement17.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse15 = Premisse(premissesgroup=premissegroup14.uid, statement=statement18.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse16 = Premisse(premissesgroup=premissegroup15.uid, statement=statement19.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse17 = Premisse(premissesgroup=premissegroup16.uid, statement=statement20.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse18 = Premisse(premissesgroup=premissegroup17.uid, statement=statement21.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse19 = Premisse(premissesgroup=premissegroup18.uid, statement=statement22.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse20 = Premisse(premissesgroup=premissegroup19.uid, statement=statement23.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse21 = Premisse(premissesgroup=premissegroup20.uid, statement=statement24.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse22 = Premisse(premissesgroup=premissegroup21.uid, statement=statement25.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse23 = Premisse(premissesgroup=premissegroup22.uid, statement=statement26.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse24 = Premisse(premissesgroup=premissegroup23.uid, statement=statement27.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse25 = Premisse(premissesgroup=premissegroup24.uid, statement=statement29.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse26 = Premisse(premissesgroup=premissegroup25.uid, statement=statement30.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse27 = Premisse(premissesgroup=premissegroup26.uid, statement=statement31.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse28 = Premisse(premissesgroup=premissegroup27.uid, statement=statement32.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse29 = Premisse(premissesgroup=premissegroup28.uid, statement=statement33.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse30 = Premisse(premissesgroup=premissegroup29.uid, statement=statement34.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse31 = Premisse(premissesgroup=premissegroup30.uid, statement=statement35.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse32 = Premisse(premissesgroup=premissegroup31.uid, statement=statement36.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse33 = Premisse(premissesgroup=premissegroup32.uid, statement=statement37.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse34 = Premisse(premissesgroup=premissegroup33.uid, statement=statement38.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse35 = Premisse(premissesgroup=premissegroup34.uid, statement=statement39.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse36 = Premisse(premissesgroup=premissegroup35.uid, statement=statement40.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse37 = Premisse(premissesgroup=premissegroup36.uid, statement=statement41.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse38 = Premisse(premissesgroup=premissegroup37.uid, statement=statement42.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse39 = Premisse(premissesgroup=premissegroup38.uid, statement=statement43.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse40 = Premisse(premissesgroup=premissegroup39.uid, statement=statement44.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse41 = Premisse(premissesgroup=premissegroup40.uid, statement=statement45.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse42 = Premisse(premissesgroup=premissegroup41.uid, statement=statement46.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse43 = Premisse(premissesgroup=premissegroup42.uid, statement=statement47.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse44 = Premisse(premissesgroup=premissegroup43.uid, statement=statement48.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse45 = Premisse(premissesgroup=premissegroup44.uid, statement=statement49.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse46 = Premisse(premissesgroup=premissegroup45.uid, statement=statement50.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse47 = Premisse(premissesgroup=premissegroup46.uid, statement=statement51.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse48 = Premisse(premissesgroup=premissegroup47.uid, statement=statement52.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse49 = Premisse(premissesgroup=premissegroup48.uid, statement=statement53.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse50 = Premisse(premissesgroup=premissegroup49.uid, statement=statement54.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse51 = Premisse(premissesgroup=premissegroup50.uid, statement=statement55.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse52 = Premisse(premissesgroup=premissegroup51.uid, statement=statement56.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse53 = Premisse(premissesgroup=premissegroup52.uid, statement=statement57.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse54 = Premisse(premissesgroup=premissegroup53.uid, statement=statement58.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse55 = Premisse(premissesgroup=premissegroup54.uid, statement=statement59.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse56 = Premisse(premissesgroup=premissegroup55.uid, statement=statement60.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse57 = Premisse(premissesgroup=premissegroup56.uid, statement=statement61.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse58 = Premisse(premissesgroup=premissegroup57.uid, statement=statement62.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse59 = Premisse(premissesgroup=premissegroup58.uid, statement=statement63.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse60 = Premisse(premissesgroup=premissegroup59.uid, statement=statement64.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse61 = Premisse(premissesgroup=premissegroup60.uid, statement=statement65.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse62 = Premisse(premissesgroup=premissegroup61.uid, statement=statement66.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse63 = Premisse(premissesgroup=premissegroup62.uid, statement=statement67.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse64 = Premisse(premissesgroup=premissegroup63.uid, statement=statement68.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse65 = Premisse(premissesgroup=premissegroup64.uid, statement=statement69.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse66 = Premisse(premissesgroup=premissegroup65.uid, statement=statement70.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse67 = Premisse(premissesgroup=premissegroup66.uid, statement=statement71.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse68 = Premisse(premissesgroup=premissegroup67.uid, statement=statement72.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse69 = Premisse(premissesgroup=premissegroup68.uid, statement=statement73.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse70 = Premisse(premissesgroup=premissegroup69.uid, statement=statement74.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse71 = Premisse(premissesgroup=premissegroup70.uid, statement=statement75.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse72 = Premisse(premissesgroup=premissegroup71.uid, statement=statement76.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse73 = Premisse(premissesgroup=premissegroup72.uid, statement=statement77.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse74 = Premisse(premissesgroup=premissegroup73.uid, statement=statement78.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse75 = Premisse(premissesgroup=premissegroup74.uid, statement=statement79.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse76 = Premisse(premissesgroup=premissegroup75.uid, statement=statement80.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse77 = Premisse(premissesgroup=premissegroup76.uid, statement=statement81.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse78 = Premisse(premissesgroup=premissegroup77.uid, statement=statement82.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse79 = Premisse(premissesgroup=premissegroup78.uid, statement=statement83.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse80 = Premisse(premissesgroup=premissegroup79.uid, statement=statement84.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse81 = Premisse(premissesgroup=premissegroup80.uid, statement=statement85.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse82 = Premisse(premissesgroup=premissegroup81.uid, statement=statement86.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse83 = Premisse(premissesgroup=premissegroup82.uid, statement=statement87.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse84 = Premisse(premissesgroup=premissegroup83.uid, statement=statement88.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse85 = Premisse(premissesgroup=premissegroup84.uid, statement=statement89.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse86 = Premisse(premissesgroup=premissegroup85.uid, statement=statement90.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse87 = Premisse(premissesgroup=premissegroup86.uid, statement=statement91.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse88 = Premisse(premissesgroup=premissegroup87.uid, statement=statement92.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse89 = Premisse(premissesgroup=premissegroup88.uid, statement=statement93.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse90 = Premisse(premissesgroup=premissegroup89.uid, statement=statement94.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse91 = Premisse(premissesgroup=premissegroup90.uid, statement=statement95.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse92 = Premisse(premissesgroup=premissegroup91.uid, statement=statement96.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse93 = Premisse(premissesgroup=premissegroup92.uid, statement=statement97.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse94 = Premisse(premissesgroup=premissegroup93.uid, statement=statement98.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse95 = Premisse(premissesgroup=premissegroup94.uid, statement=statement99.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse96 = Premisse(premissesgroup=premissegroup95.uid, statement=statement100.uid, isnegated=False, author=user2.uid, issue=issue1.uid)
	premisse97 = Premisse(premissesgroup=premissegroup96.uid, statement=statement101.uid, isnegated=False, author=user2.uid, issue=issue1.uid)

	premisse98 = Premisse(premissesgroup=premissegroup97.uid, statement=statement102.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)
	premisse99 = Premisse(premissesgroup=premissegroup98.uid, statement=statement103.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)
	premisse100 = Premisse(premissesgroup=premissegroup99.uid, statement=statement104.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)
	premisse101 = Premisse(premissesgroup=premissegroup100.uid, statement=statement105.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)
	premisse102 = Premisse(premissesgroup=premissegroup101.uid, statement=statement106.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)
	premisse103 = Premisse(premissesgroup=premissegroup102.uid, statement=statement107.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)
	premisse104 = Premisse(premissesgroup=premissegroup103.uid, statement=statement108.uid,  isnegated=False, author=user2.uid, issue=issue2.uid)

	DBDiscussionSession.add_all([premisse1, premisse2, premisse3, premisse4, premisse5, premisse6, premisse7, premisse8, premisse9,
	                             premisse10, premisse11, premisse12, premisse13, premisse14, premisse15, premisse16, premisse17, premisse18,
	                             premisse19, premisse20, premisse21, premisse22, premisse23, premisse24, premisse25, premisse26, premisse27,
	                             premisse28, premisse29, premisse30, premisse31, premisse32, premisse33, premisse34, premisse35, premisse36,
	                             premisse37, premisse38, premisse39, premisse40, premisse41, premisse42, premisse43, premisse44, premisse45,
	                             premisse46, premisse47, premisse48, premisse49, premisse50, premisse51, premisse52, premisse53, premisse54,
	                             premisse55, premisse56, premisse57, premisse58, premisse59, premisse60, premisse61, premisse62, premisse63,
	                             premisse64, premisse65, premisse66, premisse67, premisse68, premisse69, premisse70, premisse71, premisse72,
	                             premisse73, premisse74, premisse75, premisse76, premisse77, premisse78, premisse79, premisse80, premisse81,
	                             premisse82, premisse83, premisse84, premisse85, premisse86, premisse87, premisse88, premisse89, premisse90,
	                             premisse91, premisse92, premisse93, premisse94, premisse95, premisse96, premisse97, premisse98, premisse99,
	                             premisse100, premisse101, premisse102, premisse103, premisse104])
	DBDiscussionSession.flush()

	#Adding all arguments and set the adjacency list
	argument1 = Argument(premissegroup=premissegroup1.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement1.uid, issue=issue1.uid)
	argument2 = Argument(premissegroup=premissegroup2.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement1.uid, issue=issue1.uid)
	argument3 = Argument(premissegroup=premissegroup3.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement2.uid, issue=issue1.uid)
	argument4 = Argument(premissegroup=premissegroup4.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement2.uid, issue=issue1.uid)
	argument5 = Argument(premissegroup=premissegroup5.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument6 = Argument(premissegroup=premissegroup6.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument7 = Argument(premissegroup=premissegroup7.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement3.uid, issue=issue1.uid)
	argument8 = Argument(premissegroup=premissegroup8.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument9 = Argument(premissegroup=premissegroup9.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement10.uid, issue=issue1.uid)
	argument10 = Argument(premissegroup=premissegroup10.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement1.uid, issue=issue1.uid)
	argument11 = Argument(premissegroup=premissegroup11.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement1.uid, issue=issue1.uid)
	argument12 = Argument(premissegroup=premissegroup12.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument13 = Argument(premissegroup=premissegroup13.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument14 = Argument(premissegroup=premissegroup14.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement4.uid, issue=issue1.uid)
	argument15 = Argument(premissegroup=premissegroup15.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement4.uid, issue=issue1.uid)
	argument16 = Argument(premissegroup=premissegroup16.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument17 = Argument(premissegroup=premissegroup17.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument18 = Argument(premissegroup=premissegroup18.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement5.uid, issue=issue1.uid)
	argument19 = Argument(premissegroup=premissegroup19.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement5.uid, issue=issue1.uid)
	argument20 = Argument(premissegroup=premissegroup20.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument21 = Argument(premissegroup=premissegroup21.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument22 = Argument(premissegroup=premissegroup22.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement13.uid, issue=issue1.uid)
	argument23 = Argument(premissegroup=premissegroup23.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement13.uid, issue=issue1.uid)
	argument24 = Argument(premissegroup=premissegroup24.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument25 = Argument(premissegroup=premissegroup25.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument26 = Argument(premissegroup=premissegroup26.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument27 = Argument(premissegroup=premissegroup27.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement14.uid, issue=issue1.uid)
	argument28 = Argument(premissegroup=premissegroup27.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement15.uid, issue=issue1.uid)
	# IMPORTANT: If the conclusion is an argument, check the counter!
	argument29 = Argument(premissegroup=premissegroup28.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement14.uid, issue=issue1.uid)
	argument30 = Argument(premissegroup=premissegroup28.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement15.uid, issue=issue1.uid)
	# IMPORTANT: If the conclusion is an argument, check the counter!
	argument31 = Argument(premissegroup=premissegroup29.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument32 = Argument(premissegroup=premissegroup30.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument33 = Argument(premissegroup=premissegroup31.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument34 = Argument(premissegroup=premissegroup32.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument35 = Argument(premissegroup=premissegroup33.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument36 = Argument(premissegroup=premissegroup34.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument37 = Argument(premissegroup=premissegroup35.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument38 = Argument(premissegroup=premissegroup36.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument39 = Argument(premissegroup=premissegroup37.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument40 = Argument(premissegroup=premissegroup38.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument41 = Argument(premissegroup=premissegroup39.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument42 = Argument(premissegroup=premissegroup40.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument43 = Argument(premissegroup=premissegroup41.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument44 = Argument(premissegroup=premissegroup42.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument45 = Argument(premissegroup=premissegroup43.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument46 = Argument(premissegroup=premissegroup44.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument47 = Argument(premissegroup=premissegroup45.uid, issupportive=False, author=user2.uid, weight=0, issue=issue1.uid)
	argument48 = Argument(premissegroup=premissegroup46.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument49 = Argument(premissegroup=premissegroup47.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument50 = Argument(premissegroup=premissegroup48.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument51 = Argument(premissegroup=premissegroup49.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument52 = Argument(premissegroup=premissegroup50.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument53 = Argument(premissegroup=premissegroup51.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument54 = Argument(premissegroup=premissegroup52.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument55 = Argument(premissegroup=premissegroup53.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument56 = Argument(premissegroup=premissegroup54.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument57 = Argument(premissegroup=premissegroup55.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument58 = Argument(premissegroup=premissegroup56.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument59 = Argument(premissegroup=premissegroup57.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument60 = Argument(premissegroup=premissegroup58.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument61 = Argument(premissegroup=premissegroup59.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument62 = Argument(premissegroup=premissegroup60.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument63 = Argument(premissegroup=premissegroup61.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument64 = Argument(premissegroup=premissegroup62.uid, issupportive=True, author=user2.uid, weight=0, issue=issue1.uid)
	argument65 = Argument(premissegroup=premissegroup63.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement16.uid, issue=issue1.uid)
	argument66 = Argument(premissegroup=premissegroup64.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement17.uid, issue=issue1.uid)
	argument67 = Argument(premissegroup=premissegroup65.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement18.uid, issue=issue1.uid)
	argument68 = Argument(premissegroup=premissegroup66.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement19.uid, issue=issue1.uid)
	argument69 = Argument(premissegroup=premissegroup67.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement20.uid, issue=issue1.uid)
	argument70 = Argument(premissegroup=premissegroup68.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement21.uid, issue=issue1.uid)
	argument71 = Argument(premissegroup=premissegroup69.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement22.uid, issue=issue1.uid)
	argument72 = Argument(premissegroup=premissegroup70.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement23.uid, issue=issue1.uid)
	argument73 = Argument(premissegroup=premissegroup71.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement24.uid, issue=issue1.uid)
	argument74 = Argument(premissegroup=premissegroup72.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement25.uid, issue=issue1.uid)
	argument75 = Argument(premissegroup=premissegroup73.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement26.uid, issue=issue1.uid)
	argument76 = Argument(premissegroup=premissegroup74.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement27.uid, issue=issue1.uid)
	argument77 = Argument(premissegroup=premissegroup75.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement29.uid, issue=issue1.uid)
	argument78 = Argument(premissegroup=premissegroup76.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement30.uid, issue=issue1.uid)
	argument79 = Argument(premissegroup=premissegroup77.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement31.uid, issue=issue1.uid)
	argument80 = Argument(premissegroup=premissegroup78.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement32.uid, issue=issue1.uid)
	argument81 = Argument(premissegroup=premissegroup79.uid, issupportive=False, author=user2.uid, weight=0, conclusion=statement33.uid, issue=issue1.uid)
	argument82 = Argument(premissegroup=premissegroup80.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement16.uid, issue=issue1.uid)
	argument83 = Argument(premissegroup=premissegroup81.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement17.uid, issue=issue1.uid)
	argument84 = Argument(premissegroup=premissegroup82.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement18.uid, issue=issue1.uid)
	argument85 = Argument(premissegroup=premissegroup83.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement19.uid, issue=issue1.uid)
	argument86 = Argument(premissegroup=premissegroup84.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement20.uid, issue=issue1.uid)
	argument87 = Argument(premissegroup=premissegroup85.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement21.uid, issue=issue1.uid)
	argument88 = Argument(premissegroup=premissegroup86.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement22.uid, issue=issue1.uid)
	argument89 = Argument(premissegroup=premissegroup87.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement23.uid, issue=issue1.uid)
	argument90 = Argument(premissegroup=premissegroup88.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement24.uid, issue=issue1.uid)
	argument91 = Argument(premissegroup=premissegroup89.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement25.uid, issue=issue1.uid)
	argument92 = Argument(premissegroup=premissegroup90.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement26.uid, issue=issue1.uid)
	argument93 = Argument(premissegroup=premissegroup91.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement27.uid, issue=issue1.uid)
	argument94 = Argument(premissegroup=premissegroup92.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement29.uid, issue=issue1.uid)
	argument95 = Argument(premissegroup=premissegroup93.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement30.uid, issue=issue1.uid)
	argument96 = Argument(premissegroup=premissegroup94.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement31.uid, issue=issue1.uid)
	argument97 = Argument(premissegroup=premissegroup95.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement32.uid, issue=issue1.uid)
	argument98 = Argument(premissegroup=premissegroup96.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement33.uid, issue=issue1.uid)

# todo
	argument99 = Argument(premissegroup=premissegroup98.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement102.uid, issue=issue2.uid)
	argument100 = Argument(premissegroup=premissegroup99.uid, issupportive=True, author=user2.uid, weight=0, conclusion=statement102.uid, issue=issue2.uid)
	argument101 = Argument(premissegroup=premissegroup100.uid, issupportive=False, author=user2.uid, weight=0, issue=issue2.uid)
	argument102 = Argument(premissegroup=premissegroup103.uid, issupportive=False, author=user2.uid, weight=0, issue=issue2.uid)
	#premisse104 = Premisse(premissesgroup=premissegroup103.uid, statement=statement108.uid,  isnegated=False, author=user2.uid,  issue=issue2.uid)

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
	                             argument100, argument101, argument102])
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