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
	
	optimization_ack.click(function(){
		new Review().doOptimizationAck();
	});
	
	optimization_nack.click(function(){
		new Review().doOptimizationNack();
	});
	
	optimization_skip.click(function(){
		location.reload();
	});
	
	delete_ack.click(function(){
		var review_uid = $(this).data('id');
		new Review().doDeleteAck(review_uid);
	});
	
	delete_nack.click(function(){
		var review_uid = $(this).data('id');
		new Review().doDeleteNack(review_uid);
	});
	
	delete_skip.click(function(){
		location.reload();
	});
	
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
	var countdown;
	var _this = this;
	var countdown_min = 4;
	var countdown_sec = 59;
	/**
	 *
	 */
	this.doOptimizationAck = function() {
		var container = $('#optimization-container');
		var button = $('#opti_ack');
		container.show();
		button.addClass('disabled');
		
		$('#close-optimization-container').click(function(){
			container.hide();
			button.removeClass('disabled');
			_this.stopCountdown();
		});
		
		button.click(function(){
			if (!$(this).hasClass('disabled')){
			_this.stopCountdown();
				
			}
		});
		_this.startCountdown();
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
	this.doDeleteAck = function(review_uid) {
		new AjaxReviewHandler().reviewDeleteArgument(true, review_uid);
	};
	
	/**
	 *
	 */
	this.doDeleteNack = function(review_uid) {
		new AjaxReviewHandler().reviewDeleteArgument(false, review_uid);
	};
	
	this.startCountdown = function(){
		var mm = $('#countdown_timer_min');
		var ss = $('#countdown_timer_sec');
		var point = $('#countdown_timer_point');
		mm.text(countdown_min).removeClass('text-danger');
		ss.text(countdown_sec).removeClass('text-danger');
		point.removeClass('text-danger');
		countdown = new Countdown({
            seconds: countdown_min * 60 + countdown_sec,  // number of seconds to count down
            onUpdateStatus: function(sec){
            	var m = parseInt(sec / 60);
	            var s = sec - m * 60;
	            console.log(m + ' ' + (s < 10 ? '0' + s : s));
            	mm.text(m);
            	ss.text(s < 10 ? '0' + s : s);
	            if (sec == 60){
	            	mm.addClass('text-danger');
	            	ss.addClass('text-danger');
		            point.addClass('text-danger');
	            }
            }, // callback for each second
            onCounterEnd: function(){
            	setGlobalErrorHandler(_t(ohsnap), _t(countdownEnded));
	            $('#opti_nack').addClass('disabled');
	            $('#send-edit').addClass('disabled');
            } // final action
		});
		countdown.start();
	};
	
	this.stopCountdown = function(){
		countdown.stop();
	}
	
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
				location.reload();
			}
		}
	}
}

/**
 *
 * @param options
 * @constructor
 */
function Countdown(options) {
	var timer;
	var instance = this;
	var seconds = options.seconds;
	var updateStatus = options.onUpdateStatus;
	var counterEnd = options.onCounterEnd;
	function decrementCounter() {
		updateStatus(seconds);
		if (seconds === 0) {
			counterEnd();
			instance.stop();
		}
		seconds--;
	}
	
	/**
	 *
	 */
	this.start = function () {
		clearInterval(timer);
		seconds = options.seconds;
		timer = setInterval(decrementCounter, 1000);
	};
	
	/**
	 *
	 */
	this.stop = function () {
		clearInterval(timer);
	};
}