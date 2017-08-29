/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

/**
 *
 * @param linkname name of the link
 */
function setLinkActive(linkname) {
	'use strict';
	
	$('#navbar-right').find('>li').each(function(){
		$(this).removeClass('active');
	});
	$(linkname).addClass('active');
}

/**
 * Jumps to clicked chapter, which is defined in the header
 */
function jmpToChapter() {
    'use strict';
    
	// jump to chapter-function
	$('a[href^="#"]').on('click', function (e) {
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
 * Adds a small border to the active navbar element
 */
function addBorderToActiveNavbar(){
    'use strict';
	
	var active_element = $('.navbar-right > .active');
	if (active_element.length === 0){
		return;
	}
	var border_size = '2';
	
	// replace padding of the inner element
	var inner_element = active_element.find('a');
	var pad_top = parseInt(inner_element.css('padding-top').replace('px', ''));
	var pad_bottom = parseInt(inner_element.css('padding-bottom').replace('px', ''));
	inner_element.css('padding-top', (pad_top - border_size / 2) + 'px');
	inner_element.css('padding-bottom', (pad_bottom - border_size / 2) + 'px');
	
    // add border to the navbar element
	active_element.css('border-top', border_size + 'px solid #2196F3');
}

/**
 * Go back to top arrow
 */
function goBackToTop() {
    'use strict';
    
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
    'use strict';
    
	var body = $('body');
	var img = body.find('.img-circle');
	if (img.length === 0) {
		return true;
	}
	
	var src = body.find('.img-circle')[0].src;
	$.get(src, function() {
    	replace_gravtar_with_default_image(true);
    }).fail(function() {
    	replace_gravtar_with_default_image(false);
    });
}

/**
 *
 * @param only_on_error
 */
function replace_gravtar_with_default_image(only_on_error){
    'use strict';
    
	$('body').find('.img-circle').each(function (){
		var icons =
			[  { 'name': 'faces', 'length': 98
			}, { 'name': 'flat-smileys', 'length': 32
			}, { 'name': 'human', 'length': 81
			}, { 'name': 'lego', 'length': 10 }];
		var t = 3;
		var no = Math.floor(Math.random() * icons[t].length);
		var src = mainpage + 'static/images/fallback-' + icons[t].name + '/' +  no + '.svg';
		
		var width = $(this).width();
		if (only_on_error) {
			$(this).attr('onerror', 'this.src="' + src + '"');
		} else {
			$(this).attr('src', src);
		}
		$(this).css('width', width + 'px');
	});
}

/**
 *
 * @param titleText
 * @param bodyText
 * @param functionForAccept
 * @param functionForRefuse
 * @param small_dialog
 */
function displayConfirmationDialog(titleText, bodyText, functionForAccept, functionForRefuse, small_dialog) {
    'use strict';
    
	// display dialog
	var dialog = $('#' + popupConfirmDialogId);
    dialog.find('#confirm-dialog-accept-btn').show();
	dialog.find('#confirm-dialog-refuse-btn').show();
	if (small_dialog) {
		dialog.find('.modal-dialog').addClass('modal-sm');
	}
	dialog.modal('show');
	$('#' + popupConfirmDialogId + ' h4.modal-title').text(titleText);
	$('#' + popupConfirmDialogId + ' div.modal-body').html(bodyText);
	$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		if (functionForRefuse) {
			functionForAccept();
		}
	});
	$('#' + popupConfirmDialogRefuseBtn).show().click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		if (functionForRefuse) {
			functionForRefuse();
		}
	});
	dialog.on('hidden.bs.modal', function () {
		$('#' + popupConfirmDialogRefuseBtn).show();
		dialog.find('.modal-dialog').removeClass('modal-sm');
		dialog.find('#confirm-dialog-accept-btn').text(_t(okay));
		dialog.find('#confirm-dialog-refuse-btn').text(_t(cancel));
		// unload buttons
		$('#' + popupConfirmDialogAcceptBtn).off('click');
		$('#' + popupConfirmDialogRefuseBtn).off('click');
		
	});
}

/**
 * Displays dialog
 *
 * @param titleText
 * @param bodyText
 */
function displayConfirmationDialogWithoutCancelAndFunction(titleText, bodyText) {
    'use strict';
    
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
    'use strict';
    
	// display dialog only if the cookie was not set yet
	if (Cookies.get(WARNING_CHANGE_DISCUSSION_POPUP)){
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
				Cookies.set(WARNING_CHANGE_DISCUSSION_POPUP, true, { expires: 7 });
			}

			if (isRestartingDiscussion) {
				window.location.href = functionForAccept;
			} else {
				functionForAccept();
			}

		});
		$('#' + popupConfirmChecbkoxDialogRefuseBtn).click( function () {
			$('#' + popupConfirmChecbkoxDialogId).modal('hide');
		});
	}
}

/**
 *
 * @param lang
 */
function setPiwikOptOutLink(lang){
    'use strict';
    
	var src = mainpage + 'piwik/index.php?module=CoreAdminHome&action=optOut&idsite=1&language=' + lang;
	$('#piwik-opt-out-iframe').attr('src', src);
}

/**
 *
 */
function setEasterEggs(){
    'use strict';
    
	$('#roundhousekick').click(function(){ new AjaxMainHandler().roundhouseKick(); });
	//$('#yomamma').click(function(){ new AjaxMainHandler().ajaxMama(); });
	$('#logo_dbas, #logo_dbas_s').click(function(){
		if (!$(this)){
			return;
		}
		var counter = parseInt($(this).data('counter'));
		counter += 1;
		if (counter === 7){
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
 * Prepares the login popup
 */
function prepareLoginRegistrationPopup(){
    'use strict';
    
	var popupLoginGeneratePasswordBody = $('#' + popupLoginGeneratePasswordBodyId);
	// hide on startup
	new PopupHandler().hideExtraViewsOfLoginPopup();
	popupLoginGeneratePasswordBody.hide();

	// switching tabs
	$('.tab-login a').on('click', function (e) {
		e.preventDefault();
		$(this).parent().addClass('active');
		$(this).parent().siblings().removeClass('active');
		var target = $(this).attr('href');
		$('.tab-content > div').not(target).hide();
		$(target).fadeIn(600);

		if ($(this).attr('href').indexOf('signup') !== -1){
			$('#' + popupLoginButtonLogin).hide();
			$('#' + popupLoginButtonRegister).show();
		} else {
			$('#' + popupLoginButtonLogin).show();
			$('#' + popupLoginButtonRegister).hide();
		}
	});

	$('#' + popupLoginButtonLogin).show().click(function() {
		new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false);
		Cookies.set(DBAS_DATA_DISCLAIMER, true, { expires: 180 });
	}).keypress(function(e) {
		if (e.which === 13) {
			new AjaxMainHandler().registration();
		}
	});
	
	// data disclaimer
	if (Cookies.get(DBAS_DATA_DISCLAIMER) === 'true') {
		$('#dbas-login-data-disclaimer').hide();
	}

	$('#' + popupLoginForgotPasswordText).click(function(){
		var body = $('#' + popupLoginForgotPasswordBody);
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
		new PopupHandler().hideExtraViewsOfLoginPopup();
		$('#' + popupLogin).modal('hide');
		$('#' + popupLoginButtonLogin).show();
	});

	$('#' + popupLoginPasswordInputId).keyup(function popupLoginPasswordInputKeyUp() {
		new PasswordHandler().check_strength($('#' + popupLoginPasswordInputId), $('#' + popupLoginPasswordMeterId),
				$('#' + popupLoginPasswordStrengthId), $('#' + popupLoginPasswordExtrasId));
	});

	$('#' + popupLoginButtonRegister).click(function(){
		var userfirstname = $('#' + popupLoginUserfirstnameInputId).val();
		var userlastname = $('#' + popupLoginUserlastnameInputId).val();
		var nick = $('#' + popupLoginNickInputId).val();
		var email = $('#' + popupLoginEmailInputId).val();
		var password = $('#' + popupLoginPasswordInputId).val();
		var passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val();
		var text = '';
		var i;
		var fields = [userfirstname, userlastname, nick, email, password, passwordconfirm];
		var tvalues = [_t(checkFirstname), _t(checkLastname), _t(checkNickname), _t(checkEmail),_t(checkPassword),
				_t(checkConfirmation), _t(checkPasswordConfirm)];

		// check all vields for obivously errors
		for (i=0; i<fields.length; i++){
			if (!fields[i] || /^\s*$/.test(fields[i]) || 0 === fields[i].length) {
				text = tvalues[i];
				break;
			}
		}

		if (text === '' ){
			$('#' + popupLoginWarningMessage).hide();
			new AjaxMainHandler().registration();
		} else {
			$('#' + popupLoginWarningMessage).fadeIn("slow");
			$('#' + popupLoginWarningMessageText).text(text);
		}

	});

	// bind enter key
	$('#' + loginUserId).keypress(function(e) {						 if (e.which === 13) {	new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false); } });
	$('#' + loginPwId).keypress(function(e) {						 if (e.which === 13) {	new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false); } });
	$('#admin-login-user').keypress(function(e) {   				 if (e.which === 13) {	new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false); } });
	$('#admin-login-pw').keypress(function(e) {						 if (e.which === 13) {	new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false); } });
	$('#' + popupLoginUserfirstnameInputId).keypress(function(e) {	 if (e.which === 13) {	new AjaxMainHandler().registration();	}	});
	$('#' + popupLoginUserlastnameInputId).keypress(function(e) {	 if (e.which === 13) {	new AjaxMainHandler().registration();	}	});
	$('#' + popupLoginNickInputId).keypress(function(e) {			 if (e.which === 13) {	new AjaxMainHandler().registration();	}	});
	$('#' + popupLoginEmailInputId).keypress(function(e) {			 if (e.which === 13) {	new AjaxMainHandler().registration();	}	});
	$('#' + popupLoginPasswordconfirmInputId).keypress(function(e) { if (e.which === 13) {	new AjaxMainHandler().registration();	}	});

	$('#' + popupLoginButtonRequest).click(function() {
		new AjaxMainHandler().passwordRequest();
	});
}

/**
 *
 * @param element
 * @param display_at_top
 */
function setTextWatcherInputLength(element, display_at_top){
    'use strict';
    
	var min_length = element.data('min-length');
	var max_length = element.data('max-length');
	if (!max_length) {
		max_length = 1000;
	}
	var id = element.attr('id') + '-text-counter';
	var msg = _t_discussion(textMinCountMessageBegin1) + ' ' + min_length + ' ' + _t_discussion(textMinCountMessageBegin2);
	var field = $('<span>').text(msg).attr('id', id).addClass('text-info').addClass('text-counter-input');
	if (display_at_top){
		field.insertBefore(element);
	} else {
		field.insertAfter(element);
	}
	
	element.keyup(function(){
		var text = element.val().trim();
		var current_length = text.length;
		
		if (current_length === 0){
			field.addClass('text-info');
			field.removeClass('text-danger');
			field.text(msg);
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
			var left = max_length < current_length ? 0 : max_length - current_length;
			field.text(left + ' ' + _t_discussion(textMaxCountMessage));
			if (max_length <= current_length) {
				field.removeClass('text-danger');
			field.addClass('text-info');
				field.text(_t_discussion(textMaxCountMessageError));
			}
		}
	});
}

/**
 * Sets data for the global sucess field
 *
 * @param heading text
 * @param body text
 */
function setGlobalErrorHandler(heading, body){
    'use strict';
    
	$('#' + requestFailedContainer).fadeIn();
	$('#' + requestFailedContainerClose).click(function(){
		$('#' + requestFailedContainer).fadeOut();
	});
	$('#' + requestFailedContainerHeading).html(decodeString(heading));
	$('#' + requestFailedContainerMessage).html(decodeString(body));
	setTimeout(function(){
		$('#' + requestFailedContainer).fadeOut();
	}, 5000);
}

/**
 * Sets data for the global success field
 *
 * @param heading text
 * @param body text
 */
function setGlobalSuccessHandler(heading, body){
    'use strict';
    
	$('#' + requestSuccessContainer).fadeIn();
	$('#' + requestSuccessContainerClose).click(function(){
		$('#' + requestSuccessContainer).fadeOut();
	});
	$('#' + requestSuccessContainerHeading).html(decodeString(heading));
	$('#' + requestSuccessContainerMessage).html(decodeString(body));
	setTimeout(function(){
		$('#' + requestSuccessContainer).fadeOut();
	}, 5000);
}

/**
 * Sets data for the global info field
 *
 * @param heading text
 * @param body text
 */
function setGlobalInfoHandler(heading, body){
    'use strict';
    
	$('#' + requestInfoContainer).fadeIn();
	$('#' + requestInfoContainerClose).click(function(){
		$('#' + requestInfoContainer).fadeOut();
	});
	$('#' + requestInfoContainerHeading).html(decodeString(heading));
	$('#' + requestInfoContainerMessage).html(decodeString(body));
	setTimeout(function(){
		$('#' + requestInfoContainer).fadeOut();
	}, 5000);
}

/**
 *
 * @param encodedString
 */
function decodeString(encodedString){
    'use strict';
    
	// var textArea = document.createElement('textarea');
    // textArea.innerHTML = encodedString;
    // return textArea.value;
	return decodeURIComponent(encodedString);
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
    'use strict';
    
	try {
		if (data.error.length !== 0) {
			if (showGlobalError) {
					setGlobalErrorHandler('Ohh!', data.error);
			} else {
				$('#' + popupLoginFailed).show();
				$('#' + popupLoginFailed + '-message').html(data.error);
			}
		} else {
			$('#' + popupLogin).modal('hide');
			location.reload(true);
		}
	} catch(err){
		var url = location.href;
		if (url.indexOf('?session_expired=true') !== -1) {
			url = url.substr(0, url.length - '?session_expired=true'.length);
		}
		location.href = url;
	}

}

/**
 *
 * @param data
 */
function callbackIfDoneForRegistration(data){
    'use strict';
    
	var success = $('#' + popupLoginSuccess); //popupLoginRegistrationSuccess);
	var failed = $('#' + popupLoginRegistrationFailed);
	var info = $('#' + popupLoginRegistrationInfo);
	success.hide();
	failed.hide();
	info.hide();

	if (data.success.length > 0) {
		// trigger click
		$('a[href="#login"]').trigger('click');
		success.show();
		$('#' + popupLoginSuccess + '-message').text(data.success);
	}
	if (data.error.length > 0) {
		failed.show();
		$('#' + popupLoginRegistrationFailed + '-message').text(data.error);
	}
	if (data.info.length > 0) {
		info.show();
		$('#' + popupLoginRegistrationInfo + '-message').text(data.info);
		$('#popup-login-spamanswer-input').attr('placeholder', data.spamquestion).val('');
	}
}

/**
 *
 * @param data
 */
function callbackIfDoneForPasswordRequest(data){
    'use strict';
    
	var success = $('#' + popupLoginSuccess);
	var failed = $('#' + popupLoginFailed);
	var info = $('#' + popupLoginInfo);
	success.hide();
	failed.hide();
	info.hide();
	if (data.success.length > 0) {
		$('#' + popupLoginForgotPasswordBody).hide();
		$('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
		success.show();
		$('#' + popupLoginSuccess + '-message').text(data.success);
	}
	if (data.error.length > 0) {
		failed.show();
		$('#' + popupLoginFailed + '-message').text(data.error);
	}
	if (data.info.length > 0) {
		info.show();
		$('#' + popupLoginInfo + '-message').text(data.info);
	}
}

// *********************
//	MAIN
// *********************
$(document).ready(function () {
    'use strict';
    
	// ajax loading animation
	var timer;
	$(document).on({
		ajaxStart: function ajaxStartFct() {
            timer && clearTimeout(timer);
            timer = setTimeout(function(){
                $('body').addClass('loading');
            }, 150);
		},
		ajaxStop: function ajaxStopFct() {
            clearTimeout(timer);
            $('body').removeClass('loading');
		}
	});
	
	
	var path = window.location.href;
	var lang = $('#hidden_language').val();

	jmpToChapter();
	goBackToTop();
	setPiwikOptOutLink(lang);
	setEasterEggs();
	setGravatarFallback();
	setTimeout(function(){
		addBorderToActiveNavbar();
	}, 150);
	$('#' + popupLogin).on('shown.bs.modal', function (e) {
		new PopupHandler().showLoginPopup(true);
	});

	// set current file to active
		 if (path.indexOf(urlContact) !== -1){ 	setLinkActive('#' + contactLink); }
	else if (path.indexOf(urlLogin) !== -1){	setLinkActive('#' + loginLinkId); }
	else if (path.indexOf(urlNews) !== -1){		setLinkActive('#' + newsLink); }
	else if (path.indexOf(urlContent) !== -1){ 	setLinkActive('#' + contentLink); }
	else if (path.indexOf(urlReview) !== -1){ 	setLinkActive('#' + reviewLinkId); }
	// else if (path.indexOf(urlSettings) !== -1 ||
	// 		 path.indexOf(urlImprint) !== -1 ||
	// 		 path.indexOf(urlLogout) !== -1){}
	else { 										setLinkActive(''); }

	// gui preperation
	prepareLoginRegistrationPopup();

	// activate tooltips
	$(function () {
		$('body').tooltip({ selector: '[data-toggle=tooltip]' });
    });

	// add minimal text length field
	$('input[data-min-length]').each(function(){
		setTextWatcherInputLength($(this), false);
	});
	$('textarea[data-min-length]').each(function(){
		setTextWatcherInputLength($(this), false);
	});

	// session expired popup
	if ($('#' + sessionExpiredContainer).length === 1) {
		setTimeout(function () {
			$('#' + sessionExpiredContainer).fadeOut();
		}, 3000);
	}
	
	// start guided tour, if the cookie is not set
	if (!Cookies.get(GUIDED_TOUR)){
		new GuidedTour().start();
	}

	// language switch
	$('#' + translationLinkDe).click(function(){ new GuiHandler().lang_switch('de'); });
	$('#' + translationLinkEn).click(function(){ new GuiHandler().lang_switch('en'); });
	$('#' + translationLinkDe + ' img').click(function(){ new GuiHandler().lang_switch('de'); });
	$('#' + translationLinkEn + ' img').click(function(){ new GuiHandler().lang_switch('en'); });
	$('#' + logoutLinkId).click(function(e){
		e.preventDefault();
		new AjaxMainHandler().logout();
	});

	$(window).scroll(function() {
		if ($(document).scrollTop() > 50) {
            $('nav').addClass('shrink');
		} else {
			$('nav').removeClass('shrink');
		}
	});
	
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
