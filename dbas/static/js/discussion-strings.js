/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

/**
 * Messages & Errors
 * @type {string}
 */
var addedEverything = 'Everything was added.';
var correctionsSet = 'Your correction was set.';
var internalFailureWhileDeletingTrack = 'Internal failure, please try again or did you have deleted your track recently?';
var noIslandView = 'Could not fetch data for the island view. Sorry!';
var noCorrections = 'No corrections for the given statement.';
var noCorrectionsSet = 'Correction could not be set, because your user was not fount in the database. Are you currently logged in?';
var notInsertedErrorBecauseEmpty = "Your idea was not inserted, because your input text is empty.";
var notInsertedErrorBecauseDuplicate = "Your idea was not inserted, because your idea is a duplicate.";
var notInsertedErrorBecauseUnknown = "Your idea was not inserted due to an unkown error.";
var selectStatement = 'Please select a statement!';

/**
 * TEXT
 * @type {string[]}
 */
var sentencesOpenersForArguments = [
	'Okay, you have got the opinion: ',
	'Interesting, your opinion is: ',
	'You have said, that: ',
	'So your opinion is: '];
var sentencesOpenersArguing = [
	'I agree because ',
	'I disagree because ',
	'Alternatively ',
	'Therefore '];
var sentencesOpenersInforming = [
	'I think we should ',
	'Let me explain it this way ',
	'I\'m reasonably sure that '];
var sentencesOpenersRequesting = [
	'Can you explain why  ',
	'Why do you think that '];
var clickToChoose = 'Click to choose';
var agreeBecause = 'I agree because';
var disagreeBecause = 'I disagree because ';
var firstOneText = 'You are the first one, who said: ';
var firstPositionText = 'You are the first one in this discussion!';
var goodPointTakeMeBackButtonText = 'I agree, that is a good argument! Take me one step back.';
var islandViewHeaderText = 'These are all arguments for: ';
var newArgumentRadioButtonText = 'I disagree! Let me state my own reason(s)!';
var newPositionRadioButtonText = 'Neither of the above, I have a different idea!';
var firstArgumentRadioButtonText = 'Let me insert my reasons!';
var firstPositionRadioButtonText = 'Let me insert my ideas!';
var statementContainerH4TextIfArgument = 'You want to state your own reason(s)?';
var statementContainerH4TextIfPosition = 'What is your idea?';
var startDiscussionText = 'OK. Let\'s move on. Wich point do you want to discuss?';