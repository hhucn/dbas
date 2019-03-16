/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

var mainpage = location.origin + '/';

/**
 * Messages & Errors
 * @type {string}
 */

var checkmark = '&#x2713;'; // ✓
var ballot = '&#x2717;'; // ✗
var and = 'and';
var answer = 'answer';
var andAtTheSameTime = 'andAtTheSameTime';
var addedEverything = 'addedEverything';
var addTopic = 'addTopic';
var addTopicTitleText = 'addTopicTitleText';
var addTopicShortText = 'addTopicShortText';
var addTopicLangText = 'addTopicLangText';
var acceptIt = 'acceptIt';
var an_anonymous_user = 'an_anonymous_user';
var allEditsDone = 'allEditsDone';
var allStatementsPosted = 'allStatementsPosted';
var allGivenVotes = 'allGivenVotes';
var allGivenInterests = 'allGivenInterests';
var author = 'author';
var avatar = 'avatar';
var askAFriendText = 'askAFriendText';
var askAFriendTitle = 'askAFriendTitle';
var acceptItTitle = 'acceptItTitle';
var caution = 'caution';
var cancel = 'cancel';
var correctionsSet = 'correctionsSet';
var because = 'because';
var changelog = 'changelog';
var checkFirstname = 'checkFirstname';
var checkLastname = 'checkLastname';
var checkNickname = 'checkNickname';
var checkEmail = 'checkEmail';
var checkPassword = 'checkPassword';
var checkConfirmation = 'checkConfirmation';
var checkPasswordConfirm = 'checkPasswordConfirm';
var changelogView = 'changelogView';
var changelogHide = 'changelogHide';
var clickedOnThis = 'clickedOnThis';
var countOfArguments = 'countOfArguments';
var countdownEnded = 'countdownEnded';
var urlCopy = 'urlCopy';
var couldNotLock = 'couldNotLock';
var contentWillBeRevoked = 'contentWillBeRevoked';
var dataRemoved = 'dataRemoved';
var dataAdded = 'dataAdded';
var didYouMean = 'didYouMean';
var duplicateDialog = 'duplicateDialog';
var doNotHesitateToContact = 'doNotHesitateToContact';
var date = 'date';
var deleteTrack = 'deleteTrack';
var deleteAccount = 'deleteAccount';
var deleteHistory = 'deleteHistory';
var deleteEverything = 'deleteEverything';
var deleteMarked = 'deleteMarked';
var discussionsPropertySet = 'discussionsPropertySet';
var deleteStatisticsTitle = 'deleteStatisticsTitle';
var deleteStatisticsBody = 'deleteStatisticsBody';
var euCookiePopupTitle = 'euCookiePopupTitle';
var euCookiePopupText = 'euCookiePopupText';
var euCookiePopoupButton1 = 'euCookiePopoupButton1';
var euCookiePopoupButton2 = 'euCookiePopoupButton2';
var empty_news_input = 'empty_news_input';
var email = 'email';
var emailWasSent = 'emailWasSent';
var emailWasNotSent = 'emailWasNotSent';
var emailUnknown = 'emailUnknown';
var edit = 'edit';
var errorCode = 'error_code';
var editTitle = 'editTitle';
var forText = 'forText';
var forward = 'forward';
var fillLine = 'fillLine';
var feelFreeToShareUrl = 'feelFreeToShareUrl';
var fetchLongUrl = 'fetchLongUrl';
var fetchShortUrl = 'fetchShortUrl';
var forgotPassword = 'forgotPassword';
var firstname = 'firstname';
var gender = 'gender';
var generateSecurePassword = 'generateSecurePassword';
var goodPointTakeMeBackButtonText = 'goodPointTakeMeBackButtonText';
var group_uid = 'group_uid';
var haveALookAt = 'haveALookAt';
var hidePasswordRequest = 'hidePasswordRequest';
var hideGenerator = 'hideGenerator';
var inputEmpty = 'inputEmpty';
var internalError = 'internalError';
var interestingOnDBAS = 'interestingOnDBAS';
var initialPositionInterest = 'initialPositionInterest';
var itIsTrueThat = 'itIsTrueThat';
var itIsFalseThat = 'itIsFalseThat';
var interestingNews = 'interestingNews';
var isItTrueThat = 'isItTrueThat';
var isItFalseThat = 'isItFalseThat';
var keepSetting = 'keepSetting';
var hideAllUsers = 'hideAllUsers';
var hideAllArguments = 'hideAllArguments';
var languageCouldNotBeSwitched = 'languageCouldNotBeSwitched';
var languageSwitchModalTitle = 'languageSwitchModalTitle';
var languageSwitchModalBody = 'languageSwitchModalBody';
var last_action = 'last_action';
var last_login = 'last_login';
var legend = 'legend';
var logfile = 'logfile';
var login = 'login';
var letsGo = 'letsGo';
var listOfDoneEdits = 'listOfDoneEdits';
var listOfPostedStatements = 'listOfPostedStatements';
var listOfGivenVotes = 'listOfGivenVotes';
var mayTakeAWhile = 'mayTakeAWhile';
var medium = 'medium';
var messageInfoTitle = 'messageInfoTitle';
var messageInfoStatementCreatedBy = 'messageInfoStatementCreatedBy';
var messageInfoAt = 'messageInfoAt';
var messageInfoMessage = 'messageInfoMessage';
var messageInfoCurrentlySupported = 'messageInfoCurrentlySupported';
var messageInfoParticipant = 'messageInfoParticipant';
var messageInfoParticipantPl = 'messageInfoParticipantPl';
var messageInfoSupporterSg = 'messageInfoSupporterSg';
var messageInfoSupporterPl = 'messageInfoSupporterPl';
var nickname = 'nickname';
var noCorrections = 'noCorrections';
var noCorrectionsSet = 'noCorrectionsSet';
var noDecisionDone = 'noDecisionDone';
var notInsertedErrorBecauseEmpty = 'notInsertedErrorBecauseEmpty';
var notInsertedErrorBecauseDuplicate = 'notInsertedErrorBecauseDuplicate';
var notInsertedErrorBecauseUnknown = 'notInsertedErrorBecauseUnknown';
var notInsertedErrorBecauseInternal = 'notInsertedErrorBecauseInternal';
var notInsertedErrorBecauseTooShort = 'notInsertedErrorBecauseTooShort';
var noTrackedData = 'noTrackedData';
var noDecisionstaken = 'noDecisionstaken';
var noReferencesButYouCanAdd = 'noReferencesButYouCanAdd';
var noEntries = 'noEntries';
var noEntriesFor = 'noEntriesFor';
var note = 'note';
var no = 'no';
var no_data_selected = 'no_data_selected';
var neww = 'new';
var number = 'number';
var notificationWasSend = 'notificationWasSend';
var noEditsInOptimization = 'noEditsInOptimization';
var opinionBarometer = 'opinionBarometer';
var okay = 'okay';
var otherParticipantsDontHaveOpinionForThis = 'otherParticipantsDontHaveOpinionForThis';
var option = 'option';
var ohsnap = 'ohsnap';
var report = 'report';
var reportTitle = 'reportTitle';
var passwordSubmit = 'passwordSubmit';
var proposalsWereForwarded = 'proposalsWereForwarded';
var participantsSawThisStatement = 'participantsSawThisStatement';
var participantSawThisStatement = 'participantSawThisStatement';
var participantsSawArgumentsToThis = 'participantsSawArgumentsToThis';
var participantSawArgumentsToThis = 'participantSawArgumentsToThis';
var pinNavigation = 'pinNavigation';
var pleaseEditAtLeast = 'pleaseEditAtLeast';
var pleaseEnterYourTextHere = 'pleaseEnterYourTextHere';
var pleaseEnterYourTextForSearchHere = 'pleaseEnterYourTextForSearchHere';
var queueCompleteSeen = 'queueCompleteSeen';
var questionMergeStatementSg = 'questionMergeStatementSg';
var questionSplitStatementSg = 'questionSplitStatementSg';
var questionMergeStatementPl = 'questionMergeStatementPl';
var questionSplitStatementPl = 'questionSplitStatementPl';
var revokedArgument = 'revokedArgument';
var registered = 'registered';
var requestTrack = 'requestTrack';
var refreshTrack = 'refreshTrack';
var requestHistory = 'requestHistory';
var refreshHistory = 'refreshHistory';
var requestFailed = 'requestFailed';
var requestFailedBadToken = 'requestFailedBadToken';
var requestFailedInternalError = 'requestFailedInternalError';
var restartOnError = 'restartOnError';
var repuationChartSum = 'repuationChartSum';
var repuationChartDay = 'repuationChartDay';
var readEverything = 'readEverything';
var readMarked = 'readMarked';
var searchStatementPopupTitleText = 'searchStatementPopupTitleText';
var searchStatementPopupBodyText = 'searchStatementPopupBodyText';
var sawThis = 'saw this';
var saveMyStatement = 'saveMyStatement';
var saveMyStatements = 'saveMyStatements';
var showAllUsers = 'showAllUsers';
var showAllArguments = 'showAllArguments';
var showMeAnArgumentFor = 'showMeAnArgumentFor';
var strength = 'strength';
var stepCannotBeUndone = 'stepCannotBeUndone';
var strong = 'strong';
var shortenedBy = 'shortenedBy';
var statement = 'statement';
var statisticsDeleted = 'statisticsDeleted';
var statisticsNotDeleted = 'statisticsNotDeleted';
var statisticsNotFetched = 'statisticsNotFetched';
var statisticsNotThere = 'statisticsNotThere';
var switchDiscussion = 'switchDiscussion';
var switchDiscussionText = 'switchDiscussionText';
var surname = 'surname';
var sureToDeleteReview = 'sureToDeleteReview';
var showAllAttacksTitle = 'showAllAttacksTitle';
var showAllUsersTitle = 'showAllUsersTitle';
var text = 'text';
var to = 'to';
var textMinCountMessageBegin1 = 'textMinCountMessageBegin1';
var textMinCountMessageBegin2 = 'textMinCountMessageBegin2';
var textMinCountMessageDuringTyping = 'textMinCountMessageDuringTyping';
var textMaxCountMessage = 'textMaxCountMessage';
var textMaxCountMessageError = 'textMaxCountMessageError';
var timestamp = 'timestamp';
var typeofVote = 'typeofVote';
var users = 'users';
var userPasswordNotMatch = 'userPasswordNotMatch';
var usersWithSameOpinion = 'usersWithSameOpinion';
var unpinNavigation = 'unpinNavigation';
var veryweak = 'veryweak';
var valid = 'valid';
var vote = 'vote';
var yes = 'yes';
var youAreAbleToReviewNow = 'youAreAbleToReviewNow';
var yourAreNotTheAuthorOfThisAnymore = 'yourAreNotTheAuthorOfThisAnymore';
var weak = 'weak';
var wrongCaptcha = 'wrongCaptcha';
var next = 'next';
var prev = 'prev';
var tourEnd = 'tourEnd';
var welcomeDialogBody = 'welcomeDialogBody';
var tourWelcomeTitle = 'tourWelcomeTitle';
var tourWelcomeContent = 'tourWelcomeContent';
var tourStartButtonTitle = 'tourStartButtonTitle';
var tourStartButtonContent = 'tourStartButtonContent';
var tourStartHeaderTitle = 'tourStartHeaderTitle';
var tourStartHeaderContent = 'tourStartHeaderContent';
var tourLoginTitle = 'tourLoginTitle';
var tourLoginContent = 'tourLoginContent';
var tourOverviewTitle = 'tourOverviewTitle';
var tourOverviewContent = 'tourOverviewContent';
var tourInfosTitle = 'tourInfosTitle';
var tourInfosContent = 'tourInfosContent';
var tourIssueTitle = 'tourIssueTitle';
var tourIssueContent = 'tourIssueContent';
var tourStartDiscussionTitle = 'tourStartDiscussionTitle';
var tourStartDiscussionContent = 'tourStartDiscussionContent';
var tourMarkOpinionTitle = 'tourMarkOpinionTitle';
var tourMarkOpinionContent = 'tourMarkOpinionContent';
var tourMarkOpinionText = 'tourMarkOpinionText';
var tourSidebarTitle = 'tourSidebarTitle';
var tourSidebarContent = 'tourSidebarContent';
var tourSelectAnswertTitle = 'tourSelectAnswertTitle';
var tourSelectAnswertContent = 'tourSelectAnswertContent';
var tourEnterStatementTitle = 'tourEnterStatementTitle';
var tourEnterStatementContent = 'tourEnterStatementContent';
var tourStatementActionTitle = 'tourStatementActionTitle';
var tourStatementActionContent = 'tourStatementActionContent';
var tourHaveFunTitle = 'tourHaveFunTitle';
var tourHaveFunContent = 'tourHaveFunContent';

// cookies
var WARNING_CHANGE_DISCUSSION_POPUP = 'WARNING_CHANGE_DISCUSSION_POPUP';
var BUBBLE_INFOS = 'SPEECH_BUBBLE_INFOS';
var GUIDED_TOUR = 'PASSED_GUIDED_TOUR';
var ADMIN_WARNING = 'hide-admin-caution-warning';
var LANG_SWITCH_WARNING = 'LANG_SWITCH_WARNING';
var EU_COOKIE_LAW_CONSENT = 'EU_COOKIE_LAW_CONSENT';

/**
 * URL's
 * @type {string}
 */
var urlContact = 'contact';
var urlLogin = 'login';
var urlContent = 'discuss';
var urlDiscussions = 'mydiscussions';
var urlSettings = 'settings';
var urlImprint = 'imprint';
var urlLogout = 'logout';
var urlReview = 'review';

var dbas_en = {
    'an_anonymous_user': 'an anonymous user',
    'avatar': 'Avatar',
    'and': 'and',
    'answer': 'antworten',
    'andAtTheSameTime': 'and at the same time',
    'addedEverything': 'Everything was added.',
    'addTopic': 'Add a Topic',
    'addTopicTitleText': 'Please enter your topic here:',
    'addTopicShortText': 'Please enter a shorttext for your topic here:',
    'addTopicLangText': 'Please select the language of the new discussion here:',
    'acceptIt': 'Accept it...',
    'acceptItTitle': 'Accept it...',
    'allEditsDone': 'All edits you\'ve done',
    'allStatementsPosted': 'All statements you\'ve posted',
    'allGivenVotes': 'All Votes',
    'allGivenInterests': 'All Interests',
    'attack': 'Attack',
    'author': 'Author',
    'askAFriendTitle': 'Share your opinion',
    'askAFriendText': 'Hey my friend,\nI think that you could improve the discussion here: ',
    'because': 'because',
    'countOfArguments': 'Count of arguments',
    'urlCopy': 'URL was copied into your clipboard',
    'countdownEnded': 'Your time is up. Unfortunately you cannot edit anything on this page anymore.',
    'contentWillBeRevoked': 'You will be disassociated from the content.',
    'couldNotLock': 'Set could not be locked, please try again!',
    'confirmTranslation': 'If you change the language, your process on this page will be lost and you have to restart ' +
        'the discussion!',
    'caution': 'Caution',
    'cancel': 'cancel',
    'correctionsSet': 'Your correction was set.',
    'changelog': 'changelog',
    'checkFirstname': 'Better check your first name, because the input is empty!',
    'checkLastname': 'Better check your last name, because the input is empty!',
    'checkNickname': 'Better check your nickname, because the input is empty!',
    'checkEmail': 'Better check your email, because the input is empty!',
    'checkPassword': 'Better check your password, because the input is empty!',
    'checkConfirmation': 'Better check the confirmation of your password, because the input is empty!',
    'checkPasswordConfirm': 'Better check your passwords, because they are not equal!',
    'changelogView': 'view changelog',
    'changelogHide': 'hide changelog',
    'clickedOnThis': 'clicked on this',
    'deleteTrack': 'Delete track',
    'deleteAccount': 'Delete Account',
    'deleteHistory': 'Delete history',
    'deleteEverything': 'Delete everything',
    'deleteMarked': 'Delete marked elements',
    'discussionsPropertySet': 'The discussions property was set.',
    'dataRemoved': 'Data was successfully removed.',
    'dataAdded': 'Data was successfully added.',
    'date': 'Date',
    'didYouMean': 'Top10 statements, which you probably could mean:',
    'duplicateDialog': 'This textversion is deprecated, because it was already edited to this version.\nDo you want to ' +
        'set this version as the current one once again?',
    'doNotHesitateToContact': 'Do not hesitate to <b><span style="cursor: pointer;" id="contact_on_error">contact us ' +
        '(click here)</span></b>',
    'deleteStatisticsTitle': 'Delete Statistics',
    'deleteStatisticsBody': 'Are you sure? This will delete all stored information about clicks respectively votes you ' +
        'have done.',
    'euCookiePopupTitle': 'This website uses cookies.',
    'euCookiePopupText': 'We use them to give you the best experience. If you continue using our website, we\'ll ' +
        'assume that you are happy to receive all cookies.',
    'euCookiePopoupButton1': 'Got it!',
    'euCookiePopoupButton2': 'Learn&nbsp;more',
    'empty_news_input': 'News title or text is empty or too short!',
    'email': 'E-Mail',
    'emailWasSent': 'An E-Mail was sent to the given address.',
    'emailWasNotSent': 'Your message could not be send due to a system error!',
    'emailUnknown': 'The given e-mail address is unkown.',
    'error_code': 'Error code',
    'edit': 'Edit',
    'editTitle': 'Editing the statements.',
    'feelFreeToShareUrl': 'Please feel free to share this url',
    'fetchLongUrl': 'Fetch long url!',
    'fetchShortUrl': 'Fetch short url!',
    'forgotPassword': 'Forgot Password',
    'forward': 'forward',
    'firstname': 'Firstname',
    'fillLine': 'Please, fill this this line with your report',
    'gender': 'Gender',
    'generateSecurePassword': 'Generate secure password',
    'goodPointTakeMeBackButtonText': 'I agree, that is a good argument! Take me one step back.',
    'group_uid': 'Group',
    'haveALookAt': 'Hey, please have a look at ',
    'hidePasswordRequest': 'Hide Password Request',
    'hideGenerator': 'Hide Generator',
    'internalError': '<strong>Internal Error:</strong> Maybe the server is offline.',
    'inputEmpty': 'Input is empty!',
    'initialPositionInterest': 'I want to talk about the position',
    'interestingOnDBAS': 'Interesting discussion on DBAS',
    'itIsTrueThat': 'it is true that',
    'itIsFalseThat': 'it is false that',
    'interestingNews': 'Interesting news from',
    'isItTrueThat': 'it is true that',
    'isItFalseThat': 'it is false that',
    'issue': 'Issue',
    'keepSetting': 'Keep this',
    'hideAllUsers': 'Hide all users',
    'hideAllArguments': 'Hide all arguments',
    'languageCouldNotBeSwitched': 'Unfortunately, the language could not be switched',
    'languageSwitchModalTitle': 'Change of Language',
    'languageSwitchModalBody': 'Changing current language does not affect the discussion language, because this ' +
        'language is mapped to the content of the discussion.',
    'last_action': 'Last Action',
    'last_login': 'Last Login',
    'legend': 'Legend',
    'logfile': 'Logfile for',
    'login': 'Log In',
    'letsGo': 'Click here to start now!',
    'listOfPostedStatements': 'This is a list of all posted statements:',
    'listOfDoneEdits': 'This is a list of all edits:',
    'listOfGivenVotes': 'This is a list of all votes:',
    'mayTakeAWhile': 'This may take a while',
    'medium': 'medium',
    'messageInfoTitle': 'Infos about an argument',
    'messageInfoStatementCreatedBy': 'This was created by',
    'messageInfoAt': 'at',
    'messageInfoMessage': 'Message',
    'messageInfoCurrentlySupported': 'and is supported by',
    'messageInfoParticipant': 'participant',
    'messageInfoParticipantPl': 's',
    'messageInfoSupporterSg': 'Supporter is',
    'messageInfoSupporterPl': 'Supporters are',
    'nickname': 'Nickname',
    'new': 'NEW',
    'no': 'No',
    'noCorrections': 'No corrections for the given statement.',
    'noCorrectionsSet': 'Correction could not be set, because your user was not fount in the database. Are you ' +
        'currently logged in?',
    'noDecisionDone': 'No decision was done.',
    'notInsertedErrorBecauseEmpty': 'Your idea was not inserted, because your input text is empty.',
    'notInsertedErrorBecauseDuplicate': 'Your idea was not inserted, because your idea is a duplicate.',
    'notInsertedErrorBecauseUnknown': 'Your idea was not inserted due to an unkown error.',
    'notInsertedErrorBecauseInternal': 'Your idea was not inserted due to an internal error.',
    'notInsertedErrorBecauseTooShort': 'Your idea was not inserted due to the shortness.',
    'notificationWasSend': 'Notification was send!',
    'noEntriesFor': 'No entries for',
    'noTrackedData': 'No data was tracked.',
    'noDecisionstaken': 'No decision has yet been taken.',
    'noReferencesButYouCanAdd': 'There are no references for this statement, but you can add a new one (Source from ' +
        'a newspaper etc.):',
    'number': 'No',
    'note': 'Note',
    'noEditsInOptimization': 'You have edited nothing!',
    'no_data_selected': 'no data selected',
    'opinionBarometer': 'Mood Barometer',
    'option': 'Options',
    'ohsnap': 'Oh snap!',
    'okay': 'Okay',
    'otherParticipantsDontHaveOpinionForThis': 'Other participants do not have any opinion for this statement.',
    'participantsSawThisStatement': 'participants saw this statement.',
    'participantSawThisStatement': 'participant saw this statement.',
    'participantsSawArgumentsToThis': 'participants saw an argument for this opinition.',
    'participantSawArgumentsToThis': 'participant saw an argument for this opinition.',
    'passwordSubmit': 'Change Password',
    'proposalsWereForwarded': 'Your proposals were forwarded!',
    'pinNavigation': 'Pin Navigation',
    'pleaseEditAtLeast': 'Please edit at least X chars to reduce noise!',
    'pleaseEnterYourTextHere': 'Please enter your text here ...',
    'pleaseEnterYourTextForSearchHere': 'Please enter your text for searching here ...',
    'queueCompleteSeen': 'You have seen every open task, so we will start from the beginning again.',
    'questionMergeStatementSg': 'Do you really want to merge the given statement into the XXX statement you have entered?',
    'questionSplitStatementSg': 'Do you really want to split the given statement with the XXX statement you have entered?',
    'questionMergeStatementPl': 'Do you really want to merge the given statement into the XXX statements you have entered?',
    'questionSplitStatementPl': 'Do you really want to split the given statement with the XXX statements you have entered?',
    'position': 'Position',
    'revokedArgument': 'revoked argument',
    'readEverything': 'Set everything as read',
    'readMarked': 'Set marked elements as read',
    'registered': 'Registered',
    'restartOnError': 'Please try to reload this page or restart the discussion when the error stays',
    'report': 'Report',
    'reportTitle': 'Opens a new mail for reporting an issue!',
    'requestTrack': 'Request track',
    'refreshTrack': 'Refresh track',
    'requestHistory': 'Request history',
    'refreshHistory': 'Refresh history',
    'requestFailed': 'Request failed, please reload the page.',
    'requestFailedBadToken': 'Your session is invalid, please reload the page.',
    'requestFailedInternalError': 'Request failed due to internal error, please reload this page. If the reload fails ' +
        'again, please do not hesitate to <span style="cursor: pointer;" id="contact_on_error">contact us (click here)</span>',
    'repuationChartSum': 'Summarized Reputation',
    'repuationChartDay': 'Reputation per Day',
    'sawThis': 'saw this',
    'saveMyStatement': 'Save my Statement!',
    'saveMyStatements': 'Save my Statements!',
    'searchStatementPopupTitleText': 'Search a statement!',
    'searchStatementPopupBodyText': 'If you select an statement, you will jump to this step in the discussion.',
    'showAllUsers': 'Show all users',
    'showAllArguments': 'Show all arguments',
    'showAllArgumentsTitle': 'Show all arguments, done by users',
    'showAllUsersTitle': 'Show all users, which are registered',
    'supportPosition': 'support position',
    'strength': 'Strength',
    'stepCannotBeUndone': 'This step cannot be undone.',
    'strong': 'strong',
    'statement': 'Statement',
    'statisticsDeleted': 'Statistics were deleted.',
    'statisticsNotDeleted': 'Statistics could not be deleted.',
    'statisticsNotFetched': 'Statistics could not be fetched.',
    'statisticsNotThere': 'You have no statistics for this point.',
    'support': 'Support',
    'surname': 'Surname',
    'sureToDeleteReview': 'Are you sure, that you want to revoke this decision? This revoke cannot be undone!',
    'shortenedBy': 'which was shortened by',
    'switchDiscussion': 'Change of discussion\'s topic',
    'switchDiscussionText': 'Do you really want to leave the current discussion and go the discussions about <strong>XXX</strong>?',
    'showMeAnArgumentFor': 'Show me an argument for',
    'text': 'Text',
    'to': 'To',
    'timestamp': 'Timestamp',
    'typeofVote': 'Agree / Disagree',
    'textMinCountMessageBegin1': 'Enter at least',
    'textMinCountMessageBegin2': 'characters',
    'textMinCountMessageDuringTyping': 'more to go ...',
    'textMaxCountMessage': 'characters left',
    'textMaxCountMessageError': 'Put it in a nutshell!', //'Please shorten!',
    'users': 'Users',
    'userPasswordNotMatch': 'User / Password do not match',
    'usersWithSameOpinion': 'Users with the same decision',
    'unpinNavigation': 'Unpin Navigation',
    'unkownError': 'Unknown error',
    'youAreAbleToReviewNow': 'You are now able to visit the review section.',
    'yourAreNotTheAuthorOfThisAnymore': 'You are not the author of this post anymore.',
    'yes': 'Yes',
    'valid': 'Valid',
    'veryweak': 'very weak',
    'vote': 'vote',
    'votes': 'votes',
    'weak': 'weak',
    'wrongCaptcha': 'Please fill in the correct solution for the captcha.',
    'next': 'Next',
    'prev': 'Prev',
    'tourEnd': 'End Tour',
    'welcomeDialogBody': 'It seems that you are the first time here. Would you like to start a short, guided tour?',
    'tourWelcomeTitle': 'Welcome!',
    'tourWelcomeContent': 'Welcome to D-BAS. You will be shown a short introduction now.',
    'tourStartButtonTitle': 'Starting the discussion',
    'tourStartButtonContent': 'You can start the discussion here.',
    'tourStartHeaderTitle': 'Starting the discussion',
    'tourStartHeaderContent': '.. or here!',
    'tourLoginTitle': 'Login',
    'tourLoginContent': 'In every case you should register yourself for enter your own statements.',
    'tourOverviewTitle': 'Issue Overview',
    'tourOverviewContent': 'This table contains the available topics.',
    'tourInfosTitle': 'Information',
    'tourInfosContent': 'Each row displays more information about the topic, whereby the titel opens the discussion.',
    'tourIssueTitle': 'Topic',
    'tourIssueContent': 'Here you can see the topic about current discussion.',
    'tourStartDiscussionTitle': 'First steps',
    'tourStartDiscussionContent': 'On the left side there are messages of the system and on the right side there are your answers.',
    'tourMarkOpinionTitle': 'Mark opinon',
    'tourMarkOpinionContent': 'With this little star you can mark your own opinion.',
    'tourMarkOpinionText': 'We should shut down University Park.',
    'tourSidebarTitle': 'Sidebar',
    'tourSidebarContent': 'There are many more options hidden behind the menu icon.',
    'tourSelectAnswertTitle': 'First selection',
    'tourSelectAnswertContent': 'In the lower part you can choose your answers ...',
    'tourEnterStatementTitle': 'Your own response',
    'tourEnterStatementContent': '... or enter new statement, if you are logged in ...',
    'tourStatementActionTitle': 'Interaction',
    'tourStatementActionContent': '... or would you like to interact with the already given statements?',
    'tourHaveFunTitle': 'And now ...',
    'tourHaveFunContent': '... have fun!',
};

var dbas_de = {
    'an_anonymous_user': 'einem anonymen Nutzer',
    'avatar': 'Avatar',
    'and': 'und',
    'answer': 'antworten',
    'addTopic': 'Thema hinzufügen',
    'addTopicTitleText': 'Bitte geben Sie Ihr Thema an:',
    'addTopicShortText': 'Bitte geben Sie die Kurform Ihres Themas an:',
    'addTopicLangText': 'Bitte geben Sie die Sprache Ihres Themas an:',
    'andAtTheSameTime': 'und zur selben Zeit',
    'addedEverything': 'Alles wurde hinzugefügt.',
    'acceptItTitle': 'Einsenden...',
    'acceptIt': 'Eintragen...',
    'allEditsDone': 'Alle Änderungen von Ihnen:',
    'allStatementsPosted': 'Alle Aussagen von Ihnen:',
    'allGivenVotes': 'Alle Stimmen',
    'allGivenInterests': 'Alle Interessen',
    'attack': 'Angriff',
    'author': 'Autor',
    'askAFriendTitle': 'Teile deine Meinung',
    'askAFriendText': 'Hey,\nIch denke, dass du hier zu der Diskussion beitragen kannst: ',
    'because': 'weil',
    'confirmTranslation': 'Wenn Sie die Sprache ändern, geht Ihr aktueller Fortschritt verloren!',
    'caution': 'Achtung',
    'cancel': 'Abbrechen',
    'correctionsSet': 'Ihre Korrektur wurde gesetzt.',
    'countOfArguments': 'Anzahl der Argumente',
    'urlCopy': 'URL wurde in Ihre Zwischenablage kopiert',
    'countdownEnded': 'Ihre Zeit ist abgelaufen, leider können Sie auf dieser Seite keine Änderungen mehr vornehmen.',
    'contentWillBeRevoked': 'Sie werden vom Inhalt entfernt werden.',
    'couldNotLock': 'Datensatz konnte nicht für Sie gesperrt werden, bitte versuchen Sie es erneut!',
    'changelog': 'Änderungsprotokoll',
    'checkFirstname': 'Bitte überprüfen Sie Ihren Vornamen, da die Eingabe leer ist!',
    'checkLastname': 'Bitte überprüfen Sie Ihren Nachnamen, da die Eingabe leer ist!',
    'checkNickname': 'Bitte überprüfen Sie Ihren Spitznamen, da die Eingabe leer ist!',
    'checkEmail': 'Bitte überprüfen Sie Ihre E-Mail, da die Eingabe leer ist!',
    'checkPassword': 'Bitte überprüfen Sie Ihre Passwort, da die Eingabe leer ist!',
    'checkConfirmation': 'Bitte überprüfen Sie Ihre Passwort-Bestätigung, da die Eingabe leer ist!',
    'checkPasswordConfirm': 'Bitte überprüfen Sie Ihre Passwörter, da die Passwärter nicht gleich sind!',
    'changelogView': 'Änderungen zeigen',
    'changelogHide': 'Änderungen ausblenden',
    'clickedOnThis': 'haben\'s geklickt',
    'dataRemoved': 'Daten wurden erfolgreich gelöscht.',
    'dataAdded': 'Daten wurden erfolgreich hinzugefügt.',
    'date': 'Datum',
    'didYouMean': 'Top 10 der Aussagen, die Sie eventuell meinten:',
    'duplicateDialog': 'Diese Textversion ist veraltet, weil Sie schon editiert wurde.\nMöchten Sie diese Version ' +
        'dennoch als die aktuellste markieren?',
    'deleteTrack': 'Track löschen',
    'deleteAccount': 'Account löschen',
    'deleteHistory': 'History löschen',
    'deleteEverything': 'Alle löschen',
    'deleteMarked': 'Ausgewählte Elemente löschen',
    'discussionsPropertySet': 'Die Eigenschaft der Diskussion wurde geändert.',
    'doNotHesitateToContact': 'Bitte zögern Sie bei Fehlern nicht, <b><span style="cursor: pointer;" ' +
        'id="contact_on_error">uns zu kontaktieren (hier klicken)</span></b>',
    'deleteStatisticsTitle': 'Statistik löschen',
    'deleteStatisticsBody': 'Dies löscht die Statstik. Dadurch werden alle Klicks, die von Ihnen getätigt wurden, wieder entfernt.',
    'euCookiePopupTitle': 'Diese Seite nutzt Cookies.',
    'euCookiePopupText': 'Wir benutzen Cookies, um Ihnen die beste Erfahrung zu geben. Wenn Sie unsere Seite weiter nutzen,' +
        ' akzeptieren Sie alle Cookies unserer Seite an und sind glücklich damit.',
    'euCookiePopoupButton1': 'Alles klar!',
    'euCookiePopoupButton2': 'Mehr&nbsp;Infos',
    'empty_news_input': 'Nachrichten-Titel oder Text ist leer oder zu kurz!',
    'email': 'E-Mail',
    'emailWasSent': 'Eine E-Mail wurde zu der genannten Adresse gesendet.',
    'emailWasNotSent': 'Ihre E-Mail konnte nicht gesendet werden!',
    'emailUnknown': 'Die Adresse ist nicht gültig.',
    'edit': 'Bearbeiten',
    'error_code': 'Fehler-Code',
    'editTitle': 'Aussagen bearbeiten',
    'fillLine': 'Bitte, füllen Sie diese Zeilen mit Ihrer Meldung',
    'feelFreeToShareUrl': 'Bitte teilen Sie diese URL',
    'fetchLongUrl': 'Normale URL',
    'fetchShortUrl': 'Kurze URL',
    'forgotPassword': 'Passwort vergessen',
    'forward': 'weiterleiten',
    'firstname': 'Vorname',
    'gender': 'Geschlecht',
    'generateSecurePassword': 'Generate secure password',
    'goodPointTakeMeBackButtonText': 'Ich stimme zu, dass ist ein gutes Argument. Geh einen Schritt zurück.',
    'group_uid': 'Gruppe',
    'haveALookAt': 'Hey, schau dir mal das an: ',
    'hidePasswordRequest': 'Verstecke die Passwort-Anfrage',
    'hideGenerator': 'Verstecke Generator',
    'internalError': '<strong>Interner Fehler:</strong> Wahrscheinlich ist der Server nicht erreichbar. Bitte laden Sie die Seite erneut!.',
    'inputEmpty': 'Ihre Eingabe ist leer!',
    'initialPositionInterest': 'Ich möchte darüber reden, dass',
    'interestingOnDBAS': 'Interessante Diskussion in D-BAS',
    'itIsTrueThat': 'es ist richtig, dass',
    'itIsFalseThat': 'es ist falsch, dass',
    'interestingNews': 'Interessante Neuigkeiten vom',
    'isItTrueThat': 'ist es richtig, dass',
    'isItFalseThat': 'ist es falsch, dass',
    'issue': 'Thema',
    'keepSetting': 'Entscheidung merken',
    'hideAllUsers': 'Verstecke alle Benutzer',
    'hideAllArguments': 'Verstecke alle Argumente',
    'hideAllAttacks': 'Verstecke alle Angriffe',
    'languageCouldNotBeSwitched': 'Leider konnte die Sprache nicht gewechselt werden',
    'languageSwitchModalTitle': 'Wechseln der Sprache',
    'languageSwitchModalBody': 'Eine Umstellung der Sprache ändert nicht die Diskussionssprache. Diese ist an den Inhalt der Diskussion geknüpft.',
    'last_action': 'Letzte Aktion',
    'last_login': 'Letze Anmeldung',
    'logfile': 'Logdatei für',
    'login': 'Login',
    'legend': 'Legende',
    'letsGo': 'Wenn Sie direkt starten möchten, klicken Sie bitte hier!',
    'listOfPostedStatements': 'Dies ist eine Liste von allen gemachten Aussagen:',
    'listOfDoneEdits': 'Dies ist eine Liste von allen Änderungen:',
    'listOfGivenVotes': 'Dies ist eine Liste von allen Stimmen:',
    'mayTakeAWhile': 'Dies kann einen Momeent dauern.',
    'medium': 'mittel',
    'messageInfoTitle': 'Informationen über ein Argument',
    'messageInfoStatementCreatedBy': 'Dieses Argument stammt von',
    'messageInfoAt': 'am',
    'messageInfoMessage': 'Aussage',
    'messageInfoCurrentlySupported': 'und wird aktuell von',
    'messageInfoParticipant': 'Teilnehmer/in unterstützt',
    'messageInfoParticipantPl': '/n/nen',
    'messageInfoSupporterSg': 'Unterstützer/in ist',
    'messageInfoSupporterPl': 'Unterstützer/innen sind',
    'nickname': 'Spitzname',
    'new': 'neu',
    'noCorrections': 'Keinte Korreturen für die aktuelle Aussage.',
    'noDecisionDone': 'Es liegt keine Entscheidung vor.',
    'noCorrectionsSet': 'Korrektur wurde nicht gespeichert, da der Benutzer unbekannt ist. Sind Sie angemeldet?',
    'notInsertedErrorBecauseEmpty': 'Ihre Idee wurde nicht gespeichert, da das Feld leer ist.',
    'notInsertedErrorBecauseDuplicate': 'Ihre Idee wurde nicht gespeichert, da Ihre Idee ein Duplikat ist.',
    'notInsertedErrorBecauseUnknown': 'Ihre Idee wurde aufgrund eines unbekannten Fehlers nicht gespeichert.',
    'notInsertedErrorBecauseInternal': 'Ihre Idee wurde aufgrund eines internen Fehlers nicht gespeichert.',
    'notInsertedErrorBecauseTooShort': 'Ihre Idee wurde aufgrund der Kürze nicht gespeichert.',
    'notificationWasSend': 'Nachricht wurde gesendet',
    'noEntries': 'Keine Einträge vorhanden',
    'no': 'Nein',
    'noEntriesFor': 'Keine Einträge vorhanden für',
    'noTrackedData': 'Keine Daten wurden gespeichert.',
    'noDecisionstaken': 'Es wurden noch keine Entscheidungen getroffen',
    'noReferencesButYouCanAdd': 'Aktuell wurden noch keine Referenzen eingetragen, aber Sie können eine hinzufügen (Quelle aus einer Zeitung o.Ä.):',
    'number': 'Nr',
    'note': 'Hinweis',
    'no_data_selected': 'Nichts ausgewählt',
    'noEditsInOptimization': 'Sie haben keine Änderungen vorgenommen!',
    'opinionBarometer': 'Stimmungsbarometer',
    'option': 'Optionen',
    'ohsnap': 'Mist!',
    'okay': 'Okay',
    'otherParticipantsDontHaveOpinionForThis': 'Andere Teilnehmer haben bisher keine Meinung dazu.',
    'participantsSawThisStatement': 'Teilnehmer/innen sahen diese Aussage.',
    'participantSawThisStatement': 'Teilnehmer/in sah diese Aussage.',
    'participantsSawArgumentsToThis': 'Teilnehmer/innen sahen Argumente für diese Aussage.',
    'participantSawArgumentsToThis': 'Teilnehmer/in sah Argumente für diese Aussage.',
    'passwordSubmit': 'Passwort ändern',
    'proposalsWereForwarded': 'Ihr Vorschlag wurde eingereicht!',
    'pinNavigation': 'Navigation anheften',
    'pleaseEditAtLeast': 'Bitte ändern Sie mindestens X Zeichen um unnötige Änderungen zu vermeiden.',
    'pleaseEnterYourTextForSearchHere': 'Bitte geben Sie hier Ihren Suchtext ein ...',
    'pleaseEnterYourTextHere': 'Bitte geben Sie hier Ihren Text ein ...',
    'queueCompleteSeen': 'Wir haben Ihnen schon leider alles gezeigt, also fangen wir nochmal von vorne an!',
    'questionMergeStatementSg': 'Möchten Sie wirklich die gegebene Aussage mit der XXX eingegebene Aussage verbinden?',
    'questionSplitStatementSg': 'Möchten Sie wirklich die gegebene Aussage in die XXX eingegebene Aussage trennen?',
    'questionMergeStatementPl': 'Möchten Sie wirklich die gegebene Aussage mit den XXX eingegebenen Aussagen verbinden?',
    'questionSplitStatementPl': 'Möchten Sie wirklich die gegebene Aussage in die XXX eingegebenen Aussagen trennen?',
    'position': 'Position',
    'report': 'Melden',
    'reportTitle': 'Öffnet eine E-Mail, damit etwas gemeldet werden kann.',
    'revokedArgument': 'wiederrufenes Argument',
    'readEverything': 'Alle als gelesen markieren',
    'readMarked': 'Ausgewählte Elemente als gelesen markieren',
    'registered': 'Registriert',
    'requestTrack': 'Track anfragen',
    'refreshTrack': 'Track neuladen',
    'requestHistory': 'History anfragen',
    'refreshHistory': 'History neuladen',
    'requestFailed': 'Anfrage fehlgeschlagen, bitte laden Sie die Seite erneut.',
    'requestFailedBadToken': 'Ihre Sitzung ist abgelaufen. Bitte laden Sie die Seite neu.',
    'requestFailedInternalError': 'Anfrage aufgrund eines internen Fehlers fehlgeschlagen. Bitte laden Sie die Seite ' +
        'neu, sollte der Fehler bestehen bleiben, so <span style="cursor: pointer;" id="contact_on_error">' +
        'kontaktieren sie uns bitte (hier klicken)</span>',
    'repuationChartSum': 'Reputation ingsesamt',
    'repuationChartDay': 'Reputation pro Tag',
    'restartOnError': 'Bitte laden Sie die Seite erneut oder starten Sie die Diskussion neu, sofern der Fehler bleibt',
    'sawThis': 'sahen dies!',
    'saveMyStatement': 'Aussage speichern!',
    'saveMyStatements': 'Aussagen speichern!',
    'searchStatementPopupTitleText': 'Aussagensuche!',
    'searchStatementPopupBodyText': 'Bei der Auswahl einer Aussage, springen Sie zu diesem Abschnitt in der Diskussion.',
    'showAllUsers': 'Zeig\' alle Benutzer',
    'showAllArguments': 'Zeig\' alle Argumente',
    'showAllArgumentsTitle': 'Zeigt alle Argumente',
    'showAllUsersTitle': 'Zeige alle Nutzer',
    'statisticsDeleted': 'Statistiken wurden gelöscht.',
    'statisticsNotDeleted': 'Statistiken konnten nicht gelöscht werden.',
    'statisticsNotFetched': 'Statistiken konnten nicht angefordert werden.',
    'statisticsNotThere': 'Sie haben keine Statistiken für diesen Punkt.',
    'strength': 'Stärke',
    'stepCannotBeUndone': 'Dieser Schritt kann nicht rückgängig gemacht werden.',
    'strong': 'stark',
    'statement': 'Aussage',
    'shortenedBy': 'gekürzt mit',
    'switchDiscussion': 'Diskussionsthema ändern',
    'switchDiscussionText': 'Wollen Sie wirklich die aktuelle Diskussion verlassen und zur Diskussion über ' +
        '<strong>XXX</strong> wechseln?',
    'support': 'Unterstützung',
    'surname': 'Nachname',
    'sureToDeleteReview': 'Sind Sie sicher, dass Sie diese Entscheidung rückgangig machen möchten? Dieser Schritt kann ' +
        'nicht rückgangig gemacht werden!',
    'showMeAnArgumentFor': 'Zeig\' mir ein Argument für',
    'text': 'Text',
    'to': 'An',
    'timestamp': 'Zeit',
    'users': 'Benutzer',
    'userPasswordNotMatch': 'Benutzername und/oder Passwort stimmen nicht überein',
    'usersWithSameOpinion': 'Teilnehmer/innen mit derselben Interesse',
    'unpinNavigation': 'Navigation lösen',
    'unkownError': 'Unbekannter Fehler',
    'typeofVote': 'Zustimmung/Ablehnung',
    'thxForFlagText': 'Danke für Ihre Meldung, wir kümmern uns drum!',
    'textMinCountMessageBegin1': 'Geben Sie mindestens',
    'textMinCountMessageBegin2': 'Zeichen ein',
    'textMinCountMessageDuringTyping': 'Zeichen noch ...',
    'textMaxCountMessage': 'Zeichen verbleibend',
    'textMaxCountMessageError': 'Bringen Sie Ihre Aussagen bitte auf den Punkt.', //Versuchen Sie zu kürzen!',
    'valid': 'Gültigkeit',
    'veryweak': 'sehr schwach',
    'youAreAbleToReviewNow': 'Sie können nun andere Beiträge begutachten.',
    'yourAreNotTheAuthorOfThisAnymore': 'Sie werden nicht mehr als Autor des Beitrags angezeigt.',
    'vote': 'Stimme',
    'votes': 'Stimmen',
    'weak': 'schwach',
    'wrongCaptcha': 'Bitte füllen Sie das Captcha korrekt aus.',
    'next': 'Weiter',
    'prev': 'Zurück',
    'yes': 'Ja',
    'tourEnd': 'Beenden',
    'welcomeDialogBody': 'Es scheint, dass Sie zum ersten Mal hier sind. Möchten Sie eine kurze Einführung sehen?',
    'tourWelcomeTitle': 'Willkommen!',
    'tourWelcomeContent': 'Willkommen bei D-BAS! Sie werden nun eine kurze Einführung bekommen.',
    'tourStartButtonTitle': 'Diskussion starten',
    'tourStartButtonContent': 'Hier können Sie die Diskussion direkt starten.',
    'tourStartHeaderTitle': 'Diskussion starten',
    'tourStartHeaderContent': '... oder auch hier.',
    'tourLoginTitle': 'Anmeldung',
    'tourLoginContent': 'Sie sollten sich aber anmelden, um Beiträge verfassen zu können.',
    'tourOverviewTitle': 'Themenübersicht',
    'tourOverviewContent': 'Hier sehen Sie alle verfügbaren Diskussionsthemen.',
    'tourInfosTitle': 'Informationen',
    'tourInfosContent': 'Jede Reihe enthält weitere Informationen. Wenn Sie den Titel anklicken, rufen Sie die Diskussion auf.',
    'tourIssueTitle': 'Thema',
    'tourIssueContent': 'Hier sehen Sie das aktuelle Diskussionsthema.',
    'tourStartDiscussionTitle': 'Erste Schritte',
    'tourStartDiscussionContent': 'In diesem Abschnitt sehen Sie links Nachrichten des Systems und rechts später ' +
        'Ihre eigenen Nachrichten.',
    'tourMarkOpinionTitle': 'Meinung markieren',
    'tourMarkOpinionContent': 'Mit dem kleinen Stern neben dem Text können Sie Ihre eigene Meinung markieren.',
    'tourMarkOpinionText': 'Sie interessiert, dass der Park geschlossen werden soll.',
    'tourSidebarTitle': 'Seitenleiste',
    'tourSidebarContent': 'Hinter dem Menü-Icon sind noch weitere Optionen versteckt.',
    'tourSelectAnswertTitle': 'Erste Auswahl',
    'tourSelectAnswertContent': 'Im unteren Teil können Sie Antworten auswählen ...',
    'tourEnterStatementTitle': 'Eigene Antworten',
    'tourEnterStatementContent': '... oder eigene Antworten eingeben, sofern Sie angemeldet sind ...',
    'tourStatementActionTitle': 'Interaktionen',
    'tourStatementActionContent': '... oder doch lieber mit den vorhandenen Antworten agieren?',
    'tourHaveFunTitle': 'Und nun ...',
    'tourHaveFunContent': '... viel Spaß!',
};

var dataTables_german_lang = {
    "sEmptyTable": "Keine Daten in der Tabelle vorhanden",
    "sInfo": "_START_ bis _END_ von _TOTAL_ Einträgen",
    "sInfoEmpty": "0 bis 0 von 0 Einträgen",
    "sInfoFiltered": "(gefiltert von _MAX_ Einträgen)",
    "sInfoPostFix": "",
    "sInfoThousands": ".",
    "sLengthMenu": "_MENU_ Einträge anzeigen",
    "sLoadingRecords": "Wird geladen...",
    "sProcessing": "Bitte warten...",
    "sSearch": "Suchen",
    "sZeroRecords": "Keine Einträge vorhanden.",
    "oPaginate": {
        "sFirst": "Erste",
        "sPrevious": "Zurück",
        "sNext": "Nächste",
        "sLast": "Letzte"
    },
    "oAria": {
        "sSortAscending": ": aktivieren, um Spalte aufsteigend zu sortieren",
        "sSortDescending": ": aktivieren, um Spalte absteigend zu sortieren"
    }
};

var dataTables_english_lang = {
    "sEmptyTable": "No data available in table",
    "sInfo": "Showing _START_ to _END_ of _TOTAL_ entries",
    "sInfoEmpty": "Showing 0 to 0 of 0 entries",
    "sInfoFiltered": "(filtered from _MAX_ total entries)",
    "sInfoPostFix": "",
    "sInfoThousands": ",",
    "sLengthMenu": "Show _MENU_ entries",
    "sLoadingRecords": "Loading...",
    "sProcessing": "Processing...",
    "sSearch": "Search:",
    "sZeroRecords": "No matching records found",
    "oPaginate": {
        "sFirst": "First",
        "sLast": "Last",
        "sNext": "Next",
        "sPrevious": "Previous"
    },
    "oAria": {
        "sSortAscending": ": activate to sort column ascending",
        "sSortDescending": ": activate to sort column descending"
    }
};

var get_it = function (val, id) {
    'use strict';
    var value = 'unknown value';
    if (typeof val !== 'undefined' && val.indexOf('de') !== -1 && dbas_de.hasOwnProperty(id)) {
        value = dbas_de[id];
    } else if (dbas_en.hasOwnProperty(id)) {
        value = dbas_en[id];
    }
    return value;

};

/**
 * Returns a translated string
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
function _t(id) {
    'use strict';
    return get_it(getLanguage(), id);
}

/**
 * Returns a translated string in the discussion language
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
function _t_discussion(id) {
    'use strict';

    var info = $('#issue_info');
    if (typeof info === 'undefined') {
        return get_it('en', id);
    }
    var lang = info.data('discussion-language');
    return get_it(lang, id);
}

/**
 * Returns the tag of current language. This is either {en,de} or 'unknown value' *
 * @returns {string} language tag
 */
function getLanguage() {
    'use strict';
    return $('#hidden_language').val();
}

/**
 * Returns the tag of current discussion language. This is either {en,de} or 'unknown value' *
 * @returns {string} language tag
 */
function getDiscussionLanguage() {
    'use strict';

    var lang = $('#issue_info').data('discussion-language'), value;
    if (lang.indexOf('en') !== -1) {
        value = 'en';
    } else if (lang.indexOf('de') !== -1) {
        value = 'de';
    } else {
        value = 'unknown value';
    }
    return value;
}
