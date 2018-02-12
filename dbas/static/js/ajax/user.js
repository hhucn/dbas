/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxUserHandler(){
	"use strict";
	/**
	 * Ajax call for user data
	 */
	this.getPublicUserData = function () {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_public_user_data',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({'nickname': $('#public_nick').text()}),
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getPublicUserDataDone(data) {
			new User().callbackDone(data);
		}).fail(function getPublicUserDataFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		});
	};
}
