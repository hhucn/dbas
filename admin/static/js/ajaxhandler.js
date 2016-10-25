/**
 * Created by tobias on 20.10.16.
 */

function AdminAjaxHandler(){
	
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
		console.log(JSON.stringify(new_data));
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
			new AdminCallbackHandler().doUpdateDone(element, data);
		}).fail(function () {
			new AdminCallbackHandler().doSomethingOnFail();
		});
	};
}

function AdminCallbackHandler(){
	
	/**
	 *
	 */
	this.doSomethingOnFail = function(){
		setGlobalErrorHandler(_t(ohsnap), _t_discussion(requestFailed));
	};
	
	/**
	 *
	 * @param element
	 * @param data
	 */
	this.doUpdateDone = function(element, data){
        var jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
	        var gui = new AdminGui();
	        gui.deactivateElement(element, 'floppy', 'text-success');
	        gui.deactivateElement(element, 'square', 'text-danger');
	        gui.activateElement(element, 'pencil', '');
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};
	
	/**
	 *
	 * @param data
	 * @param element
	 */
	this.doDeleteDone = function(data, element){
        var jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
	        element.remove();
			setGlobalSuccessHandler('Yehaw!', _t(dataRemoved));
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};
	
	/**
	 *
	 * @param data
	 * @param new_data
	 */
	this.doAddDone = function(data, new_data){
        var jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
			setGlobalSuccessHandler('Yehaw!', _t(addedEverything));
	        $('#' + popupConfirmRowDialogId).modal('hide');
	        var data = $('#data');
	        var tbody = data.find('tbody');
	        var tr = $('<tr>');
	        $.each( new_data, function( key, value ) {
		        tr.append($('<td>').append($('<span>').text(value)));
	        });
	        var modify = data.find('.pencil:first').parent().parent().clone();
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
}