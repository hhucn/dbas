/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	// buttons
	var optimization_ack = $('#optimization_ack');
	var optimization_nack = $('#optimization_nack');
	var optimization_skip = $('#optimization_skip');
	var delete_ack = $('#delete_ack');
	var delete_nack = $('#delete_nack');
	var delete_skip = $('#delete_skip');
	
	// text
	var more_about_reason = $('#more_about_reason');
	var less_about_reason = $('#less_about_reason');
	var more_about_reason_content = $('#more_about_reason_content');
	
	optimization_ack.click(function(){ do_optimization_ack(); });
	optimization_nack.click(function(){ do_optimization_nack(); });
	optimization_skip.click(function(){ location.reload(); });
	delete_ack.click(function(){ do_delete_ack(); });
	delete_nack.click(function(){ do_delete_nack(); });
	delete_skip.click(function(){ location.reload(); });
	
	more_about_reason.click(function() {
		$(this).hide();
		less_about_reason.show();
		more_about_reason_content.show();
	});
	less_about_reason.click(function() {
		$(this).hide();
		more_about_reason.show();
		more_about_reason_content.hide();
	});
});

/**
 *
 */
function do_optimization_ack(){
	alert('do_optimization_ack');
}

/**
 *
 */
function do_optimization_nack(){
	alert('do_optimization_nack');
}

/**
 *
 */
function do_delete_ack(){
	alert('do_delete_ack');
}

/**
 *
 */
function do_delete_nack(){
	alert('do_delete_nack');
}
