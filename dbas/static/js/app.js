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
		if (jQuery(this).scrollTop() > 500) {
			$('.back-to-top').fadeIn('slow');
			setTimeout(function() { $('.back-to-top').fadeOut('slow'); }, 2500);
		} else {
			$('.back-to-top').fadeOut('slow');
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

function changeBackgroundOnScroll(){
	$(window).scroll(function () {
		if (jQuery(this).scrollTop() > 10) {
			$('#custom-bootstrap-menu').removeClass('navbar-transparent');
		} else {
			$('#custom-bootstrap-menu').addClass('navbar-transparent');
		}
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
	$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		if (isRestartingDiscussion)
			window.location.href = mainpage + 'discussion/start/issue=' + functionForAccept;
		else
			functionForAccept();
	});
	$('#' + popupConfirmDialogRefuseBtn).show().click( function () {
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
		$('#' + popupConfirmChecbkoxDialogRefuseBtn).click( function () {
			$('#' + popupConfirmChecbkoxDialogId).modal('hide');
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

/**
 * Changes the value and title of every button
 */
function setButtonLanguage(){
	$('#' + reportButtonId).prop('value', _t(report)).prop('title', _t(reportTitle));
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
	$('#' + deleteHistoryButtonId).prop('value', _t(deleteHistory)).prop('title', _t(deleteHistory));
	$('#' + requestHistoryButtonId).prop('value', _t(requestHistory)).prop('title', _t(requestHistory));
	$('#' + settingsPasswordSubmitButtonId).prop('value', _t(passwordSubmit)).prop('title', _t(passwordSubmit));
	// $('#' + popupEditStatementShowLogButtonId).prop('value', _t(changelog)).prop('title', _t(changelog));
	$('#' + contactSubmitButtonId).prop('value', _t(contactSubmit)).prop('title', _t(contactSubmit));
	$('#' + discussionStartToggleButtonId).next().children().eq(0).text(_t(attackPosition));
	$('#' + discussionStartToggleButtonId).next().children().eq(1).text(_t(supportPosition));
	$('#' + startDiscussionButtonId).prop('value', _t(letsGo)).prop('title', _t(letsGo));
}

function setPiwikOptOutLink(lang){
	var src = 'https://dbas.cs.uni-duesseldorf.de/piwik/index.php?module=CoreAdminHome&action=optOut&idsite=1&language=';
	if (lang === 'de')	src += 'de';
	else 				src += 'en';
	$('#piwik-opt-out-iframe').attr('src',src);
}

/**
 *
 */
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

/**
 * Prepares the login popup
 */
function prepareLoginRegistrationPopup(){
	// hide on startup
	hideExtraViewsOfLoginPopup();
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

	$('#' + popupLoginButtonLogin).show().click(function() {
		ajaxLogin()
	}).keypress(function(e) { if (e.which == 13) { ajaxRegistration() } });

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
		$('#' + popupLoginButtonLogin).show();
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

		if (!userfirstname || /^\s*$/.test(userfirstname) || 0 === userfirstname.length) {
			$('#' + popupLoginRegistrationFailed).fadeIn("slow");
			$('#' + popupLoginRegistrationFailed + '-message').text(_t(checkFirstname));

		} else if (!userlastname || /^\s*$/.test(userlastname) || 0 === userlastname.length) {
			$('#' + popupLoginRegistrationFailed).fadeIn("slow");
			$('#' + popupLoginRegistrationFailed + '-message').text(_t(checkLastname));

		} else if (!nick || /^\s*$/.test(nick) || 0 === nick.length) {
			$('#' + popupLoginRegistrationFailed).fadeIn("slow");
			$('#' + popupLoginRegistrationFailed + '-message').text(_t(checkNickname));

		} else if (!email || /^\s*$/.test(email) || 0 === email.length) {
			$('#' + popupLoginRegistrationFailed).fadeIn("slow");
			$('#' + popupLoginRegistrationFailed + '-message').text(_t(checkEmail));

		} else if (!password || /^\s*$/.test(password) || 0 === password.length) {
			$('#' + popupLoginRegistrationFailed).fadeIn("slow");
			$('#' + popupLoginRegistrationFailed + '-message').text(_t(checkPassword));

		} else if (!passwordconfirm || /^\s*$/.test(passwordconfirm) || 0 === passwordconfirm.length) {
			$('#' + popupLoginRegistrationFailed).fadeIn("slow");
			$('#' + popupLoginRegistrationFailed + '-message').text(_t(checkConfirmation));

		} else if (password !== passwordconfirm) {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(_t(checkPasswordEqual));

		} else {
			$('#' + popupLoginWarningMessage);
			ajaxRegistration();
		}

	});

	// bind enter key
	$('#' + loginUserId).keypress(function(e) {							if (e.which == 13) {	ajaxLogin()			}	});
	$('#' + loginPwId).keypress(function(e) {							if (e.which == 13) {	ajaxLogin()			}	});
	$('#' + popupLoginUserfirstnameInputId).keypress(function(e) {		if (e.which == 13) {	ajaxRegistration()	}	});
	$('#' + popupLoginUserlastnameInputId).keypress(function(e) {		if (e.which == 13) {	ajaxRegistration()	}	});
	$('#' + popupLoginNickInputId).keypress(function(e) {				if (e.which == 13) {	ajaxRegistration()	}	});
	$('#' + popupLoginEmailInputId).keypress(function(e) {				if (e.which == 13) {	ajaxRegistration()	}	});
	$('#' + popupLoginPasswordconfirmInputId).keypress(function(e) {	if (e.which == 13) {	ajaxRegistration()	}	});

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
	var user = $('#' + loginUserId).val(),
		password = $('#' + loginPwId).val(),
		url = window.location.href;
		// csrfToken = $('#' + hiddenCSRFTokenId).val(); // Todo CSRF
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
			if (window.location.href.indexOf('settings') != 0){
				window.location.href = mainpage;
			} else {
				location.reload(); // TODO page will not be reloaded properly
			}
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
		password = $('#' + popupLoginPasswordInputId).val(),
		passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val(),
		gender = '';
		// csrfToken = $('#' + hiddenCSRFTokenId).val(); // Todo CSRF

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
				passwordconfirm: passwordconfirm,
				lang: getLanguage()},
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
		data: { email: email, lang: getLanguage()},
		dataType: 'json',
		async: true
	}).done(function ajaxPasswordRequestDone(data) {
		callbackIfDoneForPasswordRequest(data);
	}).fail(function ajaxPasswordRequestFail() {
		$('#' + popupLoginRegistrationFailed).show();
		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
	});
}

/**
 * Get-Request for an roundhouse kick
 */
function ajaxRoundhouseKick(){
	$.ajax({
		url: 'additional_service',
		type: 'GET',
		data: {type:'chuck'},
		global: false,
		async: true
	}).done(function ajaxPasswordRequestDone(data) {
		if (data.type == 'success'){
			displayConfirmationDialog('Chuck Norris Fact #' + data.value.id,  '<h4>' + data.value.joke + '</h4>\n\n<span' +
					' style="float:right;">powered by <a href="http://www.icndb.com/">http://www.icndb.com/</a></span>');
			$('#' + popupConfirmDialogAcceptBtn).removeClass('btn-success');
			$('#' + popupConfirmDialogRefuseBtn).hide();

		}
	});
}

/**
 * Get your mama with broadband dsl, because she is so ...
 */
function ajaxMama(){
	$.ajax({
		url: 'additional_service',
		type: 'GET',
		data: {type:'mama'},
		global: false,
		async: true
	}).done(function ajaxPasswordRequestDone(data) {
		displayConfirmationDialog('Yo Mamma',  '<h4>' + data.joke + '</h4>\n\n<span' +
				' style="float:right;">powered by <a href="http://yomomma.info/">http://yomomma.info/</a></span>');
		$('#' + popupConfirmDialogAcceptBtn).removeClass('btn-success');
		$('#' + popupConfirmDialogRefuseBtn).hide();
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
	setPiwikOptOutLink(new_lang);
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
	var path = window.location.href, lang = $('#hidden_language').val();

	jmpToChapter();

	goBackToTop();

	//changeBackgroundOnScroll();

	setActiveLanguage(lang);
	setButtonLanguage();
	setPiwikOptOutLink(lang);

	// set current file to active
		 if (path.indexOf(urlContact) != -1){ 	setLinkActive('#' + contactLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlLogin) != -1){		setLinkActive('#' + loginLinkId);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlNews) != -1){		setLinkActive('#' + newsLink);		$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlContent) != -1){ 	setLinkActive('#' + contentLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlSettings) != -1 ||
			 path.indexOf(urlImprint) != -1 ||
			 path.indexOf(urlLogout) != -1){											$('#' + navbarLeft).hide(); }
	else { 											setLinkActive(''); 					$('#' + navbarLeft).show(); }

	// language switch
	$('#' + translationLinkDe).click(function(){ ajaxSwitchDisplayLanguage('de') });
	$('#' + translationLinkEn).click(function(){ ajaxSwitchDisplayLanguage('en') });
	$('#' + translationLinkDe + ' img').click(function(){ ajaxSwitchDisplayLanguage('de') });
	$('#' + translationLinkEn + ' img').click(function(){ ajaxSwitchDisplayLanguage('en') });
	$('#roundhousekick').click(function(){ ajaxRoundhouseKick(); });
	//$('#yomamma').click(function(){ ajaxMama(); });
	$('#' + logoutLinkId).click(function(){ ajaxLogout()});

	// gui preperation
	prepareLoginRegistrationPopup();

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});

});
