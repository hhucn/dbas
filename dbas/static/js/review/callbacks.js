/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function ReviewCallbacks() {
    'use strict';
    	
	/**
	 *
	 * @param jsonData
	 */
	this.forReviewArgumentOrStatement = function(jsonData){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else {
			// reload, when the user is still in the review page
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		}
	};
	
	/**
	 *
	 * @param jsonData
	 * @param review_instance
	 */
	this.forReviewLock = function(jsonData, review_instance){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else if (parsedData.info.length !== 0) {
			setGlobalInfoHandler('Mhh!', parsedData.info);
		} else {
			if (parsedData.is_locked) {
				//setGlobalSuccessHandler('Hurey', parsedData.success);
				review_instance.startCountdown();
				$('#optimization-container').show();
				$('#opti_ack').addClass('disabled');
				$('#request-lock').hide();
				$('#request-not-lock-text').hide();
	            $('#send_edit').removeClass('disabled');
				
				var review_argument_text = $('#reviewed-argument-text');
				review_argument_text.attr('data-oem', review_argument_text.text());
				
				$.each($('#argument-part-table').find('input'), function(){
					var html_text = review_argument_text.html();
					var pos = html_text.toLowerCase().indexOf($(this).attr('placeholder').toLowerCase());
					var replacement = '<span id="text' + $(this).data('id') + '">' + $(this).attr('placeholder') + '</span>';
					var repl_text = html_text.substr(0, pos) + replacement + html_text.substr(pos + $(this).attr('placeholder').length);
					review_argument_text.html(repl_text);
					
					$(this).focusin(function(){
						$('#text' + $(this).data('id')).addClass('text-warning');
					});
					
					$(this).focusout(function(){
						$('#text' + $(this).data('id')).removeClass('text-warning');
					});
					
					$(this).on('input',function(){
						$('#text' + $(this).data('id')).text($(this).val());
					});
				});
			} else {
				setGlobalInfoHandler('Ohh!', _t(couldNotLock));
			}
		}
	};
	
	/**
	 *
	 * @param jsonData
	 */
	this.forReviewUnlock = function(jsonData){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else if (parsedData.info.length !== 0) {
			setGlobalInfoHandler('Mhh!', parsedData.info);
		// } else {
		//	setGlobalSuccessHandler('Hurey', parsedData.success);
		}
	};
	
	// http://kevin.vanzonneveld.net/techblog/article/javascript_equivalent_for_phps_preg_quote/
	function preg_quote( str ) {
    // http://kevin.vanzonneveld.net
    // +   original by: booeyOH
    // +   improved by: Ates Goral (http://magnetiq.com)
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   bugfixed by: Onno Marsman
    // *     example 1: preg_quote("$40");
    // *     returns 1: '\$40'
    // *     example 2: preg_quote("*RRRING* Hello?");
    // *     returns 2: '\*RRRING\* Hello\?'
    // *     example 3: preg_quote("\\.+*?[^]$(){}=!<>|:");
    // *     returns 3: '\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:'
        return (str+'').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1");
	}
}
