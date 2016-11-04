/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

/**
 *
 * @param linkname
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
		var img = $('<img>').attr('src','../static/images/explanation_bubbles_' + ($(document).width() > 992?'long' : 'short') + '.png');
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
	var src = mainpage + 'piwik/index.php?module=CoreAdminHome&action=optOut&idsite=1&language=' + lang;
	$('#piwik-opt-out-iframe').attr('src', src);
}

/**
 *
 */
function setEasterEggs(){
	$('#roundhousekick').click(function(){ new AjaxMainHandler().ajaxRoundhouseKick(); });
	//$('#yomamma').click(function(){ new AjaxMainHandler().ajaxMama(); });

	if (window.location.href == mainpage) {
		/* christmas only
        var div = $('<div>'),
        christmas = $('<input>').attr('type','checkbox').data('toggle','toggle').data('onstyle','primary').bootstrapToggle('off'),
        silvester = $('<input>').attr('type','checkbox').data('toggle','toggle').data('onstyle','primary').bootstrapToggle('off'),
        spanChristmas = $('<span>').text('Christmas'),
        spanSilvester = $('<span>').text('Silvester');
        christmas.attr('style','margin-left: 5px;');
        silvester.attr('style','margin-left: 5px;');
        spanSilvester.attr('style','margin-left: 20px;');
        div.attr('style','padding-right: 50px; z-index: 200; text-align: right;')
		        .append(spanChristmas)
		        .append(christmas)
		        .append(spanSilvester)
		        .append(silvester);
		div.prependTo($('.first-container'));
		$('#cot_tl3_fixed').hide();
		$('#cot_tl4_fixed').hide();
		christmas.change(function() {
			if($(this).is(":checked")) {
				$('#cot_tl3_fixed').show();
				$('#cot_tl4_fixed').show();
			} else {
				$('#cot_tl3_fixed').hide();
				$('#cot_tl4_fixed').hide();
			}
		});
		silvester.change(function() {
			if($(this).is(":checked")) {
				document.body.appendChild(canvas);
				window.scrollTo(0,document.body.scrollHeight);
			} else {
				canvas.remove();
			}
		});
		*/
	}

	$('#dbas-logo').click(function(){
		var counter = parseInt($(this).data('counter'));
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
	var popupLoginGeneratePasswordBody = $('#' + popupLoginGeneratePasswordBodyId);
	// hide on startup
	hideExtraViewsOfLoginPopup();
	popupLoginGeneratePasswordBody.hide();

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
		new AjaxMainHandler().ajaxLogin($('#' + loginUserId).val(), $('#' + loginPwId).val(), false)
	}).keypress(function(e) { if (e.which == 13) { new AjaxMainHandler().ajaxRegistration() } });

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
		hideExtraViewsOfLoginPopup();
		$('#' + popupLogin).modal('hide');
		$('#' + popupLoginButtonLogin).show();
	});

	$('#' + popupLoginPasswordInputId).keyup(function popupLoginPasswordInputKeyUp() {
		new PasswordHandler().check_strength($('#' + popupLoginPasswordInputId), $('#' + popupLoginPasswordMeterId),
				$('#' + popupLoginPasswordStrengthId), $('#' + popupLoginPasswordExtrasId));
	});

	$('#' + popupLoginButtonRegister).click(function(){
		var userfirstname   = $('#' + popupLoginUserfirstnameInputId).val(),
			userlastname    = $('#' + popupLoginUserlastnameInputId).val(),
			nick            = $('#' + popupLoginNickInputId).val(),
			email           = $('#' + popupLoginEmailInputId).val(),
			password        = $('#' + popupLoginPasswordInputId).val(),
			passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val(),
			text = '',
			i,
			fields = [userfirstname, userlastname, nick, email, password, passwordconfirm],
			tvalues = [_t(checkFirstname), _t(checkLastname), _t(checkNickname), _t(checkEmail),_t(checkPassword),
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
	var min_length = element.data('min-length');
	var max_length = element.data('max-length');
	if (!max_length)
		max_length = 1000;
	var id = element.attr('id') + '-text-counter';
	var msg = _t_discussion(textMinCountMessageBegin1) + ' ' + min_length + ' ' + _t_discussion(textMinCountMessageBegin2);
	var field = $('<span>').text(msg).attr('id', id).addClass('text-min-counter-input');
	field.insertBefore(element);
	
	element.keyup(function(){
		var text = element.val().trim();
		var current_length = text.length;
		
		if (current_length == 0){
			field.removeClass('text-counter-input');
			field.addClass('text-min-counter-input');
			field.removeClass('text-max-counter-input');
			field.text(msg)
		} else if (current_length < min_length) {
			field.addClass('text-counter-input');
			field.removeClass('text-max-counter-input');
			field.removeClass('text-max-counter-input');
			field.text((min_length - current_length) + ' ' + _t_discussion(textMinCountMessageDuringTyping));
		} else {
				field.removeClass('text-min-counter-input');
			if (current_length * 2 > max_length){
				field.removeClass('text-counter-input');
				field.addClass('text-max-counter-input');
			} else {
				field.addClass('text-counter-input');
				field.removeClass('text-max-counter-input');
			}
			var left = max_length < current_length ? 0 : max_length - current_length;
			field.text(left + ' ' + _t_discussion(textMaxCountMessage));
			if (max_length <= current_length)
				field.text(field.text() + ' ' + _t_discussion(textMaxCountMessageError));
				// element.val(element.val().substr(0, maxlength));
		}
	});
}

/**
 * Sets an text watcher for the given element. After every input the attribute 'data-min-length' will be checked
 * and maybe a text is shown
 * @param element
 */
function setTextWatcherForMinLength(element){
	var text = element.val().trim();
	var minlength = element.data('min-length');
	var offset = parseInt(minlength - text.length);
	var id = element.attr('id') + '-text-min-counter';
	var msg = _t_discussion(textMinCountMessage1) + ' ' + offset + ' ' + _t_discussion(textMinCountMessage2);
	var field = $('#' + id);
	if (offset > 0) {
		if (field.length > 0) {
			field.text(msg);
		} else {
			$('<span>').text(msg).attr('id', id).addClass('text-min-counter-input').insertBefore(element);
		}
	} else {
		if (field.length > 0) {
			field.text(_t_discussion(textMinCountMessageBegin1) + ' ' + minlength + ' ' + _t_discussion(textMinCountMessageBegin2));
			field.remove();
		}
	}
}

/**
 * Sets an text watcher for the given element. After every input the attribute 'data-min-length' will be checked
 * and maybe a text is shown
 * @param element
 */
function setTextWatcherForMaxLength(element){
	var text = element.val().trim();
	var maxlength = element.data('max-length');
	var offset = parseInt(maxlength - text.length);
	var id = element.attr('id') + '-text-max-counter';
	var msg = _t_discussion(textMaxCountMessage);
	var field = $('#' + id);
	if (offset < 0) {
		if (field.length > 0) {
			field.text(msg);
		} else {
			$('<span>').text(msg).attr('id', id).addClass('text-max-counter-input').insertBefore(element);
		}
	} else {
		if (field.length > 0) {
			field.remove();
		}
	}
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
	delay(function(){
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
	delay(function(){
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
	delay(function(){
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
		var parsedData = $.parseJSON(data);
		
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
		var url = location.href;
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
	var parsedData = $.parseJSON(data);
	var success = $('#' + popupLoginSuccess); //popupLoginRegistrationSuccess);
	var failed = $('#' + popupLoginRegistrationFailed);
	var info = $('#' + popupLoginRegistrationInfo);
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
	var parsedData = $.parseJSON(data);
	var success = $('#' + popupLoginSuccess);
	var failed = $('#' + popupLoginFailed);
	var info = $('#' + popupLoginInfo);
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
	var path = window.location.href, lang = $('#hidden_language').val();

	jmpToChapter();
	goBackToTop();
	setPiwikOptOutLink(lang);
	setEasterEggs();

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
		delay(function(){
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
