/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	var optimization_ack = $('#optimization_ack');
	var optimization_nack = $('#optimization_nack');
	var optimization_skip = $('#optimization_skip');
	var delete_ack = $('#delete_ack');
	var delete_nack = $('#delete_nack');
	var delete_skip = $('#delete_skip');
	
	optimization_skip.click(function(){
		location.reload();
	});
	
	delete_skip.click(function(){
		location.reload();
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
