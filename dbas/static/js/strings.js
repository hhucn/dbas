/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */
	
var mainpage = 'http://localhost:4284/';
//var mainpage = 'https://dbas.cs.uni-duesseldorf.de/discussion/';

/**
 * Messages & Errors
 * @type {string}
 */
var addedEverything 					= "Everything was added.";
var confirmation 						= "Confirmation";
var confirmTranslation 					= "If you change the language, your process on this page will be lost and you have to restart the discussion!";
var correctionsSet 						= "Your correction was set.";
var euCookiePopupTitle 					= "This website is using cookies and Google Analytics.";
var euCookiePopupText 					= "We use them to give you the best experience. If you continue using our website, we\'ll assume that you are happy to receive all cookies on this website.";
var euCookiePopoupButton1 				= "Continue";
var euCookiePopoupButton2 				= "Learn&nbsp;more";
var empty_news_input  					= "News title or text is empty or too short!";
var feelFreeToShareUrl 					= "Please feel free to share this url";
var fetchLongUrl 						= "Fetch long url!";
var fetchShortUrl 						= "Fetch short url!";
var internalFailureWhileDeletingTrack 	= "Internal failure, please try again or did you have deleted your track recently?";
var internal_error 						= 'Internal Error: Maybe the server is offline or your session run out.';
var hideAllUsers 						= "Hide all users";
var hideAllAttacks 						= "Hide all attacks";
var noIslandView 						= "Could not fetch data for the island view. Sorry!";
var noCorrections 						= "No corrections for the given statement.";
var noCorrectionsSet 					= "Correction could not be set, because your user was not fount in the database. Are you currently logged in?";
var notInsertedErrorBecauseEmpty 		= "Your idea was not inserted, because your input text is empty.";
var notInsertedErrorBecauseDuplicate 	= "Your idea was not inserted, because your idea is a duplicate.";
var notInsertedErrorBecauseUnknown 		= "Your idea was not inserted due to an unkown error.";
var request_failed 						= "Request failed";
var selectStatement 					= "Please select a statement!";
var showAllUsers 						= "Show all users";
var showAllAttacks 						= "Show all attacks";

var strength 							= "Strength";
var veryweak 							= "very weak";
var weak 								= "weak";
var medium 								= "medium";
var strong 								= "strong";

/**
 * Text for the dialogue
 * @type {string[]}
 */
var sentencesOpenersForArguments = [
	//"Okay, you have got the opinion: ",
	//"Interesting, your opinion is: ",
	//"You have said, that: ",
	"So your opinion is that"];
var sentencesOpenersArguingWithAgreeing = [
	"I agree because ",
	"Therefore "];
var sentencesOpenersArguingWithDisagreeing = [
	"I disagree because ",
	"Alternatively "];
var sentencesOpenersInforming = [
	"I think we should ",
	"Let me explain it this way ",
	"I\"m reasonably sure that "];
var sentencesOpenersRequesting = [
	//"Can you explain why ",
	"Why do you think that"];
var agreeBecause = "I agree because ";
var because = "Because";
var clickToChoose = "Click to choose";
var canYouGiveAReason = "Can you give a reason?";
var disagreeBecause = "I disagree because ";
var firstOneText = "You are the first one, who said: ";
var firstPositionText = "You are the first one in this discussion!";
var goodPointTakeMeBackButtonText = "I agree, that is a good argument! Take me one step back.";
var otherParticipantsThinkThat = "Other users think that";
var otherParticipantsDontThink = "Other users do not have any counter-argument for ";
var otherParticipantsAcceptBut = "Other users accept your argument, but";
var otherParticipantAgree = "Other partcipants agree, that ";
var otherParticipantDisagree = "Other partcipants disagree, that ";
var islandViewHeaderText = "These are all arguments for: ";
var newPremisseRadioButtonText = "None of the above! Let me state my own reason(s)!";
var newConclusionRadioButtonText = "Neither of the above, I have a different idea!";
var addPremisseRadioButtonText = "Let me insert my reason(s)!";
var addArgumentRadioButtonText = "Let me insert my own argument(s)!";
var firstConclusionRadioButtonText = "Let me insert my idea!";
var argumentContainerH4TextIfPremisse = "You want to state your own reason(s)?";
var argumentContainerH4TextIfArgument = "You want to state your own argument(s)?";
var argumentContainerH4TextIfConclusion = "What is your idea? What should we do?";
var startDiscussionText = "What is your initial position?"; //"OK. Let\'s move on. Wich point do you want to discuss?";
var whatDoYouThink = "What do you think about that?";