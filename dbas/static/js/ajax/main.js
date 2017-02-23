/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxMainHandler(){
	/**
	 * Sends a request for language change
	 * @param new_lang is the shortcut for the language
	 */
	this.ajaxSwitchDisplayLanguage = function (new_lang){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: mainpage + 'ajax_switch_language',
			type: 'POST',
			data: { lang: new_lang},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSwitchDisplayLanguageDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.error.length !== 0) {
				setGlobalErrorHandler(_t(ohsnap), parsedData.error);
			} else {
				location.reload(true);
				setPiwikOptOutLink(new_lang);
			}
		}).fail(function ajaxSwitchDisplayLanguageFail(xhr) {
			if (xhr.status == 400) {
				setGlobalErrorHandler(_t(ohsnap), _t(requestFailedBadToken));
			} else if (xhr.status == 500) {
				setGlobalErrorHandler(_t(ohsnap), _t(requestFailedInternalError));
			} else {
				setGlobalErrorHandler(_t(ohsnap), _t(languageCouldNotBeSwitched));
			}
		});
	};
	
	/**
	 *
	 */
	this.ajaxLogin = function(user, password, showGlobalError){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var url = window.location.href;
		var keep_login = $('#keep-login-box').prop('checked') ? 'true' : 'false';
		$('#' + popupLoginFailed).hide();
		$('#' + popupLoginFailed + '-message').text('');

		$.ajax({
			url: mainpage + 'ajax_user_login',
			type: 'POST',
			data: {
				user: user,
				password: password,
				url: url,
				keep_login: keep_login
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxLoginDone(data) {
			callbackIfDoneForLogin(data, showGlobalError);
		}).fail(function ajaxLoginFail(xhr) {
			var errorMsg = '';
			
			if (xhr.status == 200) {			location.reload(true);
			} else if (xhr.status == 302) {		location.href = xhr.getResponseHeader('Location');
			} else if (xhr.status == 400) {		errorMsg = _t(requestFailedBadToken);
			} else if (xhr.status == 500) {		errorMsg = _t(requestFailedInternalError);
			} else {            				errorMsg = _t(requestFailed);
			}
			
			if (errorMsg.length > 0){
				if (showGlobalError) {
					setGlobalErrorHandler('Ohh!', errorMsg);
				} else {
					$('#' + popupLoginFailed).show();
					$('#' + popupLoginFailed + '-message').html(errorMsg);
				}
			}
		}).always(function ajaxLoginAlways(){
			$('#' + loginPwId).val('');
		});
	};

	/**
	 *
	 */
	this.ajaxLogout = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: mainpage + 'ajax_user_logout',
			type: 'POST',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxLogoutDone() {
			location.reload();
		}).fail(function ajaxLogoutFail(xhr) {
			if (xhr.status == 200) {
				if (window.location.href.indexOf('settings') !== 0){
					window.location.href = mainpage;
				} else {
					location.reload();
				}
			} else if (xhr.status == 403) {
				window.location.href = mainpage;
			} else {
				location.reload();
			}
		});
	};

	/**
	 *
	 */
	this.ajaxRegistration = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var firstname = $('#userfirstname-input').val(),
			lastname = $('#userlastname-input').val(),
			nickname = $('#nick-input').val(),
			email = $('#email-input').val(),
			password = $('#' + popupLoginPasswordInputId).val(),
			passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val(),
			spamanswer = $('#popup-login-spamanswer-input').val(),
			gender = '';

		if ($('#' + popupLoginInlineRadioGenderN).is(':checked')) gender = 'n';
		if ($('#' + popupLoginInlineRadioGenderM).is(':checked')) gender = 'm';
		if ($('#' + popupLoginInlineRadioGenderF).is(':checked')) gender = 'f';

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
					spamanswer: spamanswer,
					lang: getLanguage()},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRegistrationDone(data) {
			callbackIfDoneForRegistration(data);
		}).fail(function ajaxRegistrationFail(xhr) {
			$('#' + popupLoginRegistrationFailed).show();
			if (xhr.status == 400) {		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedBadToken));
			} else if (xhr.status == 500) {	$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedInternalError));
			} else {                		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
			}
		}).always(function ajaxLoginAlways(){
			$('#' + popupLoginPasswordInputId).val('');
			$('#' + popupLoginPasswordconfirmInputId).val('');
		});
	};

	/**
	 *
	 */
	this.ajaxPasswordRequest = function(){
		var email = $('#password-request-email-input').val();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_user_password_request',
			type: 'POST',
			data: { email: email, lang: getLanguage()},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxPasswordRequestDone(data) {
			callbackIfDoneForPasswordRequest(data);
		}).fail(function ajaxPasswordRequestFail(xhr) {
			$('#' + popupLoginRegistrationFailed).show();
			if (xhr.status == 400) {		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedBadToken));
			} else if (xhr.status == 500) {	$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedInternalError));
			} else {            			$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
			}
		});
	};

	/**
	 * Get-Request for an roundhouse kick
	 */
	this.ajaxRoundhouseKick = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'additional_service',
			type: 'POST',
			data: {type:'chuck'},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRoundhouseKickDone(data) {
			if (data.type == 'success'){
				displayConfirmationDialogWithoutCancelAndFunction('Chuck Norris Fact #' + data.value.id,
					'<h5>' + data.value.joke + '</h5>\n\n' +
					'<span style="float:right;">powered by <a href="http://www.icndb.com/" target="_blank">http://www.icndb.com/</a></span>');

			}
		});
	};

	/**
	 * Get your mama
	 */
	this.ajaxMama = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'additional_service',
			type: 'POST',
			data: {type:'mama'},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxMamaDone(data) {
			displayConfirmationDialogWithoutCancelAndFunction('Yo Mamma',  '<h4>' + data.joke + '</h4>\n\n<span' +
					' style="float:right;">powered by <a href="http://yomomma.info/">http://yomomma.info/</a></span>');
		});
	};
	
	/**
	 *
	 * @param uid
	 * @param reason
	 * @param is_argument
	 * @param extra_uid
	 */
	this.ajaxFlagArgumentOrStatement = function(uid, reason, is_argument, extra_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_flag_argument_or_statement',
			method: 'POST',
			data: {
				uid: uid,
				reason: reason,
				extra_uid: extra_uid,
				is_argument: is_argument
			},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxFlagArgumentDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.error.length !== 0){
				setGlobalErrorHandler(_t(ohsnap), parsedData.error);
			} else if (parsedData.info.length !== 0) {
				setGlobalInfoHandler('Ohh!', parsedData.info);
				$('#popup-duplicate-statement').modal('hide');
			} else {
				setGlobalSuccessHandler('Yeah!', parsedData.success);
				$('#popup-duplicate-statement').modal('hide');
			}
			
		}).fail(function ajaxFlagArgumentFail() {
			setGlobalErrorHandler('', _t_discussion(requestFailed));
		});
	};
}
