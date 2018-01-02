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
			method: 'GET',
			data:{ 'nickname': $('#public_nick').text() },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getPublicUserDataDone(data) {
			new User().callbackDone(data);
		}).fail(function getPublicUserDataFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}
