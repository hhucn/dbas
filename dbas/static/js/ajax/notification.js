function AjaxNotificationHandler() {
    'use strict';

    /**
     *
     * @param id_list
     */
    this.readMessages = function (id_list) {
        new Notifications().hideInfoSpaces();

        var url = 'notifications_read';
        var d = {
            ids: id_list
        };
        var done = function sendAjaxForReadMessagesDone(data) {
            $.each(id_list, function (key, uid) {
                var el = $('#' + uid);
                el.find('.label-info').remove();
                var title = el.find('.panel-title-link').text().trim();
                var spanEl = $('<span>').addClass('text-primary').text(title);
                el.find('.panel-title-link').empty().append(spanEl);
            });
            new Notifications().setNewBadgeCounter(data.unread_messages);
            $('.msg-checkbox:checked').each(function () {
                $(this).prop('checked', false);
            });
        };
        var fail = function sendAjaxForReadMessagesFail(data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     * @param id_list
     */
    this.deleteMessages = function (id_list) {
        new Notifications().hideInfoSpaces();

        var url = 'notifications_delete';
        var d = {
            ids: id_list
        };
        var done = function sendAjaxForDeleteMessagesDone(data) {
            $.each(id_list, function (key, value) {
                $('#' + value).remove();
            });
            new Notifications().setNewBadgeCounter(data.unread_messages);
            $('#total_in_counter').text(data.total_in_messages);
            $('#total_out_counter').text(data.total_out_messages);
            setGlobalSuccessHandler('', data.success);
            $('.msg-checkbox:checked').each(function () {
                $(this).prop('checked', false);
            });
        };
        var fail = function sendAjaxForDeleteMessagesFail(data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     * @param recipient
     */
    this.sendNotification = function (recipient) {
        $('#popup-writing-notification-success').hide();
        $('#popup-writing-notification-failed').hide();

        var url = 'send_notification';
        var d = {
            title: $('#popup-writing-notification-title').val(),
            text: $('#popup-writing-notification-text').val(),
            recipient: recipient
        };
        var done = function ajaxSendNotificationDone() {
            $('#popup-writing-notification-success').show();
            $('#popup-writing-notification-success-message').text(_t(notificationWasSend));
            var out_counter = $('#total_out_counter');
            out_counter.text(' ' + (parseInt(out_counter.text()) + 1) + ' ');
            location.reload(true);
        };
        var fail = function ajaxSendNotificationFail(data) {
            $('#popup-writing-notification-failed').show();
            $('#popup-writing-notification-failed-message').html(data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };
}
