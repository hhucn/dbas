

/**
 * main function
 */
$(document).ready(function mainDocumentReady() {
	'use strict';
	//$('.btn-dbas').click(function(){
	//	$('#popup-login-registration-field').removeClass('hidden');
	//	$('#' + popupLogin).find('.modal-footer').removeClass('hidden');
	//});
	
	//$('.btn-hhu').click(function(){
	//	$('#popup-login-hhu-text').removeClass('hidden');
	//	$('#nav-tab-login').find('a').trigger('click');
	//	$('#' + popupLogin).find('.modal-footer').removeClass('hidden');
	//});
	
	$('.btn-google').click(function(){
		new AjaxMainHandler().oauthLogin('google', window.location.href);
	});
	
	$('.btn-facebook').click(function(){
		new AjaxMainHandler().oauthLogin('facebook', window.location.href);
	});
	
	$('.btn-twitter').click(function(){
		alert('todo: twitter');
	});
	
	$('.btn-github').click(function(){
		new AjaxMainHandler().oauthLogin('github', window.location.href);
	});
	
	$('#nav-tab-login').click(function(){
		$('#' + popupLogin).find('.modal-footer').addClass('hidden');
	});
	
	$('#nav-tab-signup').click(function(){
		$('#' + popupLogin).find('.modal-footer').removeClass('hidden');
	});
	
	// restore login popup to default
	$('#' + popupLogin).on('hidden.bs.modal', function () {
		var list = $('#' + discussionSpaceListId);
		if (list) {
			var login_item = list.find('#item_login');
			if (login_item.length > 0) {
				login_item.prop('checked', false);
			}
		}
	}).on('shown.bs.modal', function () {
		$('#' + loginUserId).focus();
		$('#' + popupLogin).find('.modal-footer').addClass('hidden');
	});
	
	// check href for id's
	var url = window.location.href;
	
	if (url.indexOf('state=') !== -1 && url.indexOf('code=') !== -1){
		new AjaxMainHandler().oauthLogin('google', url);
	}
	
});