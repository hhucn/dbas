/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxReferenceHandler(){
	'use strict';

	/**
	 *
	 * @param uid
	 * @param reference
	 * @param ref_source
	 */
	this.setReference = function(uid, reference, ref_source){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();

		$.ajax({
			url: 'set_references',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				uid: uid,
				ref_source: ref_source,
				reference: reference
			}),
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function () {
			setGlobalSuccessHandler('Yeah!', _t_discussion(dataAdded));
			$('#' + popupReferences).modal('hide');
		}).fail(function (data) {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
		});
	};

	/**
	 *
	 * @param uids
	 * @param is_argument
	 */
	this.getReferences = function(uids, is_argument){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'get_references',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				'uids': uids,
				'is_argument': is_argument
			}),
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function (data) {
			new PopupHandler().showReferencesPopup(data);
		}).fail(function (data) {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
		});
	};
}
