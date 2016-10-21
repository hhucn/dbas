/**
 * Created by tobias on 20.10.16.
 */

function AdminAjaxHandler(){
	
	/**
	 *
	 * @param uid
	 */
	this.deleteSomething = function(uid, element){
		console.log('ajax delete ' + uid);
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: mainpage + 'ajax_admin_delete',
			type: 'POST',
			dataType: 'json',
			data: {
				'uid': uid,
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
	 * @param uid
	 * @param keys
	 * @param values
	 */
	this.saveSomething = function(uid, keys, values){
		console.log('ajax save ' + uid);
		console.log('ajax save ' + keys);
		console.log('ajax save ' + values);
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: mainpage + 'ajax_admin_update',
			type: 'POST',
			dataType: 'json',
			data: {
				'uid': uid,
				'table': table,
				'keys': keys,
				'values': values
			},
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function (data) {
			new AdminCallbackHandler().doUpdateDone(data);
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
	 * @param uid
	 */
	this.doUpdateDone = function(uid){
        var jsonData = $.parseJSON(data);
        if (jsonData.error.length === 0) {
	        console.log('callback success' + uid);
	        var gui = new AdminGui();
	        gui.deactivateElement(this, 'floppy', 'text-success');
	        gui.deactivateElement(this, 'square', 'text-danger');
	        gui.activateElement(this, 'pencil', '');
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
	        console.log('callback delete ' + uid);
	        element.clear();
        } else {
			setGlobalErrorHandler(_t(ohsnap), jsonData.error);
        }
	};
}