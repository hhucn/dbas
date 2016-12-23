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
		const table = $('#table_name').text();
		const csrf_token = $('#hidden_csrf_token').val();
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
		const table = $('#table_name').text();
		const csrf_token = $('#hidden_csrf_token').val();
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
		const table = $('#table_name').text();
		const csrf_token = $('#hidden_csrf_token').val();
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
	
	/**
	 *
	 */
	this.updateCountBadges = function () {
		const csrf_token = $('#hidden_csrf_token').val();
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
	}
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
        const jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
	        const gui = new AdminGui();
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
	 * @param data
	 * @param element
	 */
	this.doDeleteDone = function(data, element){
        const jsonData = $.parseJSON(data);
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
        const jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
			setGlobalSuccessHandler('Yehaw!', _t(addedEverything));
	        $('#' + popupConfirmRowDialogId).modal('hide');
	        const data = $('#data');
	        const tbody = data.find('tbody');
	        const tr = $('<tr>');
	        $.each( new_data, function( key, value ) {
		        tr.append($('<td>').append($('<span>').text(value)));
	        });
	        const modify = data.find('.pencil:first').parent().parent().clone();
	        tr.append(modify);
	        tbody.append(tr);
	        const gui = new AdminGui();
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
	 * @param data
	 */
	this.doUpdateBadges = function(data){
        const jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
        	console.log(jsonData);
        	$.each(jsonData.data, function(index, element){
        		console.log(element);
        		$('#' + element['name']).find('.badge').text(element['count']);
	        });
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	}
}
