/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

const mainpage = location.origin + '/'; //get_hostname(window.location.href);

/**
 * Returns a translated string
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
_t = function(id){
    let this_id;
    let value = 'unknown identifier';
    $('#' + languageDropdownId).children().each(function(){
        if ($(this).hasClass('active')){
            this_id = $(this).children().first().attr('id');

            if (this_id.indexOf('en') != -1 && dbas_en.hasOwnProperty(id)){            value = dbas_en[id];
            } else if (this_id.indexOf('de') != -1 && dbas_de.hasOwnProperty(id)){    value = dbas_de[id];
            } else {                                                                value = 'unknown value';
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
    let info = $('#issue_info');
    if (info.length == 0){
        return _t(id);
    }
    let lang = info.data('discussion-language');
    let value = 'unknown identifier';
    if (lang.indexOf('en') != -1 && dbas_en.hasOwnProperty(id)){        value = dbas_en[id];
    } else if (lang.indexOf('de') != -1 && dbas_de.hasOwnProperty(id)){    value = dbas_de[id];
    } else {                                                            value = 'unknown value';
    }
    return value;
};

/**
 * Returns the tag of current language. This is either {en,de} or 'unknown value' *
 * @returns {string} language tag
 */
getLanguage = function(){
    let this_id, value = 'unknown value';
    $('#' + languageDropdownId).children().each(function(){
        if ($(this).hasClass('active')){
            this_id = $(this).children().first().attr('id');
            if (this_id.indexOf('en') != -1){           value = 'en';
            } else if (this_id.indexOf('de') != -1){    value = 'de';
            } else {                                    value = 'unknown value';
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
    let lang = $('#issue_info').data('discussion-language'),
        value = 'unknown identifier';
    if (lang.indexOf('en') != -1){          value = 'en';
    } else if (lang.indexOf('de') != -1){    value = 'de';
    } else {                                value = 'unknown value';
    }
    return value;
};

/**
 * Messages & Errors
 * @type {string}
 */
const checkmark                       = '&#x2713;'; // ✓
const ballot                          = '&#x2717;'; // ✗
const and                             = 'and';
const answer                          = 'answer';
const andAtTheSameTime                = 'andAtTheSameTime';
const addedEverything                 = 'addedEverything';
const addTopic                        = 'addTopic';
const addTopicTitleText               = 'addTopicTitleText';
const addTopicShortText               = 'addTopicShortText';
const addTopicLangText                = 'addTopicLangText';
const acceptIt                        = 'acceptIt';
const an_anonymous_user               = 'an_anonymous_user';
const allEditsDone                    = 'allEditsDone';
const allStatementsPosted             = 'allStatementsPosted';
const allGivenVotes                   = 'allGivenVotes';
const author                          = 'author';
const avatar                          = 'avatar';
const acceptItTitle                   = 'acceptItTitle';
const caution                         = 'caution';
const correctionsSet                  = 'correctionsSet';
const because                         = 'because';
const changelog                       = 'changelog';
const checkFirstname                  = 'checkFirstname';
const checkLastname                   = 'checkLastname';
const checkNickname                   = 'checkNickname';
const checkEmail                      = 'checkEmail';
const checkPassword                   = 'checkPassword';
const checkConfirmation               = 'checkConfirmation';
const checkPasswordConfirm            = 'checkPasswordConfirm';
const changelogView                   = 'changelogView';
const changelogHide                   = 'changelogHide';
const clickedOnThis                   = 'clickedOnThis';
const countOfArguments                = 'countOfArguments';
const countdownEnded                  = 'countdownEnded';
const couldNotLock                    = 'couldNotLock';
const contentWillBeRevoked            = 'contentWillBeRevoked';
const dataRemoved                     = 'dataRemoved';
const dataAdded                       = 'dataAdded';
const didYouMean                      = 'didYouMean';
const duplicateDialog                 = 'duplicateDialog';
const doNotHesitateToContact          = 'doNotHesitateToContact';
const date                            = 'date';
const deleteTrack                     = 'deleteTrack';
const deleteHistory                   = 'deleteHistory';
const deleteStatisticsTitle           = 'deleteStatisticsTitle';
const deleteStatisticsBody            = 'deleteStatisticsBody';
const euCookiePopupTitle              = 'euCookiePopupTitle';
const euCookiePopupText               = 'euCookiePopupText';
const euCookiePopoupButton1           = 'euCookiePopoupButton1';
const euCookiePopoupButton2           = 'euCookiePopoupButton2';
const empty_news_input                = 'empty_news_input';
const email                           = 'email';
const emailWasSent                    = 'emailWasSent';
const emailWasNotSent                 = 'emailWasNotSent';
const emailUnknown                    = 'emailUnknown';
const edit                            = 'edit';
const errorCode                       = 'error_code';
const editTitle                       = 'editTitle';
const forText                         = 'forText';
const forward                         = 'forward';
const fillLine                        = 'fillLine';
const feelFreeToShareUrl              = 'feelFreeToShareUrl';
const fetchLongUrl                    = 'fetchLongUrl';
const fetchShortUrl                   = 'fetchShortUrl';
const forgotPassword                  = 'forgotPassword';
const firstname                       = 'firstname';
const gender                          = 'gender';
const generateSecurePassword          = 'generateSecurePassword';
const goodPointTakeMeBackButtonText   = 'goodPointTakeMeBackButtonText';
const group_uid                       = 'group_uid';
const history                         = 'history';
const haveALookAt                     = 'haveALookAt';
const hidePasswordRequest             = 'hidePasswordRequest';
const hideGenerator                   = 'hideGenerator';
const inputEmpty                      = 'inputEmpty';
const internalError                   = 'internalError';
const interestingOnDBAS               = 'interestingOnDBAS';
const initialPositionInterest         = 'initialPositionInterest';
const itIsTrueThat                    = 'itIsTrueThat';
const itIsFalseThat                   = 'itIsFalseThat';
const isItTrueThat                    = 'isItTrueThat';
const isItFalseThat                   = 'isItFalseThat';
const keepSetting                     = 'keepSetting';
const hideAllUsers                    = 'hideAllUsers';
const hideAllArguments                = 'hideAllArguments';
const languageCouldNotBeSwitched      = 'languageCouldNotBeSwitched';
const last_action                     = 'last_action';
const last_login                      = 'last_login';
const legend                          = 'legend';
const logfile                         = 'logfile';
const login                           = 'login';
const letsGo                          = 'letsGo';
const listOfDoneEdits                 = 'listOfDoneEdits';
const listOfPostedStatements          = 'listOfPostedStatements';
const listOfGivenVotes                = 'listOfGivenVotes';
const medium                          = 'medium';
const messageInfoTitle                = 'messageInfoTitle';
const messageInfoStatementCreatedBy   = 'messageInfoStatementCreatedBy';
const messageInfoAt                   = 'messageInfoAt';
const messageInfoMessage              = 'messageInfoMessage';
const messageInfoCurrentlySupported   = 'messageInfoCurrentlySupported';
const messageInfoParticipant          = 'messageInfoParticipant';
const messageInfoParticipantPl        = 'messageInfoParticipantPl';
const messageInfoSupporterSg          = 'messageInfoSupporterSg';
const messageInfoSupporterPl          = 'messageInfoSupporterPl';
const nickname                        = 'nickname';
const noCorrections                   = 'noCorrections';
const noCorrectionsSet                = 'noCorrectionsSet';
const noDecisionDone                  = 'noDecisionDone';
const notInsertedErrorBecauseEmpty    = 'notInsertedErrorBecauseEmpty';
const notInsertedErrorBecauseDuplicate= 'notInsertedErrorBecauseDuplicate';
const notInsertedErrorBecauseUnknown  = 'notInsertedErrorBecauseUnknown';
const notInsertedErrorBecauseInternal = 'notInsertedErrorBecauseInternal';
const notInsertedErrorBecauseTooShort = 'notInsertedErrorBecauseTooShort';
const noTrackedData                   = 'noTrackedData';
const noDecisionstaken                = 'noDecisionstaken';
const noReferencesButYouCanAdd        = 'noReferencesButYouCanAdd';
const noEntries                       = 'noEntries';
const noEntriesFor                    = 'noEntriesFor';
const note                            = 'note';
const neww                            = 'new';
const number                          = 'number';
const notificationWasSend             = 'notificationWasSend';
const noEditsInOptimization           = 'noEditsInOptimization';
const opinionBarometer                = 'opinionBarometer';
const option                          = 'option';
const ohsnap                          = 'ohsnap';
const report                          = 'report';
const reportTitle                     = 'reportTitle';
const passwordSubmit                  = 'passwordSubmit';
const proposalsWereForwarded          = 'proposalsWereForwarded';
const participantsSawThisStatement    = 'participantsSawThisStatement';
const participantSawThisStatement     = 'participantSawThisStatement';
const participantsSawArgumentsToThis  = 'participantsSawArgumentsToThis';
const participantSawArgumentsToThis   = 'participantSawArgumentsToThis';
const pinNavigation                   = 'pinNavigation';
const pleaseEditAtLeast               = 'pleaseEditAtLeast';
const queueCompleteSeen               = 'queueCompleteSeen';
const revokedArgument                 = 'revokedArgument';
const registered                      = 'registered';
const requestTrack                    = 'requestTrack';
const refreshTrack                    = 'refreshTrack';
const requestHistory                  = 'requestHistory';
const refreshHistory                  = 'refreshHistory';
const requestFailed                   = 'requestFailed';
const requestFailedBadToken           = 'requestFailedBadToken';
const requestFailedInternalError      = 'requestFailedInternalError';
const restartOnError                  = 'restartOnError';
const repuationChartSum               = 'repuationChartSum';
const repuationChartDay               = 'repuationChartDay';
const sawThis                         = 'saw this';
const saveMyStatement                 = 'saveMyStatement';
const saveMyStatements                = 'saveMyStatements';
const showAllUsers                    = 'showAllUsers';
const showAllArguments                = 'showAllArguments';
const showMeAnArgumentFor             = 'showMeAnArgumentFor';
const strength                        = 'strength';
const strong                          = 'strong';
const shortenedBy                     = 'shortenedBy';
const statisticsDeleted               = 'statisticsDeleted';
const statisticsNotDeleted            = 'statisticsNotDeleted';
const statisticsNotFetched            = 'statisticsNotFetched';
const statisticsNotThere              = 'statisticsNotThere';
const switchDiscussion                = 'switchDiscussion';
const switchDiscussionText            = 'switchDiscussionText';
const surname                         = 'surname';
const sureToDeleteReview              = 'sureToDeleteReview';
const showAllAttacksTitle             = 'showAllAttacksTitle';
const showAllUsersTitle               = 'showAllUsersTitle';
const text                            = 'text';
const to                              = 'to';
const textMinCountMessageBegin1       = 'textMinCountMessageBegin1';
const textMinCountMessageBegin2       = 'textMinCountMessageBegin2';
const textMinCountMessageDuringTyping = 'textMinCountMessageDuringTyping';
const textMaxCountMessage             = 'textMaxCountMessage';
const textMaxCountMessageError        = 'textMaxCountMessageError';
const timestamp                       = 'timestamp';
const typeofVote                      = 'typeofVote';
const users                           = 'users';
const usersWithSameOpinion            = 'usersWithSameOpinion';
const unpinNavigation                 = 'unpinNavigation';
const veryweak                        = 'veryweak';
const valid                           = 'valid';
const vote                            = 'vote';
const votes                           = 'votes';
const youAreAbleToReviewNow           = 'youAreAbleToReviewNow';
const yourAreNotTheAuthorOfThisAnymore = 'yourAreNotTheAuthorOfThisAnymore'
const weak                            = 'weak';

const next                            = 'next';
const prev                            = 'prev';
const tourEnd                         = 'tourEnd';
const welcomeDialogBody               = 'welcomeDialogBody';
const tourWelcomeTitle                = 'tourWelcomeTitle';
const tourWelcomeContent              = 'tourWelcomeContent';
const tourStartButtonTitle            = 'tourStartButtonTitle';
const tourStartButtonContent          = 'tourStartButtonContent';
const tourStartHeaderTitle            = 'tourStartHeaderTitle';
const tourStartHeaderContent          = 'tourStartHeaderContent';
const tourLoginTitle                  = 'tourLoginTitle';
const tourLoginContent                = 'tourLoginContent';
const tourIssueTitle                  = 'tourIssueTitle';
const tourIssueContent                = 'tourIssueContent';
const tourStartDiscussionTitle        = 'tourStartDiscussionTitle';
const tourStartDiscussionContent      = 'tourStartDiscussionContent';
const tourSelectAnswertTitle          = 'tourSelectAnswertTitle';
const tourSelectAnswertContent        = 'tourSelectAnswertContent';
const tourEnterStatementTitle         = 'tourEnterStatementTitle';
const tourEnterStatementContent       = 'tourEnterStatementContent';
const tourHaveFunTitle                = 'tourHaveFunTitle';
const tourHaveFunContent              = 'tourHaveFunContent';

// cookies
const WARNING_CHANGE_DISCUSSION_POPUP = 'WARNING_CHANGE_DISCUSSION_POPUP';
const BUBBLE_INFOS = 'SPEECH_BUBBLE_INFOS';
const GUIDED_TOUR = 'DID_GUIDED_TOUR';
const GUIDED_TOUR_RUNNING = 'GUIDED_TOUR_RUNNING';
const ADMIN_WARNING = 'hide-admin-caution-warning';

/**
 * URL's
 * @type {string}
 */
const urlContact  = 'contact';
const urlLogin    = 'login';
const urlNews     = 'news';
const urlContent  = 'discuss';
const urlSettings = 'settings';
const urlImprint  = 'imprint';
const urlLogout   = 'logout';
const urlReview   = 'review';


const dbas_en = {
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
    'attack': 'Attack',
    'author': 'Author',
    'because': 'because',
    'countOfArguments': 'Count of arguments',
    'countdownEnded': 'Your time is up. Unfortunately you cannot edit anything on this page anymore.',
    'contentWillBeRevoked': 'You will be disassociated from the content.',
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
    'clickedOnThis': 'clicked on this',
    'deleteTrack': 'Delete track',
    'deleteHistory': 'Delete history',
    'dataRemoved': 'Data was successfully removed.',
    'dataAdded': 'Data was successfully added.',
    'date': 'Date',
    'didYouMean': 'Top10 statements, which you probably could mean:',
    'duplicateDialog': 'This textversion is deprecated, because it was already edited to this version.\nDo you want to set this version as the current one once again?',
    'doNotHesitateToContact': 'Do not hesitate to <b><span style="cursor: pointer;" id="contact_on_error">contact us (click here)</span></b>',
    'deleteStatisticsTitle': 'Delete Statistics',
    'deleteStatisticsBody': 'Are you sure? This will delete all stored information about clicks respectively votes you have done.',
    'euCookiePopupTitle': 'This website uses cookies and Piwik.',
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
    'messageInfoTitle': 'Infos about an argument',
    'messageInfoStatementCreatedBy': 'This was created by',
    'messageInfoAt': 'at',
    'messageInfoMessage': 'Message',
    'messageInfoCurrentlySupported': 'This argument is supported by',
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
    'pleaseEditAtLeast': 'Please edit at least X chars to reduce noise!',
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
    'sawThis': 'saw this',
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
    'textMaxCountMessageError': 'Please shorten!',
    'users': 'Users',
    'usersWithSameOpinion': 'Users with same opinion',
    'unpinNavigation': 'Unpin Navigation',
    'youAreAbleToReviewNow': 'You are now able to visit the review section.',
    'yourAreNotTheAuthorOfThisAnymore': 'You are not the author of this post anymore.',
    'valid': 'Valid',
    'veryweak': 'very weak',
    'vote': 'vote',
    'votes': 'votes',
    'weak': 'weak',
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
    'tourIssueTitle': 'Topic',
    'tourIssueContent': 'Here you can the topic, which the current discussion is about.',
    'tourStartDiscussionTitle': 'First steps',
    'tourStartDiscussionContent': 'On the left side there are messages of the system and on the right side there are your answers.',
    'tourSelectAnswertTitle': 'First selection',
    'tourSelectAnswertContent': 'In the lower part you can choose your answers ...',
    'tourEnterStatementTitle': 'Your own response',
    'tourEnterStatementContent': '... or enter new statement, if you are logged in.',
    'tourHaveFunTitle': 'And now ...',
    'tourHaveFunContent': '... have fun!',
};

const dbas_de = {
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
    'attack': 'Angriff',
    'author': 'Autor',
    'because':'weil',
    'confirmTranslation': 'Wenn Sie die Sprache ändern, geht Ihr aktueller Fortschritt verloren!',
    'caution': 'Achtung',
    'correctionsSet': 'Ihre Korrektur wurde gesetzt.',
    'countOfArguments': 'Anzahl der Argumente',
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
    'clickedOnThis': 'haben\'s angeklickt',
    'dataRemoved': 'Daten wurden erfolgreich gelöscht.',
    'dataAdded': 'Daten wurden erfolgreich hinzugefügt.',
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
    'messageInfoTitle': 'Informationen über ein Argument',
    'messageInfoStatementCreatedBy': 'Dieses Argument stammt von',
    'messageInfoAt': 'am',
    'messageInfoMessage': 'Aussage',
    'messageInfoCurrentlySupported': 'Das Argument wird aktuell von',
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
    'pleaseEditAtLeast': 'Bitte ändern Sie mindestens X Zeichen um unnötige Änderungen zu vermeiden.',
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
    'sawThis': 'sahen dies!',
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
    'switchDiscussionText': 'Wollen Sie wirklich die aktuelle Diskussion verlassen und zur Diskussion über <strong>XXX</strong> wechseln?',
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
    'textMaxCountMessageError': 'Versuchen Sie zu kürzen!',
    'valid': 'Gültigkeit',
    'veryweak': 'sehr schwach',
    'youAreAbleToReviewNow': 'Sie können nun andere Beiträge begutachten.',
    'yourAreNotTheAuthorOfThisAnymore': 'Sie werden nicht mehr als Autor des Beitrags angezeigt.',
    'vote': 'Stimme',
    'votes': 'Stimmen',
    'weak': 'schwach',
    'next': 'Nächster',
    'prev': 'Zurück',
    'tourEnd': 'Beenden',
    'welcomeDialogBody': 'Es scheint, dass Sie zum ersten mal hier sind. Möchten Sie eine kurze Einführung sehen?',
    'tourWelcomeTitle': 'Willkommen!',
    'tourWelcomeContent': 'Willkommen bei D-BAS! Sie werden nun eine kurze Einführung bekommen.',
    'tourStartButtonTitle': 'Diskussion starten',
    'tourStartButtonContent': 'Hier können Sie die Diskussion direkt starten.',
    'tourStartHeaderTitle': 'Diskussion starten',
    'tourStartHeaderContent': '... oder auch hier.',
    'tourLoginTitle': 'Anmeldung',
    'tourLoginContent': 'Sie sollten sich aber anmelden, um Beiträge verfassen zu können.',
    'tourIssueTitle': 'Thema',
    'tourIssueContent': 'Hier sehen Sie das aktuelle Diskussionsthema.',
    'tourStartDiscussionTitle': 'Erste Schritte',
    'tourStartDiscussionContent': 'In diesem Abschnitt sehen Sie links Nachrichten des System und rechts Ihre eigenen Nachrichten.',
    'tourSelectAnswertTitle': 'Erste Auswahl',
    'tourSelectAnswertContent': 'Im unteren Teil können Sie Antworten auswählen ...',
    'tourEnterStatementTitle': 'Eigene Antworten',
    'tourEnterStatementContent': '... oder eigene Antworten eingeben, sofern Sie eingeloggt sind.',
    'tourHaveFunTitle': 'Und nun ...',
    'tourHaveFunContent': '... viel Spaß!',
};
