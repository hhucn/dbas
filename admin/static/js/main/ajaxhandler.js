/**
 * Created by tobias on 20.10.16.
 */

function AdminAjaxHandler() {
	'use strict';
	
	/**
	 *
	 * @param uids
	 * @param element
	 */
	this.deleteSomething = function (uids, element) {
		var table = $('#table_name').text();
		var url = 'delete';
		var data = {
			'uids': uids,
			'table': table
		};
		var done = function () {
			element.remove();
			setGlobalSuccessHandler('Yehaw!', _t(dataRemoved));
		};
		var fail = function (data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param new_data
	 */
	this.addSomething = function (new_data) {
		var table = $('#table_name').text();
		var url = 'add';
		var data = {
			'new_data': new_data,
			'table': table
		};
		var done = function () {
			setGlobalSuccessHandler('Yehaw!', _t(addedEverything));
			$('#' + popupConfirmRowDialogId).modal('hide');
			var d = $('#data');
			var tbody = d.find('tbody');
			var tr = $('<tr>');
			$.each(new_data, function (key, value) {
				tr.append($('<td>').append($('<span>').text(value)));
			});
			var modify = d.find('.pencil:first').parent().parent().clone();
			tr.append(modify);
			tbody.append(tr);
			var gui = new AdminGui();
			gui.setEditClickEvent(modify);
			gui.setDeleteClickEvent(modify);
			gui.setSaveClickEvent(modify);
			gui.setCancelClickEvent(modify);
		};
		var fail = function (data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param element
	 * @param uids
	 * @param keys
	 * @param values
	 */
	this.updateSomething = function (element, uids, keys, values) {
		var table = $('#table_name').text();
		var url = 'update';
		var data = {
			'table': table,
			'uids': uids,
			'keys': keys,
			'values': values
		};
		var done = function () {
			var gui = new AdminGui();
			gui.deactivateElement(element, 'floppy', 'text-success');
			gui.deactivateElement(element, 'square', 'text-danger');
			gui.activateElement(element, 'pencil', '');
			setGlobalSuccessHandler('Yeah!', _t(dataAdded));
		};
		var fail = function (data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	this.revokeToken = function (id) {
		console.log("Revoking " + id);
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'revoke_token/' + id,
			type: 'DELETE',
			headers: {'X-CSRF-Token': csrf_token},
			cache: false,
			data: {'token_id': id},
			dataType: 'json',
			success: function (result) {
				$('#admin-token-' + id).hide();
				console.log("Token " + id + " revoked!");
			}
		});
	};
	
	this.generateToken = function (owner) {
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'api_token/',
			type: 'POST',
			headers: {'X-CSRF-Token': csrf_token},
			data: $.param({'owner': owner}),
			dataType: 'json',
			cache: false,
			success: function (result) {
				$('#api-token-generate-form').hide();
				$('#api-token').append(result.token).show();
				$('#api-token-footer').show();
			}
		});
	};
}
