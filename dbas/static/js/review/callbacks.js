function ReviewCallbacks() {
    'use strict';

    /**
     *
     * @param jsonData
     * @param review_instance
     */
    this.forReviewLock = function (jsonData, review_instance) {
        if (jsonData.info.length !== 0) {
            setGlobalInfoHandler('Mhh!', jsonData.info);
            return true;
        }
        if (!jsonData.is_locked) {
            setGlobalInfoHandler('Ohh!', _t(couldNotLock));
            return true;
        }
        review_instance.startCountdown();
        $('#optimization-container').show();
        $('#opti_ack').addClass('disabled');
        $('#request-lock').hide();
        $('#request-not-lock-text').hide();
        $('#send_edit').removeClass('disabled');

        var reviewArgumentText = $('#reviewed-argument-text');
        reviewArgumentText.attr('data-oem', reviewArgumentText.text());

        $.each($('#argument-part-table').find('input'), function () {
            var htmlText = reviewArgumentText.html();
            var pos = htmlText.toLowerCase().indexOf($(this).attr('placeholder').toLowerCase());
            var replacement = '<span id="text' + $(this).data('id') + '">' + $(this).attr('placeholder') + '</span>';
            var replText = htmlText.substr(0, pos) + replacement + htmlText.substr(pos + $(this).attr('placeholder').length);
            reviewArgumentText.html(replText);

            $(this).focusin(function () {
                $('#text' + $(this).data('id')).addClass('text-warning');
            });

            $(this).focusout(function () {
                $('#text' + $(this).data('id')).removeClass('text-warning');
            });

            $(this).on('input', function () {
                $('#text' + $(this).data('id')).text($(this).val());
            });
        });
        return true;
    };

    /**
     *
     * @param data
     */
    this.forReviewUnlock = function (data) {
        if (parsedData.error.length !== 0) {
            setGlobalErrorHandler(_t(ohsnap), data.error);
        } else if (parsedData.info.length !== 0) {
            setGlobalInfoHandler('Mhh!', data.info);
        }
    };
}
