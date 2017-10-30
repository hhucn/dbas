

/**
 * main function
 */
$(document).ready(function mainDocumentReady() {
	'use strict';
	$('.btn-dbas').click(function(){
		$('#popup-login-registration-field').removeClass('hidden');
	});
	
	$('.btn-hhu').click(function(){
		$('#popup-login-hhu-text').removeClass('hidden');
		$('#' + popupLogin).find('.nav-tabs:first').find('a');
	});
	
	$('.btn-google').click(function(){
		new AjaxMainHandler().oauthLogin('google', window.location.href);
	});
	
	$('.btn-facebook').click(function(){
		alert('todo: facebook');
	});
	
	$('.btn-twitter').click(function(){
		alert('todo: twitter');
	});
	
	$('.btn-github').click(function(){
		alert('todo: github');
	});
	
	
	$('#' + popupLogin).on('hidden.bs.modal', function () {// uncheck login button on hide
		var list = $('#' + discussionSpaceListId);
		if (list) {
			var login_item = list.find('#item_login');
			if (login_item.length > 0) {
				login_item.prop('checked', false);
			}
		}
		$('#popup-login-registration-field').addClass('hidden');
		$('#popup-login-hhu-text').addClass('hidden');
	}).on('shown.bs.modal', function () {
		$('#' + loginUserId).focus();
	});
	
	// check href for id's
	var url = window.location.href;
	if (url.indexOf('state=') !== -1 && url.indexOf('code=') !== -1){
		new AjaxMainHandler().oauthLogin('google', url);
	}
	
});