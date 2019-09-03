$(document).ready(function () {
    'use strict';

    // buttons
    var optimizationAck = $('#opti_ack');
    var optimizationNack = $('#opti_nack');
    var optimizationSkip = $('#opti_skip');
    var deleteAck = $('#del_ack');
    var deleteNack = $('#del_nack');
    var deleteSkip = $('#del_skip');
    var editAck = $('#edit_ack');
    var editNack = $('#edit_nack');
    var editSkip = $('#edit_skip');
    var duplicateAck = $('#duplicate_ack');
    var duplicateNack = $('#duplicate_nack');
    var duplicateSkip = $('#duplicate_skip');
    var mergeAck = $('#merge_ack');
    var mergeNack = $('#merge_nack');
    var mergeSkip = $('#merge_skip');
    var splitAck = $('#split_ack');
    var splitNack = $('#split_nack');
    var splitSkip = $('#split_skip');
    var requestLock = $('#request-lock');
    var sendEdit = $('#send_edit');

    // text
    var moreAboutReason = $('#more_about_reason');
    var lessAboutReason = $('#less_about_reason');
    var moreAboutReasonContent = $('#more_about_reason_content');

    /**
     * OPTIMIZATION
     */
    optimizationAck.click(function () {
        new Review().doOptimizationAck($(this).data('id'));
    });

    optimizationNack.click(function () {
        new AjaxReviewHandler().reviewOptimizationArgument(false, $(this).data('id'), []);
    });

    optimizationSkip.click(function () {
        new Review().reloadPageAndUnlockData();
    });

    sendEdit.click(function () {
        new Review().sendOptimization();
    });

    /**
     * DELETE
     */
    deleteAck.click(function () {
        new Review().doDeleteAck($(this).data('id'));
    });

    deleteNack.click(function () {
        new Review().doDeleteNack($(this).data('id'));
    });

    deleteSkip.click(function () {
        new Review().reloadPage();
    });

    /**
     * Edit
     */
    editAck.click(function () {
        new Review().doEditAck($(this).data('id'));
    });

    editNack.click(function () {
        new Review().doEditNack($(this).data('id'));
    });

    editSkip.click(function () {
        new Review().reloadPage();
    });

    /**
     * Duplicate
     */
    duplicateAck.click(function () {
        new Review().doDuplicateAck($(this).data('id'));
    });

    duplicateNack.click(function () {
        new Review().doDuplicateNack($(this).data('id'));
    });

    duplicateSkip.click(function () {
        new Review().reloadPage();
    });

    /**
     * Merge
     */
    mergeAck.click(function () {
        new Review().doMergeAck($(this).data('id'));
    });

    mergeNack.click(function () {
        new Review().doMergeNack($(this).data('id'));
    });

    mergeSkip.click(function () {
        new Review().reloadPage();
    });

    /**
     * Split
     */
    splitAck.click(function () {
        new Review().doSplitAck($(this).data('id'));
    });

    splitNack.click(function () {
        new Review().doSplitNack($(this).data('id'));
    });

    splitSkip.click(function () {
        new Review().reloadPage();
    });

    /**
     * MORE
     */
    moreAboutReason.click(function () {
        $(this).hide();
        lessAboutReason.show();
        moreAboutReasonContent.show();
    });

    lessAboutReason.click(function () {
        $(this).hide();
        moreAboutReason.show();
        moreAboutReasonContent.hide();
    });

    requestLock.click(function () {
        new Review().doOptimizationAck($(this).data('id'));
    });

    // align buttons
    var max = 0;
    var elements = $("*[class^='review-btn-']");
    elements.each(function () {
        max = $(this).outerWidth() > max ? $(this).outerWidth() : max;
    });
    elements.each(function () {
        $(this).css('width', max + 'px');
    });

    // extra info when user has already seen the complete queue
    if ($('#stats-table').data('extra-info') === 'already_seen') {
        setGlobalInfoHandler('Info', _t(queueCompleteSeen));
    }

    // unlock data on tab close/reload/...
    $(window).bind('beforeunload', function () {
        if (window.location.href.indexOf('review/optimiz') !== -1) {
            new Review().reloadPageAndUnlockData(true);
        }
    });
});
