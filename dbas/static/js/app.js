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
					'#' + loginLink,
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
 * Displays dialog for language translation and send ajax requests
 * @param id of the selected translation link
 */
function displayConfirmTranslationDialog(id) {
	// if parent is already active, nothing will happen
	if ($('#' + translationLink + id).parent().hasClass('active')){
		return;
	}
	// display dialog
	$('#' + popupConfirmDialogId).modal('show');
	$('#' + popupConfirmDialogId + ' h4.modal-title').text(confirmation);
	$('#' + popupConfirmDialogId + ' div.modal-body').text(confirmTranslation);
	// ask for display switch
	$('#' + confirmDialogAcceptBtn).click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		// ajax
		switchDisplayLanguage(id);
	});
	$('#' + confirmDialogRefuseBtn).click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
	});
}

/**
 * Will display a dialog, when we are on the content page, otherwise it will change de language
 * @param path current path
 * @param lang current language code
 */
function language_switcher (path, lang){
	// preserve reload, when the user is arguing
	if (path == 'content')
		displayConfirmTranslationDialog(lang);
	else
		ajaxSwitchDisplayLanguage(lang);
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
	} else {
		$('#' + translationLinkEn).parent().removeClass('active');
		$('#' + translationLinkDe).parent().addClass('active');
		$('.logo').attr('src','../static/images/logo_de.png');
	}
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
	$('#generate-password-body').hide();
}

function prepareLoginRegistrationPopup(){
	// hide on startup
	hideExtraViewsOfLoginPopup();
	$('#' + popupLoginButtonLogin).show();
	$('#generate-password-body').hide();

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

	$('#forgot-password-text').click(function(){
		if ($('#' + popupLoginForgotPasswordBody).is(':visible')){
			$('#' + popupLoginForgotPasswordBody).hide();
			$('#' + popupLoginForgotPasswordText).text('Forgot Password?');
		} else {
			$('#' + popupLoginForgotPasswordBody).show();
			$('#' + popupLoginForgotPasswordText).text('Hide Password Request');
		}
	});

	$('#' + popupLoginGeneratePassword + ' > a').click(function(){
		if ($('#' + popupLoginGeneratePasswordBody).is(':visible')){
			$('#' + popupLoginGeneratePasswordBody).hide();
			$('#' + popupLoginGeneratePassword + ' > a span').text('Generate secure password');
		} else {
			$('#' + popupLoginGeneratePasswordBody).show();
			$('#' + popupLoginGeneratePassword + ' > a span').text('Hide Generator');
		}
	});

	$('#' + popupLoginCloseButton).click(function(){
		hideExtraViewsOfLoginPopup();
		$('#' + popupLogin).modal('hide');

	});

	$('#' + popupLoginButtonRegister).click(function(){
		var userfirstname = $('#userfirstname-input').val(),
			userlastname = $('#userlastname-input').val(),
			nick = $('#nick-input').val(),
			email = $('#email-input').val(),
			password = $('#password-input').val(),
			passwordconfirm = $('#passwordconfirm-input').val();
			ajaxRegistration();

		if (!userfirstname || /^\s*$/.test(userfirstname) || 0 === userfirstname.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check your first name, because the input is empty!');

		} else if (!userlastname || /^\s*$/.test(userlastname) || 0 === userlastname.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check your last name, because the input is empty!');

		} else if (!nick || /^\s*$/.test(nick) || 0 === nick.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check your nickname, because the input is empty!');

		} else if (!email || /^\s*$/.test(email) || 0 === email.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check email, because the input is empty!');

		} else if (!password || /^\s*$/.test(password) || 0 === password.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check password, because the input is empty!');

		} else if (!passwordconfirm || /^\s*$/.test(passwordconfirm) || 0 === passwordconfirm.length) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check the confirmation of your password, because the input is empty!');

		} else if (password !== passwordconfirm) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text('Better check your passwords, because they are not equal!');

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
		alert('Unfortunately, the language could not be switched');
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
			$('#' + popupLoginFailed + '-message').text("Request failed");
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
		$('#' + popupLoginRegistrationFailed + '-message').text(request_failed);
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
		$('#' + popupLoginRegistrationFailed + '-message').text(request_failed);
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
		$('#' + popupLoginFailed + '-message').text(parsedData.message);
	} else {
		$('#' + popupLoginForgotPasswordBody).hide();
		$('#' + popupLoginFailed).hide();
		$('#' + popupLoginSuccess).show();
		$('#' + popupLoginSuccess + '-message').text(parsedData.message);
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

	// set current file to active
	var path = window.location.href;
		 if (path.indexOf('contact') != -1){ 	setLinkActive('#' + contactLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf('login') != -1){		setLinkActive('#' + loginLink);		$('#' + navbarLeft).hide(); }
	else if (path.indexOf('news') != -1){		setLinkActive('#' + newsLink);		$('#' + navbarLeft).hide(); }
	else if (path.indexOf('content') != -1){ 	setLinkActive('#' + contentLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf('settings') != -1 ||
			 path.indexOf('imprint') != -1 ||
			 path.indexOf('logout') != -1){											$('#' + navbarLeft).hide(); }
	else { 										setLinkActive(''); 					$('#' + navbarLeft).show(); }

	// language switch
	$('#' + translationLinkDe).click(function(){ language_switcher(path, 'de') });
	$('#' + translationLinkEn).click(function(){ language_switcher(path, 'en') });
	$('#' + translationLinkDe + ' img').click(function(){ language_switcher(path, 'de') });
	$('#' + translationLinkEn + ' img').click(function(){ language_switcher(path, 'en') });

	prepareLoginRegistrationPopup();

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});

});