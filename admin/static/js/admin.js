/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

// main function
$(document).ready(function () {
	$('#admin-login-button').click(function(){
		new AjaxMainHandler().ajaxLogin($('#admin-login-user').val(), $('#admin-login-pw').val(), true);
	});
	
	const data = $('#data');
	
	// gui modification for the caution row
	if (!Cookies.get(ADMIN_WARNING)) {
		$('#close-warning').fadeIn();
		$('#close-warning-btn').click(function(){
			$('#close-warning').fadeOut();
			Cookies.set(ADMIN_WARNING, true, { expires: 7 });
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
