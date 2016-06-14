#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from .strings_de import GermanDict
from .strings_en import EnglischDict

from .database import DBDiscussionSession
from .database.discussion_model import Statement, Premise, VoteStatement
from .logger import logger


class Translator(object):
    """
    Class for translating string
    """
    def __init__(self, lang):
        """
        Initializes keywords

        :param lang: current language
        :return:
        """
        self.lang = lang

        self.arguments = 'arguments'
        self.error = 'error'
        self.forgotInputRadio = 'forgotInputRadio'
        self.iActuallyHave = 'iActuallyHave'
        self.insertOneArgument = 'insertOneArgument'
        self.insertDontCare = 'insertDontCare'
        self.needHelpToUnderstandStatement = 'needHelpToUnderstandStatement'
        self.setPremisegroupsIntro1 = 'setPremisegroupsIntro1'
        self.setPremisegroupsIntro2 = 'setPremisegroupsIntro2'

        self.aand = 'and'
        self.addedEverything = 'addedEverything'
        self.addTopic = 'addTopic'
        self.addStatementRow = 'addStatementRow'
        self.alreadyInserted = 'alreadyInserted'
        self.at = 'at'
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
        self.attitudeFor = 'attitudeFor'
        self.agreeBecause = 'agreeBecause'
        self.andIDoBelieveCounterFor = 'andIDoBelieveCounterFor'
        self.andIDoBelieveArgument = 'andIDoBelieveArgument'
        self.addArguments = 'addArguments'
        self.addStatements = 'addStatements'
        self.addArgumentsTitle = 'addArgumentsTitle'
        self.acceptItTitle = 'acceptItTitle'
        self.acceptIt = 'acceptIt'
        self.attack = 'attack'
        self.accountWasAdded = 'accountWasAdded'
        self.accountRegistration = 'accountRegistration'
        self.accountWasRegistered = 'accountWasRegistered'
        self.accoutErrorTryLateOrContant = 'accoutErrorTryLateOrContant'
        self.antispamquestion = 'antispamquestion'
        self.addATopic = 'addATopic'
        self.because = 'because'
        self.breadcrumbsStart = 'breadcrumbsStart'
        self.breadcrumbsChoose = 'breadcrumbsChoose'
        self.breadcrumbsJustifyStatement = 'breadcrumbsJustifyStatement'
        self.breadcrumbsGetPremisesForStatement = 'breadcrumbsGetPremisesForStatement'
        self.breadcrumbsMoreAboutArgument = 'breadcrumbsMoreAboutArgument'
        self.breadcrumbsReplyForPremisegroup = 'breadcrumbsReplyForPremisegroup'
        self.breadcrumbsReplyForResponseOfConfrontation = 'breadcrumbsReplyForResponseOfConfrontation'
        self.breadcrumbsReplyForArgument = 'breadcrumbsReplyForArgument'
        self.butOtherParticipantsDontHaveOpinionRegardingYourOpinion = 'butOtherParticipantsDontHaveOpinionRegardingYourOpinion'
        self.butOtherParticipantsDontHaveArgument = 'butOtherParticipantsDontHaveArgument'
        self.butOtherParticipantsDontHaveCounterArgument = 'butOtherParticipantsDontHaveCounterArgument'
        self.butIDoNotBelieveCounterFor = 'butIDoNotBelieveCounterFor'
        self.butIDoNotBelieveReasonForReject = 'butIDoNotBelieveReasonForReject'
        self.butIDoNotBelieveArgumentFor = 'butIDoNotBelieveArgument'
        self.butTheyDoNotBelieveCounter = 'butTheyDoNotBelieveCounter'
        self.butTheyDoNotBelieveArgument = 'butTheyDoNotBelieveArgument'
        self.because = 'because'
        self.butWhich = 'butWhich'
        self.butThenYouCounteredWith = 'butThenYouCounteredWith'
        self.butYouCounteredWith = 'butYouCounteredWith'
        self.butYouAgreedWith = 'butYouAgreedWith'
        self.clickHereForRegistration = 'clickHereForRegistration'
        self.confirmation = 'confirmation'
        self.contact = 'contact'
        self.contactSubmit = 'contactSubmit'
        self.confirmTranslation = 'confirmTranslation'
        self.correctionsSet = 'correctionsSet'
        self.countOfArguments = 'countOfArguments'
        self.countOfPosts = 'countOfPosts'
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
        self.clearStatistics = 'clearStatistics'
        self.clickForMore = 'clickForMore'
        self.completeView = 'completeView'
        self.completeViewTitle = 'completeViewTitle'
        self.currentDiscussion = 'currentDiscussion'
        self.cancel = 'cancel'
        self.close = 'close'
        self.confPwdEmpty = 'confPwdEmpty'
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
        self.decisionIndex7 = 'decisionIndex7'
        self.decisionIndex30 = 'decisionIndex30'
        self.decisionIndex7Info = 'decisionIndex7Info'
        self.decisionIndex30Info = 'decisionIndex30Info'
        self.dataRemoved = 'dataRemoved'
        self.didYouMean = 'didYouMean'
        self.discussionEnd = 'discussionEnd'
        self.discussionEndLinkText = 'discussionEndLinkText'
        self.duplicate = 'duplicate'
        self.duplicateDialog = 'duplicateDialog'
        self.displayControlDialogGuidedTitle = 'displayControlDialogGuidedTitle'
        self.displayControlDialogGuidedBody = 'displayControlDialogGuidedBody'
        self.displayControlDialogIslandTitle = 'displayControlDialogIslandTitle'
        self.displayControlDialogIslandBody = 'displayControlDialogIslandBody'
        self.displayControlDialogExpertTitle = 'displayControlDialogExpertTitle'
        self.displayControlDialogExpertBody = 'displayControlDialogExpertBody'
        self.discussionInfoTooltip1 = 'discussionInfoTooltip1'
        self.discussionInfoTooltip2 = 'discussionInfoTooltip2'
        self.discussionInfoTooltip3sg = 'discussionInfoTooltip3sg'
        self.discussionInfoTooltip3pl = 'discussionInfoTooltip3pl'
        self.doesNotHold = 'doesNotHold'
        self.doesNotHoldBecause = 'doesNotHoldBecause'
        self.doesJustify = 'doesJustify'
        self.doesNotJustify = 'doesNotJustify'
        self.deleteTrack = 'deleteTrack'
        self.deleteHistory = 'deleteHistory'
        self.doYouWantToEnterYourStatements = 'doYouWantToEnterYourStatements'
        self.doNotHesitateToContact = 'doNotHesitateToContact'
        self.doesNotHoldBecause = 'doesNotHoldBecause'
        self.dbasPwdRequest = 'dbasPwdRequest'
        self.defaultView = 'defaultView'
        self.earlierYouArguedThat = 'earlierYouArguedThat'
        self.editIndex = 'editIndex'
        self.editIndexInfo = 'editIndexInfo'
        self.euCookiePopupTitle = 'euCookiePopupTitle'
        self.euCookiePopupText = 'euCookiePopupText'
        self.euCookiePopoupButton1 = 'euCookiePopoupButton1'
        self.euCookiePopoupButton2 = 'euCookiePopoupButton2'
        self.empty_news_input = 'empty_news_input'
        self.empty_notification_input = 'empty_notification_input'
        self.email = 'email'
        self.emailWasSent = 'emailWasSent'
        self.emailWasNotSent = 'emailWasNotSent'
        self.emailUnknown = 'emailUnknown'
        self.edit = 'edit'
        self.error_code = 'error_code'
        self.editTitle = 'editTitle'
        self.emailBodyText = 'emailBodyText'
        self.emailWasSent = 'emailWasSent'
        self.emailWasNotSent = 'emailWasNotSent'
        self.emptyName = 'emptyName'
        self.emptyEmail = 'emptyEmail'
        self.emtpyContent = 'emtpyContent'
        self.errorTryLateOrContant = 'errorTryLateOrContant'
        self.editStatementViewChangelog = 'editStatementViewChangelog'
        self.editStatementHere = 'editStatementHere'
        self.feelFreeToLogin = 'feelFreeToLogin'
        self.forText = 'forText'
        self.fillLine = 'fillLine'
        self.firstConclusionRadioButtonText = 'firstConclusionRadioButtonText'
        self.firstArgumentRadioButtonText = 'firstArgumentRadioButtonText'
        self.feelFreeToShareUrl = 'feelFreeToShareUrl'
        self.fetchLongUrl = 'fetchLongUrl'
        self.fetchShortUrl = 'fetchShortUrl'
        self.forgotPassword = 'forgotPassword'
        self.firstOneText = 'firstOneText'
        self.firstOneInformationText = 'firstOneInformationText'
        self.firstOneReason = 'firstOneReason'
        self.firstPositionText = 'firstPositionText'
        self.firstPremiseText1 = 'firstPremiseText1'
        self.firstPremiseText2 = 'firstPremiseText2'
        self.firstname = 'firstname'
        self.finishTitle = 'finishTitle'
        self.fromm = 'fromm'
        self.gender = 'gender'
        self.goBack = 'goBack'
        self.goHome = 'goHome'
        self.goStepBack = 'goStepBack'
        self.generateSecurePassword = 'generateSecurePassword'
        self.goodPointTakeMeBackButtonText = 'goodPointTakeMeBackButtonText'
        self.group_uid = 'group_uid'
        self.haveALookAt = 'haveALookAt'
        self.hidePasswordRequest = 'hidePasswordRequest'
        self.hideGenerator = 'hideGenerator'
        self.hold = 'holds'
        self.howeverIHaveMuchStrongerArgumentRejecting = 'howeverIHaveMuchStrongerArgumentRejecting'
        self.howeverIHaveEvenStrongerArgumentRejecting = 'howeverIHaveEvenStrongerArgumentRejecting'
        self.howeverIHaveMuchStrongerArgumentAccepting = 'howeverIHaveMuchStrongerArgumentAccepting'
        self.howeverIHaveEvenStrongerArgumentAccepting = 'howeverIHaveEvenStrongerArgumentAccepting'
        self.hideContent = 'hideContent'
        self.islandViewFor = 'islandViewFor'
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
        self.itTrueIs = 'itTrueIs'
        self.itFalseIs = 'itFalseIs'
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
        self.iHaveNoOpinionYet = 'iHaveNoOpinionYet'
        self.iHaveNoOpinionYetInColor = 'iHaveNoOpinionYetInColor'
        self.iHaveNoOpinion = 'iHaveNoOpinion'
        self.iDisagreeWith = 'iDisagreeWith'
        self.iHaveMuchStrongerArgumentRejecting = 'iHaveMuchStrongerArgumentRejecting'
        self.iHaveEvenStrongerArgumentRejecting = 'iHaveEvenStrongerArgumentRejecting'
        self.iHaveMuchStrongerArgumentAccepting = 'iHaveMuchStrongerArgumentAccepting'
        self.iHaveEvenStrongerArgumentAccepting = 'iHaveEvenStrongerArgumentAccepting'
        self.iNoOpinion = 'iNoOpinion'
        self.isNotAGoodIdea = 'isNotAGoodIdea'
        self.interestingOnDBAS = 'interestingOnDBAS'
        self.informationForStatements = 'informationForStatements'
        self.invalidEmail = 'invalidEmail'
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
        self.holds = 'holds'
        self.letMeExplain = 'letMeExplain'
        self.levenshteinDistance = 'levenshteinDistance'
        self.languageCouldNotBeSwitched = 'languageCouldNotBeSwitched'
        self.last_action = 'last_action'
        self.last_login = 'last_login'
        self.login = 'login'
        self.logfile = 'logfile'
        self.letsGo = 'letsGo'
        self.letsGoBack = 'letsGoBack'
        self.letsGoHome = 'letsGoHome'
        self.medium = 'medium'
        self.more = 'more'
        self.message = 'message'
        self.messageDeleted = 'messageDeleted'
        self.maliciousAntiSpam = 'maliciousAntiSpam'
        self.mail = 'mail'
        self.mailIsTaken = 'mailIsTaken'
        self.mailNotValid = 'mailNotValid'
        self.mailSettingsTitle = 'mailSettingsTitle'
        self.moreAbout = 'moreAbout'
        self.minLength = 'minLength'
        self.nickIsTaken = 'nickIsTaken'
        self.nicknameIs = 'nicknameIs'
        self.newPwdEmtpy = 'newPwdEmtpy'
        self.newPwdIs = 'newPwdIs'
        self.nonValidCSRF = 'nonValidCSRF'
        self.name = 'name'
        self.newPwdNotEqual = 'newPwdNotEqual'
        self.notificationSettingsTitle = 'notificationSettingsTitle'
        self.notification = 'notification'
        self.notificationDeleted = 'notificationDeleted'
        self.next = 'next'
        self.newPremisesRadioButtonText = 'newPremisesRadioButtonText'
        self.newPremisesRadioButtonTextAsFirstOne = 'newPremisesRadioButtonTextAsFirstOne'
        self.newStatementsRadioButtonTextAsFirstOne = 'newStatementsRadioButtonTextAsFirstOne'
        self.newPremiseRadioButtonText = 'newPremiseRadioButtonText'
        self.newPremiseRadioButtonTextAsFirstOne = 'newPremiseRadioButtonTextAsFirstOne'
        self.newStatementRadioButtonTextAsFirstOne = 'newStatementRadioButtonTextAsFirstOne'
        self.newConclusionRadioButtonText = 'newConclusionRadioButtonText'
        self.newsAboutDbas = 'newsAboutDbas'
        self.nickname = 'nickname'
        self.noOtherAttack = 'noOtherAttack'
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
        self.now = 'now'
        self.number = 'number'
        self.note = 'note'
        self.no_entry = 'no_entry'
        self.noRights = 'noRights'
        self.notLoggedIn = 'notLoggedIn'
        self.unfortunatelyOnlyOneItem = 'unfortunatelyOnlyOneItem'
        self.on = 'on'
        self.off = 'off'
        self.onlyOneItem = 'onlyOneItem'
        self.onlyOneItemWithLink = 'onlyOneItemWithLink'
        self.otherParticipantsConvincedYouThat = 'otherParticipantsConvincedYouThat'
        self.otherParticipantsThinkThat = 'otherParticipantsThinkThat'
        self.otherParticipantsAgreeThat = 'otherParticipantsAgreeThat'
        self.otherParticipantsDontHaveCounter = 'otherParticipantsDontHaveCounter'
        self.otherParticipantsDontHaveCounterForThat = 'otherParticipantsDontHaveCounterForThat'
        self.otherParticipantsDontHaveNewCounterForThat = 'otherParticipantsDontHaveNewCounterForThat'
        self.otherParticipantsDontHaveOpinion = 'otherParticipantsDontHaveOpinion'
        self.otherParticipantsDontHaveOpinionRegaringYourSelection = 'otherParticipantsDontHaveOpinionRegaringYourSelection'
        self.otherParticipantsDontHaveArgument = 'otherParticipantsDontHaveArgument'
        self.otherParticipantsAcceptBut = 'otherParticipantsAcceptBut'
        self.otherParticipantDisagreeThat = 'otherParticipantDisagreeThat'
        self.otherUsersClaimStrongerArgumentRejecting = 'otherUsersClaimStrongerArgumentRejecting'
        self.otherUsersClaimStrongerArgumentAccepting = 'otherUsersClaimStrongerArgumentAccepting'
        self.otherUsersHaveCounterArgument = 'otherUsersHaveCounterArgument'
        self.otherUsersSaidThat = 'otherUsersSaidThat'
        self.opinionBarometer = 'opinionBarometer'
        self.overbid1 = 'overbid1'
        self.overbid2 = 'overbid2'
        self.oldPwdEmpty = 'oldPwdEmpty'
        self.oldPwdWrong = 'oldPwdWrong'
        self.pleaseEnterTopic = 'pleaseEnterTopic'
        self.pleaseEnterShorttextForTopic = 'pleaseEnterShorttextForTopic'
        self.pleaseSelectLanguageForTopic = 'pleaseSelectLanguageForTopic'
        self.premise = 'premise'
        self.phone = 'phone'
        self.pwdNotEqual = 'pwdNotEqual'
        self.pwdsSame = 'pwdsSame'
        self.pwdChanged = 'pwdChanged'
        self.pleaseAddYourSuggestion = 'pleaseAddYourSuggestion'
        self.premiseGroup = 'premiseGroup'
        self.previous = 'previous'
        self.passwordSubmit = 'passwordSubmit'
        self.publicNickTitle = 'publicNickTitle'
        self.rebut1 = 'rebut1'
        self.rebut2 = 'rebut2'
        self.resumeHere = 'resumeHere'
        self.report = 'report'
        self.reportTitle = 'reportTitle'
        self.registered = 'registered'
        self.right = 'right'
        self.requestTrack = 'requestTrack'
        self.refreshTrack = 'refreshTrack'
        self.requestHistory = 'requestHistory'
        self.refreshHistory = 'refreshHistory'
        self.requestFailed = 'requestFailed'
        self.remStatementRow = 'remStatementRow'
        self.restartDiscussion = 'restartDiscussion'
        self.restartDiscussionTitle = 'restartDiscussionTitle'
        self.restartOnError = 'restartOnError'
        self.recipientNotFound = 'recipientNotFound'
        self.reactionFor = 'reactionFor'
        self.questionTitle = 'questionTitle'
        self.selectStatement = 'selectStatement'
        self.showAllUsers = 'showAllUsers'
        self.showAllArguments = 'showAllArguments'
        self.showAllArgumentsTitle = 'showAllArgumentsTitle'
        self.showAllUsersTitle = 'showAllUsersTitle'
        self.saveMyStatement = 'saveMyStatement'
        self.statementIndex = 'statementIndex'
        self.statementIndexInfo = 'statementIndexInfo'
        self.strength = 'strength'
        self.strong = 'strong'
        self.strongerStatementForAccepting = 'strongerStatementForAccepting'
        self.strongerStatementForRecjecting = 'strongerStatementForRecjecting'
        self.soYouEnteredMultipleReasons = 'soYouEnteredMultipleReasons'
        self.soYourOpinionIsThat = 'soYourOpinionIsThat'
        self.soYouWantToArgueAgainst = 'soYouWantToArgueAgainst'
        self.soThatOtherParticipantsDontHaveOpinionRegardingYourOpinion = 'soThatOtherParticipantsDontHaveOpinionRegardingYourOpinion'
        self.shortenedBy = 'shortenedBy'
        self.shareUrl = 'shareUrl'
        self.showMeAnotherArgument = 'showMeAnotherArgument'
        self.switchDiscussion = 'switchDiscussion'
        self.switchDiscussionTitle = 'switchDiscussionTitle'
        self.switchDiscussionText1 = 'switchDiscussionText1'
        self.switchDiscussionText2 = 'switchDiscussionText2'
        self.switchLanguage = 'switchLanguage'
        self.supportPosition = 'supportPosition'
        self.statement = 'statement'
        self.sureThat = 'sureThat'
        self.surname = 'surname'
        self.showMeAnArgumentFor = 'showMeAnArgumentFor'
        self.save = 'save'
        self.submit = 'submit'
        self.signs = 'signs'
        self.showContent = 'showContent'
        self.support = 'support'
        self.support1 = 'support1'
        self.tightView = 'tightView'
        self.textAreaReasonHintText = 'textAreaReasonHintText'
        self.theCounterArgument = 'theCounterArgument'
        self.therefore = 'therefore'
        self.thinkWeShould = 'thinkWeShould'
        self.thisConfrontationIs = 'thisConfrontationIs'
        self.thisIsACopyOfMail = 'thisIsACopyOfMail'
        self.textversionChangedTopic = 'textversionChangedTopic'
        self.textversionChangedContent = 'textversionChangedContent'
        self.to = 'to'
        self.track = 'track'
        self.history = 'history'
        self.topicString = 'topicString'
        self.text = 'text'
        self.theySay = 'theySay'
        self.theyThink = 'theyThink'
        self.veryweak = 'veryweak'
        self.wantToStateNewPosition = 'wantToStateNewPosition'
        self.weak = 'weak'
        self.wrong = 'wrong'
        self.wouldYourShareArgument = 'wouldYourShareArgument'
        self.wrongURL = 'wrongURL'
        self.whatDoYouThinkAbout = 'whatDoYouThinkAbout'
        self.whatDoYouThinkAboutThat = 'whatDoYouThinkAboutThat'
        self.whyDoYouThinkThat = 'whyDoYouThinkThat'
        self.whatIsYourIdea = 'whatIsYourIdea'
        self.whatIsYourMostImportantReasonFor = 'whatIsYourMostImportantReasonFor'
        self.whatIsYourMostImportantReasonWhy = 'whatIsYourMostImportantReasonWhy'
        self.whyAreYouDisagreeingWith = 'whyAreYouDisagreeingWith'
        self.whyAreYouAgreeingWith = 'whyAreYouAgreeingWith'
        self.whyAreYouDisagreeingWithInColor = 'whyAreYouDisagreeingWithInColor'
        self.whyAreYouAgreeingWithInColor = 'whyAreYouAgreeingWithInColor'
        self.whyAreYouDisagreeingWithThat = 'whyAreYouDisagreeingWithThat'
        self.youMadeA = 'youMadeA'
        self.youMadeAn = 'youMadeAn'
        self.relation_undermine = 'relation_undermine'
        self.relation_support = 'relation_support'
        self.relation_undercut = 'relation_undercut'
        self.relation_overbid = 'relation_overbid'
        self.relation_rebut = 'relation_rebut'
        self.uid = 'uid'
        self.unfortunatelyNoMoreArgument = 'unfortunatelyNoMoreArgument'
        self.userPasswordNotMatch = 'userPasswordNotMatch'
        self.userOptions = 'userOptions'
        self.undermine = 'undermine'
        self.undercut1 = 'undercut1'
        self.undercut2 = 'undercut2'
        self.urlSharing = 'urlSharing'
        self.urlSharingDescription = 'urlSharingDescription'
        self.userPasswordNotMatch = 'userPasswordNotMatch'
        self.voteCountTextFirst = 'voteCountTextFirst'
        self.voteCountTextMayBeFirst = 'voteCountTextMayBeFirst'
        self.voteCountTextOneOther = 'voteCountTextOneOther'
        self.voteCountTextMore = 'voteCountTextMore'
        self.warning = 'warning'
        self.where = 'where'
        self.wideView = 'wideView'
        self.welcome = 'welcome'
        self.welcomeMessage = 'welcomeMessage'
        self.youAreInterestedIn = 'youAreInterestedIn'
        self.youAgreeWith = 'youAgreeWith'
        self.youDisagreeWith = 'youDisagreeWith'
        self.youSaidThat = 'youSaidThat'
        self.youUsedThisEarlier = 'youUsedThisEarlier'
        self.youRejectedThisEarlier = 'youRejectedThisEarlier'
        self.youHaveMuchStrongerArgumentForAccepting = 'youHaveMuchStrongerArgumentForAccepting'
        self.youHaveMuchStrongerArgumentForRejecting = 'youHaveMuchStrongerArgumentForRejecting'

        self.sentencesOpenersArguingWithAgreeing = [self.agreeBecause, self.therefore]
        self.sentencesOpenersArguingWithDisagreeing = [self.disagreeBecause, self.alternatively]
        self.sentencesOpenersInforming = [self.thinkWeShould, self.letMeExplain, self.sureThat]

        self.en_dict = EnglischDict().set_up(self)
        self.de_dict = GermanDict().set_up(self)

    def get(self, sid):
        """
        Returns an localized string

        :param sid: string identifier
        :return: string
        """
        if self.lang == 'de' and sid in self.de_dict:
            return self.de_dict[sid]

        elif self.lang == 'en' and sid in self.en_dict:
            return self.en_dict[sid]

        elif self.lang == 'de' and sid not in self.de_dict:
            return 'unbekannter identifier im deutschen Wörterbuch'

        elif self.lang == 'en' and sid not in self.en_dict:
            return 'unknown identifier in the englisch dictionary'

        else:
            return 'unknown language: ' + str(self.lang)


class TextGenerator(object):
    """
    Generates text for D-BAS
    """

    def __init__(self, lang):
        """
        Sets current language

        :param lang: current language
        :return:
        """
        self.lang = lang

    def get_text_for_add_premise_container(self, confrontation, premise, attack_type, conclusion, is_supportive):
        """
        Based on the users reaction, text will be build. This text can be used for the container where users can
        add their statements

        :param confrontation: choosen confrontation
        :param premise: current premise
        :param attack_type: type of the attack
        :param conclusion: current conclusion
        :param is_supportive: boolean
        :return: string
        """
        _t = Translator(self.lang)

        if premise[-1] == '.':
            premise = premise[:-1]

        if conclusion[-1] == '.':
            conclusion = premise[:-1]

        confrontation = '<strong>' + confrontation[0:1].upper() + confrontation[1:] + '</strong>'

        premise = '<strong>' + premise[0:1].lower() + premise[1:] + '</strong>'
        conclusion = '<strong>' + conclusion[0:1].lower() + conclusion[1:] + '</strong>'

        # different cases
        ret_text = ''
        if attack_type == 'undermine':
            ret_text = _t.get(_t.itIsFalse) + ' ' + premise
        if attack_type == 'support':
            ret_text = _t.get(_t.itIsTrue) if is_supportive else _t.get(_t.itIsFalse)
            ret_text += ' <strong>' + conclusion + ' '
            ret_text += _t.get(_t.hold) if is_supportive else _t.get(_t.doesNotHold)
            ret_text += '</strong>'
        if attack_type == 'undercut':
            ret_text = confrontation + ', ' + _t.get(_t.butIDoNotBelieveCounterFor) + ' ' + conclusion
        if attack_type == 'overbid':
            ret_text = confrontation + ', ' + _t.get(_t.andIDoBelieveCounterFor) + ' ' + conclusion
        #  + '.' + _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) + ' ' + longConclusion + '.'
        if attack_type == 'rebut':
            ret_text = confrontation + ' ' \
                       + (_t.get(_t.iAcceptCounter) if is_supportive else _t.get(_t.iAcceptArgument)) \
                       + ' ' + conclusion

        return ret_text + ', '  + _t.get(_t.because).lower() + '...'

    def get_header_for_users_confrontation_response(self, premise, attack_type, conclusion, start_lower_case,
                                                    is_supportive, is_logged_in):
        """
        Based on the users reaction, text will be build. This text can be used for the speech bubbles where users
        justify an argument they have choosen.

        :param premise: current premise
        :param attack_type: type of the attack
        :param conclusion: current conclusion
        :param start_lower_case: boolean
        :param is_supportive: boolean
        :param is_logged_in: boolean
        :return: string
        """
        _t         = Translator(self.lang)
        user_msg   = ''
        system_msg = ''
        premise    = premise[0:1].lower() + premise[1:]
        if self.lang != 'de':
            conclusion = conclusion[0:1].lower() + conclusion[1:]

        if premise[-1] == '.':
            premise = premise[:-1]

        if conclusion[-1] == '.':
            conclusion = premise[:-1]

        # pretty print
        #  w = (_t.get(_t.wrong)[0:1].lower() if start_lower_case else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:] + ', '
        r = (_t.get(_t.right)[0:1].lower() if start_lower_case else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:] + ', '
        f = (_t.get(_t.itIsFalse)[0:1].lower() if start_lower_case else _t.get(_t.itIsFalse)[0:1].upper()) + _t.get(_t.itIsFalse)[1:]
        t = (_t.get(_t.itIsTrue)[0:1].lower() if start_lower_case else _t.get(_t.itIsTrue)[0:1].upper()) + _t.get(_t.itIsTrue)[1:]

        if self.lang == 'de':
            r += _t.get(_t.itIsTrue)[0:1].lower() + _t.get(_t.itIsTrue)[1:] + ' '
            f = _t.get(_t.wrong) + ', ' + _t.get(_t.itIsFalse)[0:1].lower() + _t.get(_t.itIsFalse)[1:] + ' '

        # different cases
        if attack_type == 'undermine':
            user_msg = f + ' <strong>' + premise + '</strong>.'

        if attack_type == 'support':
            user_msg = t if is_supportive else f
            user_msg += ' <strong>' + conclusion + ' '
            user_msg += _t.get(_t.hold) if is_supportive else _t.get(_t.doesNotHold)
            user_msg += '</strong>.'

        if attack_type == 'undercut':
            user_msg = r + '<strong>' + premise + '</strong>, '
            user_msg += _t.get(_t.butIDoNotBelieveCounterFor) if is_supportive else _t.get(_t.butIDoNotBelieveArgumentFor)
            user_msg += ' <strong>' + conclusion + '</strong>.'

        if attack_type == 'overbid':
            user_msg = r + '<strong>' + premise + '</strong>, '
            user_msg += _t.get(_t.andIDoBelieveCounterFor) if is_supportive else _t.get(_t.andIDoBelieveArgument)
            user_msg += ' <strong>' + conclusion + '</strong>. '
            user_msg += _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) if is_supportive else _t.get(_t.howeverIHaveEvenStrongerArgumentRejecting)
            user_msg += ' <strong>' + conclusion + '</strong>.'

        if attack_type == 'rebut':
            user_msg = r + '<strong>' + premise + '</strong>, '
            user_msg += _t.get(_t.iAcceptCounter) if is_supportive else _t.get(_t.iAcceptArgument)
            user_msg += ' <strong>' + conclusion + '</strong>. '
            user_msg += _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting) if is_supportive else _t.get(_t.howeverIHaveMuchStrongerArgumentAccepting)
            user_msg += ' <strong>' + conclusion + '</strong>.'

        # is logged in?
        if is_logged_in:
            system_msg  = _t.get(_t.canYouGiveAReasonForThat)

        return user_msg, system_msg

    def get_relation_text_dict(self, premises, conclusion, start_lower_case, with_no_opinion_text, is_attacking,
                               is_dont_know=False, first_conclusion=None, for_island_view=False):
        """
        Text of the different reaction types for an given argument

        :param premises: String
        :param conclusion: String
        :param start_lower_case: Boolean
        :param with_no_opinion_text: Boolean
        :param is_attacking: Boolean
        :param is_dont_know: Boolean
        :param first_conclusion: String
        :param for_island_view: Boolean
        :return: dict()
        """
        _t = Translator(self.lang)
        ret_dict = dict()

        if conclusion[-1] == '.':
            conclusion = conclusion[:-1]
        if first_conclusion:
            if first_conclusion[-1] == '.':
                first_conclusion = first_conclusion[:-1]

        premise = ''
        if type(premises) is dict:
            for p in premises:
                premise += premises[p]['text'] + _t.get(_t.aand)
            premise = premise[0:-4]
        else:
            premise = premises

        w = (_t.get(_t.wrong)[0:1].lower() if start_lower_case else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
        r = (_t.get(_t.right)[0:1].lower() if start_lower_case else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]

        w += ', ' + _t.get(_t.itIsFalse)[0:1].lower() + _t.get(_t.itIsFalse)[1:] + ' ' if self.lang == 'de' else ', '
        r += ', ' + _t.get(_t.itIsTrue)[0:1].lower() + _t.get(_t.itIsTrue)[1:] + ' ' if self.lang == 'de' else ', '

        ret_dict['undermine_text'] = w + (_t.get(_t.itIsFalse) if self.lang != 'de' else '') + ' <strong>' + premise + '</strong>.'

        ret_dict['support_text'] = r + (_t.get(_t.itIsTrue) if self.lang != 'de' else '') + ' <strong>' + premise + '</strong>.'

        tmp = _t.get(_t.butIDoNotBelieveCounterFor) if is_attacking else _t.get(_t.butIDoNotBelieveArgumentFor)
        ret_dict['undercut_text'] = r + '<strong>' + premise + '</strong>, '
        ret_dict['undercut_text'] += (_t.get(_t.butIDoNotBelieveArgumentFor) if is_dont_know else tmp)
        ret_dict['undercut_text'] += ' <strong>' + conclusion + '</strong>' + '.'

        ret_dict['overbid_text'] = r + '<strong>' + premise + '</strong>, '
        ret_dict['overbid_text'] += (_t.get(_t.andIDoBelieveArgument) if is_dont_know else _t.get(_t.andIDoBelieveCounterFor))
        ret_dict['overbid_text'] += ' <strong>' + conclusion + '</strong>. '
        ret_dict['overbid_text'] += (_t.get(_t.howeverIHaveEvenStrongerArgumentRejecting) if is_attacking else _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting))
        ret_dict['overbid_text'] += ' <strong>' + conclusion + '</strong>.'

        ret_dict['rebut_text'] = r + '<strong>' + premise + '</strong> '
        ret_dict['rebut_text'] += (_t.get(_t.iAcceptCounter) if is_attacking else _t.get(_t.iAcceptArgument))
        ret_dict['rebut_text'] += ' <strong>' + conclusion + '</strong>. '
        ret_dict['rebut_text'] += (_t.get(_t.howeverIHaveMuchStrongerArgumentAccepting) if is_attacking else _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting))
        ret_dict['rebut_text'] += ' <strong>' + (first_conclusion if first_conclusion else conclusion) + '</strong>.'
        # + (_t.get(_t.doesNotHold) if is_attacking else _t.get(_t.hold)) + '</strong>.'

        if for_island_view and self.lang == 'de':
            ret_dict['undermine_text'] = ret_dict['undermine_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['support_text'] = ret_dict['support_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['undercut_text'] = ret_dict['undercut_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['overbid_text'] = ret_dict['overbid_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['rebut_text'] = ret_dict['rebut_text'][:-1] + ', ' + _t.get(_t.because).lower()

        if with_no_opinion_text:
            ret_dict['step_back_text'] = _t.get(_t.iHaveNoOpinion) + '. ' + _t.get(_t.goStepBack) + '. (' + _t.get(_t.noOtherAttack) + ')'
            ret_dict['no_opinion_text'] = _t.get(_t.iHaveNoOpinion) + '. ' + _t.get(_t.showMeAnotherArgument) + '.'

        return ret_dict

    def get_text_for_confrontation(self, premise, conclusion, sys_conclusion, supportive, attack, confrontation,
                                   reply_for_argument, user_is_attacking, user_arg, sys_arg):
        """
        Text for the confrontation of the system

        :param premise: String
        :param conclusion: String
        :param sys_conclusion: String
        :param supportive: String
        :param attack: String
        :param confrontation: String
        :param reply_for_argument: Boolean
        :param user_is_attacking: Boolean
        :param user_arg: Argument
        :param sys_arg: Argument
        :return: String
        """
        _t = Translator(self.lang)

        #  build some confrontation text
        if self.lang == 'de':
            confrontation = '<strong>' + confrontation + '</strong>'
        else:
            confrontation = '<strong>' + confrontation[0:1].lower() + confrontation[1:] + '</strong>'
            premise = premise[0:1].lower() + premise[1:]
            sys_conclusion = sys_conclusion[0:1].lower() + sys_conclusion[1:]
            conclusion = conclusion[0:1].lower() + conclusion[1:]

        confrontation_text = ''

        # build some confrontation text
        if attack == 'undermine':
            confrontation_text = _t.get(_t.otherParticipantsThinkThat) + ' <strong>' + premise + ' '
            confrontation_text += _t.get(_t.hold) if sys_arg.is_supportive else _t.get(_t.doesNotHold)
            confrontation_text += '</strong>, ' + _t.get(_t.because).lower() + ' ' + confrontation

        elif attack == 'rebut':
            #
            db_users_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=user_arg.premisesgroup_uid).join(Statement).first()
            db_votes = DBDiscussionSession.query(VoteStatement).filter_by(statement_uid=db_users_premise.statements.uid).all()

            # distinguish between reply for argument and reply for premise group
            if reply_for_argument:  # reply for argument
                # changing arguments for better understanding
                if not user_arg.is_supportive:
                    user_is_attacking = not user_is_attacking
                    conclusion = sys_conclusion
                if user_is_attacking:
                    confrontation_text = _t.get(_t.otherUsersClaimStrongerArgumentRejecting)
                else:
                    confrontation_text = _t.get(_t.otherUsersClaimStrongerArgumentAccepting)
                confrontation_text += ' <strong>' + conclusion + '</strong>.' + ' ' + _t.get(_t.theySay)
                confrontation_text += ' ' if self.lang == 'de' else ': '
                confrontation_text += confrontation
            else:  # reply for premise group
                confrontation_text = _t.get(_t.otherParticipantsAgreeThat) if len(db_votes) > 1 else _t.get(_t.otherParticipantsDontHaveOpinion)
                confrontation_text += ' <strong>' + premise + '</strong>, '
                confrontation_text += _t.get(_t.strongerStatementForAccepting) if user_is_attacking else _t.get(_t.strongerStatementForRecjecting)
                confrontation_text += ' <strong>' + conclusion + '</strong>.' + ' '
                confrontation_text += _t.get(_t.theySay)
                confrontation_text += ' ' if self.lang == 'de' else ': '
                confrontation_text += confrontation

        elif attack == 'undercut':
            confrontation_text = _t.get(_t.otherParticipantsAgreeThat) + ' <strong>' + premise + '</strong>, '
            confrontation_text += (_t.get(_t.butTheyDoNotBelieveArgument) if supportive else _t.get(_t.butTheyDoNotBelieveCounter))
            confrontation_text += ' <strong>' + conclusion + '</strong>'
            if self.lang == 'de':
                confrontation_text += '. ' + _t.get(_t.theyThink)
            else:
                confrontation_text += ', ' + _t.get(_t.because).lower() + ' ' + _t.get(_t.theyThink).lower()
            confrontation_text += ' ' if self.lang == 'de' else ': '
            confrontation_text += confrontation

        sys_text = confrontation_text + '.<br><br>' + _t.get(_t.whatDoYouThinkAboutThat) + '?'
        return sys_text

    def __get_text_dict_for_attacks_only(self, premises, conclusion, start_lower_case):
        """

        :param premises: String
        :param conclusion: String
        :param start_lower_case: Boolean
        :return: dict()
        """
        _t = Translator(self.lang)
        ret_dict = dict()

        if conclusion[-1] == '.':
            conclusion = conclusion[:-1]

        premise = ''
        for p in premises:
            premise += premises[p]['text'] + _t.get(_t.aand)
        premise = premise[0:-4]

        w = (_t.get(_t.wrong)[0:1].lower() if start_lower_case else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
        r = (_t.get(_t.right)[0:1].lower() if start_lower_case else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]
        counter_justi = ' <strong>' + conclusion + ', ' + _t.get(t.because).toLocaleLowerCase() + ' ' + premise + '</strong>'

        ret_dict['undermine_text'] = w + ', <strong>' + premise + '</strong>.'
        ret_dict['undercut_text'] = r + ', <strong>' + conclusion + '</strong>, ' + _t.get(_t.butIDoNotBelieveArgumentFor) + ' ' + counter_justi + '.'
        ret_dict['rebut_text'] = r + ', <strong>' + premise + '</strong> ' + _t.get(_t.iAcceptArgument) + ' <strong>' + conclusion + '</strong>. '\
                                 + _t.get(_t.howeverIHaveMuchStrongerArgumentRejecting) + ' <strong>' + conclusion + '</strong>.'
        ret_dict['no_opinion_text'] = _t.get(_t.iNoOpinion) + ': <strong>' + conclusion + ', ' + _t.get(_t.because).toLocaleLowerCase() \
                                      + ' ' + premise + '</strong>. ' + _t.get(_t.goStepBack) + '.'
        return ret_dict
