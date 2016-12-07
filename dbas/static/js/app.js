/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

/**
 *
 * @param linkname name of the link
 */
function setLinkActive(linkname) {
	'use strict';
	$('#navbar-right').find('>li').each(function(){
		$(this).removeClass('active')
	});
	$(linkname).addClass('active');
}

/**
 * Jumps to clicked chapter, which is defined in the header
 */
function jmpToChapter() {
	// jump to chapter-function
	$('a[href^="#"]').on('click', function (e) {
		try {
			const href = $(this).attr('href');
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

/**
 * Display smiley as fallback on (connection) errors
 */
function setGravatarFallback() {
	const body = $('body');
	const img = body.find('.img-circle');
	if (img.length == 0)
		return true;
	
	const src = body.find('.img-circle')[0].src;
	const jqxhr = $.get(src, function() {
    	replace_gravtar_with_default_image(true);
    }).fail(function() {
    	replace_gravtar_with_default_image(false);
    });
}

function replace_gravtar_with_default_image(only_on_error){
	$('body').find('.img-circle').each(function (){
		const icons =
			[  { 'name': 'faces', 'length': 98
			}, { 'name': 'flat-smileys', 'length': 32
			}, { 'name': 'human', 'length': 81
			}, { 'name': 'lego', 'length': 10 }];
		const t = 3;
		const no = Math.floor(Math.random() * icons[t].length);
		const src = mainpage + 'static/images/fallback-' + icons[t].name + '/' +  no + '.svg';
		
		const width = $(this).width();
		if (only_on_error)
			$(this).attr('onerror', 'this.src="' + src + '"');
		else
			$(this).attr('src', src);
		$(this).css('width', width + 'px');
	});
}

/**
 * Displays dialog
 * @param titleText
 * @param bodyText
 * @param functionForAccept
 */
function displayConfirmationDialog(titleText, bodyText, functionForAccept) {
	// display dialog
	$('#' + popupConfirmDialogId).modal('show');
	$('#' + popupConfirmDialogId + ' h4.modal-title').text(titleText);
	$('#' + popupConfirmDialogId + ' div.modal-body').html(bodyText);
	$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		functionForAccept();
	});
	$('#' + popupConfirmDialogRefuseBtn).show().click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
	});
}

/**
 * Displays dialog
 * @param titleText
 * @param bodyText
 */
function displayConfirmationDialogWithoutCancelAndFunction(titleText, bodyText) {
	// display dialog
	$('#' + popupConfirmDialogId).modal('show');
	$('#' + popupConfirmDialogId + ' h4.modal-title').html(titleText);
	$('#' + popupConfirmDialogId + ' div.modal-body').html(bodyText);
	$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
		$('#' + popupConfirmDialogId).modal('hide').find('.modal-dialog').removeClass('modal-sm');
	}).removeClass('btn-success');
	$('#' + popupConfirmDialogRefuseBtn).hide();
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
	if (isCookieSet(WARNING_CHANGE_DISCUSSION_POPUP)){
		window.location.href = functionForAccept;
	} else {
		$('#' + popupConfirmChecbkoxDialogId).modal('show');
		$('#' + popupConfirmChecbkoxDialogId + ' h4.modal-title').text(titleText);
		$('#' + popupConfirmChecbkoxDialogId + ' div.modal-body').html(bodyText);
		$('#' + popupConfirmChecbkoxDialogTextId).text(checkboxText);
		$('#' + popupConfirmChecbkoxDialogAcceptBtn).click( function () {
			$('#' + popupConfirmChecbkoxDialogId).modal('hide');
			// maybe set a cookie
			if ($('#' + popupConfirmChecbkoxId).prop('checked')) {
				setCookieForDays(WARNING_CHANGE_DISCUSSION_POPUP, 7, true);
			}

			if (isRestartingDiscussion) {
				window.location.href = functionForAccept;
			} else {
				functionForAccept();
			}

		});
		$('#' + popupConfirmChecbkoxDialogRefuseBtn).click( function () {
			$('#' + popupConfirmChecbkoxDialogId).modal('hide');
		})
	}
}

/**
 *
 */
function displayBubbleInformationDialog(){
	if (!isCookieSet(BUBBLE_INFOS)){
		const img = $('<img>').attr('src','../static/images/explanation_bubbles_' + ($(document).width() > 992?'long' : 'short') + '.png');
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' .modal-dialog').attr('style', 'width: ' + ($(document).width() > 992? '430' : '200') + 'px;');
		$('#' + popupConfirmDialogId + ' h4.modal-title').html('Introduction');
		$('#' + popupConfirmDialogId + ' div.modal-body').html(img);
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
			setCookieForDays(BUBBLE_INFOS, 30, true);
		}).removeClass('btn-success');
		$('#' + popupConfirmDialogRefuseBtn).hide();
	}
}

/**
 *
 * @param lang
 */
function setPiwikOptOutLink(lang){
	const src = mainpage + 'piwik/index.php?module=CoreAdminHome&action=optOut&idsite=1&language=' + lang;
	$('#piwik-opt-out-iframe').attr('src', src);
}

/**
 *
 */
function setEasterEggs(){
	$('#roundhousekick').click(function(){ new AjaxMainHandler().ajaxRoundhouseKick(); });
	//$('#yomamma').click(function(){ new AjaxMainHandler().ajaxMama(); });
	$('#logo_dbas,#logo_dbas_s').click(function(){
		let counter = parseInt($(this).data('counter'));
		counter += 1;
		if (counter == 7){
			$(this).attr('src', mainpage + 'static/images/dabas.png');
			$('body').find('span').each(function(){
				$(this).text(dolan_translate(dolan_dictionary, $(this).text()));
			});
			$('.popup_author_img').attr('src', mainpage + 'static/images/dolan.png').css('width', '150%');
		}
		$(this).data('counter', counter);
	});
}

/**
 *
 */
function hideExtraViewsOfLoginPopup(){
	$('#' + popupLoginWarningMessage).hide();
	$('#' + popupLoginFailed).hide();
	$('#' + popupLoginSuccess).hide();
	$('#' + popupLoginInfo).hide();
	$('#' + popupLoginRegistrationSuccess).hide();
	$('#' + popupLoginRegistrationFailed).hide();
	$('#' + popupLoginRegistrationInfo).hide();
	$('#' + popupLoginButtonRegister).hide();
	$('#' + popupLoginButtonLogin).hide();
	$('#' + popupLoginForgotPasswordBody).hide();
	$('#' + generatePasswordBodyId).hide();
}

/**
 * Prepares the login popup
 */
function prepareLoginRegistrationPopup(){
	const popupLoginGeneratePasswordBody = $('#' + popupLoginGeneratePasswordBodyId);
	// hide on startup
	hideExtraViewsOfLoginPopup();
	popupLoginGeneratePasswordBody.hide();

	// switching tabs
	$('.tab-login a').on('click', function (e) {
		e.preventDefault();
		$(this).parent().addClass('active');
		$(this).parent().siblings().removeClass('active');
		const target = $(this).attr('href');
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
		new AjaxMainHandler().ajaxLogin($('#' + loginUserId).val(), $('#' + loginPwId).val(), false)
	}).keypress(function(e) { if (e.which == 13) { new AjaxMainHandler().ajaxRegistration() } });

	$('#' + popupLoginForgotPasswordText).click(function(){
		const body = $('#' + popupLoginForgotPasswordBody);
		if (body.is(':visible')){
			body.fadeOut();
			$('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
			$('#' + popupLoginFailed).fadeOut();
			$('#' + popupLoginSuccess).fadeOut();
			$('#' + popupLoginInfo).fadeOut();
		} else {
			body.fadeIn();
			$('#' + popupLoginForgotPasswordText).text(_t(hidePasswordRequest));
		}
	});

	$('#' + popupLoginGeneratePassword + ' > a').click(function(){
		if (popupLoginGeneratePasswordBody.is(':visible')){
			popupLoginGeneratePasswordBody.hide();
			$('#' + popupLoginGeneratePassword + ' > a span').text(_t(generateSecurePassword));
		} else {
			popupLoginGeneratePasswordBody.show();
			$('#' + popupLoginGeneratePassword + ' > a span').text(_t(hideGenerator));
		}
	});

	$('#' + popupLoginCloseButton).click(function(){
		hideExtraViewsOfLoginPopup();
		$('#' + popupLogin).modal('hide');
		$('#' + popupLoginButtonLogin).show();
	});

	$('#' + popupLoginPasswordInputId).keyup(function popupLoginPasswordInputKeyUp() {
		new PasswordHandler().check_strength($('#' + popupLoginPasswordInputId), $('#' + popupLoginPasswordMeterId),
				$('#' + popupLoginPasswordStrengthId), $('#' + popupLoginPasswordExtrasId));
	});

	$('#' + popupLoginButtonRegister).click(function(){
		const userfirstname   = $('#' + popupLoginUserfirstnameInputId).val();
		const userlastname    = $('#' + popupLoginUserlastnameInputId).val();
		const nick            = $('#' + popupLoginNickInputId).val();
		const email           = $('#' + popupLoginEmailInputId).val();
		const password        = $('#' + popupLoginPasswordInputId).val();
		const passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val();
		let text = '';
		let i;
		const fields = [userfirstname, userlastname, nick, email, password, passwordconfirm];
		const tvalues = [_t(checkFirstname), _t(checkLastname), _t(checkNickname), _t(checkEmail),_t(checkPassword),
				_t(checkConfirmation), _t(checkPasswordConfirm)];

		// check all vields for obivously errors
		for (i=0; i<fields.length; i++){
			if (!fields[i] || /^\s*$/.test(fields[i]) || 0 === fields[i].length) {
				text = tvalues[i];
				break;
			}
		}

		if (text == '' ){
			$('#' + popupLoginWarningMessage).hide();
			new AjaxMainHandler().ajaxRegistration();
		} else {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(text);
		}

	});

	// bind enter key
	$('#' + loginUserId).keypress(function(e) {							if (e.which == 13) {	new AjaxMainHandler().ajaxLogin($('#' + loginUserId).val(), $('#' + loginPwId).val(), false) } });
	$('#' + loginPwId).keypress(function(e) {							if (e.which == 13) {	new AjaxMainHandler().ajaxLogin($('#' + loginUserId).val(), $('#' + loginPwId).val(), false) } });
	$('#admin-login-user').keypress(function(e) {   					if (e.which == 13) {	new AjaxMainHandler().ajaxLogin($('#' + loginUserId).val(), $('#' + loginPwId).val(), false) } });
	$('#admin-login-pw').keypress(function(e) {							if (e.which == 13) {	new AjaxMainHandler().ajaxLogin($('#' + loginUserId).val(), $('#' + loginPwId).val(), false) } });
	$('#' + popupLoginUserfirstnameInputId).keypress(function(e) {		if (e.which == 13) {	new AjaxMainHandler().ajaxRegistration()	}	});
	$('#' + popupLoginUserlastnameInputId).keypress(function(e) {		if (e.which == 13) {	new AjaxMainHandler().ajaxRegistration()	}	});
	$('#' + popupLoginNickInputId).keypress(function(e) {				if (e.which == 13) {	new AjaxMainHandler().ajaxRegistration()	}	});
	$('#' + popupLoginEmailInputId).keypress(function(e) {				if (e.which == 13) {	new AjaxMainHandler().ajaxRegistration()	}	});
	$('#' + popupLoginPasswordconfirmInputId).keypress(function(e) {	if (e.which == 13) {	new AjaxMainHandler().ajaxRegistration()	}	});

	$('#' + popupLoginButtonRequest).click(function() {
		new AjaxMainHandler().ajaxPasswordRequest();
	});
}

/**
 *
 * @param element
 */
function setTextWatcherInputLength(element){
	const min_length = element.data('min-length');
	let max_length = element.data('max-length');
	if (!max_length)
		max_length = 1000;
	const id = element.attr('id') + '-text-counter';
	const msg = _t_discussion(textMinCountMessageBegin1) + ' ' + min_length + ' ' + _t_discussion(textMinCountMessageBegin2);
	const field = $('<span>').text(msg).attr('id', id).addClass('text-info').addClass('text-counter-input');
	field.insertBefore(element);
	
	element.keyup(function(){
		const text = element.val().trim();
		const current_length = text.length;
		
		if (current_length == 0){
			field.addClass('text-info');
			field.removeClass('text-danger');
			field.text(msg)
		} else if (current_length < min_length) {
			field.removeClass('text-danger');
			field.text((min_length - current_length) + ' ' + _t_discussion(textMinCountMessageDuringTyping));
		} else {
				field.removeClass('text-info');
			if (current_length > max_length * 3 / 4){
				field.addClass('text-danger');
			} else {
				field.removeClass('text-danger');
			}
			const left = max_length < current_length ? 0 : max_length - current_length;
			field.text(left + ' ' + _t_discussion(textMaxCountMessage));
			if (max_length <= current_length)
				field.text(field.text() + ' ' + _t_discussion(textMaxCountMessageError));
		}
	});
}

/**
 * Sets data for the global sucess field
 * @param heading text
 * @param body text
 */
function setGlobalErrorHandler(heading, body){
	$('#' + requestFailedContainer).fadeIn();
	$('#' + requestFailedContainerClose).click(function(){
		$('#' + requestFailedContainer).fadeOut();
	});
	$('#' + requestFailedContainerHeading).html(heading);
	$('#' + requestFailedContainerMessage).html(body);
	setTimeout(function(){
		$('#' + requestFailedContainer).fadeOut();
	}, 5000);
}

/**
 * Sets data for the global success field
 * @param heading text
 * @param body text
 */
function setGlobalSuccessHandler(heading, body){
	$('#' + requestSuccessContainer).fadeIn();
	$('#' + requestSuccessContainerClose).click(function(){
		$('#' + requestSuccessContainer).fadeOut();
	});
	$('#' + requestSuccessContainerHeading).html(heading);
	$('#' + requestSuccessContainerMessage).html(body);
	setTimeout(function(){
		$('#' + requestSuccessContainer).fadeOut();
	}, 5000);
}

/**
 * Sets data for the global info field
 * @param heading text
 * @param body text
 */
function setGlobalInfoHandler(heading, body){
	$('#' + requestInfoContainer).fadeIn();
	$('#' + requestInfoContainerClose).click(function(){
		$('#' + requestInfoContainer).fadeOut();
	});
	$('#' + requestInfoContainerHeading).html(heading);
	$('#' + requestInfoContainerMessage).html(body);
	setTimeout(function(){
		$('#' + requestInfoContainer).fadeOut();
	}, 5000);
}

// *********************
//	CALLBACKS
// *********************

/**
 *
 * @param data
 * @param showGlobalError
 */
function callbackIfDoneForLogin(data, showGlobalError){
	try {
		const parsedData = $.parseJSON(data);
		
		if (parsedData.error.length != 0) {
			if (showGlobalError) {
					setGlobalErrorHandler('Ohh!', parsedData.error);
			} else {
				$('#' + popupLoginFailed).show();
				$('#' + popupLoginFailed + '-message').html(parsedData.error);
			}
		} else {
			$('#' + popupLogin).modal('hide');
			location.reload(true);
		}
	} catch(err){
		console.log('ERROR');
		//console.log(err);
		let url = location.href;
		if (url.indexOf('?session_expired=true') != -1)
			url = url.substr(0, url.length - '?session_expired=true'.length);
		location.href = url;
	}

}

/**
 *
 * @param data
 */
function callbackIfDoneForRegistration(data){
	const parsedData = $.parseJSON(data);
	const success = $('#' + popupLoginSuccess); //popupLoginRegistrationSuccess);
	const failed = $('#' + popupLoginRegistrationFailed);
	const info = $('#' + popupLoginRegistrationInfo);
	success.hide();
	failed.hide();
	info.hide();

	if (parsedData.success.length > 0) {
		// trigger click
		$('a[href="#login"]').trigger('click');
		success.show();
		$('#' + popupLoginSuccess + '-message').text(parsedData.success);
	}
	if (parsedData.error.length > 0) {
		failed.show();
		$('#' + popupLoginRegistrationFailed + '-message').text(parsedData.error);
	}
	if (parsedData.info.length > 0) {
		info.show();
		$('#' + popupLoginRegistrationInfo + '-message').text(parsedData.info);
		$('#popup-login-spamanswer-input').attr('placeholder', parsedData.spamquestion).val('');
	}
}

/**
 *
 * @param data
 */
function callbackIfDoneForPasswordRequest(data){
	const parsedData = $.parseJSON(data);
	const success = $('#' + popupLoginSuccess);
	const failed = $('#' + popupLoginFailed);
	const info = $('#' + popupLoginInfo);
	success.hide();
	failed.hide();
	info.hide();
	if (parsedData.success.length > 0) {
		$('#' + popupLoginForgotPasswordBody).hide();
		$('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
		success.show();
		$('#' + popupLoginSuccess + '-message').text(parsedData.success);
	}
	if (parsedData.error.length > 0) {
		failed.show();
		$('#' + popupLoginFailed + '-message').text(parsedData.error);
	}
	if (parsedData.info.length > 0) {
		info.show();
		$('#' + popupLoginInfo + '-message').text(parsedData.info);
	}
}

// *********************
//	MAIN
// *********************
$(document).ready(function () {
	'use strict';
	const path = window.location.href;
	const lang = $('#hidden_language').val();

	jmpToChapter();
	goBackToTop();
	setPiwikOptOutLink(lang);
	setEasterEggs();
	setGravatarFallback();

	// set current file to active
		 if (path.indexOf(urlContact) != -1){ 	setLinkActive('#' + contactLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlLogin) != -1){		setLinkActive('#' + loginLinkId);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlNews) != -1){		setLinkActive('#' + newsLink);		$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlContent) != -1){ 	setLinkActive('#' + contentLink);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlReview) != -1){ 	setLinkActive('#' + reviewLinkId);	$('#' + navbarLeft).hide(); }
	else if (path.indexOf(urlSettings) != -1 ||
			 path.indexOf(urlImprint) != -1 ||
			 path.indexOf(urlLogout) != -1){										$('#' + navbarLeft).hide(); }
	else { 										setLinkActive(''); 					$('#' + navbarLeft).show(); }

	// language switch
	$('#' + translationLinkDe).click(function(){ new AjaxMainHandler().ajaxSwitchDisplayLanguage('de') });
	$('#' + translationLinkEn).click(function(){ new AjaxMainHandler().ajaxSwitchDisplayLanguage('en') });
	$('#' + translationLinkDe + ' img').click(function(){ new AjaxMainHandler().ajaxSwitchDisplayLanguage('de') });
	$('#' + translationLinkEn + ' img').click(function(){ new AjaxMainHandler().ajaxSwitchDisplayLanguage('en') });
	$('#' + logoutLinkId).click(function(e){
		e.preventDefault();
		new AjaxMainHandler().ajaxLogout();
	});

	// gui preperation
	prepareLoginRegistrationPopup();

	// activate tooltips
	$(function () {
		$('body').tooltip({ selector: '[data-toggle=tooltip]' });
    });

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct() {
			setTimeout("$('body').addClass('loading')", 0);
		},
		ajaxStop: function ajaxStopFct() {
			setTimeout("$('body').removeClass('loading')", 0);
		}
	});
	//$(document).ajaxError(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
    //    alert("There was an ajax error!");
	//});

	// add minimal text length field
	$('input[data-min-length]').each(function(){
		setTextWatcherInputLength($(this));
	});
	$('textarea[data-min-length]').each(function(){
		setTextWatcherInputLength($(this));
	});

	// session expired popup
	if ($('#' + sessionExpiredContainer).length == 1)
		setTimeout(function(){
			$('#' + sessionExpiredContainer).fadeOut();
		}, 3000);

	// testing with gremlins
	//var horde = gremlins.createHorde()
	//	.gremlin(gremlins.species.formFiller())
	//	.gremlin(gremlins.species.clicker().clickTypes(['click']))
	//	.gremlin(gremlins.species.typer())
	//	.gremlin(function() {
	//		window.$ = function() {};
	//	});
    //horde.unleash();
	// gremlins will act randomly, at 10 ms interval, 1000 times
});
