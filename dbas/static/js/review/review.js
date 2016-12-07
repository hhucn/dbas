/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function Review() {
	const sec = parseInt($('#request-lock').data('lock_sec'));
	let countdown;
	const _this = this;
	const countdown_min = parseInt(sec/60);
	const countdown_sec = sec - countdown_min * 60;
	
	/**
	 *
	 */
	this.doOptimizationAck = function(review_uid) {
		const container = $('#optimization-container');
		const opti_ack = $('#opti_ack');
		const send_edit = $('#send_edit');
		
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
	
	/**
	 *
	 */
	this.sendOptimization = function(){
		const container = $('#optimization-container');
		let edit_array = [];
		// getting all edited values
		$.each($('#argument-part-table').find('input'), function(){
			if ($(this).val().length > 0 && $(this).val() != $(this).attr('placeholder')) {
				edit_array.push({
					statement: $(this).data('statement'),
					type: $(this).data('type'),
					argument: $(this).data('argument'),
					val: $(this).val()
				});
			}
		});
		
		if (edit_array.length > 0){
			const id = $('#send_edit').data('id');
			new AjaxReviewHandler().reviewOptimizationArgument(true, id, edit_array);
		} else {
			setGlobalInfoHandler('Ohh!', _t(noEditsInOptimization));
		}
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
	 * @param review_uid
	 */
	this.doEditAck = function(review_uid){
		new AjaxReviewHandler().reviewEditArgument(true, review_uid);
	};
	
	/**
	 *
	 * @param review_uid
	 */
	this.doEditNack = function(review_uid){
		new AjaxReviewHandler().reviewEditArgument(false, review_uid);
	};
	
	/**
	 *
	 */
	this.startCountdown = function(){
		const mm = $('#countdown_timer_min');
		const ss = $('#countdown_timer_sec');
		const point = $('#countdown_timer_point');
		mm.text(countdown_min).removeClass('text-danger').addClass('text-info');
		ss.text(countdown_sec < 10 ? '0' + countdown_sec : countdown_sec).removeClass('text-danger').addClass('text-info');
		point.removeClass('text-danger').addClass('text-info');
		$('#request-lock-text').show();
		$('#request-not-lock-text').show();
		
		countdown = new Countdown({
            seconds: countdown_min * 60 + countdown_sec,  // number of seconds to count down
            onUpdateStatus: function(sec){
            	const m = parseInt(sec / 60);
	            const s = sec - m * 60;
            	mm.text(m);
            	ss.text(s < 10 ? '0' + s : s);
	            if (sec <= 60){
	            	mm.addClass('text-danger').removeClass('text-info');
	            	ss.addClass('text-danger').removeClass('text-info');
		            point.addClass('text-danger').removeClass('text-info');
	            }
            }, // callback for each second
            onCounterEnd: function(){
            	setGlobalErrorHandler(_t(ohsnap), _t(countdownEnded));
	            $('#send_edit').addClass('disabled');
				$('#request-lock-text').hide();
				$('#request-not-lock-text').show();
				const button = $('#request-lock');
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
		const button = $('#request-lock');
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