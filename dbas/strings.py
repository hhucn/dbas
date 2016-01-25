from .logger import logger
from .database_helper import DBDiscussionSession
from .database.discussion_model import User

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015-2016

class Translator(object):

	def __init__(self, lang):
		"""

		:param lang: current language
		:return:
		"""
		self.lang = lang

		self.attack = 'attack'
		self.support = 'support'
		self.premise = 'premise'
		self.because = 'because'
		self.doesNotHoldBecause = 'doesNotHoldBecause'
		self.moreAbout = 'moreAbout'
		self.undermine1 = 'undermine1'
		self.undermine2 = 'undermine2'
		self.support1 = 'support1'
		self.support2 = 'support2'
		self.undercut1 = 'undercut1'
		self.undercut2 = 'undercut2'
		self.overbid1 = 'overbid1'
		self.overbid2 = 'overbid2'
		self.rebut1 = 'rebut1'
		self.rebut2 = 'rebut2'
		self.oldPwdEmpty = 'oldPwdEmpty'
		self.newPwdEmtpy = 'newPwdEmtpy'
		self.confPwdEmpty = 'confPwdEmpty'
		self.newPwdNotEqual = 'newPwdNotEqual'
		self.pwdsSame = 'pwdsSame'
		self.oldPwdWrong = 'oldPwdWrong'
		self.pwdChanged = 'pwdChanged'
		self.emptyName = 'emptyName'
		self.emptyEmail = 'emptyEmail'
		self.emtpyContent = 'emtpyContent'
		self.maliciousAntiSpam = 'maliciousAntiSpam'
		self.nonValidCSRF = 'nonValidCSRF'
		self.name = 'name'
		self.mail = 'mail'
		self.phone = 'phone'
		self.message = 'message'
		self.pwdNotEqual = 'pwdNotEqual'
		self.nickIsTaken = 'nickIsTaken'
		self.mailIsTaken = 'mailIsTaken'
		self.mailNotValid = 'mailNotValid'
		self.errorTryLateOrContant = 'errorTryLateOrContant'
		self.accountWasAdded = 'accountWasAdded'
		self.accountWasRegistered = 'accountWasRegistered'
		self.accoutErrorTryLateOrContant = 'accoutErrorTryLateOrContant'
		self.nicknameIs = 'nicknameIs'
		self.newPwdIs = 'newPwdIs'
		self.dbasPwdRequest = 'dbasPwdRequest'
		self.emailBodyText = 'emailBodyText'
		self.emailWasSent = 'emailWasSent'
		self.emailWasNotSent = 'emailWasNotSent'
		self.antispamquestion = 'antispamquestion'
		self.signs = 'signs'

		self.aand = 'and'
		self.addedEverything = 'addedEverything'
		self.alreadyInserted = 'alreadyInserted'
		self.addPremisesRadioButtonText = 'addPremisesRadioButtonText'
		self.addArgumentsRadioButtonText = 'addArgumentsRadioButtonText'
		self.argumentContainerTextIfPremises = 'argumentContainerTextIfPremises'
		self.argumentContainerTextIfArguments = 'argumentContainerTextIfArguments'
		self.addPremiseRadioButtonText = 'addPremiseRadioButtonText'
		self.addArgumentRadioButtonText = 'addArgumentRadioButtonText'
		self.argumentContainerTextIfPremise = 'argumentContainerTextIfPremise'
		self.argumentContainerTextIfArgument = 'argumentContainerTextIfArgument'
		self.argumentContainerTextIfConclusion = 'argumentContainerTextIfConclusion'
		self.argueAgainstPositionToggleButton = 'argueAgainstPositionToggleButton'
		self.argueForPositionToggleButton = 'argueForPositionToggleButton'
		self.alternatively = 'alternatively'
		self.argument = 'argument'
		self.andIDoNotBelieveCounter = 'andIDoNotBelieveCounter'
		self.andIDoNotBelieveArgument = 'andIDoNotBelieveArgument'
		self.andTheyDoNotBelieveCounter = 'andTheyDoNotBelieveCounter'
		self.andTheyDoNotBelieveArgument = 'andTheyDoNotBelieveArgument'
		self.asReasonFor = 'asReasonFor'
		self.attackedBy = 'attackedBy'
		self.attackedWith = 'attackedWith'
		self.attackPosition = 'attackPosition'
		self.agreeBecause = 'agreeBecause'
		self.andIDoBelieve = 'andIDoBelieve'
		self.addArguments = 'addArguments'
		self.addStatements = 'addStatements'
		self.addArgumentsTitle = 'addArgumentsTitle'
		self.acceptItTitle = 'acceptItTitle'
		self.acceptIt = 'acceptIt'
		self.breadcrumbsStart = 'breadcrumbsStart'
		self.breadcrumbsChooseActionForStatement = 'breadcrumbsChooseActionForStatement'
		self.breadcrumbsGetPremisesForStatement = 'breadcrumbsGetPremisesForStatement'
		self.breadcrumbsMoreAboutArgument = 'breadcrumbsMoreAboutArgument'
		self.breadcrumbsReplyForPremisegroup = 'breadcrumbsReplyForPremisegroup'
		self.breadcrumbsReplyForResponseOfConfrontation = 'breadcrumbsReplyForResponseOfConfrontation'
		self.breadcrumbsReplyForArgument = 'breadcrumbsReplyForArgument'
		self.butOtherParticipantsDontHaveArgument = 'butOtherParticipantsDontHaveArgument'
		self.butIDoNotBelieveCounter = 'butIDoNotBelieveCounter'
		self.butIDoNotBelieveArgument = 'butIDoNotBelieveArgument'
		self.butTheyDoNotBelieveCounter = 'butTheyDoNotBelieveCounter'
		self.butTheyDoNotBelieveArgument = 'butTheyDoNotBelieveArgument'
		self.because = 'because'
		self.butWhich = 'butWhich'
		self.clickHereForRegistration = 'clickHereForRegistration'
		self.confirmation = 'confirmation'
		self.contactSubmit = 'contactSubmit'
		self.confirmTranslation = 'confirmTranslation'
		self.correctionsSet = 'correctionsSet'
		self.countOfArguments = 'countOfArguments'
		self.checkFirstname = 'checkFirstname'
		self.checkLastname = 'checkLastname'
		self.checkNickname = 'checkNickname'
		self.checkEmail = 'checkEmail'
		self.checkPassword = 'checkPassword'
		self.checkConfirmation = 'checkConfirmation'
		self.checkPasswordConfirm = 'checkPasswordConfirm'
		self.clickToChoose = 'clickToChoose'
		self.canYouGiveAReason = 'canYouGiveAReason'
		self.canYouGiveAReasonFor = 'canYouGiveAReasonFor'
		self.canYouGiveACounterArgumentWhy1 = 'canYouGiveACounterArgumentWhy1'
		self.canYouGiveACounterArgumentWhy2 = 'canYouGiveACounterArgumentWhy2'
		self.canYouGiveACounter = 'canYouGiveACounter'
		self.canYouGiveAReasonForThat = 'canYouGiveAReasonForThat'
		self.completeView = 'completeView'
		self.completeViewTitle = 'completeViewTitle'
		self.dialogView = 'dialogView'
		self.dialogViewTitle = 'dialogViewTitle'
		self.dateString = 'dateString'
		self.disagreeBecause = 'disagreeBecause'
		self.description_undermine = 'description_undermine'
		self.description_support = 'description_support'
		self.description_undercut = 'description_undercut'
		self.description_overbid = 'description_overbid'
		self.description_rebut = 'description_rebut'
		self.description_no_opinion = 'description_no_opinion'
		self.dataRemoved = 'dataRemoved'
		self.didYouMean = 'didYouMean'
		self.discussionEnd = 'discussionEnd'
		self.discussionEndText = 'discussionEndText'
		self.discussionEndFeelFreeToLogin = 'discussionEndFeelFreeToLogin'
		self.duplicateDialog = 'duplicateDialog'
		self.displayControlDialogGuidedTitle = 'displayControlDialogGuidedTitle'
		self.displayControlDialogGuidedBody = 'displayControlDialogGuidedBody'
		self.displayControlDialogIslandTitle = 'displayControlDialogIslandTitle'
		self.displayControlDialogIslandBody = 'displayControlDialogIslandBody'
		self.displayControlDialogExpertTitle = 'displayControlDialogExpertTitle'
		self.displayControlDialogExpertBody = 'displayControlDialogExpertBody'
		self.doesNotHold = 'doesNotHold'
		self.doesNotHoldBecause = 'doesNotHoldBecause'
		self.doesJustify = 'doesJustify'
		self.doesNotJustify = 'doesNotJustify'
		self.deleteTrack = 'deleteTrack'
		self.deleteHistory = 'deleteHistory'
		self.doYouWantToEnterYourStatements = 'doYouWantToEnterYourStatements'
		self.doNotHesitateToContact = 'doNotHesitateToContact'
		self.euCookiePopupTitle = 'euCookiePopupTitle'
		self.euCookiePopupText = 'euCookiePopupText'
		self.euCookiePopoupButton1 = 'euCookiePopoupButton1'
		self.euCookiePopoupButton2 = 'euCookiePopoupButton2'
		self.empty_news_input = 'empty_news_input'
		self.email = 'email'
		self.emailWasSent = 'emailWasSent'
		self.emailWasNotSent = 'emailWasNotSent'
		self.emailUnknown = 'emailUnknown'
		self.edit = 'edit'
		self.error_code = 'error_code'
		self.editTitle = 'editTitle'
		self.forText = 'forText'
		self.fillLine = 'fillLine'
		self.firstConclusionRadioButtonText = 'firstConclusionRadioButtonText'
		self.firstArgumentRadioButtonText = 'firstArgumentRadioButtonText'
		self.feelFreeToShareUrl = 'feelFreeToShareUrl'
		self.fetchLongUrl = 'fetchLongUrl'
		self.fetchShortUrl = 'fetchShortUrl'
		self.forgotPassword = 'forgotPassword'
		self.firstOneText = 'firstOneText'
		self.firstOneReason = 'firstOneReason'
		self.firstPositionText = 'firstPositionText'
		self.firstPremiseText1 = 'firstPremiseText1'
		self.firstPremiseText2 = 'firstPremiseText2'
		self.firstname = 'firstname'
		self.gender = 'gender'
		self.goStepBack = 'goStepBack'
		self.generateSecurePassword = 'generateSecurePassword'
		self.goodPointTakeMeBackButtonText = 'goodPointTakeMeBackButtonText'
		self.group_uid = 'group_uid'
		self.haveALookAt = 'haveALookAt'
		self.hidePasswordRequest = 'hidePasswordRequest'
		self.hideGenerator = 'hideGenerator'
		self.howeverIHaveMuchStrongerArgumentRejecting = 'howeverIHaveMuchStrongerArgumentRejecting'
		self.howeverIHaveEvenStrongerArgumentRejecting = 'howeverIHaveEvenStrongerArgumentRejecting'
		self.howeverIHaveMuchStrongerArgumentAccepting = 'howeverIHaveMuchStrongerArgumentAccepting'
		self.howeverIHaveEvenStrongerArgumentAccepting = 'howeverIHaveEvenStrongerArgumentAccepting'
		self.internalFailureWhileDeletingTrack = 'internalFailureWhileDeletingTrack'
		self.internalFailureWhileDeletingHistory = 'internalFailureWhileDeletingHistory'
		self.internalError = 'internalError'
		self.inputEmpty = 'inputEmpty'
		self.informationForExperts = 'informationForExperts'
		self.issueList = 'issueList'
		self.islandViewHeaderText = 'islandViewHeaderText'
		self.irrelevant = 'irrelevant'
		self.itIsTrue = 'itIsTrue'
		self.itIsFalse = 'itIsFalse'
		self.islandView = 'islandView'
		self.isFalse = 'isFalse'
		self.isTrue = 'isTrue'
		self.initialPosition = 'initialPosition'
		self.initialPositionSupport = 'initialPositionSupport'
		self.initialPositionAttack = 'initialPositionAttack'
		self.initialPositionInterest = 'initialPositionInterest'
		self.islandViewTitle = 'islandViewTitle'
		self.iAcceptCounter = 'iAcceptCounter'
		self.iAcceptArgument = 'iAcceptArgument'
		self.iAgreeWithInColor = 'iAgreeWithInColor'
		self.iAgreeWith = 'iAgreeWith'
		self.iDisagreeWithInColor = 'iDisagreeWithInColor'
		self.iDoNotKnow = 'iDoNotKnow'
		self.iDoNotKnowInColor = 'iDoNotKnowInColor'
		self.iDisagreeWith = 'iDisagreeWith'
		self.iHaveMuchStrongerArgumentRejecting = 'iHaveMuchStrongerArgumentRejecting'
		self.iHaveMuchEvenArgumentRejecting = 'iHaveMuchEvenArgumentRejecting'
		self.iHaveMuchStrongerArgumentAccepting = 'iHaveMuchStrongerArgumentAccepting'
		self.iHaveEvenStrongerArgumentAccepting = 'iHaveEvenStrongerArgumentAccepting'
		self.iNoOpinion = 'iNoOpinion'
		self.interestingOnDBAS = 'interestingOnDBAS'
		self.keyword = 'keyword'
		self.keywordStart = 'keywordStart'
		self.keywordChooseActionForStatement = 'keywordChooseActionForStatement'
		self.keywordGetPremisesForStatement = 'keywordGetPremisesForStatement'
		self.keywordMoreAboutArgument = 'keywordMoreAboutArgument'
		self.keywordReplyForPremisegroup = 'keywordReplyForPremisegroup'
		self.keywordReplyForResponseOfConfrontation = 'keywordReplyForResponseOfConfrontation'
		self.keywordReplyForArgument = 'keywordReplyForArgument'
		self.keepSetting = 'keepSetting'
		self.hideAllUsers = 'hideAllUsers'
		self.hideAllAttacks = 'hideAllAttacks'
		self.letMeExplain = 'letMeExplain'
		self.levenshteinDistance = 'levenshteinDistance'
		self.languageCouldNotBeSwitched = 'languageCouldNotBeSwitched'
		self.last_action = 'last_action'
		self.last_login = 'last_login'
		self.logfile = 'logfile'
		self.letsGo = 'letsGo'
		self.medium = 'medium'
		self.newPremisesRadioButtonText = 'newPremisesRadioButtonText'
		self.newPremisesRadioButtonTextAsFirstOne = 'newPremisesRadioButtonTextAsFirstOne'
		self.newStatementsRadioButtonTextAsFirstOne = 'newStatementsRadioButtonTextAsFirstOne'
		self.newPremiseRadioButtonText = 'newPremiseRadioButtonText'
		self.newPremiseRadioButtonTextAsFirstOne = 'newPremiseRadioButtonTextAsFirstOne'
		self.newStatementRadioButtonTextAsFirstOne = 'newStatementRadioButtonTextAsFirstOne'
		self.newConclusionRadioButtonText = 'newConclusionRadioButtonText'
		self.nickname = 'nickname'
		self.noIslandView = 'noIslandView'
		self.noCorrections = 'noCorrections'
		self.noDecisionDone = 'noDecisionDone'
		self.noCorrectionsSet = 'noCorrectionsSet'
		self.notInsertedErrorBecauseEmpty = 'notInsertedErrorBecauseEmpty'
		self.notInsertedErrorBecauseDuplicate = 'notInsertedErrorBecauseDuplicate'
		self.notInsertedErrorBecauseUnknown = 'notInsertedErrorBecauseUnknown'
		self.notInsertedErrorBecauseInternal = 'notInsertedErrorBecauseInternal'
		self.noEntries = 'noEntries'
		self.noTrackedData = 'noTrackedData'
		self.number = 'number'
		self.note = 'note'
		self.no_entry = 'no_entry'
		self.otherParticipantsThinkThat = 'otherParticipantsThinkThat'
		self.otherParticipantsDontHaveCounter = 'otherParticipantsDontHaveCounter'
		self.otherParticipantsDontHaveOpinion = 'otherParticipantsDontHaveOpinion'
		self.otherParticipantsDontHaveArgument = 'otherParticipantsDontHaveArgument'
		self.otherParticipantsAcceptBut = 'otherParticipantsAcceptBut'
		self.otherParticipantAgree = 'otherParticipantAgree'
		self.otherParticipantDisagree = 'otherParticipantDisagree'
		self.otherUsersClaimStrongerArgumentRejecting = 'otherUsersClaimStrongerArgumentRejecting'
		self.otherUsersClaimStrongerArgumentAccepting = 'otherUsersClaimStrongerArgumentAccepting'
		self.opinionBarometer = 'opinionBarometer'
		self.premiseGroup = 'premiseGroup'
		self.passwordSubmit = 'passwordSubmit'
		self.report = 'report'
		self.reportTitle = 'reportTitle'
		self.registered = 'registered'
		self.right = 'right'
		self.requestTrack = 'requestTrack'
		self.refreshTrack = 'refreshTrack'
		self.requestHistory = 'requestHistory'
		self.refreshHistory = 'refreshHistory'
		self.requestFailed = 'requestFailed'
		self.restartDiscussion = 'restartDiscussion'
		self.restartDiscussionTitle = 'restartDiscussionTitle'
		self.restartOnError = 'restartOnError'
		self.selectStatement = 'selectStatement'
		self.showAllUsers = 'showAllUsers'
		self.showAllAttacks = 'showAllAttacks'
		self.showAllAttacksTitle = 'showAllAttacksTitle'
		self.showAllUsersTitle = 'showAllUsersTitle'
		self.strength = 'strength'
		self.strong = 'strong'
		self.strongerStatementForRecjecting = 'strongerStatementForRecjecting'
		self.soYourOpinionIsThat = 'soYourOpinionIsThat'
		self.soYouWantToArgueAgainst = 'soYouWantToArgueAgainst'
		self.shortenedBy = 'shortenedBy'
		self.switchDiscussion = 'switchDiscussion'
		self.switchDiscussionText1 = 'switchDiscussionText1'
		self.switchDiscussionText2 = 'switchDiscussionText2'
		self.supportPosition = 'supportPosition'
		self.statement = 'statement'
		self.sureThat = 'sureThat'
		self.surname = 'surname'
		self.showMeAnArgumentFor = 'showMeAnArgumentFor'
		self.textAreaReasonHintText = 'textAreaReasonHintText'
		self.theCounterArgument = 'theCounterArgument'
		self.therefore = 'therefore'
		self.thinkWeShould = 'thinkWeShould'
		self.thisConfrontationIs = 'thisConfrontationIs'
		self.track = 'track'
		self.history = 'history'
		self.topicString = 'topicString'
		self.text = 'text'
		self.theySay = 'theySay'
		self.veryweak = 'veryweak'
		self.weak = 'weak'
		self.wrong = 'wrong'
		self.wouldYourShareArgument = 'wouldYourShareArgument'
		self.wrongURL = 'wrongURL'
		self.whatDoYouThinkAbout = 'whatDoYouThinkAbout'
		self.whatDoYouThinkAboutThat = 'whatDoYouThinkAboutThat'
		self.whyDoYouThinkThat = 'whyDoYouThinkThat'
		self.whyAreYouDisagreeing = 'whyAreYouDisagreeing'
		self.youMadeA = 'youMadeA'
		self.youMadeAn = 'youMadeAn'
		self.relation_undermine = 'relation_undermine'
		self.relation_support = 'relation_support'
		self.relation_undercut = 'relation_undercut'
		self.relation_overbid = 'relation_overbid'
		self.relation_rebut = 'relation_rebut'
		self.uid = 'uid'
		self.unfortunatelyNoMoreArgument = 'unfortunatelyNoMoreArgument'

		self.sentencesOpenersRequesting = [self.whyDoYouThinkThat]
		self.sentencesOpenersForArguments = [self.soYourOpinionIsThat]
		self.sentencesOpenersArguingWithAgreeing = [self.agreeBecause, self.therefore]
		self.sentencesOpenersArguingWithDisagreeing = [self.disagreeBecause, self.alternatively]
		self.sentencesOpenersInforming = [self.thinkWeShould, self.letMeExplain, self.sureThat]

		self.en_dict = self.setUpEnDict()
		self.de_dict = self.setUpDeDict()

	def setUpEnDict(self):
		"""

		:return: dictionary for the english language
		"""
		en_lang = {}
		en_lang[self.attack]                       = 'You disagreed with'
		en_lang[self.support]                      = 'You agreed with'
		en_lang[self.premise]                      = 'Premise'
		en_lang[self.because]                      = 'because'
		en_lang[self.doesNotHoldBecause]           = 'does not hold because'
		en_lang[self.moreAbout]                    = 'More about'
		en_lang[self.undermine1]                   = 'It is false that'
		en_lang[self.undermine2]                   = ''
		en_lang[self.support1]                     = ''
		en_lang[self.support2]                     = ''
		en_lang[self.undercut1]                    = 'It is false that'
		en_lang[self.undercut2]                    = 'and this is no good counter-argument'
		en_lang[self.overbid1]                     = 'It is false that'
		en_lang[self.overbid2]                     = 'and this is a good counter-argument'
		en_lang[self.rebut1]                       = 'It is right that'
		en_lang[self.rebut2]                       = ', but I have a better statement'
		en_lang[self.oldPwdEmpty]                  = 'Old password field is empty.'
		en_lang[self.newPwdEmtpy]                  = 'New password field is empty.'
		en_lang[self.confPwdEmpty]                 = 'Password confirmation field is empty.'
		en_lang[self.newPwdNotEqual]               = 'New passwords are not equal'
		en_lang[self.pwdsSame]                     = 'New and old password are the same'
		en_lang[self.oldPwdWrong]                  = 'Your old password is wrong.'
		en_lang[self.pwdChanged]                   = 'Your password was changed'
		en_lang[self.emptyName]                    = 'Your name is empty!'
		en_lang[self.emptyEmail]                   = 'Your e-mail is empty!'
		en_lang[self.emtpyContent]                 = 'Your content is empty!'
		en_lang[self.maliciousAntiSpam]            = 'Your anti-spam message is empty or wrong!'
		en_lang[self.nonValidCSRF]                 = 'CSRF-Token is not valid'
		en_lang[self.name]                         = 'Name'
		en_lang[self.mail]                         = 'Mail'
		en_lang[self.phone]                        = 'Phone'
		en_lang[self.message]                      = 'Message'
		en_lang[self.pwdNotEqual]                  = 'Passwords are not equal'
		en_lang[self.nickIsTaken]                  = 'Nickname is taken'
		en_lang[self.mailIsTaken]                  = 'E-Mail is taken'
		en_lang[self.mailNotValid]                 = 'E-Mail is not valid'
		en_lang[self.errorTryLateOrContant]        = 'An error occured, please try again later or contact the author'
		en_lang[self.accountWasAdded]              = 'Your account was added and you are now able to login.'
		en_lang[self.accountWasRegistered]         = 'Your account was successfully registered for this e-mail.'
		en_lang[self.accoutErrorTryLateOrContant]  = 'Your account with the nick could not be added. Please try again or contact the author.'
		en_lang[self.nicknameIs]                   = 'Your nickname is: '
		en_lang[self.newPwdIs]                     = 'Your new password is: '
		en_lang[self.dbasPwdRequest]               = 'D-BAS Password Request'
		en_lang[self.emailBodyText] = 'This is an automatically generated mail by the D-BAS System.\nFor contact please write an mail to krauthoff@cs.uni-duesseldorf.de\nThis system is part of a doctoral thesis and currently in an alpha-phase.'
		en_lang[self.emailWasSent]                 = 'E-Mail was sent.'
		en_lang[self.emailWasNotSent]              = 'E-Mail was not sent.'
		en_lang[self.antispamquestion]             = 'What is'
		en_lang[self.signs]                        = ['+','*','/','-']
		en_lang['0']                               = 'zero'
		en_lang['1']                               = 'one'
		en_lang['2']                               = 'two'
		en_lang['3']                               = 'three'
		en_lang['4']                               = 'four'
		en_lang['5']                               = 'five'
		en_lang['6']                               = 'six'
		en_lang['7']                               = 'seven'
		en_lang['8']                               = 'eight'
		en_lang['9']                               = 'nine'
		en_lang['+']                               = 'plus'
		en_lang['-']                               = 'minus'
		en_lang['*']                               = 'times'
		en_lang['/']                               = 'divided by'
		
		en_lang[self.aand] =  'and'
		en_lang[self.addedEverything] =  'Everything was added.'
		en_lang[self.alreadyInserted] =  'This is a duplicate and already there.'
		en_lang[self.addPremisesRadioButtonText] =  'Let me enter my reasons!'
		en_lang[self.addArgumentsRadioButtonText] =  'Let me enter my own statements!'
		en_lang[self.argumentContainerTextIfPremises] =  'You want to state your own reasons?'
		en_lang[self.argumentContainerTextIfArguments] =  'You want to state your own arguments?'
		en_lang[self.addPremiseRadioButtonText] =  'Let me enter my reason!'
		en_lang[self.addArgumentRadioButtonText] =  'Let me enter my own statement!'
		en_lang[self.argumentContainerTextIfPremise] =  'You want to state your own reason?'
		en_lang[self.argumentContainerTextIfArgument] =  'You want to state your own argument?'
		en_lang[self.argumentContainerTextIfConclusion] =  'What is your idea? What should we do?'
		en_lang[self.argueAgainstPositionToggleButton] = 'Or do you want to argue against a position? Please toggle this button:'
		en_lang[self.argueForPositionToggleButton] = 'Or do you want to argue for a position? Please toggle this button:'
		en_lang[self.andIDoNotBelieveCounter] =  'and I do not believe that this is a good counter-argument for'
		en_lang[self.andIDoNotBelieveArgument] =  'and I do not believe that this is a good argument for'
		en_lang[self.andTheyDoNotBelieveCounter] =  'and they do not believe that this is a good counter-argument for'
		en_lang[self.andTheyDoNotBelieveArgument] =  'and they do not believe that this is a good argument for'
		en_lang[self.alternatively] =  'Alternatively'
		en_lang[self.addArguments] =  'Add arguments'
		en_lang[self.addStatements] =  'Add statements'
		en_lang[self.addArgumentsTitle] =  'Adds new arguments'
		en_lang[self.acceptItTitle] =  'Accept it...'
		en_lang[self.acceptIt] =  'Accept it...'
		en_lang[self.asReasonFor] =  'as reason for'
		en_lang[self.argument] =  'Argument'
		en_lang[self.attackPosition] =  'attack Position'
		en_lang[self.attackedBy] =  'You were attacked by'
		en_lang[self.attackedWith] =  'You\'ve attacked with'
		en_lang[self.agreeBecause] =  'I agree because '
		en_lang[self.andIDoBelieve] =  'and I do believe that this is a good counter-argument for'
		en_lang[self.breadcrumbsStart] =  'Start'
		en_lang[self.breadcrumbsChooseActionForStatement] =  'Choose action'
		en_lang[self.breadcrumbsGetPremisesForStatement] =  'Get premisses'
		en_lang[self.breadcrumbsMoreAboutArgument] =  'More about'
		en_lang[self.breadcrumbsReplyForPremisegroup] =  'Reply for group'
		en_lang[self.breadcrumbsReplyForResponseOfConfrontation] =  'Reply for confrontation'
		en_lang[self.breadcrumbsReplyForArgument] =  'Reply for argument'
		en_lang[self.butIDoNotBelieveCounter] =  'but I do not believe that this is a good counter-argument for'
		en_lang[self.butIDoNotBelieveArgument] =  'but I do not believe that this is a good argument for'
		en_lang[self.butTheyDoNotBelieveCounter] =  'but they do not believe that this is a good counter-argument for'
		en_lang[self.butTheyDoNotBelieveArgument] =  'but they do not believe that this is a good argument for'
		en_lang[self.butOtherParticipantsDontHaveArgument] =  'but other partcipants do not have any argument for that.'
		en_lang[self.because] =  'Because'
		en_lang[self.butWhich] =  'but which one'
		en_lang[self.canYouGiveAReason] =  'Can you give a reason?'
		en_lang[self.canYouGiveAReasonFor] =  'Can you give a reason for'
		en_lang[self.canYouGiveACounter] =  'Can you give a counter-argument?'
		en_lang[self.canYouGiveACounterArgumentWhy1] =  'Can you give a counter-argument, why are you against'
		en_lang[self.canYouGiveACounterArgumentWhy2] =  '?'
		en_lang[self.canYouGiveAReasonForThat] =  'Can you give a reason for that?'
		en_lang[self.clickHereForRegistration] =  'Click <a href="" data-toggle="modal" data-target="#popup_login" title="Login">here</a> for login or registration!'
		en_lang[self.countOfArguments] =  'Count of arguments'
		en_lang[self.confirmation] =  'Confirmation'
		en_lang[self.contactSubmit] = 'Submit your Message'
		en_lang[self.confirmTranslation] =  'If you change the language, your process on this page will be lost and you have to restart the discussion!'
		en_lang[self.correctionsSet] =  'Your correction was set.'
		en_lang[self.checkFirstname] =  'Better check your first name, because the input is empty!'
		en_lang[self.checkLastname] =  'Better check your last name, because the input is empty!'
		en_lang[self.checkNickname] =  'Better check your nickname, because the input is empty!'
		en_lang[self.checkEmail] =  'Better check your email, because the input is empty!'
		en_lang[self.checkPassword] =  'Better check your password, because the input is empty!'
		en_lang[self.checkConfirmation] =  'Better check the confirmation of your password, because the input is empty!'
		en_lang[self.completeView] =  'Complete View'
		en_lang[self.completeViewTitle] =  'Shows the complete graph'
		en_lang[self.checkPasswordConfirm] =  'Better check your passwords, because they are not equal!'
		en_lang[self.clickToChoose] =  'Click to choose'
		en_lang[self.description_undermine] = 'This statement attacks the premise.'
		en_lang[self.description_support] = 'This statement supports the premise.'
		en_lang[self.description_undercut] = 'This statement attacks the justification (undercut). You do not believe that the premise justifies the conclusion.'
		en_lang[self.description_overbid] = 'This statement supports the justification (overbid). You do believe that the premise justifies the conclusion.'
		en_lang[self.description_rebut] = 'This statement is against the conclusion itstelf.'
		en_lang[self.description_no_opinion] = 'You just have no opinion regarding the confrontation or you just want to skip this.'
		en_lang[self.dateString] =  'Date'
		en_lang[self.deleteTrack] =  'Delete track'
		en_lang[self.deleteHistory] =  'Delete history'
		en_lang[self.disagreeBecause] =  'I disagree because '
		en_lang[self.dataRemoved] =  'Data was successfully removed.'
		en_lang[self.didYouMean] =  'Top10 statements, which you probably could mean:'
		en_lang[self.dialogView] =  'Dialog View'
		en_lang[self.dialogViewTitle] =  'Show the dialog View'
		en_lang[self.discussionEnd] =  'The discussion ends here.'
		en_lang[self.displayControlDialogGuidedTitle] =  'Dialog View'
		en_lang[self.displayControlDialogGuidedBody] =  'You will never see something like an argumentation map, because the systems seems to be like a dynamic and generic.'
		en_lang[self.displayControlDialogIslandTitle] =  'Island View'   
		en_lang[self.displayControlDialogIslandBody] =  'Okay, you want to see more as, but not everything. Therefore the island view will present you a list of every connected statement for an specific statement.'
		en_lang[self.displayControlDialogExpertTitle] =  'Expert View'   
		en_lang[self.displayControlDialogExpertBody] =  'So, you think you are an expert? Okay, you can have a view of the complete argumentation map'
		en_lang[self.discussionEndText] =  'You can click <a id="discussionEndStepBack" href="#">here</a> to go one step back or you can use the button above or <a id="discussionEndRestart" href="">this link</a> to restart the discussion.'
		en_lang[self.discussionEndFeelFreeToLogin] =  'The discussion ends here. If you want to proceed, please feel free to login yourself :)'
		en_lang[self.duplicateDialog] =  'This textversion is deprecated, because it was already edited to this version.\nDo you want to set this version as the current one once again?'
		en_lang[self.doesNotHold] =  'does not hold'
		en_lang[self.doesNotHoldBecause] =  'does not hold, because'
		en_lang[self.doNotHesitateToContact] =  'Do not hesitate to <strong><span style="cursor: pointer;" id="contact_on_error">contact us (click here)</span></strong>'
		en_lang[self.doesJustify] =  'does justify that'
		en_lang[self.doesNotJustify] =  'does not justify that'
		en_lang[self.doYouWantToEnterYourStatements] =  'Do you want to enter your statement(s)?'
		en_lang[self.euCookiePopupTitle] =  'This website is using cookies and Piwik.'
		en_lang[self.euCookiePopupText] =  'We use them to give you the best experience. If you continue using our website, we\'ll assume that you are happy to receive all cookies on this website and beeing tracked for academic purpose. All tracked data are saved anonymously with reduced masked IP-adresses.'
		en_lang[self.euCookiePopoupButton1] =  'Continue'
		en_lang[self.euCookiePopoupButton2] =  'Learn&nbsp;more'
		en_lang[self.empty_news_input] =  'News title or text is empty or too short!'
		en_lang[self.email] =  'E-Mail'
		en_lang[self.emailWasSent] =  'An E-Mail was sent to the given address.'
		en_lang[self.emailWasNotSent] =  'Your message could not be send due to a system error!'
		en_lang[self.emailUnknown] =  'The given e-mail address is unkown.'
		en_lang[self.error_code] =  'Error code'
		en_lang[self.edit] =  'Edit'
		en_lang[self.editTitle] =  'Editing the statements.'
		en_lang[self.forText] =  'for'
		en_lang[self.firstConclusionRadioButtonText] =  'Let me enter my idea!'
		en_lang[self.firstArgumentRadioButtonText] =  'Let me enter my own statement(s)!'
		en_lang[self.feelFreeToShareUrl] =  'Please feel free to share this url'
		en_lang[self.fetchLongUrl] =  'Fetch long url!'
		en_lang[self.fetchShortUrl] =  'Fetch short url!'
		en_lang[self.forgotPassword] =  'Forgot Password'
		en_lang[self.firstOneText] =  'You are the first one, who said: '
		en_lang[self.firstOneReason] =  'You are the first one with this argument, please give a reason.'
		en_lang[self.firstPositionText] =  'You are the first one in this discussion!<br><br>Please add your suggestion!'
		en_lang[self.firstPremiseText1] =  'You are the first one, who said that'
		en_lang[self.firstPremiseText2] =  'Please enter your reason for your statement.'
		en_lang[self.firstname] =  'Firstname'
		en_lang[self.fillLine] =  'Please, fill this this line with your report'
		en_lang[self.gender] =  'Gender'
		en_lang[self.goStepBack] =  'Go one step back'
		en_lang[self.generateSecurePassword] =  'Generate secure password'
		en_lang[self.goodPointTakeMeBackButtonText] =  'I agree, that is a good argument! Take me one step back.'
		en_lang[self.group_uid] =  'Group'
		en_lang[self.haveALookAt] =  'Hey, please have a look at '
		en_lang[self.hidePasswordRequest] =  'Hide Password Request'
		en_lang[self.hideGenerator] =  'Hide Generator'
		en_lang[self.howeverIHaveMuchStrongerArgumentRejecting] =  'However, I have a much stronger argument for rejecting that'
		en_lang[self.howeverIHaveEvenStrongerArgumentRejecting] = 'However, I have a even stronger argument for rejecting that'
		en_lang[self.howeverIHaveMuchStrongerArgumentAccepting] =  'However, I have a much stronger argument for accepting that'
		en_lang[self.howeverIHaveEvenStrongerArgumentAccepting] =  'However, I have a even stronger argument for accepting that'
		en_lang[self.iAgreeWithInColor] = 'I <span class=\'text-success\'>agree</span> with'
		en_lang[self.iAgreeWith] = 'I agree with'
		en_lang[self.iDisagreeWithInColor] = 'I <span class=\'text-danger\'>disagree</span> with'
		en_lang[self.iDisagreeWith] = 'I disagree with'
		en_lang[self.iDoNotKnow] =  'I do not know'
		en_lang[self.iDoNotKnowInColor] =  'I <span class=\'text-info\'>do not know</span>'
		en_lang[self.informationForExperts] =  'Infos for experts'
		en_lang[self.internalFailureWhileDeletingTrack] =  'Internal failure, please try again or did you have deleted your track recently?'
		en_lang[self.internalFailureWhileDeletingHistory] =  'Internal failure, please try again or did you have deleted your history recently?'
		en_lang[self.internalError] =  '<strong>Internal Error:</strong> Maybe the server is offline or your session run out.'
		en_lang[self.issueList] =  'Topics'
		en_lang[self.islandViewHeaderText] =  'These are all arguments for: '
		en_lang[self.islandView] =  'Island View'
		en_lang[self.islandViewTitle] =  'Shows the island View'
		en_lang[self.irrelevant] =  'Irrelevant'
		en_lang[self.itIsTrue] =  'it is true that'
		en_lang[self.itIsFalse] =  'it is false that'
		en_lang[self.isFalse] =  'is not a good idea'
		en_lang[self.isTrue] =  'holds'
		en_lang[self.initialPosition] = 'Initial Position'
		en_lang[self.initialPositionSupport] = 'What is your initial position you are supporting?'
		en_lang[self.initialPositionAttack] = 'What is your initial position you want to attack?'
		en_lang[self.initialPositionInterest] = 'What is the initial position you are interested in?'
		en_lang[self.iAcceptCounter] =  'and I do accept that this is a counter-argument for'
		en_lang[self.iAcceptArgument] =  'and I do accept that this is an argument for'
		en_lang[self.iHaveMuchStrongerArgumentRejecting] =  'I have a much stronger argument for rejecting that'
		en_lang[self.iHaveMuchEvenArgumentRejecting] = 'I have a even stronger argument for rejecting that'
		en_lang[self.iHaveMuchStrongerArgumentAccepting] =  'I have a much stronger argument for accepting that'
		en_lang[self.iHaveEvenStrongerArgumentAccepting] =  'I have a even stronger argument for accepting that'
		en_lang[self.iNoOpinion] =  'I have no opinion regarding'
		en_lang[self.interestingOnDBAS] =  'Interesting discussion on DBAS'
		en_lang[self.inputEmpty] =  'Input is empty!'
		en_lang[self.keyword] =  'Keyword'
		en_lang[self.keywordStart] =  'Start'
		en_lang[self.keywordChooseActionForStatement] =  'Choosing attitude'
		en_lang[self.keywordGetPremisesForStatement] =  'Getting premises'
		en_lang[self.keywordMoreAboutArgument] =  'More about'
		en_lang[self.keywordReplyForPremisegroup] =  'Reply for argument'
		en_lang[self.keywordReplyForResponseOfConfrontation] =  'Justification of'
		en_lang[self.keywordReplyForArgument] =  'Confrontation'
		en_lang[self.keepSetting] =  'Keep this'
		en_lang[self.hideAllUsers] =  'Hide all users'
		en_lang[self.hideAllAttacks] =  'Hide all attacks'
		en_lang[self.letMeExplain] =  'Let me explain it this way'
		en_lang[self.levenshteinDistance] =  'Levenshtein-Distance'
		en_lang[self.languageCouldNotBeSwitched] =  'Unfortunately, the language could not be switched'
		en_lang[self.last_action] =  'Last Action'
		en_lang[self.last_login] =  'Last Login'
		en_lang[self.logfile] =  'Logfile for'
		en_lang[self.letsGo] =  'Click here to start now!'
		en_lang[self.medium] =  'medium'
		en_lang[self.newPremisesRadioButtonText] =  'None of the above! Let me state my own reason(s)!'
		en_lang[self.newPremisesRadioButtonTextAsFirstOne] =  'Yes, let me state my own reason(s)!'
		en_lang[self.newStatementsRadioButtonTextAsFirstOne] =  'Yes, let me state my own statement(s)!'
		en_lang[self.newPremiseRadioButtonText] =  'None of the above! Let me state my own reason!'
		en_lang[self.newPremiseRadioButtonTextAsFirstOne] =  'Yes, let me state my own reason!'
		en_lang[self.newStatementRadioButtonTextAsFirstOne] =  'Yes, let me state my own statement!'
		en_lang[self.newConclusionRadioButtonText] =  'Neither of the above, I have a different idea!'
		en_lang[self.nickname] =  'Nickname'
		en_lang[self.noIslandView] =  'Could not fetch data for the island view. Sorry!'
		en_lang[self.noCorrections] =  'No corrections for the given statement.'
		en_lang[self.noCorrectionsSet] =  'Correction could not be set, because your user was not fount in the database. Are you currently logged in?'
		en_lang[self.noDecisionDone] =  'No decision was done.'
		en_lang[self.notInsertedErrorBecauseEmpty] =  'Your idea was not inserted, because your input text is empty.'
		en_lang[self.notInsertedErrorBecauseDuplicate] =  'Your idea was not inserted, because your idea is a duplicate.'
		en_lang[self.notInsertedErrorBecauseUnknown] =  'Your idea was not inserted due to an unkown error.'
		en_lang[self.notInsertedErrorBecauseInternal] =  'Your idea was not inserted due to an internal error.'
		en_lang[self.noEntries] =  'No entries'
		en_lang[self.noTrackedData] =  'No data was tracked.'
		en_lang[self.number] =  'No'
		en_lang[self.note] =  'Note'
		en_lang[self.no_entry] = 'No entry'
		en_lang[self.otherParticipantsThinkThat] =  'Other partcipants think that'
		en_lang[self.otherParticipantsDontHaveOpinion] =  'Other partcipants do not have any opinion regarding your selection.'
		en_lang[self.otherParticipantsDontHaveCounter] =  'Other partcipants do not have any counter-argument for '
		en_lang[self.otherParticipantsDontHaveArgument] =  'Other partcipants do not have any argument for '
		en_lang[self.otherParticipantsAcceptBut] =  'Other partcipants accept your argument, but'
		en_lang[self.otherParticipantAgree] =  'Other partcipants agree, that '
		en_lang[self.otherParticipantDisagree] =  'Other partcipants disagree, that '
		en_lang[self.otherUsersClaimStrongerArgumentRejecting] =  'Other users claim to have a stronger statement for rejecting'
		en_lang[self.otherUsersClaimStrongerArgumentAccepting] =  'Other users claim to have a stronger statement for accepting'
		en_lang[self.opinionBarometer] =  'Opinion Barometer'
		en_lang[self.premiseGroup] =  'PremiseGroup'
		en_lang[self.passwordSubmit] =  'Change Password'
		en_lang[self.registered] =  'Registered'
		en_lang[self.restartDiscussion] =  'Restart Discussion'
		en_lang[self.restartDiscussionTitle] =  'Restart Discussion'
		en_lang[self.restartOnError] =  'Please try to reload this page or restart the discussion when the error stays'
		en_lang[self.report] =  'Report'
		en_lang[self.reportTitle] =  'Opens the contact for reporting!'
		en_lang[self.right] =  'Right'
		en_lang[self.requestTrack] =  'Request track'
		en_lang[self.refreshTrack] =  'Refresh track'
		en_lang[self.requestHistory] =  'Request history'
		en_lang[self.refreshHistory] =  'Refresh history'
		en_lang[self.requestFailed] =  'Request failed'
		en_lang[self.selectStatement] =  'Please select a statement!'
		en_lang[self.showAllUsers] =  'Show all users'
		en_lang[self.showAllAttacks] =  'Show all attacks'
		en_lang[self.showAllAttacksTitle] =  'Show all attacks, done by users'
		en_lang[self.showAllUsersTitle] =  'Show all users, which are registered'
		en_lang[self.supportPosition] =  'support position'
		en_lang[self.strength] =  'Strength'
		en_lang[self.strong] =  'strong'
		en_lang[self.strongerStatementForRecjecting] =  'they claim to have a stronger statement for rejecting'
		en_lang[self.soYourOpinionIsThat] =  'So your opinion is that'
		en_lang[self.soYouWantToArgueAgainst] =  'So you want to counter-argue against'
		en_lang[self.shortenedBy] =  'which was shortened with'
		en_lang[self.switchDiscussion] =  'Change the discussion\'s topic'
		en_lang[self.switchDiscussionText1] =  'If you accept, you will change the topic of the discussion to'
		en_lang[self.switchDiscussionText2] =  'and the discussion will be restarted.'
		en_lang[self.statement] =  'Statement'
		en_lang[self.sureThat] =  'I\'m reasonably sure that '
		en_lang[self.surname] =  'Surname'
		en_lang[self.showMeAnArgumentFor] =  'Show me an argument for'
		en_lang[self.textAreaReasonHintText] =  'Please use a new textarea for every reason, write short and clear!'
		en_lang[self.theCounterArgument] =  'the counter-argument'
		en_lang[self.therefore] =  'Therefore'
		en_lang[self.thinkWeShould] =  'I think we should '
		en_lang[self.track] =  'Track'
		en_lang[self.history] =  'History'
		en_lang[self.topicString] =  'Topic'
		en_lang[self.text] =  'Text'
		en_lang[self.theySay] =  'They say'
		en_lang[self.thisConfrontationIs] =  'This confrontation is a'
		en_lang[self.veryweak] =  'very weak'
		en_lang[self.weak] =  'weak'
		en_lang[self.wrong] =  'Wrong'
		en_lang[self.wouldYourShareArgument] =  'Would you share your argument?'
		en_lang[self.whatDoYouThinkAbout] =  'What do you think about'
		en_lang[self.whatDoYouThinkAboutThat] =  'What do you think about that'
		en_lang[self.whyDoYouThinkThat] =  'Why do you think that'
		en_lang[self.wrongURL] =  'Your URL seems to be wrong.'
		en_lang[self.whyAreYouDisagreeing] =  'Why are you disagreeing with that?'
		en_lang[self.youMadeA] =  'You made a'
		en_lang[self.youMadeAn] =  'You made an'
		en_lang[self.relation_undermine] =  'is a counter-argument for'
		en_lang[self.relation_support] =  'is a reason for'
		en_lang[self.relation_undercut] =  'is a counter-argument for'
		en_lang[self.relation_overbid] =  'is a reason for'
		en_lang[self.relation_rebut] =  'is a counter-argument for'
		en_lang[self.uid] =  'ID'
		en_lang[self.unfortunatelyNoMoreArgument] =  'Unfortunately there are no more arguments about'

		logger('Translator', 'setUpEnDict', 'length ' + str(len(en_lang)))
		return en_lang

	def setUpDeDict(self):
		"""

		:return: dictionary for the german language
		"""
		de_lang = {}
		de_lang[self.attack]                       = 'Sie lehnen ab, dass'
		de_lang[self.support]                      = 'Sie akzeptieren'
		de_lang[self.premise]                      = 'Prämisse'
		de_lang[self.because]                      = 'weil'
		de_lang[self.doesNotHoldBecause]           = 'gilt nicht, weil'
		de_lang[self.moreAbout]                    = 'Mehr über'
		de_lang[self.undermine1]                   = 'Es ist falsch, dass'
		de_lang[self.undermine2]                   = ''
		de_lang[self.support1]                     = 'Es ist richtig, dass'
		de_lang[self.support2]                     = ''
		de_lang[self.undercut1]                    = 'Es ist falsch, dass'
		de_lang[self.undercut2]                    = 'und das ist ein schlechter Konter'
		de_lang[self.overbid1]                     = 'Es ist falsch, dass'
		de_lang[self.overbid2]                     = 'und das ist ein guter Konter'
		de_lang[self.rebut1]                       = 'Es ist richtig, dass'
		de_lang[self.rebut2]                       = ', aber ich habe etwas besseres'
		de_lang[self.oldPwdEmpty]                  = 'Altes Passwortfeld ist leer.'
		de_lang[self.newPwdEmtpy]                  = 'Neues Passwortfeld ist leer.'
		de_lang[self.confPwdEmpty]                 = 'Bestätigungs-Passwordfeld ist leer.'
		de_lang[self.newPwdNotEqual]               = 'Password und Bestätigung stimmen nicht überein.'
		de_lang[self.pwdsSame]                     = 'Altes und neues Passwort sind identisch.'
		de_lang[self.oldPwdWrong]                  = 'Ihr altes Passwort ist falsch.'
		de_lang[self.pwdChanged]                   = 'Ihr Passwort würde geändert.'
		de_lang[self.emptyName]                    = 'Ihr Name ist leer!'
		de_lang[self.emptyEmail]                   = 'Ihre E-Mail ist leer!'
		de_lang[self.emtpyContent]                 = 'Ihr Inhalt ist leer!'
		de_lang[self.maliciousAntiSpam]            = 'Ihr Anti-Spam-Nachricht ist leer oder falsch!'
		de_lang[self.nonValidCSRF]                 = 'CSRF-Token ist nicht valide'
		de_lang[self.name]                         = 'Name'
		de_lang[self.mail]                         = 'Mail'
		de_lang[self.phone]                        = 'Telefon'
		de_lang[self.message]                      = 'Nachricht'
		de_lang[self.pwdNotEqual]                  = 'Passwörter sind nicht gleich.'
		de_lang[self.nickIsTaken]                  = 'Nickname ist schon vergeben.'
		de_lang[self.mailIsTaken]                  = 'E-Mail ist schon vergeben.'
		de_lang[self.mailNotValid]                 = 'E-Mail ist nicht gültig.'
		de_lang[self.errorTryLateOrContant]        = 'Leider ist ein Fehler aufgetreten, bitte versuchen Sie später erneut oder kontaktieren Sie uns.'
		de_lang[self.accountWasAdded]              = 'Ihr Account wurde angelegt. Sie können sich nun anmelden.'
		de_lang[self.accountWasRegistered]         = 'Ihr Account wurde erfolgreich für die genannte E-Mail registiert.'
		de_lang[self.accoutErrorTryLateOrContant]  = 'Ihr Account konnte nicht angelegt werden, bitte versuchen Sie später erneut oder kontaktieren Sie uns.'
		de_lang[self.nicknameIs]                   = 'Ihr Nickname lautet: '
		de_lang[self.newPwdIs]                     = 'Ihr Passwort lautet: '
		de_lang[self.dbasPwdRequest]               = 'D-BAS Passwort Nachfrage'
		de_lang[self.emailBodyText]                = 'Dies ist eine automatisch generierte E-Mail von D-BAS.\nFür Kontakt können Sie gerne eine E-Mail an krauthoff@cs.uni-duesseldorf.de verfassen.\nDieses System ist Teil einer Promotion und noch in der Testphase.'
		de_lang[self.emailWasSent]                 = 'E-Mail wurde gesendet.'
		de_lang[self.emailWasNotSent]              = 'E-Mail wurde nicht gesendet.'
		de_lang[self.antispamquestion]             = 'Was ist'
		de_lang[self.signs]                        = ['+','*','/','-']
		de_lang['0']                               = 'null'
		de_lang['1']                               = 'eins'
		de_lang['2']                               = 'zwei'
		de_lang['3']                               = 'drei'
		de_lang['4']                               = 'vier'
		de_lang['5']                               = 'fünf'
		de_lang['6']                               = 'sechs'
		de_lang['7']                               = 'sieben'
		de_lang['8']                               = 'acht'
		de_lang['9']                               = 'neun'
		de_lang['+']                               = 'plus'
		de_lang['-']                               = 'minus'
		de_lang['*']                               = 'mal'
		de_lang['/']                               = 'durch'


		de_lang[self.aand] = 'und',
		de_lang[self.addedEverything] = 'Alles wurde hinzugefügt.',
		de_lang[self.alreadyInserted] = 'Dies ist ein Duplikat und schon vorhanden.',
		de_lang[self.addPremisesRadioButtonText] = 'Lass\' mich meine eigenen Gründe angeben!',
		de_lang[self.addArgumentsRadioButtonText] = 'Lass\' mich meine eigenen Aussagen angeben!',
		de_lang[self.argumentContainerTextIfPremises] = 'Sie möchten Ihre eigenen Gründe angeben?',
		de_lang[self.argumentContainerTextIfArguments] = 'Sie möchten Ihre eigenen Argumente angeben?',
		de_lang[self.addPremiseRadioButtonText] = 'Lass\' mich meinen eigenen Grund angeben!',
		de_lang[self.addArgumentRadioButtonText] = 'Lass\' mich meine eigene Aussage angeben!',
		de_lang[self.argumentContainerTextIfPremise] = 'Sie möchten Ihren eigenen Grund angeben?',
		de_lang[self.argumentContainerTextIfArgument] = 'Sie möchten Ihr eigenes Argument angeben?',
		de_lang[self.argumentContainerTextIfConclusion] = 'Was ist Ihre Idee? Was sollten wir unternehmen?',
		de_lang[self.argueAgainstPositionToggleButton] =  'Oder wenn Sie gegen eine Position argumentieren möchten, drücken Sie bitte diesen Schalter:',
		de_lang[self.argueForPositionToggleButton] =  'Oder wenn Sie für eine Position argumentieren möchten, drücken Sie bitte diesen Schalter:',
		de_lang[self.alternatively] = 'Alternativ',
		de_lang[self.argument] = 'Argument',
		de_lang[self.andIDoNotBelieveCounter] = 'und ich glaube, dass ist kein gutes Gegenargument für',
		de_lang[self.andIDoNotBelieveArgument] = 'und ich glaube, dass ist kein gutes Argument für',
		de_lang[self.andTheyDoNotBelieveCounter] = 'und sie glauben, dass ist kein gutes Gegenargument für',
		de_lang[self.andTheyDoNotBelieveArgument] = 'und sie glauben, dass ist kein gutes Argument für',
		de_lang[self.asReasonFor] = 'als einen Grund für',
		de_lang[self.attackedBy] = 'Sie wurden attackiert mit',
		de_lang[self.attackedWith] = 'Sie haben attackiert mit',
		de_lang[self.attackPosition] = 'Position angreifen',
		de_lang[self.agreeBecause] = 'Ich stimme zu, weil ',
		de_lang[self.andIDoBelieve] = 'und ich glaube, dass ist ein gutes Gegenargument für',
		de_lang[self.addArguments] = 'Argumente hizufügen',
		de_lang[self.addStatements] = 'Aussagen hizufügen',
		de_lang[self.addArgumentsTitle] = 'Fügt neue Argumente hinzu',
		de_lang[self.acceptItTitle] = 'Einsenden...',
		de_lang[self.acceptIt] = 'Eintragen...',
		de_lang[self.breadcrumbsStart] = 'Start',
		de_lang[self.breadcrumbsChooseActionForStatement] = 'Aktion wählen',
		de_lang[self.breadcrumbsGetPremisesForStatement] = 'Prämissen',
		de_lang[self.breadcrumbsMoreAboutArgument] = 'mehr Über',
		de_lang[self.breadcrumbsReplyForPremisegroup] = 'Antwort für Gruppe',
		de_lang[self.breadcrumbsReplyForResponseOfConfrontation] = 'Antwort für die Konfrontation',
		de_lang[self.breadcrumbsReplyForArgument] = 'Antwort fürs Argument',
		de_lang[self.butOtherParticipantsDontHaveArgument] = 'aber andere Teilnehmer haben keine begründung für dafür',
		de_lang[self.butIDoNotBelieveCounter] = 'aber ich glaube, dass ist kein gutes Gegenargument für',
		de_lang[self.butIDoNotBelieveArgument] = 'aber ich glaube, dass ist kein gutes Argument für',
		de_lang[self.butTheyDoNotBelieveCounter] = 'aber sie glauben, dass ist kein gutes Gegenargument für',
		de_lang[self.butTheyDoNotBelieveArgument] = 'aber sie glauben, dass ist kein gutes Argument für',
		de_lang[self.because] = 'Weil',
		de_lang[self.butWhich] = 'aber welches',
		de_lang[self.clickHereForRegistration] = 'Klick <a href="" data-toggle="modal" data-target="#popup_login" title="Login">hier</a> für die Anmeldung oder eine Registrierung!',
		de_lang[self.confirmation] = 'Bestätigung',
		de_lang[self.contactSubmit] =  'Absenden der Nachricht',
		de_lang[self.confirmTranslation] = 'Wenn Sie die Sprache ändern, geht Ihr aktueller Fortschritt verloren!',
		de_lang[self.correctionsSet] = 'Ihre Korrektur wurde gesetzt.',
		de_lang[self.countOfArguments] = 'Anzahl der Argumente',
		de_lang[self.checkFirstname] = 'Bitte überprüfen Sie Ihren Vornamen, da die Eingabe leer ist!',
		de_lang[self.checkLastname] = 'Bitte überprüfen Sie Ihren Nachnamen, da die Eingabe leer ist!',
		de_lang[self.checkNickname] = 'Bitte überprüfen Sie Ihren Spitznamen, da die Eingabe leer ist!',
		de_lang[self.checkEmail] = 'Bitte überprüfen Sie Ihre E-Mail, da die Eingabe leer ist!',
		de_lang[self.checkPassword] = 'Bitte überprüfen Sie Ihre Passwort, da die Eingabe leer ist!',
		de_lang[self.checkConfirmation] = 'Bitte überprüfen Sie Ihre Passwort-Bestätigung, da die Eingabe leer ist!',
		de_lang[self.checkPasswordConfirm] = 'Bitte überprüfen Sie Ihre Passwörter, da die Passwärter nicht gleich sind!',
		de_lang[self.clickToChoose] = 'Klicken zum wählen',
		de_lang[self.canYouGiveAReason] = 'Können Sie einen Grund angeben?',
		de_lang[self.canYouGiveAReasonFor] = 'Können Sie einen Grund für folgendes angeben:',
		de_lang[self.canYouGiveACounterArgumentWhy1] = 'Können Sie begründen, wie so sie gegen',
		de_lang[self.canYouGiveACounterArgumentWhy2] = 'sind?',
		de_lang[self.canYouGiveACounter] = 'Können Sie einen Grund dagegen angeben?',
		de_lang[self.canYouGiveAReasonForThat] = 'Können Sie dafür einen Grund angeben?',
		de_lang[self.completeView] = 'Komplette View',
		de_lang[self.completeViewTitle] = 'Kompletten Graphen anzeigen',
		de_lang[self.dialogView] = 'Dialog-Ansicht',
		de_lang[self.dialogViewTitle] = 'Dialog-Ansicht',
		de_lang[self.dateString] = 'Datum',
		de_lang[self.disagreeBecause] = 'Ich widerspreche, weil ',
		de_lang[self.description_undermine] =  'Diese Aussage ist gegen die Prämisse.',
		de_lang[self.description_support] =  'Diese Aussage ist für die Prämisse.',
		de_lang[self.description_undercut] =  'Diese Aussage ist gegen die Begründung (undercut). Sie glauben nicht, dass aus der Prämisse die Konklusion folgt.',
		de_lang[self.description_overbid] =  'Diese Aussage ist für die Begründung (overbid). Sie glauben nicht, dass aus der Prämisse die Konklusion folgt.',
		de_lang[self.description_rebut] =  'Diese Aussage ist gegen die Konklusion.',
		de_lang[self.description_no_opinion] =  'Sie haben keine Meinung odeWas ist Ihre Meinung?r möchten diesen Punkt nur überpringen.',
		de_lang[self.dataRemoved] = 'Daten wurden erfolgreich gelöscht.',
		de_lang[self.didYouMean] = 'Top 10 der Aussagen, die Sie eventuell meinten:',
		de_lang[self.discussionEnd] = 'Die Diskussion endet hier.',
		de_lang[self.discussionEndText] = 'Sie können <a id="discussionEndStepBack" href="#">hier</a> klicken, um einen Schritt zurück zugehen oder den oberen Button bzw. <a href="" id="discussionEndRestart">diesen Link</a> nutzen, um die Diskussion neu zustarten.',
		de_lang[self.discussionEndFeelFreeToLogin] = 'Die Diskussion endet hier. Wenn Sie weiter machen möchten, melden Sie sich bitte an :)',
		de_lang[self.duplicateDialog] = 'Diese Textversion ist veraltet, weil Sie schon editiert wurde.\nMöchten Sie diese Version dennoch als die aktuellste markieren?',
		de_lang[self.displayControlDialogGuidedTitle] = 'geführte Ansicht',
		de_lang[self.displayControlDialogGuidedBody] = 'Du wirst nie etwas wie eine Argumentationskarte sehen, da das System dich führt. Das System ist daher dynamisch und generisch für dich.',
		de_lang[self.displayControlDialogIslandTitle] = 'Insel-Ansicht',
		de_lang[self.displayControlDialogIslandBody] = 'Okay, Sie möchten mehr sehen, aber nicht alles? Genau dafür haben wie eine Insel-Ansicht als weitere Modus. Mit dieser Möglichkeit sehen Sie alle Aussagen, die mit Ihrem aktuellen Standpunkt verbunden sind.',
		de_lang[self.displayControlDialogExpertTitle] = 'Expernten-Ansicht',
		de_lang[self.displayControlDialogExpertBody] = 'Du bist also ein Experte? Okay, dann darfst du wirklich alles auf einen Blick sehen.',
		de_lang[self.doesNotHold] = 'keine gute Idee ist',
		de_lang[self.doesNotHoldBecause] = 'nicht gilt, weil',
		de_lang[self.doesJustify] = 'gerechtfertigen, dass',
		de_lang[self.doesNotJustify] = 'nicht gerechtfertigen, dass',
		de_lang[self.deleteTrack] = 'Track löschen',
		de_lang[self.deleteHistory] = 'History löschen',
		de_lang[self.doYouWantToEnterYourStatements] = 'Möchten Sie Ihre eigenen Gründe angeben?',
		de_lang[self.doNotHesitateToContact] = 'Zögern Sie nicht, uns zu <strong><span style="cursor: pointer;" id="contact_on_error">kontaktieren (hier klicken)</span></strong>',
		de_lang[self.euCookiePopupTitle] = 'Diese Seite nutzt Cookies und Piwik.',
		de_lang[self.euCookiePopupText] = 'Wir benutzen Sie, um Ihnen die beste Erfahrung zu geben. Wenn Sie unsere Seite weiter nutzen, nehmen Sie alle Cookies unserer Seite an und sind glücklich damit. Zusätzlich tracken wir Ihre Aktionen und speichern diese anonym ab. Dabei wird Ihre IP-Adresse maskiert.',
		de_lang[self.euCookiePopoupButton1] = 'Weiter',
		de_lang[self.euCookiePopoupButton2] = 'Lerne&nbsp;mehr',
		de_lang[self.empty_news_input] = 'Nachrichten-Titel oder Text ist leer oder zu kurz!',
		de_lang[self.email] = 'E-Mail',
		de_lang[self.emailWasSent] = 'Eine E-Mail wurde zu der genannten Adresse gesendet.',
		de_lang[self.emailWasNotSent] = 'Ihre E-Mail konnte nicht gesendet werden!',
		de_lang[self.emailUnknown] = 'Die Adresse ist nicht gültig.',
		de_lang[self.edit] = 'Bearbeiten',
		de_lang[self.error_code] = 'Fehler-Code',
		de_lang[self.editTitle] = 'Aussagen bearbeiten',
		de_lang[self.forText] = 'für',
		de_lang[self.fillLine] = 'Bitte, füllen Sie diese Zeilen mit Ihrer Meldung',
		de_lang[self.firstConclusionRadioButtonText] = 'Lass mich meine eigenen Ideen einfügen!',
		de_lang[self.firstArgumentRadioButtonText] = 'Lass mich meine eigenen Aussagen einfügen!',
		de_lang[self.feelFreeToShareUrl] = 'Bitte teilen Sie diese URL',
		de_lang[self.fetchLongUrl] = 'Hole lange URL!',
		de_lang[self.fetchShortUrl] = 'Hole kurze URL!',
		de_lang[self.forgotPassword] = 'Passwort vergessen',
		de_lang[self.firstOneText] = 'Sie sind der Erste, der sagt: ',
		de_lang[self.firstOneReason] = 'Sie sind der Erste mit diesem Argument. Bitte geben Sie Ihre Begründung an.',
		de_lang[self.firstPositionText] = 'Sie sind der Erste in dieser Diskussion!<br><br>Bitte geben Sie Ihren Vorschlag an!',
		de_lang[self.firstPremiseText1] = 'Sie sind der erste, der sagt, dass ',
		de_lang[self.firstPremiseText2] = 'Bitte begründen Sie Ihre Aussage.',
		de_lang[self.firstname] = 'Vorname',
		de_lang[self.gender] = 'Geschlecht',
		de_lang[self.goStepBack] = 'Einen Schritt zurück',
		de_lang[self.generateSecurePassword] = 'Generate secure password',
		de_lang[self.goodPointTakeMeBackButtonText] = 'Ich stimme zu, dass ist ein gutes Argument. Geh einen Schritt zurück.',
		de_lang[self.group_uid] = 'Gruppe',
		de_lang[self.haveALookAt] = 'Hey, schau dir mal das an: ',
		de_lang[self.hidePasswordRequest] = 'Verstecke die Passwort-Anfrage',
		de_lang[self.hideGenerator] = 'Verstecke Generator',
		de_lang[self.howeverIHaveMuchStrongerArgumentRejecting] = 'Jedoch habe ich ein viel stärkeres Argument zum Ablehnen von',
		de_lang[self.howeverIHaveEvenStrongerArgumentRejecting] =  'Jedoch habe ich ein stärkeres Argument zum Ablehnen von',
		de_lang[self.howeverIHaveMuchStrongerArgumentAccepting] = 'Jedoch habe ich ein viel stärkeres Argument zum Akzeptieren von',
		de_lang[self.howeverIHaveEvenStrongerArgumentAccepting] = 'Jedoch habe ich ein stärkeres Argument zum Akzeptieren von',
		de_lang[self.internalFailureWhileDeletingTrack] = 'Interner Fehler, bitte versuchen Sie es später erneut.',
		de_lang[self.internalFailureWhileDeletingHistory] = 'Interner Fehler, bitte versuchen Sie es später erneut.',
		de_lang[self.internalError] = '<strong>Interner Fehler:</strong> Wahrscheinlich ist Ihre Sitzung abgelaufen. Bitte laden Sie die Seite erneut!.',
		de_lang[self.inputEmpty] = 'Ihre Eingabe ist leer!',
		de_lang[self.informationForExperts] = 'Infos für Experten',
		de_lang[self.issueList] = 'Themen',
		de_lang[self.islandViewHeaderText] = 'Dies sind alle Argumente für: ',
		de_lang[self.irrelevant] = 'Irrelevant',
		de_lang[self.itIsTrue] = 'es ist richtig, dass',
		de_lang[self.itIsFalse] = 'es ist falsch, dass',
		de_lang[self.islandView] = 'Insel Ansicht',
		de_lang[self.isFalse] = 'falsch ist',
		de_lang[self.isTrue] = 'richtig ist',
		de_lang[self.initialPosition] = 'Anfangs-interesse',
		de_lang[self.initialPositionSupport] =  'Was ist Ihre Meinung, die Sie unterstützen?',
		de_lang[self.initialPositionAttack] =  'Was ist Ihre Meinung, di Sie angreifen möchten?',
		de_lang[self.initialPositionInterest] =  'An welcher Aussage sind Sie interessiert?',
		de_lang[self.islandViewTitle] = 'Zeigt die Insel Ansicht',
		de_lang[self.iAcceptCounter] = 'und ich akzeptiere, dass es ein Gegenargument ist, für',
		de_lang[self.iAcceptArgument] = 'und ich akzeptiere, dass es ein Argument ist, für',
		de_lang[self.iAgreeWithInColor] =  'Ich <span class=\'text-success\'>akzeptiere</span>',
		de_lang[self.iAgreeWith] =  'Ich akzeptiere die Aussage',
		de_lang[self.iDisagreeWithInColor] =  'Ich <span class=\'text-danger\'>widerspreche</span> der Aussage',
		de_lang[self.iDoNotKnow] = 'Ich weiß es nicht',
		de_lang[self.iDoNotKnowInColor] = 'Ich <span class=\'text-info\'>weiß es nicht</span>',
		de_lang[self.iDisagreeWith] =  'Ich widerspreche die Aussage',
		de_lang[self.iHaveMuchStrongerArgumentRejecting] = 'Ich habe ein viel stärkeres Argument zum Ablehnen von',
		de_lang[self.iHaveMuchEvenArgumentRejecting] =  'Ich habe ein stärkeres Argument zum Ablehnen von',
		de_lang[self.iHaveMuchStrongerArgumentAccepting] = 'Ich habe ein viel stärkeres Argument zum Akzeptieren von',
		de_lang[self.iHaveEvenStrongerArgumentAccepting] = 'Ich habe ein stärkeres Argument zum Akzeptieren von',
		de_lang[self.iNoOpinion] = 'Ich habe keine Meinung bezüglich',
		de_lang[self.interestingOnDBAS] = 'Interessante Diskussion in D-BAS',
		de_lang[self.keyword] = 'Schlüsselwort',
		de_lang[self.keywordStart] = 'Start',
		de_lang[self.keywordChooseActionForStatement] = 'Einstellung zu',
		de_lang[self.keywordGetPremisesForStatement] = 'Prämissen von',
		de_lang[self.keywordMoreAboutArgument] = 'Mehr über',
		de_lang[self.keywordReplyForPremisegroup] = 'Antwort auf das Argument',
		de_lang[self.keywordReplyForResponseOfConfrontation] = 'Begründung von',
		de_lang[self.keywordReplyForArgument] = 'Konfrontation',
		de_lang[self.keepSetting] = 'Entscheidung merken',
		de_lang[self.hideAllUsers] = 'Verstecke alle Benutzer',
		de_lang[self.hideAllAttacks] = 'Verstecke alle Angriffe',
		de_lang[self.letMeExplain] = 'Lass\' es mich so erklären',
		de_lang[self.levenshteinDistance] = 'Levenshtein-Distanz',
		de_lang[self.languageCouldNotBeSwitched] = 'Leider konnte die Sprache nicht gewechselt werden',
		de_lang[self.last_action] = 'Letzte Aktion',
		de_lang[self.last_login] = 'Letze Anmeldung',
		de_lang[self.logfile] = 'Logdatei für',
		de_lang[self.letsGo] = 'Wenn Sie direkt starten möchten, klicken Sie bitte hier!',
		de_lang[self.medium] = 'mittel',
		de_lang[self.newPremisesRadioButtonText] = 'Nichts von alldem. Ich habe neue Gründe!',
		de_lang[self.newPremisesRadioButtonTextAsFirstOne] = 'Ja, ich möchte neue Gründe angeben!',
		de_lang[self.newStatementsRadioButtonTextAsFirstOne] = 'Ja, ich möchte neue Aussagen angeben!',
		de_lang[self.newPremiseRadioButtonText] = 'Nichts von alldem. Ich möchte einen neuen Grund angeben!',
		de_lang[self.newPremiseRadioButtonTextAsFirstOne] = 'Ja, ich möchte einen neuen Grunde angeben!',
		de_lang[self.newStatementRadioButtonTextAsFirstOne] = 'Ja, ich möchte eine neue Aussage angeben!',
		de_lang[self.newConclusionRadioButtonText] = 'Nichts von alldem. Ich habe eine andere Idee!',
		de_lang[self.nickname] = 'Spitzname',
		de_lang[self.noIslandView] = 'Daten für die Island View konnten nicht geladen werden. Tschuldigung!',
		de_lang[self.noCorrections] = 'Keinte Korreturen für die aktuelle Aussage.',
		de_lang[self.noDecisionDone] = 'Es liegt keine Entscheidung vor.',
		de_lang[self.noCorrectionsSet] = 'Korrektur wurde nicht gespeichert, da der Benutzer unbekannt ist. Sind Sie angemeldet?',
		de_lang[self.notInsertedErrorBecauseEmpty] = 'Ihre Idee wurde nicht gespeichert, da das Feld leer ist.',
		de_lang[self.notInsertedErrorBecauseDuplicate] = 'Ihre Idee wurde nicht gespeichert, da Ihre Idee ein Duplikat ist.',
		de_lang[self.notInsertedErrorBecauseUnknown] = 'Ihre Idee wurde aufgrund eines unbekannten Fehlers nicht gespeichert.',
		de_lang[self.notInsertedErrorBecauseInternal] = 'Ihre Idee wurde aufgrund eines internen Fehlers nicht gespeichert.',
		de_lang[self.noEntries] = 'Keine Einträge vorhanden',
		de_lang[self.noTrackedData] = 'Keine Daten wurden gespeichert.',
		de_lang[self.number] = 'Nr',
		de_lang[self.note] = 'Hinweis',
		de_lang[self.no_entry] = 'Kein Eintrag'
		de_lang[self.otherParticipantsThinkThat] = 'Andere Teilnehmer denken, dass',
		de_lang[self.otherParticipantsDontHaveOpinion] = 'Andere Teilnehmer haben keine Meinung zu Ihrer Aussage.'
		de_lang[self.otherParticipantsDontHaveCounter] = 'Andere Teilnehmer haben kein Gegenargument für ',
		de_lang[self.otherParticipantsDontHaveArgument] = 'Andere Teilnehmer haben kein Argument für ',
		de_lang[self.otherParticipantsAcceptBut] = 'Andere Teilnehmer akzeptieren Ihr Argument, aber',
		de_lang[self.otherParticipantAgree] = 'Andere Teilnehmer stimmen zu, dass ',
		de_lang[self.otherParticipantDisagree] = 'Andere Teilnehmer widersprechen, dass ',
		de_lang[self.otherUsersClaimStrongerArgumentRejecting] = 'Andere Teilnehmer haben eine stärkere Aussage zur Ablehnung von',
		de_lang[self.otherUsersClaimStrongerArgumentAccepting] = 'Andere Teilnehmer haben eine stärkere Aussage zur Annahme von',
		de_lang[self.opinionBarometer] = 'Meinungsbarometer',
		de_lang[self.premiseGroup] = 'Gruppe von Voraussetzung(en)',
		de_lang[self.passwordSubmit] = 'Passwort ändern',
		de_lang[self.report] = 'Melden',
		de_lang[self.reportTitle] = 'Öffnet die Kontaktseite, damit etwas gemeldet werden kann.',
		de_lang[self.registered] = 'Registriert',
		de_lang[self.right] = 'Wahr',
		de_lang[self.requestTrack] = 'Track anfragen',
		de_lang[self.refreshTrack] = 'Track neuladen',
		de_lang[self.requestHistory] = 'History anfragen',
		de_lang[self.refreshHistory] = 'History neuladen',
		de_lang[self.requestFailed] = 'Anfrage fehlgeschlagen',
		de_lang[self.restartDiscussion] = 'Diskussion neustarten',
		de_lang[self.restartDiscussionTitle] = 'Diskussion neustarten',
		de_lang[self.restartOnError] = 'Bitte laden Sie die Seite erneut oder starten Sie die Diskussion neu, sofern der Fehler bleibt.',
		de_lang[self.selectStatement] = 'Bitte Wählen Sie eine Aussage!',
		de_lang[self.showAllUsers] = 'Zeig\' alle Benutzer',
		de_lang[self.showAllAttacks] = 'Zeig\' alle Angriffe',
		de_lang[self.showAllAttacksTitle] = 'Zeige alle Attacken',
		de_lang[self.showAllUsersTitle] = 'Zeige alle Nutzer',
		de_lang[self.strength] = 'Stärke',
		de_lang[self.strong] = 'stark',
		de_lang[self.strongerStatementForRecjecting] = 'Sie haben eine stärkere Aussage zur Ablehnung von',
		de_lang[self.soYourOpinionIsThat] = 'Ihre Meinung ist, dass',
		de_lang[self.soYouWantToArgueAgainst] = 'Sie möchten ein Gegenargument bringen für',
		de_lang[self.shortenedBy] = 'welche gekürzt wurde mit',
		de_lang[self.switchDiscussion] = 'Diskussionsthema ändern',
		de_lang[self.switchDiscussionText1] = 'Wenn Sie akzeptieren, wird das Diskussionsthema gewechselt zu',
		de_lang[self.switchDiscussionText2] = 'und die Diskussion neugestartet.',
		de_lang[self.supportPosition] = 'Position unterstützen',
		de_lang[self.statement] = 'Aussage',
		de_lang[self.sureThat] = 'Ich bin sehr sicher, dass ',
		de_lang[self.surname] = 'Nachname',
		de_lang[self.showMeAnArgumentFor] = 'Zeig\' mir ein Argument für',
		de_lang[self.textAreaReasonHintText] = 'Bitte nutzen Sie ein Feld für jeden Grund. Schreiben Sie kurz und prägnant!',
		de_lang[self.theCounterArgument] = 'dem Gegenargument',
		de_lang[self.therefore] = 'Daher',
		de_lang[self.thinkWeShould] = 'Ich denke, wir sollten ',
		de_lang[self.thisConfrontationIs] = 'Dieser Angriff ist ein',
		de_lang[self.track] = 'Spur',
		de_lang[self.history] = 'Geschichte',
		de_lang[self.topicString] = 'Thema',
		de_lang[self.text] = 'Text',
		de_lang[self.theySay] = 'Sie sagen',
		de_lang[self.veryweak] = 'sehr schwach',
		de_lang[self.weak] = 'schwach',
		de_lang[self.wrong] = 'Nein',
		de_lang[self.wouldYourShareArgument] = 'Können Sie einen Grund angeben?',
		de_lang[self.wrongURL] = 'Ihre URL scheint falsch zu sein.',
		de_lang[self.whatDoYouThinkAbout] = 'Was halten Sie von',
		de_lang[self.whatDoYouThinkAboutThat] = 'Was halten Sie davon, dass',
		de_lang[self.whyDoYouThinkThat] = 'Wieso denken Sie, dass',
		de_lang[self.whyAreYouDisagreeing] = 'Warum sind Sie anderer Meinung?',
		de_lang[self.youMadeA] = 'Sie machten ein/e',
		de_lang[self.youMadeAn] = 'Sie machten ein/e',
		de_lang[self.relation_undermine] = 'ist ein Gegenargument für',
		de_lang[self.relation_support] = 'ist ein Argument für',
		de_lang[self.relation_undercut] = 'ist ein Gegenargument für',
		de_lang[self.relation_overbid] = 'ist ein Argument für',
		de_lang[self.relation_rebut] = 'ist ein Gegenargument für',
		de_lang[self.uid] = 'ID',
		de_lang[self.unfortunatelyNoMoreArgument] = 'Leider gibt es keine weiteren Argumente für'


		logger('Translator', 'setUpDeDict', 'length ' + str(len(de_lang)))
		return de_lang

	def get(self, id):
		"""
		Returns an localized string
		:param id: string identifier
		:return: string
		"""
		#logger('Translator', 'get', 'id: ' + id + ', lang: ' + self.lang)
		if self.lang == 'de' and id in self.de_dict:
		#	logger('Translator', 'get', 'return de: ' + str(self.de_dict[id]))
			return self.de_dict[id]

		elif self.lang == 'en' and id in self.en_dict:
		#	logger('Translator', 'get', 'return en: ' + str(self.en_dict[id]))
			return self.en_dict[id]

		elif self.lang == 'de' and id not in self.de_dict:
		#	logger('Translator', 'get', 'unknown id for german dict')
			return 'unbekannter identifier im deutschen Wörterbuch'

		elif self.lang == 'en' and id not in self.en_dict:
		#	logger('Translator', 'get', 'unknown id for englisch dict')
			return 'unknown identifier in the englisch dictionary'

		else:
		#	logger('Translator', 'get', 'unknown lang')
			return 'unknown language: ' + self.lang

class TextGenerator(object):

	def __init__(self, lang):
		"""

		:param lang: current language
		:return:
		"""
		self.lang = lang

	def get_text_for_add_premise_container(self, confrontation, premise, attackType, conclusion, isSupportive):
		"""
		Based on the users reaction, text will be build.
		:param confrontation: choosen confrontation
		:param premise: current premise
		:param attackType: type of the attack
		:param conclusion: current conclusion
		:param startLowerCase: boolean
		:param isSupportive: boolean
		:return: string
		"""
		_t = Translator(self.lang)

		if premise[-1] == '.':
			premise = premise[:-1]

		if conclusion[-1] == '.':
			conclusion = premise[:-1]

		#longConclusion = ''
		#if attackType == 'overbid':
		#	if (isSupportive):
		#		longConclusion = conclusion + ', ' + _t.get(_t.because).lower() + ' ' + premise
		#	else:
		#		longConclusion = premise + ', ' + _t.get(_t.doesNotJustify).lower() + ' ' + conclusion

		# different cases
		ret_text = ''
		if attackType == 'undermine':
			ret_text = _t.get(_t.itIsFalse) + ' ' + confrontation + '.'
		if attackType == 'support':
			ret_text = _t.get(_t.itIsTrue) + ' ' + confrontation + '.'
		if attackType == 'undercut':
			ret_text = confrontation + ', ' + _t.get(_t.butIDoNotBelieveCounter) + ' ' + conclusion + '.'
		if attackType == 'overbid':
			ret_text = confrontation + ', ' + _t.get(_t.andIDoBelieve) + ' ' + conclusion
			           #+ '.<br><br>' + _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) + ' ' + longConclusion + '.'
		if attackType == 'rebut':
			ret_text = confrontation + ' ' + _t.get(_t.iAcceptCounter) + ' ' + conclusion# + '.<br><br>'
			# if isSupportive:
			# 	ret_text += _t.get(_t.howeverIHaveMuchStrongerArgumentAccepting) + ' ' + conclusion + '.'
			# else:
			# 	ret_text += _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting) + ' ' + conclusion + '.'

		return ret_text

	def get_header_for_confrontation_response(self, confrontation, premise, attackType, conclusion, startLowerCase, isSupportive, user):
		"""
		Based on the users reaction, text will be build.
		:param confrontation: choosen confrontation
		:param premise: current premise
		:param attackType: type of the attack
		:param conclusion: current conclusion
		:param startLowerCase: boolean
		:param isSupportive: boolean
		:param user: nickname
		:return: string
		"""
		_t = Translator(self.lang)
		ret_text = _t.get(_t.sentencesOpenersForArguments[0])  + ': '

		if premise[-1] == '.':
			premise = premise[:-1]

		if conclusion[-1] == '.':
			conclusion = premise[:-1]

		longConclusion = ''
		if attackType == 'overbid':
			if (isSupportive):
				longConclusion = conclusion + ', ' + _t.get(_t.because).lower() + ' ' + premise
			else:
				longConclusion = premise + ', ' + _t.get(_t.doesNotJustify).lower() + ' ' + conclusion

		# pretty print
		w = (_t.get(_t.wrong)[0:1].lower() if startLowerCase else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:] + ', '
		r = (_t.get(_t.right)[0:1].lower() if startLowerCase else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:] + ', '

		# different cases
		if attackType == 'undermine':
			ret_text += w + _t.get(_t.itIsFalse) + ' <strong>' + confrontation + '</strong>.'
		if attackType == 'support':
			ret_text += r + _t.get(_t.itIsTrue) + ' <strong>' + confrontation + '</strong>.'
		if attackType == 'undercut':
			ret_text += r + '<strong>' + confrontation + '</strong>, ' + _t.get(_t.butIDoNotBelieveCounter) + ' <strong>' \
			           + conclusion + '</strong>.'
		if attackType == 'overbid':
			ret_text += r + '<strong>' + confrontation + '</strong>, ' + _t.get(_t.andIDoBelieve) + ' <strong>' \
			           + conclusion + '</strong>.<br><br>' + _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) \
			           + ' <strong>' + longConclusion + '</strong>.'
		if attackType == 'rebut':
			ret_text += r + '<strong>' + confrontation + '</strong> ' + _t.get(_t.iAcceptCounter) + ' <strong>' \
			           + conclusion + '</strong>.<br><br>'
			if isSupportive:
				ret_text += _t.get(_t.howeverIHaveMuchStrongerArgumentAccepting) + ' <strong>' + conclusion + '</strong>.'
			else:
				ret_text += _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting) + ' <strong>' + conclusion + '</strong>.'


		# is logged in?
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if db_user:
			ret_text += '<br><br>' + _t.get(_t.canYouGiveAReasonForThat)

		return ret_text

	def get_confrontation_relation_text_dict(self, confrontation, conclusion, premise, startLowerCase, isSupportive):
		"""

		:param confrontation:
		:param conclusion:
		:param premise:
		:param startLowerCase:
		:param isSupportive:
		:param lang:
		:return:
		"""
		_t = Translator(self.lang)
		ret_dict = dict()

		if isSupportive:
			counterJusti = ' <strong>' + conclusion + ', ' + _t.get(_t.because).lower() + ' ' + premise + '</strong>'
		else:
			counterJusti = ' <strong>' + premise + ', ' + _t.get(_t.doesNotJustify).lower() + ' ' + conclusion + '</strong>'

		if conclusion[-1] == '.':
			conclusion = premise[:-1]

		w = (_t.get(_t.wrong)[0:1].lower() if startLowerCase else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
		r = (_t.get(_t.right)[0:1].lower() if startLowerCase else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]

		undermine = w + ', ' + _t.get(_t.itIsFalse) + ' <strong>' + confrontation + '</strong>.'
		support	  = r + ', ' + _t.get(_t.itIsTrue) + ' <strong>' + confrontation + '</strong>.'
		undercut  = r + ', <strong>' + confrontation + '</strong>, ' + _t.get(_t.butIDoNotBelieveCounter) + ' ' + counterJusti + '.'
		overbid	  = r + ', <strong>' + confrontation + '</strong>, ' + _t.get(_t.andIDoBelieve) + ' ' + counterJusti + '.<br>'\
		               + (_t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) if isSupportive else
		                  _t.get(_t.howeverIHaveEvenStrongerArgumentRejecting)) + ' <strong>' + premise + '</strong>.'
		rebut	  = r + ', <strong>' + confrontation + '</strong> ' + _t.get(_t.iAcceptCounter) + ' <strong>' + conclusion + '</strong>.<br>' \
					+ (_t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) if isSupportive else
					   _t.get(_t.howeverIHaveEvenStrongerArgumentRejecting)) \
					+ ' <strong>' + premise + '</strong>.'
		noopinion  = _t.get(_t.iNoOpinion) + ': <strong>' + confrontation + '</strong>. ' + _t.get(_t.goStepBack) + '.'

		ret_dict['undermine_text'] = undermine
		ret_dict['support_text'] = support
		ret_dict['undercut_text'] = undercut
		ret_dict['overbid_text'] = overbid
		ret_dict['rebut_text'] = rebut
		ret_dict['no_opinion_text'] = noopinion

		return ret_dict

	def get_relation_text_dict_without_confrontation(self, premises, conclusion, startLowerCase, withNoOpinionText):
		"""

		:param premise:
		:param conclusion:
		:param startLowerCase:
		:return:
		"""
		_t = Translator(self.lang)
		ret_dict = dict()

		if conclusion[-1] == '.':
			conclusion = conclusion[:-1]

		premise = ''
		if type(premises) is dict:
			for p in premises:
				premise += premises[p]['text'] + _t.get(_t.aand)
			premise = premise[0:-4]
		else:
			premise = premises

		w = (_t.get(_t.wrong)[0:1].lower() if startLowerCase else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
		r = (_t.get(_t.right)[0:1].lower() if startLowerCase else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]

		ret_dict['undermine_text'] = w + ', ' + _t.get(_t.itIsFalse) + ' <strong>' + premise + '</strong>.'
		ret_dict['support_text'] = r + ', ' + _t.get(_t.itIsTrue) + ' <strong>' + premise + '</strong>.'
		ret_dict['undercut_text'] = r + ', <strong>' + premise + '</strong>, ' + _t.get(_t.butIDoNotBelieveArgument) + ' <strong>' + conclusion + '</strong>.'
		ret_dict['overbid_text'] = r + ', <strong>' + premise + '</strong>, ' + _t.get(_t.andIDoBelieve) + ' <strong>' + conclusion + '</strong>.'
		ret_dict['rebut_text'] = r + ', <strong>' + premise + '</strong> ' + _t.get(_t.iAcceptArgument) + ' <strong>' + conclusion + '</strong>. '\
		                         + _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting) + ' <strong>' + conclusion + '</strong>.'
		if withNoOpinionText:
			ret_dict['no_opinion_text'] = _t.get(_t.iNoOpinion) + ': <strong>' + conclusion + ', ' + _t.get(_t.because).lower() \
			                               + ' ' + premise + '</strong>. ' + _t.get(_t.goStepBack) + '.'

		return ret_dict

	def get_text_dict_for_attacks_only (self, premises, conclusion, startLowerCase):
		"""

		:param premise:
		:param conclusion:
		:param startLowerCase:
		:return:
		"""
		_t = Translator(self.lang)
		ret_dict = dict()

		if conclusion[-1] == '.':
			conclusion = conclusion[:-1]

		premise = ''
		for p in premises:
			premise += premises[p]['text'] + _t.get(_t.aand)
		premise = premise[0:-4]

		w = (_t.get(_t.wrong)[0:1].lower() if startLowerCase else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
		r = (_t.get(_t.right)[0:1].lower() if startLowerCase else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]
		counterJusti = ' <strong>' + conclusion + ', ' + _t.get(t.because).toLocaleLowerCase() + ' ' + premise + '</strong>'

		ret_dict['undermine_text'] = w + ', <strong>' + premise + '</strong>.'
		ret_dict['undercut_text'] = r + ', <strong>' + conclusion + '</strong>, ' + _t.get(_t.butIDoNotBelieveArgument) + ' ' + counterJusti + '.'
		ret_dict['rebut_text'] = r + ', <strong>' + premise + '</strong> ' + _t.get(_t.iAcceptArgument) + ' <strong>' + conclusion + '</strong>. '\
		                         + _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting) + ' <strong>' + conclusion + '</strong>.'
		ret_dict['no_opinion_text'] = _t.get(_t.iNoOpinion) + ': <strong>' + conclusion + ', ' + _t.get(_t.because).toLocaleLowerCase() \
		                              + ' ' + premise + '</strong>. ' + _t.get(_t.goStepBack) + '.'

		return ret_dict

	def get_text_for_confrontation(self, premise, conclusion, supportive, attack, confrontation, reply_for_argument,
	                               current_argument=''):
		"""

		:param premise:
		:param conclusion:
		:param supportive:
		:param attack:
		:param confrontation:
		:param reply_for_argument:
		:param current_argument:
		:return:
		"""
		_t = Translator(self.lang)
		opinion = '<strong>' + current_argument + '</strong>' if current_argument != '' else '<strong>' + premise + '</strong> ' \
		                                    + _t.get('relation_' + relation) + ' ' + '<strong>' + conclusion + '</strong>'

		#  build some confrontation text
		confrontationText = ''
		confrontation = '<strong>' + confrontation + '</strong>'

		# build some confrontation text
		if attack == 'undermine':
			confrontationText = _t.get(_t.otherParticipantsThinkThat) + ' <strong>' + premise + '</strong> ' \
			                    + _t.get(_t.doesNotHoldBecause) + ' ' + confrontation

		elif attack == 'rebut':
			# distinguish between reply for argument and reply for premise group
			if reply_for_argument:	# reply for argument
				confrontationText = _t.get(_t.otherUsersClaimStrongerArgumentRejecting)
			else:		# reply for premise group
				confrontationText = _t.get(_t.otherParticipantsAcceptBut) + ' ' + _t.get(_t.strongerStatementForRecjecting)
			confrontationText += ' <strong>' + conclusion + '</strong>.' + ' ' + _t.get(_t.theySay) + ': ' + confrontation

		elif attack == 'undercut':
			confrontationText = _t.get(_t.otherParticipantsThinkThat) + ' <strong>' + premise + '</strong> ' \
			                    + (_t.get(_t.andTheyDoNotBelieveCounter)
			                       if supportive else _t.get(_t.andTheyDoNotBelieveCounter)) \
			                    + ' <strong>' + conclusion + '</strong>,' + ' ' + _t.get(_t.because).lower() + ' ' + confrontation

		return _t.get(_t.sentencesOpenersForArguments[0]) + ': ' + opinion + '.<br><br>' + confrontationText \
		       + '.<br><br>' + _t.get(_t.whatDoYouThinkAboutThat) + '?'


	def get_text_for_status_one_in_confrontation(self, premise, conclusion, relation, supportive, attack,
	                                             url, confrontation, reply_for_argument, current_argument=''):
		"""

		:param premise:
		:param conclusion:
		:param relation:
		:param supportive:
		:param attack:
		:param url:
		:param confrontation:
		:param reply_for_argument:
		:param current_argument:
		:return:
		"""
		_t = Translator(self.lang)
		if not relation:
			connector = (', ' + _t.get(_t.because).lower())  if supportive else (' ' +  _t.get(_t.doesNotHoldBecause).lower())
			opinion = '<strong>' + conclusion + connector + ' ' + premise + '</strong>'
		else:
			opinion = '<strong>' + current_argument + '</strong>' if current_argument != '' else '<strong>' + premise + '</strong> ' + _t.get('relation_' + relation) + ' ' + '<strong>' + conclusion + '</strong>'

		#  build some confrontation text
		confrontationText = ''
		confrontation = '<strong>' + confrontation + '</strong>'

		# does we have an attack for an attack? if true, we have to pretty print a little bit
		attacks = ['undermine','rebut','undercut']
		double_attack = ([s for s in attacks if s in url] or ('supportive=false' in url)) \
		                and [s for s in attacks if s in attack]

		# build some confrontation text
		if attack == 'undermine':
			confrontationText = _t.get(_t.otherParticipantsThinkThat) + ' <strong>' + premise + '</strong> ' \
			                    + _t.get(_t.doesNotHoldBecause) + ' ' + confrontation

		elif attack == 'rebut':
			# distinguish between reply for argument and reply for premise group
			if reply_for_argument:
				# reply for argument
				confrontationText = (_t.get(_t.otherUsersClaimStrongerArgumentAccepting)
				                     if double_attack else _t.get(_t.otherUsersClaimStrongerArgumentRejecting))
			else:
				# reply for premise group
				confrontationText = _t.get(_t.otherParticipantsAcceptBut) + ' ' \
				                    + _t.get(_t.strongerStatementForRecjecting)
			confrontationText += ' <strong>' + conclusion + '</strong>.' + ' ' + _t.get(_t.theySay) + ': ' + confrontation

		elif attack == 'undercut':
			confrontationText = _t.get(_t.otherParticipantsThinkThat) + ' <strong>' + premise + '</strong> ' \
			                    + (_t.get(_t.andTheyDoNotBelieveCounter)
			                       if supportive else _t.get(_t.andTheyDoNotBelieveCounter)) \
			                    + ' <strong>' + conclusion + '</strong>,' + ' ' + _t.get(_t.because).lower() + ' ' + confrontation

		return _t.get(_t.sentencesOpenersForArguments[0]) + ': ' + opinion + '.<br><br>' + confrontationText \
		       + '.<br><br>' + _t.get(_t.whatDoYouThinkAboutThat) + '?'
	
	def get_text_for_status_zero_in_confrontation(self, premise, conclusion, relation):
		"""
		
		:param premise: 
		:param conclusion: 
		:param relation: 
		:return: 
		"""
		_t = Translator(self.lang)
		
		if not relation:
			opinion = '<strong>' + conclusion + ', ' + _t.get(_t.because)[0:1].lower() + _t.get(_t.because)[1:] + ' ' + premise + '</strong>'
		else:
			opinion = '<strong>' + premise + '</strong> ' + _t.get('relation_' + return_dict['relation']) + ' ' + '<strong>' + conclusion + '</strong>'
		
		return _t.get(_t.sentencesOpenersForArguments[0]) + ': ' + opinion + '.<br><br>' \
		       + _t.get(_t.otherParticipantsDontHaveCounter) + ' <strong>' + premise + '</strong>' + '.<br><br>' \
		       + _t.get(_t.discussionEnd) + ' ' + _t.get(_t.discussionEndText), _t.get(_t.discussionEnd)

	def get_text_for_premise_for_statement(self, conclusion, premises, supportive, logged_in):
		"""

		:param conclusion:
		:param premisses:
		:param supportive:
		:return:
		"""
		_t = Translator(self.lang)
		_tg = TextGenerator(self.lang)
		ret_dict = dict()

		if len(premises) == 0:
			text_add_on = '' if logged_in else ('<br><br>'  + _t.get(_t.discussionEndFeelFreeToLogin))
			if supportive:
				ret_dict['discussion_description'] = _t.get(_t.unfortunatelyNoMoreArgument) + ' ' + argument \
				                                     + '.<br><br>' + _t.get(_t.canYouGiveAReason) + '<br><br>' \
				                                     + _t.get(_t.alternatively) + ': ' + _t.get(_t.discussionEndText) \
				                                     + text_add_on
			else:
				ret_dict['discussion_description'] = _t.get(_t.soYouWantToArgueAgainst) + ' ' + argument + ', ' \
				                                     + _t.get(_t.butOtherParticipantsDontHaveArgument) + text_add_on
			ret_dict['argument'] = '<strong>' + conclusion + '</strong>'

		else:
			premise = ''
			for p in premises:
				premise += ('' if premise == '' else (' ' + _t.get(_t.aand) + ' ')) + premises[p]['text'][0:1].lower() + premises[p]['text'][1:]
			ret_dict['discussion_description'] = _t.get(_t.otherParticipantsThinkThat) + ' <strong>' + conclusion + '</strong>, ' \
			                                     + _t.get(_t.because)[0:1].lower() + _t.get(_t.because)[1:] \
			                                     + ' <strong>' + premise + '</strong>.<br><br>' \
			                                     + ((_t.get(_t.whatDoYouThinkAboutThat) + '?')
			                                        if supportive else _t.get(_t.whyAreYouDisagreeing))
			ret_dict['argument'] = conclusion + ' ' + _t.get(_t.because)[0:1].lower() + _t.get(_t.because)[1:] + ' ' + premise

		if supportive:
			ret_dict.update(_tg.get_relation_text_dict_without_confrontation(premises, conclusion, False, True))
		else:
			ret_dict.update(_tg.get_text_dict_for_attacks_only(premises, conclusion, False))

		return ret_dict

	def get_text_for_response_of_confrontation(self, current_argument, conclusion, relation, premise, attack,
	                                           attack_or_confrontation, supportive, is_support, supportive_argument,
	                                           user, url,  status):
		"""

		:param argument_uid:
		:param conclusion:
		:param relation:
		:param premise:
		:param attack:
		:param attack_or_confrontation:
		:param supportive:
		:param is_support:
		:param supportive_argument:
		:param user:
		:param url:
		:param status:
		:return:
		"""
		_tg = TextGenerator(self.lang)
		ret_dict = dict()

		if is_support and int(status) != 0:
			logger('reply_for_response_of_confrontation', 'def', 'path b1')
			ret_dict.update(_tg.get_confrontation_relation_text_dict(attack_or_confrontation,
			                                                         conclusion,
			                                                         premise,
			                                                         False,
			                                                         supportive))
		else:
			logger('reply_for_response_of_confrontation', 'def', 'path b2')
			ret_dict['header_text'] = _tg.get_header_for_confrontation_response(attack_or_confrontation,
			                                                                    premise,
			                                                                    relation,
			                                                                    conclusion,
			                                                                    True,
			                                                                    supportive,
			                                                                    user)

		if supportive_argument and int(status) == 0:
			logger('reply_for_response_of_confrontation', 'def', 'path c1')
			ret_dict['discussion_description'] = _tg.get_text_for_status_zero_in_confrontation(premise,
			                                                                                   conclusion,
			                                                                                   relation)
		elif int(status) == 1:
			logger('reply_for_response_of_confrontation', 'def', 'path c2')
			ret_dict['discussion_description'] = _tg.get_text_for_status_one_in_confrontation(premise,
			                                                                                  conclusion,
			                                                                                  relation,
			                                                                                  supportive,
			                                                                                  attack,
			                                                                                  url,
			                                                                                  attack_or_confrontation,
			                                                                                  False,
			                                                                                  current_argument)
		return ret_dict
