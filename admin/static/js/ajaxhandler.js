/**
 * Created by tobias on 20.10.16.
 */

function AdminIndex(){
	
	/**
	 *
	 */
	this.login = function () {
		var csrfToken = $('#' + hiddenCSRFTokenId).val();
		$('#admin-login-failed').hide();
		$('#admin-login-failed-message').html('');
		
		var user = $('#admin-login-user').val();
		var password = $('#admin-login-pw').val();
		var url = window.location.href;
		var keep_login = $('#admin-keep-login-box').prop('checked') ? 'true' : 'false';
		$.ajax({
			url: mainpage + 'ajax_user_login',
			type: 'GET',
			data: {
				user: user,
				password: password,
				url: url,
				keep_login: keep_login
			},
			dataType: 'json',
			async: true,
			headers: {'X-CSRF-Token': csrfToken}
		}).done(function (data) { // display fetched data
			try {
				var jsonData = $.parseJSON(data);
				if (jsonData.error.length != 0) {
					$('#admin-login-failed').show();
					$('#admin-login-failed-message').html(jsonData.error);
				} else {
					location.reload(true);
				}
			} catch(err){
				//var htmlData = $.parseHTML(data);
				var url = location.href;
				if (url.indexOf('?session_expired=true') != -1)
					url = url.substr(0, url.length - '?session_expired=true'.length);
				location.href = url;
			}
		}).fail(function () { // display error message
			setGlobalErrorHandler('Ohh', _t(requestFailed));
			location.reload();
		});
	};
}

function AdminAjaxHandler(){
	
	/**
	 *
	 * @param uid
	 * @param element
	 */
	this.deleteSomething = function(uid, element){
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_admin_delete',
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
	 * @param element
	 * @param uid
	 * @param keys
	 * @param values
	 */
	this.updateSomething = function(element, uid, keys, values){
		var table = $('#table_name').text();
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_admin_update',
			dataType: 'json',
			data: {
				'uid': uid,
				'table': table,
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
}