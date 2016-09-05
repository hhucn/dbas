/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function Review() {
	var countdown;
	var _this = this;
	var countdown_min = 0;
	var countdown_sec = 10;
	
	/**
	 *
	 */
	this.doOptimizationAck = function(review_uid) {
		var container = $('#optimization-container');
		var button = $('#opti_ack');
		
		$('#close-optimization-container').click(function(){
			container.hide();
			button.removeClass('disabled');
			_this.stopCountdown();
			new AjaxReviewHandler().un_lockOptimizationReview(review_uid, false, _this);
		});
		
		button.click(function(){
			if (!$(this).hasClass('disabled')){
			_this.stopCountdown();
				
			}
		});
		//_this.startCountdown();
		new AjaxReviewHandler().un_lockOptimizationReview(review_uid, true, _this);
	};
	
	/**
	 *
	 */
	this.doDeleteAck = function(review_uid) {
		new AjaxReviewHandler().reviewDeleteArgument(true, review_uid);
	};
	
	/**
	 *
	 */
	this.doDeleteNack = function(review_uid) {
		new AjaxReviewHandler().reviewDeleteArgument(false, review_uid);
	};
	
	/**
	 *
	 */
	this.startCountdown = function(){
		var mm = $('#countdown_timer_min');
		var ss = $('#countdown_timer_sec');
		var point = $('#countdown_timer_point');
		mm.text(countdown_min).removeClass('text-danger');
		ss.text(countdown_sec).removeClass('text-danger');
		point.removeClass('text-danger');
		$('#request_lock_text').show();
		$('#request_not_lock_text').show();
		
		countdown = new Countdown({
            seconds: countdown_min * 60 + countdown_sec,  // number of seconds to count down
            onUpdateStatus: function(sec){
            	var m = parseInt(sec / 60);
	            var s = sec - m * 60;
            	mm.text(m);
            	ss.text(s < 10 ? '0' + s : s);
	            if (sec <= 60){
	            	mm.addClass('text-danger');
	            	ss.addClass('text-danger');
		            point.addClass('text-danger');
	            }
            }, // callback for each second
            onCounterEnd: function(){
            	setGlobalErrorHandler(_t(ohsnap), _t(countdownEnded));
	            $('#send_edit').addClass('disabled');
				$('#request_lock_text').hide();
				$('#request_not_lock_text').show();
				var button = $('#request_lock');
				button.show();
				new AjaxReviewHandler().un_lockOptimizationReview(button.data('id'), false, undefined);
            } // final action
		});
		countdown.start();
	};
	
	/**
	 *
	 */
	this.stopCountdown = function(){
		if (countdown)
			countdown.stop();
		var button = $('#request_lock');
		button.hide();
		new AjaxReviewHandler().un_lockOptimizationReview(button.data('id'), false, undefined);
	};
	
	/**
	 *
	 * @param only_unlock
	 */
	this.reloadPageAndUnlockData = function (only_unlock){
		new AjaxReviewHandler().un_lockOptimizationReview($('#review-id').text(), false, undefined);
		if (! only_unlock)
			location.reload();
	};
	
}