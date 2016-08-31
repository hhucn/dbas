/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	$('.review-undo').click(function(){
		var queue = $(this).data('queue');
		var id = $(this).data('id');
		new ReviewHistory().showUndoPopup(queue, id);
	})
});

function ReviewHistory(){
	
	/**
	 *
	 * @param queue
	 * @param id
	 */
	this.showUndoPopup = function(queue, id){
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' h4.modal-title').text(_t(caution));
		$('#' + popupConfirmDialogId + ' div.modal-body').html(_t(sureToDeleteReview));
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
			new AjaxReviewHandler().undoReview(queue, id)
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
	 */
	this.forUndoReview = function(jsonData){
		var parsedData = $.parseJSON(jsonData);
		if (parsedData.error.length != 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else if (parsedData.info.length != 0) {
			setGlobalInfoHandler('Mhh!', parsedData.info);
		} else {
			setGlobalSuccessHandler('Yep!', parsedData.success);
		}
		
	}
}