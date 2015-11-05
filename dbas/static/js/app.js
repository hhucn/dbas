/*global $, jQuery, alert, addActiveLinksInNavBar, removeActiveLinksInNavBar*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

// just a countdowntimer by http://stackoverflow.com/a/1192001/2648872
function Countdown(options) {
	'use strict';
	var timer,
		instance = this,
		seconds = options.seconds || 10,
		updateStatus = options.onUpdateStatus || function () {},
		counterEnd = options.onCounterEnd || function () {};

	function decrementCounter() {
		updateStatus(seconds);
		if (seconds === 0) {
			counterEnd();
			instance.stop();
		}
		seconds = seconds - 1;
	}

	this.start = function () {
		clearInterval(timer);
		timer = 0;
		seconds = options.seconds;
		timer = setInterval(decrementCounter, 1000);
	};

	this.stop = function () {
		clearInterval(timer);
	};
}

/**
 *
 * @param linkname
 */
function setLinkActive(linkname) {
	'use strict';
	var linkIds = ['#' + contactLink,
					'#' + loginLinkId,
					'#' + newsLink,
					'#' + contentLink],
		i;
	for (i = 0; i < linkIds.length; i++) {
		if (linkIds[i] === linkname) {
			$(linkIds[i]).addClass('active');
		} else {
			$(linkIds[i]).removeClass('active');
		}
	}
}

/**
 * Jumps to clicked chapter, which is defined in the header
 */
function jmpToChapter() {
	// jump to chapter-function
	$('a[href^=#]').on('click', function (e) {
		try {
			var href = $(this).attr('href');
			$('html, body').animate({
				scrollTop: ($(href).offset().top - 100)
			}, 'slow');
			e.preventDefault();
		} catch (err) {
			// something like 'Cannot read property 'top' of undefined'
		}
	});
}

/**
 * Go back to top arrow
 */
function goBackToTop() {
	$(window).scroll(function () {
		if (jQuery(this).scrollTop() > 220) {
			$('.back-to-top').fadeIn(500);
		} else {
			$('.back-to-top').fadeOut(500);
		}
	});

	// going back to top
	$('.back-to-top').click(function (event) {
		event.preventDefault();
		$('html, body').animate({
			scrollTop: 0
		}, 500);
		return false;
	});
}

/**
 * Displays dialog
 * @param titleText
 * @param bodyText
 * @param functionForAccept
 * @param isRestartingDiscussion
 */
function displayConfirmationDialog(titleText, bodyText, functionForAccept, isRestartingDiscussion) {
	// display dialog
	$('#' + popupConfirmDialogId).modal('show');
	$('#' + popupConfirmDialogId + ' h4.modal-title').text(titleText);
	$('#' + popupConfirmDialogId + ' div.modal-body').html(bodyText);
	$('#' + popupConfirmDialogAcceptBtn).click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		if (isRestartingDiscussion)
			window.location.href = mainpage + 'discussion/start/issue=' + functionForAccept;
		else
			functionForAccept();
	});
	$('#' + popupConfirmDialogRefuseBtn).click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
	});
}

/**
 * Displays dialog with checkbox
 * @param titleText
 * @param bodyText
 * @param checkboxText
 * @param functionForAccept
 * @param isRestartingDiscussion
 */
function displayConfirmationDialogWithCheckbox(titleText, bodyText, checkboxText, functionForAccept, isRestartingDiscussion) {
	// display dialog only if the cookie was not set yet
	if (new Helper().isCookieSet(WARNING_CHANGE_DISCUSSION_POPUP)){
		window.location.href = mainpage + 'discussion/start/issue=' + functionForAccept;
	} else {
		$('#' + popupConfirmChecbkoxDialogId).modal('show');
		$('#' + popupConfirmChecbkoxDialogId + ' h4.modal-title').text(titleText);
		$('#' + popupConfirmChecbkoxDialogId + ' div.modal-body').html(bodyText);
		$('#' + popupConfirmChecbkoxDialogTextId).text(checkboxText);
		$('#' + popupConfirmChecbkoxDialogAcceptBtn).click( function () {
			$('#' + popupConfirmChecbkoxDialogId).modal('hide');
			// maybe set a cookie
			if ($('#' + popupConfirmChecbkoxId).prop('checked')) {
				new Helper().setCookie(WARNING_CHANGE_DISCUSSION_POPUP);
			}

			if (isRestartingDiscussion)
				window.location.href = mainpage + 'discussion/start/issue=' + functionForAccept;
			else
				functionForAccept();

		});
		$('#' + popupConfirmDialogRefuseBtn).click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		})
	}
}

/**
 * DOM manipulation for the active class
 * @param lang current language code
 */
function setActiveLanguage(lang){
	if (lang === 'en'){
		$('#' + translationLinkDe).parent().removeClass('active');
		$('#' + translationLinkEn).parent().addClass('active');
		$('.logo').attr('src','../static/images/logo.png');
		$('#' + switchLangIndicatorEnId).show();
		$('#' + switchLangIndicatorDeId).hide();
		// Buttons
	} else {
		$('#' + translationLinkEn).parent().removeClass('active');
		$('#' + translationLinkDe).parent().addClass('active');
		$('.logo').attr('src','../static/images/logo_de.png');
		$('#' + switchLangIndicatorEnId).hide();
		$('#' + switchLangIndicatorDeId).show();
	}
}

function setButtonLanguage(){
	// $('#' + reportStatementButtonId).prop('value', _t(report)).prop('title', _t(reportTitle));
	$('#' + restartDiscussionButtonId).prop('value', _t(restartDiscussion)).prop('title', _t(restartDiscussionTitle));
	$('#' + editStatementButtonId).prop('value', _t(edit)).prop('title', _t(editTitle));
	$('#' + scStyle1Id).prop('value', _t(dialogView)).prop('title', _t(dialogViewTitle));
	$('#' + scStyle2Id).prop('value', _t(islandView)).prop('title', _t(islandViewTitle));
	$('#' + scStyle3Id).prop('value', _t(completeView)).prop('title', _t(completeViewTitle));
	$('#' + islandViewAddArgumentsBtnid).prop('value', _t(addArguments)).prop('title', _t(addArguments));
	$('#' + sendNewStatementId).prop('value', _t(acceptIt)).prop('title', _t(acceptItTitle));
	$('#' + listAllUsersAttacksId).prop('value', _t(showAllAttacks)).prop('title', _t(showAllAttacks));
	$('#' + listAllUsersButtonId).prop('value', _t(showAllUsers)).prop('title', _t(showAllUsers));
	$('#' + deleteTrackButtonId).prop('value', _t(deleteTrack)).prop('title', _t(deleteTrack));
	$('#' + requestTrackButtonId).prop('value', _t(requestTrack)).prop('title', _t(requestTrack));
	$('#' + settingsPasswordSubmitButtonId).prop('value', _t(passwordSubmit)).prop('title', _t(passwordSubmit));
	// $('#' + popupEditStatementShowLogButtonId).prop('value', _t(changelog)).prop('title', _t(changelog));

	// todo every button
}

function hideExtraViewsOfLoginPopup(){
	$('#' + popupLoginWarningMessage).hide();
	$('#' + popupLoginFailed).hide();
	$('#' + popupLoginSuccess).hide();
	$('#' + popupLoginRegistrationSuccess).hide();
	$('#' + popupLoginRegistrationFailed).hide();
	$('#' + popupLoginButtonRegister).hide();
	$('#' + popupLoginButtonLogin).hide();
	$('#' + popupLoginForgotPasswordBody).hide();
	$('#' + generatePasswordBodyId).hide();
}

function prepareLoginRegistrationPopup(){
	// hide on startup
	hideExtraViewsOfLoginPopup();
	$('#' + popupLoginButtonLogin).show();
	$('#' + popupLoginGeneratePasswordBody).hide();

	// switching tabs
	$('.tab-login a').on('click', function (e) {
		e.preventDefault();
		$(this).parent().addClass('active');
		$(this).parent().siblings().removeClass('active');
		var target = $(this).attr('href');
		$('.tab-content > div').not(target).hide();
		$(target).fadeIn(600);

		if ($(this).attr('href').indexOf('signup') != -1){
			$('#' + popupLoginButtonLogin).hide();
			$('#' + popupLoginButtonRegister).show();
		} else {
			$('#' + popupLoginButtonLogin).show();
			$('#' + popupLoginButtonRegister).hide();
		}
	});

	$('#' + popupLoginForgotPasswordText).click(function(){
		if ($('#' + popupLoginForgotPasswordBody).is(':visible')){
			$('#' + popupLoginForgotPasswordBody).hide();
			$('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
		} else {
			$('#' + popupLoginForgotPasswordBody).show();
			$('#' + popupLoginForgotPasswordText).text(_t(hidePasswordRequest));
		}
	});

	$('#' + popupLoginGeneratePassword + ' > a').click(function(){
		if ($('#' + popupLoginGeneratePasswordBody).is(':visible')){
			$('#' + popupLoginGeneratePasswordBody).hide();
			$('#' + popupLoginGeneratePassword + ' > a span').text(_t(generateSecurePassword));
		} else {
			$('#' + popupLoginGeneratePasswordBody).show();
			$('#' + popupLoginGeneratePassword + ' > a span').text(_t(hideGenerator));
		}
	});

	$('#' + popupLoginCloseButton).click(function(){
		hideExtraViewsOfLoginPopup();
		$('#' + popupLogin).modal('hide');

	});

	$('#' + popupLoginPasswordInputId).keyup(function popupLoginPasswordInputKeyUp() {
		new PasswordHandler().check_strength($('#' + popupLoginPasswordInputId), $('#' + popupLoginPasswordMeterId), $('#' + popupLoginPasswordStrengthId), $('#' + popupLoginPasswordExtrasId));
	});

	$('#' + popupLoginButtonRegister).click(function(){
		var userfirstname = $('#' + popupLoginUserfirstnameInputId).val(),
			userlastname = $('#' + popupLoginUserlastnameInputId).val(),
			nick = $('#' + popupLoginNickInputId).val(),
			email = $('#' + popupLoginEmailInputId).val(),
			password = $('#' + popupLoginPasswordInputId).val(),
			passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val();
			ajaxRegistration();

		if (!userfirstname || /^\s*$/.test(userfirstname) || 0 === userfirstname.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkFirstname));

		} else if (!userlastname || /^\s*$/.test(userlastname) || 0 === userlastname.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkLastname));

		} else if (!nick || /^\s*$/.test(nick) || 0 === nick.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkNickname));

		} else if (!email || /^\s*$/.test(email) || 0 === email.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkEmail));

		} else if (!password || /^\s*$/.test(password) || 0 === password.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkPassword));

		} else if (!passwordconfirm || /^\s*$/.test(passwordconfirm) || 0 === passwordconfirm.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkConfirmation));

		} else if (password !== passwordconfirm) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkPasswordEqual));

		} else {
			$('#' + popupLoginWarningMessage);
			ajaxRegistration();
		}
		
	});

	$('#' + popupLoginButtonLogin).click(function() {
		ajaxLogin()
	});

	$('#' + popupLoginButtonRequest).click(function() {
		ajaxPasswordRequest();
	});
}

// *********************
//	AJAX
// *********************

/**
 * Sends a request for language change
 * @param new_lang is the shortcut for the language
 */
function ajaxSwitchDisplayLanguage (new_lang){
	$.ajax({
		url: 'ajax_switch_language',
		type: 'POST',
		data: { lang: new_lang},
		dataType: 'json',
		async: true
	}).done(function ajaxSwitchDisplayLanguageDone() {
		callbackIfDoneForSwitchDisplayLanguage(new_lang);
	}).fail(function ajaxSwitchDisplayLanguageFail() {
		alert(_t(languageCouldNotBeSwitched));
	});
}

/**
 *
 */
function ajaxLogin (){
	var user = $('#login-user').val(),
		password = $('#login-pw').val(),
		url = window.location.href;
	$.ajax({
		url: 'ajax_user_login',
		type: 'POST',
		data: { user: user, password: password, url: url},
		dataType: 'json',
		async: true
	}).done(function ajaxLoginDone(data) {
		callbackIfDoneForLogin(data);
	}).fail(function ajaxLoginFail(xhr) {
		if (xhr.status == 200) {
			location.reload(true);
		} else {
			$('#' + popupLoginFailed).show();
			$('#' + popupLoginFailed + '-message').text(_t(requestFailed));
		}
	});
}

/**
 *
 */
function ajaxLogout (){
	var url = window.location.href;
	$.ajax({
		url: 'ajax_user_logout',
		type: 'POST',
		data: { url: url},
		dataType: 'json',
		async: true
	}).done(function ajaxLogoutDone(data) {
	}).fail(function ajaxLogoutFail(xhr) {
		if (xhr.status == 200) {
			location.reload(true);
		} else if (xhr.status == 403) {
			window.location.href = mainpage;
		}
	});
}

/**
 *
 */
function ajaxRegistration (){
	var firstname = $('#userfirstname-input').val(),
		lastname = $('#userlastname-input').val(),
		nickname = $('#nick-input').val(),
		email = $('#email-input').val(),
		password = $('#password-input').val(),
		passwordconfirm = $('#passwordconfirm-input').val(),
		gender = '';

	if ($('#' + popupLoginInlineRadioGenderN).is(':checked'))	gender = 'n';
	if ($('#' + popupLoginInlineRadioGenderM).is(':checked'))	gender = 'm';
	if ($('#' + popupLoginInlineRadioGenderF).is(':checked'))	gender = 'f';

	$.ajax({
		url: 'ajax_user_registration',
		type: 'POST',
		data: { firstname: firstname,
			lastname: lastname,
			nickname: nickname,
			gender: gender,
			email: email,
			password: password,
			passwordconfirm: passwordconfirm},
		dataType: 'json',
		async: true
	}).done(function ajaxRegistrationDone(data) {
		callbackIfDoneForRegistration(data);
	}).fail(function ajaxRegistrationFail() {
		$('#' + popupLoginRegistrationFailed).show();
		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
	});
}

/**
 *
 */
function ajaxPasswordRequest (){
	var email = $('#password-request-email-input').val();
	$.ajax({
		url: 'ajax_user_password_request',
		type: 'POST',
		data: { email: email},
		dataType: 'json',
		async: true
	}).done(function ajaxPasswordRequestDone(data) {
		callbackIfDoneForPasswordRequest(data);
	}).fail(function ajaxPasswordRequestFail() {
		$('#' + popupLoginRegistrationFailed).show();
		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
	});
}

// *********************
//	CALLBACKS
// *********************

/**
 * Callback, when language is switched
 */
function callbackIfDoneForSwitchDisplayLanguage (new_lang) {
	location.reload(true);
	setActiveLanguage(new_lang);
	setButtonLanguage();
}

/**
 *
 * @param data
 */
function callbackIfDoneForLogin(data){
	var parsedData = $.parseJSON(data);
	if (parsedData.success == '0') {
		$('#' + popupLoginFailed).show();
		$('#' + popupLoginFailed + '-message').text(parsedData.message);
	} else {
		$('#' + popupLogin).modal('hide');
		location.reload();
	}
}

/**
 *
 * @param data
 */
function callbackIfDoneForRegistration(data){
	var parsedData = $.parseJSON(data);
	if (parsedData.success == '0') {
		$('#' + popupLoginRegistrationFailed).show();
		$('#' + popupLoginRegistrationSuccess).hide();
		$('#' + popupLoginRegistrationFailed + '-message').text(parsedData.message);
	} else {
		$('#' + popupLoginRegistrationFailed).hide();
		$('#' + popupLoginRegistrationSuccess).show();
		$('#' + popupLoginRegistrationSuccess + '-message').text(parsedData.message);
	}
}

/**
 *
 * @param data
 */
function callbackIfDoneForPasswordRequest(data){
	var parsedData = $.parseJSON(data);
	if (parsedData.success == '0') {
		$('#' + popupLoginFailed).show();
		$('#' + popupLoginSuccess).hide();
		$('#' + popupLoginFailed + '-message').text(_t(parsedData.message));
	} else {
		$('#' + popupLoginForgotPasswordBody).hide();
		$('#' + popupLoginFailed).hide();
		$('#' + popupLoginSuccess).show();
		$('#' + popupLoginSuccess + '-message').text(_t(parsedData.message));
		$('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
	}
}

// *********************
//	MAIN
// *********************

$(document).ready(function () {
	'use strict';

	jmpToChapter();

	goBackToTop();

	setActiveLanguage($('#hidden_language').val());
	setButtonLanguage();

	// set current file to active
	var path = window.location.href;
		 if (path.indexOf('contact') != -1){ 	setLinkActive('#' + contactLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf('login') != -1){		setLinkActive('#' + loginLinkId);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf('news') != -1){		setLinkActive('#' + newsLink);		$('#' + navbarLeft).hide(); }
	else if (path.indexOf('content') != -1){ 	setLinkActive('#' + contentLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf('settings') != -1 ||
			 path.indexOf('imprint') != -1 ||
			 path.indexOf('logout') != -1){											$('#' + navbarLeft).hide(); }
	else { 										setLinkActive(''); 					$('#' + navbarLeft).show(); }

	// language switch
	$('#' + translationLinkDe).click(function(){ ajaxSwitchDisplayLanguage('de') });
	$('#' + translationLinkEn).click(function(){ ajaxSwitchDisplayLanguage('en') });
	$('#' + translationLinkDe + ' img').click(function(){ ajaxSwitchDisplayLanguage('de') });
	$('#' + translationLinkEn + ' img').click(function(){ ajaxSwitchDisplayLanguage('en') });

	prepareLoginRegistrationPopup();

	// logout
	$('#' + logoutLinkId).click(function(){ ajaxLogout()});

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});

});