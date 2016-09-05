/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

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
		if (parsedData.error.length != 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else if (parsedData.info.length != 0) {
			setGlobalInfoHandler('Mhh!', parsedData.info);
		} else {
			if (parsedData.is_locked) {
				//setGlobalSuccessHandler('Hurey', parsedData.success);
				review_instance.startCountdown();
				$('#optimization-container').show();
				$('#opti_ack').addClass('disabled');
				$('#request_lock').hide();
			} else {
				setGlobalInfoHandler('Ohh!', _t(couldNotLock));
			}
		}
	};
}
