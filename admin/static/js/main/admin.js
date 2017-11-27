/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

// main function
$(document).ready(function () {
	'use strict';
	
	$('#admin-login-button').click(function(){
		var user = $('#admin-login-user').val();
		var pw = $('#admin-login-pw').val();
		new AjaxMainHandler().login(user, pw, true);
	});
	
	if ($('.batman').length === 0) {
		new AdminAjaxHandler().updateCountBadges();
	}
	
	// gui modification for the caution row
	if (!Cookies.get(ADMIN_WARNING)) {
		$('#close-warning').fadeIn();
		$('#close-warning-btn').click(function(){
			$('#close-warning').fadeOut();
			Cookies.set(ADMIN_WARNING, true, { expires: 7 });
		});
	}
	
	// set pointer and click event for every row
	$('#admin-entities').find('tr').each(function() {
		$(this).css('cursor', 'pointer');
		$(this).click(function (){
			window.location.href = $(this).data('href');
		});
	});

	// reset modal if it hides.
	$("#api-token-generate-dialog").on("hidden.bs.modal", function () {
		$('#api-token').hide().empty();
		$('#api-token-footer').hide();
		$('#api-token-generate-form').show();
	});
	
});

function revoke_token(id) {
	'use strict';
	console.log("Revoking " + id);
	var csrf_token = $('#hidden_csrf_token').val();
	$.ajax({
		url: 'revoke_token/' + id,
		type: 'DELETE',
		headers: { 'X-CSRF-Token': csrf_token },
		cache: false,
		data: {'token_id': id},
		dataType: 'json',
		success: function (result) {
			$('#admin-token-' + id).hide();
			console.log("Token " + id + " revoked!");
        }});
}

function generate_token(owner) {
	'use strict';
	var csrf_token = $('#hidden_csrf_token').val();
	$.ajax({
		url: 'api_token/',
		type: 'POST',
		headers: { 'X-CSRF-Token': csrf_token },
		data: $.param({'owner': owner}),
		dataType: 'json',
		cache: false,
		success: function (result) {
			$('#api-token-generate-form').hide();
			$('#api-token').append(result.token).show();
			$('#api-token-footer').show();
        }
	});
}