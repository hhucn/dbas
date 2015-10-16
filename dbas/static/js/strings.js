/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */
	
//var mainpage = 'http://localhost:4284/';
var mainpage = 'https://dbas.cs.uni-duesseldorf.de/';

/**
 * Messages & Errors
 * @type {string}
 */
var addedEverything 					= 'Everything was added.';
var alreadyInserted						= 'This is a duplicate and already there.';
var clickHereForRegistration 			= 'Click <a href="" data-toggle="modal" data-target="#popup_login" title="Login">here</a> for login or registration!'; // Todo insert
var confirmation 						= 'Confirmation';
var confirmTranslation 					= 'If you change the language, your process on this page will be lost and you have to restart the discussion!';
var correctionsSet 						= 'Your correction was set.';
var dataRemoved 						= 'Data was successfully removed.';
var didYouMean							= 'Did you mean:';
var discussionEnd						= 'The discussion ends here. If you want to proceed, please feel free to login yourself :)';
var duplicateDialog						= 'This textversion is deprecated, because it was already edited.\nDo you want to set this' +
	' version as the current one once again?'; // Todo insert
// into dict
var euCookiePopupTitle 					= 'This website is using cookies and Google Analytics.';
var euCookiePopupText 					= 'We use them to give you the best experience. If you continue using our website, we\'ll assume that you are happy to receive all cookies on this website.';
var euCookiePopoupButton1 				= 'Continue';
var euCookiePopoupButton2 				= 'Learn&nbsp;more';
var empty_news_input  					= 'News title or text is empty or too short!';
var feelFreeToShareUrl 					= 'Please feel free to share this url';
var fetchLongUrl 						= 'Fetch long url!';
var fetchShortUrl 						= 'Fetch short url!';
var internalFailureWhileDeletingTrack 	= 'Internal failure, please try again or did you have deleted your track recently?';
var internal_error 						= 'Internal Error: Maybe the server is offline or your session run out.';
var issueList							= 'Topics'; // todo insert;
var hideAllUsers 						= 'Hide all users';
var hideAllAttacks 						= 'Hide all attacks';
var levenshteinDistance					= 'Levenshtein-Distance';
var noIslandView 						= 'Could not fetch data for the island view. Sorry!';
var noCorrections 						= 'No corrections for the given statement.';
var noCorrectionsSet 					= 'Correction could not be set, because your user was not fount in the database. Are you currently logged in?';
var notInsertedErrorBecauseEmpty 		= 'Your idea was not inserted, because your input text is empty.';
var notInsertedErrorBecauseDuplicate 	= 'Your idea was not inserted, because your idea is a duplicate.';
var notInsertedErrorBecauseUnknown 		= 'Your idea was not inserted due to an unkown error.';
var notInsertedErrorBecauseInternal		= 'Your idea was not inserted due to an internal error.';
var noTrackedData 						= 'No data was tracked.';
var request_failed 						= 'Request failed';
var selectStatement 					= 'Please select a statement!';
var showAllUsers 						= 'Show all users';
var showAllAttacks 						= 'Show all attacks';
var switchDiscussion					= 'Change the discussion\'s topic';
var switchDiscussionText1 				= 'If you accept, you will change the topic of the discussion to'; // todo insert
var switchDiscussionText2 				= 'and the discussion will be restarted.'; // todo insert
var textAreaReasonHintText 				= 'Please use a new textarea for every reason, write short and clear!';
var theCounterArgument 					= 'the counter-argument';

var strength 							= 'Strength';
var veryweak 							= 'very weak';
var weak 								= 'weak';
var medium 								= 'medium';
var strong 								= 'strong';

var right 								= 'Right';
var wrong 								= 'Wrong';
var irrelevant 							= 'Irrelevant';
var believeThatGoodCounter 				= 'believe that this is a good counter-argument for';
var itIsTrue 							= 'it is true that';
var itIsFalse 							= 'it is false that';
var butIDoNot 							= 'but I do not';
var andIDo 								= 'and I do';
var iAcceptCounter						= 'and I do accept that this is an counter-argument for';
var iHaveStrongerArgument 				= 'However, I have a much stronger argument for accepting that';
var goStepBack 							= 'Go one step back'; // TODO: show me another one
var iNoOpinion 							= 'I have no opinion regarding';

var youMadeA 							= 'You made a';
var youMadeAn 							= 'You made an';
var doesNotHoldBecause 					= 'does not hold, because';
var strongerStatementForRecjecting 		= 'they have a stronger statement for rejecting';
var doesNotJustify 						= 'does not justify that';
var butWhich 							= 'but which one';
var interestingOnDBAS 					= 'Interesting discussion on DBAS';
var haveALookAt 						= 'Hey, please have a look at ';

var forgotPassword 						= 'Forgot Password'; // todo insert
var hidePasswordRequest 				= 'Hide Password Request'; // todo insert
var generateSecurePassword 				= 'Generate secure password'; // todo insert
var hideGenerator 						= 'Hide Generator'; // todo insert
var checkFirstname						= 'Better check your first name, because the input is empty!'; // todo insert
var checkLastname						= 'Better check your last name, because the input is empty!'; // todo insert
var checkNickname						= 'Better check your nickname, because the input is empty!'; // todo insert
var checkEmail							= 'Better check your email, because the input is empty!'; // todo insert
var checkPassword						= 'Better check your password, because the input is empty!'; // todo insert
var checkConfirmation 					= 'Better check the confirmation of your password, because the input is empty!'; // todo insert
var checkPasswordEqual 					= 'Better check your passwords, because they are not  equal!'; // todo insert
var languageCouldNotBeSwitched 			= 'Unfortunately, the language could not be switched'; // todo insert
var requestFailed 						= 'Request failed'; // todo insert


/**
 * Text for the dialogue
 * @type {string[]}
 */
var sentencesOpenersForArguments = [
	//'Okay, you have got the opinion: ',
	//'Interesting, your opinion is: ',
	//'You have said, that: ',
	'So your opinion is that'];
var sentencesOpenersArguingWithAgreeing = [
	'I agree because ',
	'Therefore '];
var sentencesOpenersArguingWithDisagreeing = [
	'I disagree because ',
	'Alternatively '];
var sentencesOpenersInforming = [
	'I think we should ',
	'Let me explain it this way ',
	'I\'m reasonably sure that '];
var sentencesOpenersRequesting = [
	//'Can you explain why ',
	'Why do you think that'];
var agreeBecause = 'I agree because ';
var because = 'Because';
var clickToChoose = 'Click to choose';
var canYouGiveAReason = 'Can you give a reason?';
var disagreeBecause = 'I disagree because ';
var firstOneText = 'You are the first one, who said: ';
var firstPositionText = 'You are the first one in this discussion!';
var goodPointTakeMeBackButtonText = 'I agree, that is a good argument! Take me one step back.';
var otherParticipantsThinkThat = 'Other users think that';
var otherParticipantsDontHave = 'Other users do not have any counter-argument for ';
var otherParticipantsAcceptBut = 'Other users accept your argument, but';
var otherParticipantAgree = 'Other partcipants agree, that ';
var otherParticipantDisagree = 'Other partcipants disagree, that ';
var islandViewHeaderText = 'These are all arguments for: ';
var newPremisseRadioButtonText = 'None of the above! Let me state my own reason(s)!';
var newConclusionRadioButtonText = 'Neither of the above, I have a different idea!';
var addPremisseRadioButtonText = 'Let me insert my reason(s)!';
var addArgumentRadioButtonText = 'Let me insert my own argument(s)!';
var firstConclusionRadioButtonText = 'Let me insert my idea!';
var argumentContainerH4TextIfPremisse = 'You want to state your own reason(s)?';
var argumentContainerH4TextIfArgument = 'You want to state your own argument(s)?';
var argumentContainerH4TextIfConclusion = 'What is your idea? What should we do?';
var startDiscussionText = 'What is your initial position?'; //'OK. Let\'s move on. Wich point do you want to discuss?';
var whatDoYouThink = 'What do you think about that?';


/**
 * URL's
 * @type {string}
 */
var attrGetPremissesForStatement = 'get_premisses_for_statement';
var attrReplyForPremissegroup = 'reply_for_premissegroup';
var attrReplyForArgument = 'reply_for_argument';
var attrReplyForResponseOfConfrontation = 'reply_for_response_of_confrontation';
var attrGo = 'go';
