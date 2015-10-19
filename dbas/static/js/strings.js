/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

var mainpage = 'http://localhost:4284/';
//var mainpage = 'https://dbas.cs.uni-duesseldorf.de/';

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
var addedEverything 					= 'Everything was added.';
var alreadyInserted						= 'This is a duplicate and already there.';
var addPremisseRadioButtonText 			= 'Let me insert my reason(s)!';
var addArgumentRadioButtonText 			= 'Let me insert my own argument(s)!';
var argumentContainerH4TextIfPremisse 	= 'You want to state your own reason(s)?';
var argumentContainerH4TextIfArgument 	= 'You want to state your own argument(s)?';
var argumentContainerH4TextIfConclusion = 'What is your idea? What should we do?';
var alternatively 						= 'Alternatively';
var argument 							= 'Argument';
var attackedBy 							= 'You were attacked by';
var attackedWith 						= 'You\'ve attacked with';
var agreeBecause 						= 'I agree because ';
var andIDoBelieve						= 'and I do believe that this is a good counter-argument for';
var butIDoNotBelieve					= 'but I do not believe that this is a good counter-argument for';
var because 							= 'Because';
var butWhich 							= 'but which one';
var clickHereForRegistration 			= 'Click <a href="" data-toggle="modal" data-target="#popup_login" title="Login">here</a> for login or registration!'; // Todo insert
var confirmation 						= 'Confirmation';
var confirmTranslation 					= 'If you change the language, your process on this page will be lost and you have to restart the discussion!';
var correctionsSet 						= 'Your correction was set.';
var checkFirstname						= 'Better check your first name, because the input is empty!';
var checkLastname						= 'Better check your last name, because the input is empty!';
var checkNickname						= 'Better check your nickname, because the input is empty!';
var checkEmail							= 'Better check your email, because the input is empty!';
var checkPassword						= 'Better check your password, because the input is empty!';
var checkConfirmation 					= 'Better check the confirmation of your password, because the input is empty!';
var checkPasswordEqual 					= 'Better check your passwords, because they are not  equal!';
var clickToChoose 						= 'Click to choose';
var canYouGiveAReason 					= 'Can you give a reason?';
var dateString							= 'Date';
var disagreeBecause 					= 'I disagree because ';
var dataRemoved 						= 'Data was successfully removed.';
var didYouMean							= 'Did you mean:';
var discussionEnd						= 'The discussion ends here. If you want to proceed, please feel free to login yourself :)';
var duplicateDialog						= 'This textversion is deprecated, because it was already edited.\nDo you want to set this version as the current one once again?';
var doesNotHoldBecause 					= 'does not hold, because';
var doesNotJustify 						= 'does not justify that';
var euCookiePopupTitle 					= 'This website is using cookies and Google Analytics.';
var euCookiePopupText 					= 'We use them to give you the best experience. If you continue using our website, we\'ll assume that you are happy to receive all cookies on this website.';
var euCookiePopoupButton1 				= 'Continue';
var euCookiePopoupButton2 				= 'Learn&nbsp;more';
var empty_news_input  					= 'News title or text is empty or too short!';
var email 								= 'E-Mail';
var firstConclusionRadioButtonText 		= 'Let me insert my idea!';
var feelFreeToShareUrl 					= 'Please feel free to share this url';
var fetchLongUrl 						= 'Fetch long url!';
var fetchShortUrl 						= 'Fetch short url!';
var forgotPassword 						= 'Forgot Password';
var firstOneText 						= 'You are the first one, who said: ';
var firstPositionText 					= 'You are the first one in this discussion!';
var firstname 							= 'Firstname';
var gender 								= 'Gender';
var goStepBack 							= 'Go one step back'; // TODO: show me another one
var generateSecurePassword 				= 'Generate secure password';
var goodPointTakeMeBackButtonText 		= 'I agree, that is a good argument! Take me one step back.';
var group_uid 							= 'Group';
var haveALookAt 						= 'Hey, please have a look at ';
var hidePasswordRequest 				= 'Hide Password Request';
var hideGenerator 						= 'Hide Generator';
var internalFailureWhileDeletingTrack 	= 'Internal failure, please try again or did you have deleted your track recently?';
var internal_error 						= 'Internal Error: Maybe the server is offline or your session run out.';
var issueList							= 'Topics';
var islandViewHeaderText 				= 'These are all arguments for: ';
var irrelevant 							= 'Irrelevant';
var itIsTrue 							= 'it is true that';
var itIsFalse 							= 'it is false that';
var iAcceptCounter						= 'and I do accept that this is an counter-argument for';
var iHaveStrongerArgument 				= 'However, I have a much stronger argument for accepting that';
var iNoOpinion 							= 'I have no opinion regarding';
var interestingOnDBAS 					= 'Interesting discussion on DBAS';
var hideAllUsers 						= 'Hide all users';
var hideAllAttacks 						= 'Hide all attacks';
var letMeExplain 						= 'Let me explain it this way';
var levenshteinDistance					= 'Levenshtein-Distance';
var languageCouldNotBeSwitched 			= 'Unfortunately, the language could not be switched';
var last_action 						= 'Last Action';
var last_login 							= 'Last Login';
var medium 								= 'medium';
var newPremisseRadioButtonText 			= 'None of the above! Let me state my own reason(s)!';
var newConclusionRadioButtonText 		= 'Neither of the above, I have a different idea!';
var nickname 							= 'Nickname';
var noIslandView 						= 'Could not fetch data for the island view. Sorry!';
var noCorrections 						= 'No corrections for the given statement.';
var noCorrectionsSet 					= 'Correction could not be set, because your user was not fount in the database. Are you currently logged in?';
var notInsertedErrorBecauseEmpty 		= 'Your idea was not inserted, because your input text is empty.';
var notInsertedErrorBecauseDuplicate 	= 'Your idea was not inserted, because your idea is a duplicate.';
var notInsertedErrorBecauseUnknown 		= 'Your idea was not inserted due to an unkown error.';
var notInsertedErrorBecauseInternal		= 'Your idea was not inserted due to an internal error.';
var noTrackedData 						= 'No data was tracked.';
var number 								= 'No';
var otherParticipantsThinkThat 			= 'Other users think that';
var otherParticipantsDontHave 			= 'Other users do not have any counter-argument for ';
var otherParticipantsAcceptBut 			= 'Other users accept your argument, but';
var otherParticipantAgree 				= 'Other partcipants agree, that ';
var otherParticipantDisagree 			= 'Other partcipants disagree, that ';
var premisseGroup 						= 'PremisseGroup';
var registered 							= 'Registered';
var right 								= 'Right';
var requestTrack 						= 'Request track';
var refreshTrack 						= 'Refresh track';
var requestFailed 						= 'Request failed';
var request_failed 						= 'Request failed';
var selectStatement 					= 'Please select a statement!';
var showAllUsers 						= 'Show all users';
var showAllAttacks 						= 'Show all attacks';
var strength 							= 'Strength';
var strong 								= 'strong';
var strongerStatementForRecjecting 		= 'they have a stronger statement for rejecting';
var soYourOpinionIsThat 				= 'So your opinion is that';
var shortenedWith 						= 'which was shortened with';
var switchDiscussion					= 'Change the discussion\'s topic';
var switchDiscussionText1 				= 'If you accept, you will change the topic of the discussion to';
var switchDiscussionText2 				= 'and the discussion will be restarted.';
var startDiscussionText 				= 'What is your initial position?'; //'OK. Let\'s move on. Wich point do you want to discuss?';
var statement 							= 'Statement';
var sureThat 							= 'I\'m reasonably sure that ';
var surname 							= 'Surname';
var textAreaReasonHintText 				= 'Please use a new textarea for every reason, write short and clear!';
var theCounterArgument 					= 'the counter-argument';
var therefore 							= 'Therefore';
var thinkWeShould 						= 'I think we should ';
var track 								= 'Track';
var topicString							= 'Topic';
var text 								= 'Text';
var veryweak 							= 'very weak';
var weak 								= 'weak';
var wrong 								= 'Wrong';
var whatDoYouThink 						= 'What do you think about that?';
var whyDoYouThinkThat 					= 'Why do you think that';
var youMadeA 							= 'You made a';
var youMadeAn 							= 'You made an';


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
