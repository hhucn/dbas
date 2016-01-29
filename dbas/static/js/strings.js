/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function get_hostname(url) {
	var m = url.match(/^http:\/\/[^/]+/);
	return m ? m[0] + '/' : null;
}
var mainpage = location.origin + '/'; //get_hostname(window.location.href);

/**
 * Returns a translated string
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
_t = function(id){
	var this_id, value = 'unknown identifier';
	$('#' + languageDropdownId).children().each(function(){
		if ($(this).hasClass('active')){
			this_id = $(this).children().first().attr('id');

			if (this_id.indexOf('en') != -1 && dbas_en.hasOwnProperty(id)){				value= dbas_en[id];
			} else if (this_id.indexOf('de') != -1 && dbas_de.hasOwnProperty(id)){		value = dbas_de[id];
			} else {                                                    				value = 'unknown value';
			}
		}
	});
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
 * Messages & Errors
 * @type {string}
 */
var checkmark                                       = '&#x2713;'; // ✓
var ballot                                          = '&#x2717;'; // ✗

var addedEverything 								= 'addedEverything';
var acceptIt 										= 'acceptIt';
var acceptItTitle 									= 'acceptItTitle';
var contactSubmit									= 'contactSubmit';
var correctionsSet 									= 'correctionsSet';
var checkFirstname									= 'checkFirstname';
var checkLastname									= 'checkLastname';
var checkNickname									= 'checkNickname';
var checkEmail										= 'checkEmail';
var checkPassword									= 'checkPassword';
var checkConfirmation 								= 'checkConfirmation';
var checkPasswordConfirm							= 'checkPasswordConfirm';
var countOfArguments                                = 'countOfArguments';
var dataRemoved 									= 'dataRemoved';
var didYouMean										= 'didYouMean';
var duplicateDialog									= 'duplicateDialog';
var doNotHesitateToContact 							= 'doNotHesitateToContact';
var deleteTrack 									= 'deleteTrack';
var deleteHistory 									= 'deleteHistory';
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
var keepSetting										= 'keepSetting';
var hideAllUsers 									= 'hideAllUsers';
var hideAllAttacks 									= 'hideAllAttacks';
var languageCouldNotBeSwitched 						= 'languageCouldNotBeSwitched';
var last_action 									= 'last_action';
var last_login 										= 'last_login';
var logfile											= 'logfile';
var letsGo 											= 'letsGo';
var medium 											= 'medium';
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
var noEntries                                       = 'noEntries';
var note 											= 'note';
var number 											= 'number';
var opinionBarometer                                = 'opinionBarometer';
var options                                         = 'options';
var report 											= 'report';
var reportTitle										= 'reportTitle';
var passwordSubmit 									= 'passwordSubmit';
var registered 										= 'registered';
var requestTrack 									= 'requestTrack';
var refreshTrack 									= 'refreshTrack';
var requestHistory 									= 'requestHistory';
var refreshHistory 									= 'refreshHistory';
var requestFailed 									= 'requestFailed';
var restartOnError									= 'restartOnError';
var showAllUsers 									= 'showAllUsers';
var showAllAttacks 									= 'showAllAttacks';
var showMeAnArgumentFor 							= 'showMeAnArgumentFor';
var strength 										= 'strength';
var strong 											= 'strong';
var shortenedBy 									= 'shortenedBy';
var switchDiscussion								= 'switchDiscussion';
var switchDiscussionText1 							= 'switchDiscussionText1';
var switchDiscussionText2 							= 'switchDiscussionText2';
var surname 										= 'surname';
var showAllAttacksTitle 							= 'showAllAttacksTitle';
var showAllUsersTitle 								= 'showAllUsersTitle';
var text 											= 'text';
var veryweak 										= 'veryweak';
var weak 											= 'weak';

// cookies
var WARNING_CHANGE_DISCUSSION_POPUP = 'WARNING_CHANGE_DISCUSSION_POPUP';

/**
 * URL's
 * @type {string}
 */
var urlContact 							= 'contact';
var urlLogin 							= 'login';
var urlNews 							= 'news';
var urlContent 							= 'content';
var urlSettings 						= 'settings';
var urlImprint 							= 'imprint';
var urlLogout 							= 'logout';
