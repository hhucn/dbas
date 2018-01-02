/**
 * Created by tobias on 20.10.16.
 */

function AdminAjaxHandler(){
	'use strict';

	/**
	 *
	 * @param uids
	 * @param element
	 */
	this.deleteSomething = function(uids, element){
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_admin_delete',
			dataType: 'json',
			data: {
				'uids': JSON.stringify(uids),
				'table': table
			},
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function (data) {
			new AdminCallbackHandler().doDeleteDone(data, element);
		}).fail(function () {
			new AdminCallbackHandler().doSomethingOnFail();
		});
	};

	/**
	 *
	 * @param new_data
	 */
	this.addSomething = function(new_data){
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_admin_add',
			dataType: 'json',
			data: {
				'new_data': JSON.stringify(new_data),
				'table': table
			},
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function (data) {
			new AdminCallbackHandler().doAddDone(data, new_data);
		}).fail(function () {
			new AdminCallbackHandler().doSomethingOnFail();
		});
	};

	/**
	 *
	 * @param element
	 * @param uids
	 * @param keys
	 * @param values
	 */
	this.updateSomething = function(element, uids, keys, values){
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_admin_update',
			dataType: 'json',
			data: {
				'table': table,
				'uids': JSON.stringify(uids),
				'keys': JSON.stringify(keys),
				'values': JSON.stringify(values)
			},
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function (data) {
			new AdminCallbackHandler().doUpdateDone(data, element);
		}).fail(function () {
			new AdminCallbackHandler().doSomethingOnFail();
		});
	};

	/**
	 *
	 */
	this.updateCountBadges = function () {
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_admin_update_badges',
			dataType: 'json',
			data: {},
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function (data) {
			new AdminCallbackHandler().doUpdateBadges(data);
		}).fail(function () {
			new AdminCallbackHandler().doSomethingOnFail();
		});
	};
}

function AdminCallbackHandler(){
	'use strict';

	/**
	 *
	 */
	this.doSomethingOnFail = function(){
		setGlobalErrorHandler(_t(ohsnap), _t_discussion(requestFailed));
	};

	/**
	 *
	 * @param jsonData
	 * @param element
	 */
	this.doUpdateDone = function(jsonData, element){
        if (jsonData.error.length === 0) {
	        var gui = new AdminGui();
	        gui.deactivateElement(element, 'floppy', 'text-success');
	        gui.deactivateElement(element, 'square', 'text-danger');
	        gui.activateElement(element, 'pencil', '');
			setGlobalSuccessHandler('Yeah!', _t(dataAdded));
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};

	/**
	 *
	 * @param jsonData
	 * @param element
	 */
	this.doDeleteDone = function(jsonData, element){
        if (jsonData.error.length === 0) {
	        element.remove();
			setGlobalSuccessHandler('Yehaw!', _t(dataRemoved));
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};

	/**
	 *
	 * @param jsonData
	 * @param new_data
	 */
	this.doAddDone = function(jsonData, new_data){
        if (jsonData.error.length === 0) {
			setGlobalSuccessHandler('Yehaw!', _t(addedEverything));
	        $('#' + popupConfirmRowDialogId).modal('hide');
	        var d = $('#data');
	        var tbody = d.find('tbody');
	        var tr = $('<tr>');
	        $.each( new_data, function( key, value ) {
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
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};

	/**
	 *
	 * @param jsonData
	 */
	this.doUpdateBadges = function(jsonData){
        if (jsonData.error.length === 0) {
        	$.each(jsonData.data, function(index, element){
        		$('#' + element.name).find('.badge').text(element.count);
	        });
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};
}
