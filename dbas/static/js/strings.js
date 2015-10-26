/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

var mainpage = 'http://localhost:4284/';
//var mainpage = 'https://dbas.cs.uni-duesseldorf.de/';

/**
 * Returns a translatet string with the given id in the right suitable.
 * @param id of the string
 * @returns {string} which is translated or unknown value
 * @private
 */
_t = function(id){
	var this_id, value = 'unknown identifier';
	$('#' + languageDropdownId).children().each(function(){
		if ($(this).hasClass('active')){
			this_id = $(this).children().first().attr('id');

			if (this_id.indexOf('en') != -1 && dbas_en.hasOwnProperty(id)){
				value= dbas_en[id];
			} else if (this_id.indexOf('de') != -1 && dbas_de.hasOwnProperty(id)){
				value = dbas_de[id]
			} else {
				value = 'unknown value';
			}
		}
	});
	return value;
};

/**
 * Messages & Errors
 * @type {string}
 */
var and 									= 'and';
var addedEverything 						= 'addedEverything';
var alreadyInserted							= 'alreadyInserted';
var addPremissesRadioButtonText 			= 'addPremissesRadioButtonText';
var addArgumentsRadioButtonText 			= 'addArgumentsRadioButtonText';
var argumentContainerH4TextIfPremisses 		= 'argumentContainerH4TextIfPremisses';
var argumentContainerH4TextIfArguments 		= 'argumentContainerH4TextIfArguments';
var addPremisseRadioButtonText 				= 'addPremisseRadioButtonText';
var addArgumentRadioButtonText 				= 'addArgumentRadioButtonText';
var argumentContainerH4TextIfPremisse 		= 'argumentContainerH4TextIfPremisse';
var argumentContainerH4TextIfArgument 		= 'argumentContainerH4TextIfArgument';
var argumentContainerH4TextIfConclusion 	= 'argumentContainerH4TextIfConclusion';
var alternatively 							= 'alternatively';
var argument 								= 'argument';
var attackedBy 								= 'attackedBy';
var attackedWith 							= 'attackedWith';
var agreeBecause 							= 'agreeBecause';
var andIDoBelieve							= 'andIDoBelieve';
var addArguments 							= 'addArguments';
var acceptIt 								= 'acceptIt';
var addArgumentsTitle 						= 'addArgumentsTitle';
var acceptItTitle 							= 'acceptItTitle';
var butIDoNotBelieve						= 'butIDoNotBelieve';
var because 								= 'because';
var butWhich 								= 'butWhich';
var clickHereForRegistration 				= 'clickHereForRegistration';
var confirmation 							= 'confirmation';
var confirmTranslation 						= 'confirmTranslation';
var correctionsSet 							= 'correctionsSet';
var checkFirstname							= 'checkFirstname';
var checkLastname							= 'checkLastname';
var checkNickname							= 'checkNickname';
var checkEmail								= 'checkEmail';
var checkPassword							= 'checkPassword';
var checkConfirmation 						= 'checkConfirmation';
var checkPasswordEqual 						= 'checkPasswordEqual';
var clickToChoose 							= 'clickToChoose';
var completeView 							= 'completeView';
var completeViewTitle						= 'completeViewTitle';
var canYouGiveAReason 						= 'canYouGiveAReason';
var dateString								= 'dateString';
var disagreeBecause 						= 'disagreeBecause';
var dialogView 								= 'dialogView';
var dialogViewTitle							= 'dialogViewTitle';
var dataRemoved 							= 'dataRemoved';
var didYouMean								= 'didYouMean';
var discussionEnd							= 'discussionEnd';
var duplicateDialog							= 'duplicateDialog';
var doesNotHoldBecause 						= 'doesNotHoldBecause';
var doesNotJustify 							= 'doesNotJustify';
var doNotHesitateToContact 					= 'doNotHesitateToContact';
var doYouWantToEnterYourStatements 			= 'doYouWantToEnterYourStatements';
var deleteTrack 							= 'deleteTrack';
var euCookiePopupTitle 						= 'euCookiePopupTitle';
var euCookiePopupText 						= 'euCookiePopupText';
var euCookiePopoupButton1 					= 'euCookiePopoupButton1';
var euCookiePopoupButton2 					= 'euCookiePopoupButton2';
var empty_news_input  						= 'empty_news_input';
var email 									= 'email';
var edit 									= 'edit';
var errorCode 								= 'error_code';
var editTitle								= 'editTitle';
var firstConclusionRadioButtonText 			= 'firstConclusionRadioButtonText';
var firstArgumentRadioButtonText			= 'firstArgumentRadioButtonText';
var feelFreeToShareUrl 						= 'feelFreeToShareUrl';
var fetchLongUrl 							= 'fetchLongUrl';
var fetchShortUrl 							= 'fetchShortUrl';
var forgotPassword 							= 'forgotPassword';
var firstOneText 							= 'firstOneText';
var firstPositionText 						= 'firstPositionText';
var firstname 								= 'firstname';
var firstPremisseText1 						= 'firstPremisseText1';
var firstPremisseText2 						= 'firstPremisseText2';
var gender 									= 'gender';
var goStepBack 								= 'goStepBack';
var generateSecurePassword 					= 'generateSecurePassword';
var goodPointTakeMeBackButtonText 			= 'goodPointTakeMeBackButtonText';
var group_uid 								= 'group_uid';
var haveALookAt 							= 'haveALookAt';
var hidePasswordRequest 					= 'hidePasswordRequest';
var hideGenerator 							= 'hideGenerator';
var internalFailureWhileDeletingTrack 		= 'internalFailureWhileDeletingTrack';
var internal_error 							= 'internal_error';
var issueList								= 'issueList';
var islandView 								= 'islandView';
var islandViewTitle							= 'islandViewTitle';
var islandViewHeaderText 					= 'islandViewHeaderText';
var irrelevant 								= 'irrelevant';
var itIsTrue 								= 'itIsTrue';
var itIsFalse 								= 'itIsFalse';
var iAcceptCounter							= 'iAcceptCounter';
var iHaveStrongerArgument 					= 'iHaveStrongerArgument';
var iNoOpinion 								= 'iNoOpinion';
var interestingOnDBAS 						= 'interestingOnDBAS';
var keepSetting								= 'keepSetting';
var hideAllUsers 							= 'hideAllUsers';
var hideAllAttacks 							= 'hideAllAttacks';
var letMeExplain 							= 'letMeExplain';
var levenshteinDistance						= 'levenshteinDistance';
var languageCouldNotBeSwitched 				= 'languageCouldNotBeSwitched';
var last_action 							= 'last_action';
var last_login 								= 'last_login';
var logfile									= 'logfile';
var medium 									= 'medium';
var newPremissesRadioButtonText 			= 'newPremisseRadioButtonText';
var newPremissesRadioButtonTextAsFirstOne	= 'newPremisseRadioButtonTextAsFirstOne';
var newStatementsRadioButtonTextAsFirstOne 	= 'newStatementRadioButtonTextAsFirstOne';
var newPremisseRadioButtonText 				= 'newPremisseRadioButtonText';
var newPremisseRadioButtonTextAsFirstOne	= 'newPremisseRadioButtonTextAsFirstOne';
var newStatementRadioButtonTextAsFirstOne 	= 'newStatementRadioButtonTextAsFirstOne';
var newConclusionRadioButtonText 			= 'newConclusionRadioButtonText';
var nickname 								= 'nickname';
var noIslandView 							= 'noIslandView';
var noCorrections 							= 'noCorrections';
var noCorrectionsSet 						= 'noCorrectionsSet';
var notInsertedErrorBecauseEmpty 			= 'notInsertedErrorBecauseEmpty';
var notInsertedErrorBecauseDuplicate 		= 'notInsertedErrorBecauseDuplicate';
var notInsertedErrorBecauseUnknown 			= 'notInsertedErrorBecauseUnknown';
var notInsertedErrorBecauseInternal			= 'notInsertedErrorBecauseInternal';
var noTrackedData 							= 'noTrackedData';
var number 									= 'number';
var otherParticipantsThinkThat 				= 'otherParticipantsThinkThat';
var otherParticipantsDontHave 				= 'otherParticipantsDontHave';
var otherParticipantsAcceptBut 				= 'otherParticipantsAcceptBut';
var otherParticipantAgree 					= 'otherParticipantAgree';
var otherParticipantDisagree 				= 'otherParticipantDisagree';
var premisseGroup 							= 'premisseGroup';
var passwordSubmit 							= 'passwordSubmit';
var registered 								= 'registered';
var right 									= 'right';
var requestTrack 							= 'requestTrack';
var refreshTrack 							= 'refreshTrack';
var requestFailed 							= 'requestFailed';
var restartDiscussion 						= 'restartDiscussion';
var restartDiscussionTitle					= 'restartDiscussionTitle';
var selectStatement 						= 'selectStatement';
var showAllUsers 							= 'showAllUsers';
var showAllAttacks 							= 'showAllAttacks';
var strength 								= 'strength';
var strong 									= 'strong';
var strongerStatementForRecjecting 			= 'strongerStatementForRecjecting';
var soYourOpinionIsThat 					= 'soYourOpinionIsThat';
var shortenedWith 							= 'shortenedWith';
var switchDiscussion						= 'switchDiscussion';
var switchDiscussionText1 					= 'switchDiscussionText1';
var switchDiscussionText2 					= 'switchDiscussionText2';
var startDiscussionText 					= 'startDiscussionText';
var statement 								= 'statement';
var sureThat 								= 'sureThat';
var surname 								= 'surname';
var showAllAttacksTitle 					= 'showAllAttacksTitle';
var showAllUsersTitle 						= 'showAllUsersTitle';
var textAreaReasonHintText 					= 'textAreaReasonHintText';
var theCounterArgument 						= 'theCounterArgument';
var therefore 								= 'therefore';
var thinkWeShould 							= 'thinkWeShould';
var track 									= 'track';
var topicString								= 'topicString';
var text 									= 'text';
var theySay 								= 'theySay';
var veryweak 								= 'veryweak';
var weak 									= 'weak';
var wrong 									= 'wrong';
var whatDoYouThink 							= 'whatDoYouThink';
var whyDoYouThinkThat 						= 'whyDoYouThinkThat';
var youMadeA 								= 'youMadeA';
var youMadeAn 								= 'youMadeAn';

// cookies
var WARNING_CHANGE_DISCUSSION_POPUP = 'WARNING_CHANGE_DISCUSSION_POPUP';

/**
 * Text for the dialogue
 * @type {string[]}
 */
var sentencesOpenersForArguments = [
	soYourOpinionIsThat
	//'Okay, you have got the opinion: ',
	//'Interesting, your opinion is: ',
	//'You have said, that: ',
	];
var sentencesOpenersArguingWithAgreeing = [
	agreeBecause,
	therefore];
var sentencesOpenersArguingWithDisagreeing = [
	disagreeBecause,
	alternatively];
var sentencesOpenersInforming = [
	thinkWeShould,
	letMeExplain,
	sureThat];
var sentencesOpenersRequesting = [
	whyDoYouThinkThat
	//'Can you explain why '
	];

/**
 * URL's
 * @type {string}
 */
var attrGetPremissesForStatement = 'get_premisses_for_statement';
var attrReplyForPremissegroup = 'reply_for_premissegroup';
var attrReplyForArgument = 'reply_for_argument';
var attrReplyForResponseOfConfrontation = 'reply_for_response_of_confrontation';
var attrGo = 'go';
