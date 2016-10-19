/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
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

// main function
$(document).ready(function () {
	$('#admin-login-button').click(function(){
		new AdminIndex().login();
	});
	
	var data = $('#data');
	
	data.find('.pencil').each(function(){
		$(this).click(function(){
			alert('todo edit');
		})
	});
	
	data.find('.trash').each(function(){
		$(this).click(function(){
			alert('todo delete');
		})
	});
	
	data.find('.add').each(function(){
		$(this).click(function(){
			alert('todo create');
		})
	});
});
