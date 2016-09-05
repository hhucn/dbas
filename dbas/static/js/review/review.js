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
		var send_edit = $('#send_edit');
		
		send_edit.addClass('disabled');
		$('#close-optimization-container').click(function(){
			container.hide();
			opti_ack.removeClass('disabled');
			_this.stopCountdown();
			send_edit.addClass('disabled');
			new AjaxReviewHandler().un_lockOptimizationReview(review_uid, false, _this);
		});
		//_this.startCountdown();
		new AjaxReviewHandler().un_lockOptimizationReview(review_uid, true, _this);
		
		// for each input in table
		$.each(container.find('table').find('input'), function(){
			$(this).focus(function(){
				if ($(this).val().length == 0){
					$(this).val($(this).attr('placeholder'));
					$('#send_edit').removeClass('disabled');
				}
			});
		});
	};
	
	this.sendOptimization = function(){
		var container = $('#optimization-container');
		$.each(container.find('table').find('input'), function(){
			var edit_array = [];
			if ($(this).val().length > 0 && $(this).val() != $(this).attr('placeholder')) {
				edit_array.push({
					'uid': $(this).data('id'),
					'type': $(this).data('type'),
					'val': $(this).val()
				});
			}
			if (edit_array.length > 0){
				//new AjaxReviewHandler().reviewOptimizationArgument(true, $('#send_edit').data('id'), JSON.stringify(edit_array));
			} else {
				setGlobalInfoHandler('Ohh!', _t(noEditsInOptimization));
			}
		});
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
		ss.text(countdown_sec < 10 ? '0' + countdown_sec : countdown_sec).removeClass('text-danger');
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