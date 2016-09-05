/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function Review() {
	var sec = parseInt($('#request-lock').data('lock_sec'));
	var countdown;
	var _this = this;
	var countdown_min = parseInt(sec/60);
	var countdown_sec = sec - countdown_min * 60;
	
	/**
	 *
	 */
	this.doOptimizationAck = function(review_uid) {
		var container = $('#optimization-container');
		var opti_ack = $('#opti_ack');
		
		$('#close-optimization-container').click(function(){
			container.hide();
			opti_ack.removeClass('disabled');
			_this.stopCountdown();
			new AjaxReviewHandler().un_lockOptimizationReview(review_uid, false, _this);
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
		$('#request-lock-text').show();
		$('#request-not-lock-text').show();
		
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
				$('#request-lock-text').hide();
				$('#request-not-lock-text').show();
				var button = $('#request-lock');
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
		var button = $('#request-lock');
		button.hide();
		new AjaxReviewHandler().un_lockOptimizationReview(button.data('id'), false, undefined);
	};
	
	/**
	 *
	 * @param only_unlock
	 */
	this.reloadPageAndUnlockData = function (only_unlock){
		new AjaxReviewHandler().un_lockOptimizationReview($('#review-id').data('id'), false, undefined);
		if (! only_unlock)
			location.reload();
	};
	
}