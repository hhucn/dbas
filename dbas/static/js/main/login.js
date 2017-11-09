

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
	
	var classes = ['.btn-google', '.btn-facebook', '.btn-twitter', '.btn-github'];
	$.each(classes, function( key, value ) {
		$(value).click(function(){
			new AjaxMainHandler().oauthLogin($(this).data('service'), window.location.href);
		});
	});
	
	$('#nav-tab-login').click(function(){
		$('#' + popupLogin).find('.modal-footer').find('button').addClass('hidden');
	});
	
	$('#nav-tab-signup').click(function(){
		$('#' + popupLogin).find('.modal-footer').find('button').removeClass('hidden');
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
		$('#' + popupLogin).find('.modal-footer').find('button').addClass('hidden');
	});
	
	// check href for id's
	var url = window.location.href;
	var services = ['google', 'facebook', 'twitter', 'github'];
	$.each(services, function( key, value ) {
		if (url.indexOf('service=' + value + '&') !== -1){
			url = url.replace('service=' + value + '&', '');
			new AjaxMainHandler().oauthLogin(value, url);
		}
	});
	
});