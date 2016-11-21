/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

// main function
$(document).ready(function () {
	$('#admin-login-button').click(function(){
		new AjaxMainHandler().ajaxLogin($('#admin-login-user').val(), $('#admin-login-pw').val(), true);
	});
	
	var data = $('#data');
	
	// gui modification for the caution row
	if (!isCookieSet('hide-admin-caution-warning')) {
		$('#close-warning').fadeIn();
		$('#close-warning-btn').click(function(){
			$('#close-warning').fadeOut();
			setCookieForDays('hide-admin-caution-warning', 7, 'true')
		});
	}
	
	// set pointer and click event for every row
	$('#admin-overview').find('tr').each(function() {
		$(this).css('cursor', 'pointer');
		$(this).click(function (){
			window.location.href = $(this).data('href');
		});
	})
	
});
