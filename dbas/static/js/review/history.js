$(document).ready(function () {
    'use strict';

    $('.review-undo').click(function () {
        var queue = $(this).data('queue');
        var id = $(this).data('id');
        var revokedArgument = $('#' + queue + id + ' td:first-child').attr('title');
        new ReviewHistory().showUndoPopup(queue, id, revokedArgument);
    });
});

function ReviewHistory() {
    'use strict';

    /**
     *
     * @param queue
     * @param id
     * @param revoked_argument
     */
    this.showUndoPopup = function (queue, id, revoked_argument) {
        var span = '<span>' + _t(sureToDeleteReview) + '</span>';
        var blockquote = '<blockquote><p>' + revoked_argument + '</p><small>' + _t(revokedArgument) + '</small>';
        var icon = '<i class="text-danger fa fa-exclamation-triangle" aria-hidden="true"></i>';
        $('#' + popupConfirmDialogId).modal('show');
        $('#' + popupConfirmDialogId + ' h4 span').html(icon + ' ' + _t(caution));
        $('#' + popupConfirmDialogId + ' div.modal-body').html(span + blockquote);
        $('#' + popupConfirmDialogAcceptBtn).show().click(function () {
            $('#' + popupConfirmDialogId).modal('hide');
            if (window.location.href.indexOf('history') !== -1) {
                new AjaxReviewHandler().undoReview(queue, id);
            } else {
                new AjaxReviewHandler().cancelReview(queue, id);
            }
        });
        $('#' + popupConfirmDialogRefuseBtn).show().click(function () {
            $('#' + popupConfirmDialogId).modal('hide');
        });
    };
}
