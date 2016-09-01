/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	// buttons
	var optimization_ack = $('#opti_ack');
	var optimization_nack = $('#opti_nack');
	var optimization_skip = $('#opti_skip');
	var delete_ack = $('#del_ack');
	var delete_nack = $('#del_nack');
	var delete_skip = $('#del_skip');
	
	// text
	var more_about_reason = $('#more_about_reason');
	var less_about_reason = $('#less_about_reason');
	var more_about_reason_content = $('#more_about_reason_content');
	
	optimization_ack.click(function(){ new Review().doOptimizationAck(); });
	optimization_nack.click(function(){ new Review().doOptimizationNack(); });
	optimization_skip.click(function(){ location.reload(); });
	delete_ack.click(function(){ new Review().doDeleteAck(); });
	delete_nack.click(function(){ new Review().doDeleteNack(); });
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
	
	// some info
	if ($('#stats-table').data('extra-info') == 'already_seen'){
		setGlobalInfoHandler('Info', _t(queueCompleteSeen));
	}
});

function Review() {
	/**
	 *
	 */
	this.doOptimizationAck = function() {
		alert('doOptimizationAck');
	};
	
	/**
	 *
	 */
	this.doOptimizationNack = function() {
		alert('doOptimizationNack');
	};
	
	/**
	 *
	 */
	this.doDeleteAck = function() {
		new AjaxReviewHandler().reviewDeleteArgument(true);
	};
	
	/**
	 *
	 */
	this.doDeleteNack = function() {
		new AjaxReviewHandler().reviewDeleteArgument(false);
	};
	
}

function ReviewCallbacks() {
	
	/**
	 *
	 * @param jsonData
	 */
	this.forReviewDeleteArgument = function(jsonData){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length != 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else {
			// reload, when the user is still in the review page
			if (window.location.href.indexOf('/review/')) {
				if (parsedData.extra_info.length != 0)
					window.location.href = window.location.href + '?info=' + parsedData.extra_info;
				else
					location.reload();
			}
		}
	}
}