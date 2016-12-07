/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	$('.review-undo').click(function(){
		let queue = $(this).data('queue');
		let id = $(this).data('id');
		let revoked_argument = $('#' + id).attr('title');
		new ReviewHistory().showUndoPopup(queue, id, revoked_argument);
	})
});

function ReviewHistory(){
	
	/**
	 *
	 * @param queue
	 * @param id
	 * @param revoked_argument
	 */
	this.showUndoPopup = function(queue, id, revoked_argument){
		let span = '<span>' + _t(sureToDeleteReview) + '</span>';
		let blockquote = '<blockquote><p>' + revoked_argument + '</p><small>' + _t(revokedArgument) + '</small>';
		let icon = '<i class="text-danger fa fa-exclamation-triangle" aria-hidden="true"></i>';
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' h4.modal-title').html(icon + ' ' + _t(caution));
		$('#' + popupConfirmDialogId + ' div.modal-body').html(span + blockquote);
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
			if (window.location.href.indexOf('history') != -1)
				new AjaxReviewHandler().undoReview(queue, id);
			else
				new AjaxReviewHandler().cancelReview(queue, id);
		});
		$('#' + popupConfirmDialogRefuseBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		});
	}
}

function ReviewHistoryCallbacks(){
	
	/**
	 *
	 * @param jsonData
	 * @param queue
	 * @param uid
	 */
	this.forUndoReview = function(jsonData, queue, uid){
		let parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length != 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else {
			setGlobalSuccessHandler('Yep!', parsedData.success);
			$('#' + queue + uid).remove();
		}
	}
}