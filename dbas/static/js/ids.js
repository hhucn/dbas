/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

/**
 * ID's
 * @type {string}
 */
var addReasonButtonId 							= 'add-reason';
var addPositionButtonId 						= 'add-position';
var addStatementContainerId 					= 'add-statement-container';
var addStatementContainerH4Id 					= 'add-statement-container-h4';
var addStatementContainerMainInputId 			= 'add-statement-container-main-input';
var addStatementContainerMainInputIntroId		= 'add-statement-container-main-input-intro';
var addProTextareaId 							= 'add-pro-textarea';
var addConTextareaId 							= 'add-con-textarea';
var adminsSpaceForUsersId 						= 'admins-space-users';
var adminsSpaceForAttacksId 					= 'admins-space-attacks';
var addStatementErrorContainer 					= 'add-statement-error-container';
var addStatementErrorMsg 						= 'add-statement-error-msg';
var argumentBloggingSidebarId 					= 'argument-blogging-sidebar';
var closeStatementContainerId 					= 'close-statement-container';
var closeIslandViewContainerId 					= 'close-island-view-container';
var confirmDialogAcceptBtn 						= 'confirm-dialog-accept-btn';
var confirmDialogRefuseBtn 						= 'confirm-dialog-refuse-btn';
var contactLink 								= 'contact-link';
var contentLink 								= 'content-link';
var conPositionColumnId 						= 'con-position-column';
var conPositionTextareaId 						= 'con-textareas';
var conIslandId 								= 'con-island';
var deleteTrackButtonId 						= 'delete-track';
var discussionsDescriptionId 					= 'discussions-description';
var discussionsAvoidanceDescriptionId 			= 'discussions-avoidance-description';
var discussionContainerId 						= 'discussion-container';
var discussionSpaceId 							= 'discussions-space';
var discussionAvoidanceSpaceId 					= 'discussions-avoidance-space';
var discussionFailureRowId 						= 'discussion-failure-row';
var discussionFailureMsgId 						= 'discussion-failure-msg';
var displayControlContainerId 					= 'display-control-container';
var discussionErrorDescriptionId 				= 'discussion-error-description';
var discussionSuccessDescriptionId 				= 'discussion-success-description';
var issueDropdownListID							= 'dropdown-issue-list';
var editStatementButtonId 						= 'edit-statement';
var emailInputId 								= 'email-input';
var forgotPasswordText 							= 'forgot-password-text';
var generatePasswordBodyId 						= 'generate-password-body';
var headingProPositionTextId 					= 'heading-pro-positions';
var headingConPositionTextId 					= 'heading-contra-positions';
var hiddenDiscussionInformationParametersId 	= 'hidden-discussion-information-parameters';
var hiddenDiscussionInformationServiceId 		= 'hidden-discussion-information-service';
var hiddenCSRFTokenId 							= 'hidden_csrf_token';
var insertStatementForm 						= 'insert-statement-form';
var islandViewContainerId 						= 'island-view-container';
var islandViewContainerH4Id 					= 'island-view-container-h4';
var islandViewAddArgumentsBtnid 				= 'island-view-add-arguments';
var issueDropdownButtonID						= 'issue-dropdown';
var issueDateId									= 'issue-date';
var listAllUsersButtonId 						= 'list-all-users';
var listAllUsersAttacksId 						= 'list-all-attacks';
var loginLink 									= 'login-link';
var languageDropdownId 							= 'language-dropdown';
var minimapId 									= 'navigation-minimap-container';
var navbarLeft									= 'navbar-left';
var newsLink 									= 'news-link';
var newsBodyId 									= 'news-body';
var nickInputId 								= 'nick-input';
var passwordInputId 							= 'password-input';
var passwordconfirmInputId 						= 'passwordconfirm-input';
var proPositionColumnId 						= 'pro-position-column';
var proPositionTextareaId 						= 'pro-textareas';
var proIslandId 								= 'pro-island';
var popupConfirmDialogId 						= 'confirm-dialog';
var popupEditStatementId 						= 'popup-edit-statement';
var popupEditStatementTableId					= 'edit_statement_table';
var popupEditStatementShowLogButtonId 			= 'show_log_of_statement';
var popupEditStatementCloseButtonXId 			= 'popup-edit-statement-close';
var popupEditStatementCloseButtonId 			= 'popup-edit-statement-close-button';
var popupEditStatementTextareaId 				= 'popup-edit-statement-textarea';
var popupEditStatementContentId 				= 'popup-edit-statement-content';
var popupEditStatementLogfileHeaderId 			= 'popup-edit-statement-logfile-header';
var popupEditStatementLogfileSpaceId 			= 'popup-edit-statement-logfile';
var popupEditStatementSubmitButtonId 			= 'popup-edit-statement-submit';
var popupEditStatementDescriptionId 			= 'popup-edit-statement-description-p';
var popupEditStatementWarning					= 'popup-edit-statement-warning';
var popupEditStatementWarningMessage 			= 'popup-edit-statement-warning-message';
var popupEditStatementErrorDescriptionId 		= 'popup-edit-statement-error-description';
var popupEditStatementSuccessDescriptionId 		= 'popup-edit-statement-success-description';
var popupHowToWriteText 						= 'popup-write-text';
var popupHowToWriteTextCloseButton 				= 'popup-write-text-close-button';
var popupHowToWriteTextClose 					= 'popup-write-text-close';
var popupHowToWriteTextOkayButton 				= 'popup-write-text-okay-button';
var popupLogin									= 'popup_login';
var popupLoginFailed 							= 'popup-login-failed';
var popupLoginSuccess 							= 'popup-login-success';
var popupLoginForgotPasswordBody				= 'forgot-password-body';
var popupLoginForgotPasswordText				= 'forgot-password-text';
var popupLoginGeneratePassword					= 'generate-password';
var popupLoginGeneratePasswordBody				= 'generate-password-body';
var popupLoginCloseButton 						= 'popup-login-close-button';
var popupLoginRegistrationSuccess 				= 'popup-login-registration-success';
var popupLoginRegistrationFailed 				= 'popup-login-registration-failed';
var popupLoginButtonRegister					= 'popup-login-button-register';
var popupLoginButtonLogin						= 'popup-login-button-login';
var popupLoginButtonRequest						= 'popup-login-button-request';
var popupLoginWarningMessage					= 'popup-login-warning-message';
var popupLoginWarningMessageText 				= 'popup-login-warning-message-text';
var popupLoginInlineRadioGenderN 				= 'inlineRadioGender1';
var popupLoginInlineRadioGenderF 				= 'inlineRadioGender2';
var popupLoginInlineRadioGenderM 				= 'inlineRadioGender3';
var popupUrlSharingLongUrlButtonID 				= 'popup-url-sharing-long-url-button';
var popupUrlSharingId 							= 'popup-url-sharing';
var popupUrlSharingCloseButtonXId 				= 'popup-url-sharing-close';
var popupUrlSharingCloseButtonId 				= 'popup-url-sharing-close-button';
var popupUrlSharingInputId 						= 'popup-url-sharing-input';
var popupUrlSharingDescriptionPId 				= 'popup-url-sharing-description-p';
var restartDiscussionButtonId 					= 'restart-discussion';
var radioButtonGroup 							= 'radioButtonGroup';
var trackFailureMessageId 						= 'track-failure-msg';
var trackSuccessMessageId 						= 'track-success-msg';
var translationLink 							= 'link-trans-';
var translationLinkDe 							= 'link-trans-de';
var translationLinkEn 							= 'link-trans-en';
var scStyleGroupId 								= 'sc-display-style';
var scStyle1Id 									= 'sc-style-1';
var scStyle2Id 									= 'sc-style-2';
var scStyle3Id 									= 'sc-style-3';
var shareUrlId 									= 'share-url';
var shareUrlButtonMail 							= 'share-url-mail';
var shareUrlButtonTwitter 						= 'share-url-twitter';
var shareUrlButtonGoogle 						= 'share-url-google';
var shareUrlButtonFacebook 						= 'share-url-facebook';
var shareButtonMail 							= 'share-mail';
var shareButtonTwitter 							= 'share-twitter';
var shareButtonGoogle 							= 'share-google';
var shareButtonFacebook 						= 'share-facebook';
var sendNewStatementId 							= 'send-new-statement';
var sendNewsButtonId 							= 'send-news';
var switchLangIndicatorEnId						= 'switch-lang-indicator-en';
var switchLangIndicatorDeId						= 'switch-lang-indicator-de';
var trackTableSuccessId 						= 'track-table-success';
var trackTableFailureId 						= 'track-table-failure';
var trackTableSpaceId 							= 'track-table-space';
var userfirstnameInputId 						= 'userfirstname-input';
var userlastnameInputId 						= 'userlastname-input';
var writingNewsFailedId 						= 'writing-news-failed';
var writingNewsSuccessId 						= 'writing-news-success';
var writingNewsFailedMessageId 					= 'writing-news-failed-message';
var writingNewsSuccessMessageId 				= 'writing-news-success-message';
var writingNewNewsTitleId 						= 'writing-news-title';
var writingNewNewsTextId 						= 'writing-news-text';


// classes and id's
var attr_id 				= 'id';
var attr_relation 			= 'relation';
var attr_premisse 			= 'premisse';
var attr_start 				= 'start';
var attr_long_id 			= 'long_id';
var attr_conclusion_id 		= 'conclusion_id';
var attr_confrontation_uid 	= 'confrontation_uid';
var attr_current_attack 	= 'current_attack';
var attr_premissegroup_uid 	= 'premissegroup_uid';
var attr_undermine 			= 'undermine';
var attr_support 			= 'support';
var attr_undercut 			= 'undercut';
var attr_overbid 			= 'overbid';
var attr_rebut 				= 'rebut';
var attr_no_opinion 		= 'noopinion';
var id_pro 					= 'pro';
var id_con 					= 'con';