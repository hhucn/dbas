/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

var mainpage = location.origin + '/'; //get_hostname(window.location.href);

/**
 * Returns a translated string
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
_t = function(id){
	var this_id;
	var value = 'unknown identifier';
	$('#' + languageDropdownId).children().each(function(){
		if ($(this).hasClass('active')){
			this_id = $(this).children().first().attr('id');

			if (this_id.indexOf('en') != -1 && dbas_en.hasOwnProperty(id)){			value = dbas_en[id];
			} else if (this_id.indexOf('de') != -1 && dbas_de.hasOwnProperty(id)){	value = dbas_de[id];
			} else {                                                    			value = 'unknown value';
			}
		}
	});
	return value;
};


/**
 * Returns a translated string in the discussion language
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
_t_discussion = function(id){
	var info = $('#issue_info');
	if (info.length == 0){
		return _t(id);
	}
	var lang = info.data('discussion-language');
	var value = 'unknown identifier';
	if (lang.indexOf('en') != -1 && dbas_en.hasOwnProperty(id)){		value = dbas_en[id];
	} else if (lang.indexOf('de') != -1 && dbas_de.hasOwnProperty(id)){	value = dbas_de[id];
	} else {                                                    		value = 'unknown value';
	}
	return value;
};

/**
 * Returns the tag of current language. This is either {en,de} or 'unknown value' *
 * @returns {string} language tag
 */
getLanguage = function(){
	var this_id, value = 'unknown value';
	$('#' + languageDropdownId).children().each(function(){
		if ($(this).hasClass('active')){
			this_id = $(this).children().first().attr('id');
			if (this_id.indexOf('en') != -1){			value = 'en';
			} else if (this_id.indexOf('de') != -1){	value = 'de';
			} else {									value = 'unknown value';
			}
		}
	});
	return value;
};

/**
 * Returns the tag of current discussion language. This is either {en,de} or 'unknown value' *
 * @returns {string} language tag
 */
getDiscussionLanguage = function(){
	var lang = $('#issue_info').data('discussion-language'),
		value = 'unknown identifier';
	if (lang.indexOf('en') != -1){  		value = 'en';
	} else if (lang.indexOf('de') != -1){	value = 'de';
	} else {                                value = 'unknown value';
	}
	return value;
};

/**
 * Messages & Errors
 * @type {string}
 */
var checkmark                                       = '&#x2713;'; // ✓
var ballot                                          = '&#x2717;'; // ✗

var and 						            		= 'and';
var answer                                          = 'answer';
var andAtTheSameTime                                = 'andAtTheSameTime';
var addedEverything 								= 'addedEverything';
var addTopic                                        = 'addTopic';
var addTopicTitleText                               = 'addTopicTitleText';
var addTopicShortText                               = 'addTopicShortText';
var addTopicLangText                                = 'addTopicLangText';
var acceptIt 										= 'acceptIt';
var allEditsDone                                    = 'allEditsDone';
var allStatementsPosted                             = 'allStatementsPosted';
var allGivenVotes                                   = 'allGivenVotes';
var author                                          = 'author';
var avatar                                          = 'avatar';
var acceptItTitle 									= 'acceptItTitle';
var caution									        = 'caution';
var correctionsSet 									= 'correctionsSet';
var because                                         = 'because';
var changelog                                       = 'changelog';
var checkFirstname									= 'checkFirstname';
var checkLastname									= 'checkLastname';
var checkNickname									= 'checkNickname';
var checkEmail										= 'checkEmail';
var checkPassword									= 'checkPassword';
var checkConfirmation 								= 'checkConfirmation';
var checkPasswordConfirm							= 'checkPasswordConfirm';
var changelogView                                   = 'changelogView';
var changelogHide                                   = 'changelogHide';
var countOfArguments                                = 'countOfArguments';
var countdownEnded                                  = 'countdownEnded';
var couldNotLock                                    = 'couldNotLock';
var dataRemoved 									= 'dataRemoved';
var didYouMean										= 'didYouMean';
var duplicateDialog									= 'duplicateDialog';
var doNotHesitateToContact 							= 'doNotHesitateToContact';
var date                                            = 'date';
var deleteTrack 									= 'deleteTrack';
var deleteHistory 									= 'deleteHistory';
var deleteStatisticsTitle                           = 'deleteStatisticsTitle';
var deleteStatisticsBody                            = 'deleteStatisticsBody';
var euCookiePopupTitle 								= 'euCookiePopupTitle';
var euCookiePopupText 								= 'euCookiePopupText';
var euCookiePopoupButton1 							= 'euCookiePopoupButton1';
var euCookiePopoupButton2 							= 'euCookiePopoupButton2';
var empty_news_input  								= 'empty_news_input';
var email 											= 'email';
var emailWasSent		 							= 'emailWasSent';
var emailWasNotSent		 							= 'emailWasNotSent';
var emailUnknown 	 								= 'emailUnknown';
var edit 											= 'edit';
var errorCode 										= 'error_code';
var editTitle										= 'editTitle';
var forText                                         = 'forText';
var forward                                         = 'forward';
var fillLine 										= 'fillLine';
var feelFreeToShareUrl 								= 'feelFreeToShareUrl';
var fetchLongUrl 									= 'fetchLongUrl';
var fetchShortUrl 									= 'fetchShortUrl';
var forgotPassword 									= 'forgotPassword';
var firstname 										= 'firstname';
var gender 											= 'gender';
var generateSecurePassword 							= 'generateSecurePassword';
var goodPointTakeMeBackButtonText 					= 'goodPointTakeMeBackButtonText';
var group_uid 										= 'group_uid';
var history 										= 'history';
var haveALookAt 									= 'haveALookAt';
var hidePasswordRequest 							= 'hidePasswordRequest';
var hideGenerator 									= 'hideGenerator';
var inputEmpty 									    = 'inputEmpty';
var internalError 									= 'internalError';
var interestingOnDBAS 								= 'interestingOnDBAS';
var initialPositionInterest                         = 'initialPositionInterest';
var itIsTrueThat                                    = 'itIsTrueThat';
var itIsFalseThat                                   = 'itIsFalseThat';
var isItTrueThat                                    = 'isItTrueThat';
var isItFalseThat                                   = 'isItFalseThat';
var keepSetting										= 'keepSetting';
var hideAllUsers 									= 'hideAllUsers';
var hideAllArguments								= 'hideAllArguments';
var languageCouldNotBeSwitched 						= 'languageCouldNotBeSwitched';
var last_action 									= 'last_action';
var last_login 										= 'last_login';
var legend                                          = 'legend';
var logfile											= 'logfile';
var login											= 'login';
var letsGo 											= 'letsGo';
var listOfDoneEdits                                 = 'listOfDoneEdits';
var listOfPostedStatements                          = 'listOfPostedStatements';
var listOfGivenVotes                                = 'listOfGivenVotes';
var medium 											= 'medium';
var messageInfoTitle                                = 'messageInfoTitle';
var messageInfoStatementCreatedBy                   = 'messageInfoStatementCreatedBy';
var messageInfoAt                                   = 'messageInfoAt';
var messageInfoMessage                              = 'messageInfoMessage';
var messageInfoCurrentlySupported                   = 'messageInfoCurrentlySupported';
var messageInfoParticipant                          = 'messageInfoParticipant';
var messageInfoParticipantPl                        = 'messageInfoParticipantPl';
var messageInfoSupporterSg                          = 'messageInfoSupporterSg';
var messageInfoSupporterPl                          = 'messageInfoSupporterPl';
var nickname 										= 'nickname';
var noCorrections 									= 'noCorrections';
var noCorrectionsSet 								= 'noCorrectionsSet';
var noDecisionDone									= 'noDecisionDone';
var notInsertedErrorBecauseEmpty 					= 'notInsertedErrorBecauseEmpty';
var notInsertedErrorBecauseDuplicate 				= 'notInsertedErrorBecauseDuplicate';
var notInsertedErrorBecauseUnknown 					= 'notInsertedErrorBecauseUnknown';
var notInsertedErrorBecauseInternal					= 'notInsertedErrorBecauseInternal';
var notInsertedErrorBecauseTooShort					= 'notInsertedErrorBecauseTooShort';
var noTrackedData 									= 'noTrackedData';
var noDecisionstaken                                = 'noDecisionstaken';
var noReferencesButYouCanAdd                        = 'noReferencesButYouCanAdd';
var noEntries                                       = 'noEntries';
var noEntriesFor                                    = 'noEntriesFor';
var note 											= 'note';
var neww 											= 'new';
var number 											= 'number';
var notificationWasSend                             = 'notificationWasSend';
var noEditsInOptimization                           = 'noEditsInOptimization';
var opinionBarometer                                = 'opinionBarometer';
var option                                          = 'option';
var ohsnap                                          = 'ohsnap';
var report 											= 'report';
var reportTitle										= 'reportTitle';
var passwordSubmit 									= 'passwordSubmit';
var proposalsWereForwarded                          = 'proposalsWereForwarded';
var participantsSawThisStatement                    = 'participantsSawThisStatement';
var participantSawThisStatement                     = 'participantSawThisStatement';
var participantsSawArgumentsToThis                  = 'participantsSawArgumentsToThis';
var participantSawArgumentsToThis                   = 'participantSawArgumentsToThis';
var pinNavigation 									= 'pinNavigation';
var pleaseEditAtLeast                               = 'pleaseEditAtLeast';
var queueCompleteSeen                               = 'queueCompleteSeen';
var revokedArgument                                 = 'revokedArgument';
var registered 										= 'registered';
var requestTrack 									= 'requestTrack';
var refreshTrack 									= 'refreshTrack';
var requestHistory 									= 'requestHistory';
var refreshHistory 									= 'refreshHistory';
var requestFailed 									= 'requestFailed';
var requestFailedBadToken							= 'requestFailedBadToken';
var requestFailedInternalError                      = 'requestFailedInternalError';
var restartOnError									= 'restartOnError';
var repuationChartSum                               = 'repuationChartSum';
var repuationChartDay                               = 'repuationChartDay';
var saveMyStatement                                 = 'saveMyStatement';
var saveMyStatements                                = 'saveMyStatements';
var showAllUsers 									= 'showAllUsers';
var showAllArguments 								= 'showAllArguments';
var showMeAnArgumentFor 							= 'showMeAnArgumentFor';
var strength 										= 'strength';
var strong 											= 'strong';
var shortenedBy 									= 'shortenedBy';
var statisticsDeleted                               = 'statisticsDeleted';
var statisticsNotDeleted                            = 'statisticsNotDeleted';
var statisticsNotFetched                            = 'statisticsNotFetched';
var statisticsNotThere                              = 'statisticsNotThere';
var switchDiscussion								= 'switchDiscussion';
var switchDiscussionText1 							= 'switchDiscussionText1';
var switchDiscussionText2 							= 'switchDiscussionText2';
var switchDiscussionText3 							= 'switchDiscussionText3';
var surname 										= 'surname';
var sureToDeleteReview                              = 'sureToDeleteReview';
var showAllAttacksTitle 							= 'showAllAttacksTitle';
var showAllUsersTitle 								= 'showAllUsersTitle';
var text 											= 'text';
var to 											    = 'to';
var textMinCountMessageBegin1                       = 'textMinCountMessageBegin1';
var textMinCountMessageBegin2                       = 'textMinCountMessageBegin2';
var textMinCountMessageDuringTyping                 = 'textMinCountMessageDuringTyping';
var textMaxCountMessage                             = 'textMaxCountMessage';
var textMaxCountMessageError                        = 'textMaxCountMessageError';
var timestamp                                       = 'timestamp';
var typeofVote                                      = 'typeofVote';
var users                                           = 'users';
var usersWithSameOpinion                            = 'usersWithSameOpinion';
var unpinNavigation 								= 'unpinNavigation';
var veryweak 										= 'veryweak';
var valid    										= 'valid';
var vote                                            = 'vote';
var votes                                           = 'votes';
var weak 											= 'weak';

// cookies
var WARNING_CHANGE_DISCUSSION_POPUP = 'WARNING_CHANGE_DISCUSSION_POPUP';
var BUBBLE_INFOS = 'SPEECH_BUBBLE_INFOS';

/**
 * URL's
 * @type {string}
 */
var urlContact 							= 'contact';
var urlLogin 							= 'login';
var urlNews 							= 'news';
var urlContent 							= 'discuss';
var urlSettings 						= 'settings';
var urlImprint 							= 'imprint';
var urlLogout 							= 'logout';
var urlReview                           = 'review';


var dbas_en = {
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
	'attack': 'Attack',
	'author': 'Author',
	'because': 'because',
	'countOfArguments': 'Count of arguments',
	'countdownEnded': 'Your time is up. Unfortunately you cannot edit anything on this page anymore.',
	'couldNotLock': 'Set could not be locked, please try again!',
	'confirmTranslation': 'If you change the language, your process on this page will be lost and you have to restart the discussion!',
	'caution': 'Caution',
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
	'deleteTrack': 'Delete track',
	'deleteHistory': 'Delete history',
	'dataRemoved': 'Data was successfully removed.',
	'date': 'Date',
	'didYouMean': 'Top10 statements, which you probably could mean:',
	'duplicateDialog': 'This textversion is deprecated, because it was already edited to this version.\nDo you want to set this version as the current one once again?',
	'doNotHesitateToContact': 'Do not hesitate to <b><span style="cursor: pointer;" id="contact_on_error">contact us (click here)</span></b>',
	'deleteStatisticsTitle': 'Delete Statistics',
	'deleteStatisticsBody': 'Are you sure? This will delete all stored information about clicks respectively votes you have done.',
	'euCookiePopupTitle': 'This website is using cookies and Piwik.',
	'euCookiePopupText': 'We use them to give you the best experience. If you continue using our website, we\'ll assume that you are happy to receive all cookies on this website and beeing tracked for academic purpose. All tracked data are saved anonymously with reduced masked IP-adresses.',
	'euCookiePopoupButton1': 'Continue',
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
	'forward' : 'forward',
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
	'initialPositionInterest': 'What is the initial position you are interested in?',
	'interestingOnDBAS': 'Interesting discussion on DBAS',
	'itIsTrueThat': 'it is true that',
	'itIsFalseThat': 'it is false that',
	'isItTrueThat': 'it is true that',
	'isItFalseThat': 'it is false that',
	'issue': 'Issue',
	'keepSetting': 'Keep this',
	'hideAllUsers': 'Hide all users',
	'hideAllArguments': 'Hide all arguments',
	'languageCouldNotBeSwitched': 'Unfortunately, the language could not be switched',
	'last_action': 'Last Action',
	'last_login': 'Last Login',
	'legend': 'Legend',
	'logfile': 'Logfile for',
	'login': 'Log In',
	'letsGo': 'Click here to start now!',
	'listOfPostedStatements': 'This is a list of all posted statements:',
	'listOfDoneEdits': 'This is a list of all edits:',
	'listOfGivenVotes': 'This is a list of all votes:',
	'medium': 'medium',
	'messageInfoTitle': 'Infos about message',
	'messageInfoStatementCreatedBy': 'This was created by',
	'messageInfoAt': 'at',
	'messageInfoMessage': 'Message',
	'messageInfoCurrentlySupported': 'Currently it is supported by',
	'messageInfoParticipant': 'participant',
	'messageInfoParticipantPl': 's',
	'messageInfoSupporterSg': 'Supporter is',
	'messageInfoSupporterPl': 'Supporters are',
	'nickname': 'Nickname',
	'new': 'NEW',
	'noCorrections': 'No corrections for the given statement.',
	'noCorrectionsSet': 'Correction could not be set, because your user was not fount in the database. Are you currently logged in?',
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
	'noReferencesButYouCanAdd': 'There are no references for this statement, but you can add a new one (Source from a newspaper etc.):',
	'number': 'No',
	'note': 'Note',
	'noEditsInOptimization': 'You have edited nothing!',
	'opinionBarometer': 'Opinion Barometer',
	'option': 'Options',
	'ohsnap': 'Oh snap!',
	'participantsSawThisStatement': 'participants saw this statement.',
	'participantSawThisStatement': 'participant saw this statement.',
	'participantsSawArgumentsToThis': 'participants saw an argument for this opinition.',
	'participantSawArgumentsToThis': 'participant saw an argument for this opinition.',
	'passwordSubmit': 'Change Password',
	'proposalsWereForwarded': 'Your proposals were forwarded!',
	'pinNavigation': 'Pin Navigation',
	'pleaseEditAtLeast': 'Please edit at least 5 chars to reduce noise!',
	'queueCompleteSeen': 'You have seen every open task, so we will start from the beginning again.',
	'position': 'Position',
	'revokedArgument': 'revoked argument',
	'registered': 'Registered',
	'restartOnError': 'Please try to reload this page or restart the discussion when the error stays',
	'report': 'Report',
	'reportTitle': 'Opens a new mail for reporting an issue!',
	'requestTrack': 'Request track',
	'refreshTrack': 'Refresh track',
	'requestHistory': 'Request history',
	'refreshHistory': 'Refresh history',
	'requestFailed': 'Request failed, please reload the page.',
	'requestFailedBadToken': 'Request failed due to bad token, please reload the page.',
	'requestFailedInternalError': 'Request failed due to bad token, please reload this page. If the reload fails again, please do not hesitate to <span style="cursor: pointer;" id="contact_on_error">contact us (click here)</span>',
	'repuationChartSum': 'Summarized Reputation',
	'repuationChartDay': 'Reputation per Day',
	'saveMyStatement': 'Save my Statement!',
	'saveMyStatements': 'Save my Statements!',
	'showAllUsers': 'Show all users',
	'showAllArguments': 'Show all arguments',
	'showAllArgumentsTitle': 'Show all arguments, done by users',
	'showAllUsersTitle': 'Show all users, which are registered',
	'supportPosition': 'support position',
	'strength': 'Strength',
	'strong': 'strong',
	'statement': 'Statement',
	'statisticsDeleted': 'Statistics were deleted.',
	'statisticsNotDeleted': 'Statistics could not be deleted.',
	'statisticsNotFetched': 'Statistics could not be fetched.',
	'statisticsNotThere': 'You have no statistics.',
	'support': 'Support',
	'surname' : 'Surname',
	'sureToDeleteReview': 'Are you sure, that you want to revoke this decision? This revoke cannot be undone!',
	'shortenedBy': 'which was shortened by',
	'switchDiscussion': 'Change of discussion\'s topic',
	'switchDiscussionText1': 'If you accept, you will change the topic of the discussion to',
	'switchDiscussionText2': 'and the discussion will be restarted.',
	'switchDiscussionText3': 'Please keep in mind, that the discussion language is without reference to the system language.',
	'showMeAnArgumentFor': 'Show me an argument for',
	'text': 'Text',
	'to': 'To',
	'timestamp': 'Timestamp',
	'typeofVote': 'Agree / Disagree',
	'textMinCountMessageBegin1': 'Enter at least',
	'textMinCountMessageBegin2': 'characters',
	'textMinCountMessageDuringTyping': 'more to go ...',
	'textMaxCountMessage': 'characters left',
	'textMaxCountMessageError': 'Please shorten!',
	'users': 'Users',
	'usersWithSameOpinion': 'Users with same opinion',
	'unpinNavigation': 'Unpin Navigation',
	'valid': 'Valid',
	'veryweak': 'very weak',
	'vote': 'vote',
	'votes': 'votes',
	'weak': 'weak'
};

var dbas_de = {
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
	'attack': 'Angriff',
	'author': 'Autor',
	'because':'weil',
	'confirmTranslation': 'Wenn Sie die Sprache ändern, geht Ihr aktueller Fortschritt verloren!',
	'caution': 'Achtung',
	'correctionsSet': 'Ihre Korrektur wurde gesetzt.',
	'countOfArguments': 'Anzahl der Argumente',
	'countdownEnded': 'Ihre Zeit ist abgelaufen, leider können Sie auf dieser Seite keine Änderungen mehr vornehmen.',
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
	'dataRemoved': 'Daten wurden erfolgreich gelöscht.',
	'date': 'Datum',
	'didYouMean': 'Top 10 der Aussagen, die Sie eventuell meinten:',
	'duplicateDialog': 'Diese Textversion ist veraltet, weil Sie schon editiert wurde.\nMöchten Sie diese Version dennoch als die aktuellste markieren?',
	'deleteTrack': 'Track löschen',
	'deleteHistory': 'History löschen',
	'doNotHesitateToContact': 'Bitte zögern Sie bei Fehlern nicht, <b><span style="cursor: pointer;" id="contact_on_error">uns zu kontaktieren (hier klicken)</span></b>',
	'deleteStatisticsTitle': 'Statistik löschen',
	'deleteStatisticsBody': 'Dies löscht die Statstik. Dadurch werden alle Klicks, die von Ihnen getätigt wurden, wieder entfernt.',
	'euCookiePopupTitle': 'Diese Seite nutzt Cookies und Piwik.',
	'euCookiePopupText': 'Wir benutzen Sie, um Ihnen die beste Erfahrung zu geben. Wenn Sie unsere Seite weiter nutzen, nehmen Sie alle Cookies unserer Seite an und sind glücklich damit. Zusätzlich tracken wir Ihre Aktionen und speichern diese anonym ab. Dabei wird Ihre IP-Adresse maskiert.',
	'euCookiePopoupButton1': 'Weiter',
	'euCookiePopoupButton2': 'Lerne&nbsp;mehr',
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
	'forward' : 'weiterleiten',
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
	'initialPositionInterest': 'An welcher Aussage sind Sie interessiert?',
	'interestingOnDBAS': 'Interessante Diskussion in D-BAS',
	'itIsTrueThat': 'es ist richtig, dass',
	'itIsFalseThat': 'es ist falsch, dass',
	'isItTrueThat': 'ist es richtig, dass',
	'isItFalseThat': 'ist es falsch, dass',
	'issue': 'Thema',
	'keepSetting': 'Entscheidung merken',
	'hideAllUsers': 'Verstecke alle Benutzer',
	'hideAllArguments': 'Verstecke alle Argumente',
	'hideAllAttacks': 'Verstecke alle Angriffe',
	'languageCouldNotBeSwitched': 'Leider konnte die Sprache nicht gewechselt werden',
	'last_action': 'Letzte Aktion',
	'last_login': 'Letze Anmeldung',
	'logfile': 'Logdatei für',
	'login': 'Login',
	'legend': 'Legende',
	'letsGo': 'Wenn Sie direkt starten möchten, klicken Sie bitte hier!',
	'listOfPostedStatements': 'Dies ist eine Liste von allen gemachten Aussagen:',
	'listOfDoneEdits': 'Dies ist eine Liste von allen Änderungen:',
	'listOfGivenVotes': 'Dies ist eine Liste von allen Stimmen:',
	'medium': 'mittel',
	'messageInfoTitle': 'Informationen über eine Aussage',
	'messageInfoStatementCreatedBy': 'Diese Aussage stammt von',
	'messageInfoAt': 'am',
	'messageInfoMessage': 'Aussage',
	'messageInfoCurrentlySupported': 'Sie wird aktuell von',
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
	'noEntriesFor': 'Keine Einträge vorhanden für',
	'noTrackedData': 'Keine Daten wurden gespeichert.',
	'noDecisionstaken': 'Es wurden noch keine Entscheidungen getroffen',
	'noReferencesButYouCanAdd': 'Aktuell wurden noch keine Referenzen eingetragen, aber Sie können eine hinzufügen (Quelle aus einer Zeitung o.Ä.):',
	'number': 'Nr',
	'note': 'Hinweis',
	'noEditsInOptimization': 'Sie haben keine Änderungen vorgenommen!',
	'opinionBarometer': 'Meinungsbarometer',
	'option': 'Optionen',
	'ohsnap': 'Mist!',
	'participantsSawThisStatement': 'Teilnehmer sahen diese Aussage.',
	'participantSawThisStatement': 'Teilnehmer sah diese Aussage.',
	'participantsSawArgumentsToThis': 'Teilnehmer sahen Argumente für diese Aussage.',
	'participantSawArgumentsToThis': 'Teilnehmer sah Argumente für diese Aussage.',
	'passwordSubmit': 'Passwort ändern',
	'proposalsWereForwarded': 'Ihre Vorschläge wurden eingereicht!',
	'pinNavigation': 'Navigation anheften',
	'pleaseEditAtLeast': 'Bitte ändern Sie mindestens 5 Zeichen um unnötige Änderungen zu vermeiden.',
	'queueCompleteSeen': 'Wir haben Ihnen schon leider alles gezeigt, also fangen wir nochmal von vorne an!',
	'position': 'Position',
	'report': 'Melden',
	'reportTitle': 'Öffnet eine E-Mail, damit etwas gemeldet werden kann.',
	'revokedArgument': 'wiederrufenes Argument',
	'registered': 'Registriert',
	'requestTrack': 'Track anfragen',
	'refreshTrack': 'Track neuladen',
	'requestHistory': 'History anfragen',
	'refreshHistory': 'History neuladen',
	'requestFailed': 'Anfrage fehlgeschlagen, bitte laden Sie die Seite erneut.',
	'requestFailedBadToken': 'Anfrage aufgrund eines falschen Tokens fehlgeschlagen. Bitte laden Sie die Seite neu.',
	'requestFailedInternalError': 'Anfrage aufgrund eines internen Fehlers fehlgeschlagen. Bitte laden Sie die Seite neu, sollte der Fehler bestehen bleiben, so <span style="cursor: pointer;" id="contact_on_error">kontaktieren sie uns bitte (hier klicken)</span>',
	'repuationChartSum': 'Reputation ingsesamt',
	'repuationChartDay': 'Reputation pro Tag',
	'restartOnError': 'Bitte laden Sie die Seite erneut oder starten Sie die Diskussion neu, sofern der Fehler bleibt',
	'saveMyStatement': 'Aussage speichern!',
	'saveMyStatements': 'Ausagen speichern!',
	'showAllUsers': 'Zeig\' alle Benutzer',
	'showAllArguments': 'Zeig\' alle Argumente',
	'showAllArgumentsTitle': 'Zeigt alle Argumente',
	'showAllUsersTitle': 'Zeige alle Nutzer',
	'statisticsDeleted': 'Statistikten wurden gelöscht.',
	'statisticsNotDeleted': 'Statistikten konnten nicht gelöscht werden.',
	'statisticsNotFetched': 'Statistikten konnten nicht angefordert werden.',
	'statisticsNotThere': 'Sie haben keine Statistiken.',
	'strength': 'Stärke',
	'strong': 'stark',
	'statement': 'Aussage',
	'shortenedBy': 'gekürzt mit',
	'switchDiscussion': 'Diskussionsthema ändern',
	'switchDiscussionText1': 'Wenn Sie akzeptieren, wird das Diskussionsthema gewechselt zu',
	'switchDiscussionText2': 'und die Diskussion neugestartet.',
	'switchDiscussionText3': 'Bitte beachten Sie dabei, dass die Diskussionssprache unabhängig von der Systemsprache ist.',
	'support': 'Unterstützung',
	'surname': 'Nachname',
	'sureToDeleteReview': 'Sind Sie sicher, dass sie diese Entscheidung rückgangig machen möchten? Dieser Schritt kann nicht rückgangig gemacht werden!',
	'showMeAnArgumentFor': 'Zeig\' mir ein Argument für',
	'text': 'Text',
	'to': 'An',
	'timestamp': 'Zeit',
	'users': 'Benutzer',
	'usersWithSameOpinion': 'Benutzer mit derselben Meinung',
	'unpinNavigation': 'Navigation lösen',
	'typeofVote': 'Zustimmung/Ablehnung',
	'thxForFlagText': 'Danke für Ihre Meldung, wir kümmern uns drum!',
	'textMinCountMessageBegin1': 'Geben Sie mindestens',
	'textMinCountMessageBegin2': 'Zeichen ein',
	'textMinCountMessageDuringTyping': 'Zeichen noch ...',
	'textMaxCountMessage': 'Zeichen verbleibend',
	'textMaxCountMessageError': 'Bitte kürzen!',
	'valid': 'Gültigkeit',
	'veryweak': 'sehr schwach',
	'vote': 'Stimme',
	'votes': 'Stimmen',
	'weak': 'schwach'
};
