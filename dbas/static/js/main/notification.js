/**
 * Script for the personal message board
 */

$(function () {
    'use strict';

    // execute only in the notifications page
    if (window.location.href.indexOf(mainpage + 'notifications') === -1) {
        return;
    }

    var not = new Notifications();
    not.setGui();
    not.setPanelClickFunctions();
    not.setClickFunctionsForAnswerNotification();
    not.setClickFunctionsForNewNotification();
    not.setClickFunctionsForRead();
    not.setClickFunctionsForDelete();
    not.setClickFunctionsForCheckboxes();
});

function Notifications() {
    'use strict';

    this.setGui = function () {
        // proposals for user while typing the recipient
        $('#popup-writing-notification-recipient').off('keyup').keyup(function () {
            setTimeout(function () {
                var escapedText = escapeHtml($('#popup-writing-notification-recipient').val());
                new AjaxDiscussionHandler().fuzzySearch(escapedText, 'popup-writing-notification-recipient', fuzzy_find_user, '');
            }, 200);
        });

        // clear proposals on focus change
        $('#popup-writing-notification-title').focusin(function () {
            $('#proposal-user-list-group').empty();
        });

        // clear proposals on focus change
        $('#popup-writing-notification-text').focusin(function () {
            $('#proposal-user-list-group').empty();
        });

        if (parseInt($('#total_in_counter').text()) > 0) {
            $('#read-inbox').removeClass('hidden');
            $('#delete-inbox').removeClass('hidden');
        }

        if (parseInt($('#total_out_counter').text()) > 0) {
            $('#delete-outbox').removeClass('hidden');
        }

    };

    /**
     *
     */
    this.setPanelClickFunctions = function () {
        $.each($('.panel-title-link'), function ajaxLinksRead() {
            $(this).click(function () {
                var id = $(this).parent().parent().parent().attr('id');
                if ($(this).html().indexOf('<strong') !== -1) {
                    new AjaxNotificationHandler().readMessages([id]);
                }
            });
        });

        $.each($('.fa-trash'), function ajaxLinksDelete() {
            $(this).off('click').click(function () {
                $(this).parent().parent().attr('href', '');
                new AjaxNotificationHandler().deleteMessages([$(this).data('id')]);
            });
        });
    };

    /**
     *
     */
    this.setClickFunctionsForNewNotification = function () {
        // send notification to users
        $('#new-notification').click(function () {
            new PopupHandler().showNotificationPopup();
        });
    };

    /**
     *
     */
    this.setClickFunctionsForAnswerNotification = function () {
        // send notification to users
        $('.answer-notification').each(function () {
            $(this).click(function () {
                $('#popup-writing-notification-recipient').show().val($(this).prev().text().trim());
                $('#popup-writing-notification').modal('show');
                $('#popup-writing-notification-success').hide();
                $('#popup-writing-notification-failed').hide();
                var panel = $(this).parent().parent().parent().parent();
                var title = panel.find('.notification-title').text();
                var content = panel.find('.notification-content').text();
                $('#popup-writing-notification-title').val(title);
                $('#popup-writing-notification-text').text(content);
                $('#popup-writing-notification-send').click(function () {
                    new AjaxNotificationHandler().sendNotification($('#popup-writing-notification-recipient').val());
                });
            });
        });

        $('.new-notification').each(function () {
            $(this).click(function () {
                $('#popup-writing-notification-recipient').hide();
                $('#popup-writing-notification').modal('show');
                $('#popup-writing-notification-success').hide();
                $('#popup-writing-notification-failed').hide();
                $('#popup-writing-notification-send').click(function () {
                    var url = window.location.href;
                    var splitted = url.split('/');
                    var recipient;
                    if (url.indexOf('/user/') === -1) {
                        recipient = $(this).prev().text();
                    } else {
                        recipient = splitted[splitted.length - 1];
                    }
                    new Notifications().sendNotification(recipient.trim());
                });
            });
        });
    };

    /**
     * Collect all messages and return their uids.
     */
    function collectMessages(selector) {
        var uids = [];
        var inbox = $(selector);
        inbox.find('.msg-checkbox:checked').each(function () {
            uids.push($(this).attr('id'));
        });
        if (uids.length === 0) {
            inbox.find('.msg-checkbox').each(function () {
                uids.push($(this).attr('id'));
            });
        }
        return uids;
    }

    this.setClickFunctionsForRead = function () {
        $('#read-inbox').click(function () {
            var uids = collectMessages('#inbox');
            new AjaxNotificationHandler().readMessages(uids);
        });
    };

    this.setClickFunctionsForDelete = function () {
        $('#delete-inbox').click(function () {
            var uids = collectMessages('#inbox');
            new AjaxNotificationHandler().deleteMessages(uids);
        });

        $('#delete-outbox').click(function () {
            var uids = collectMessages('#outbox');
            new AjaxNotificationHandler().deleteMessages(uids);
        });
    };

    /**
     *
     */
    this.setClickFunctionsForCheckboxes = function () {
        $('.msg-checkbox').each(function () {
            $(this).change(function () {
                var count = $('.msg-checkbox:checked').length;
                if (count === 0) {
                    if ($('#inbox-link').attr('aria-expanded') === 'true') {
                        $('#' + deleteInboxTxt).text(_t(deleteEverything));
                        $('#' + readInboxTxt).text(_t(readEverything));
                    } else {
                        $('#' + deleteOutboxTxt).text(_t(deleteEverything));
                    }
                } else {
                    if ($('#inbox-link').attr('aria-expanded') === 'true') {
                        $('#' + deleteInboxTxt).text(_t(deleteMarked));
                        $('#' + readInboxTxt).text(_t(readMarked));
                    } else {
                        $('#' + deleteOutboxTxt).text(_t(deleteMarked));
                    }
                }
            });
        });
    };

    /**
     *
     */
    this.hideInfoSpaces = function () {
        $('#error-space').hide();
        $('#error-description').text('');
    };

    /**
     *
     * @param counter
     */
    this.setNewBadgeCounter = function (counter) {
        if (counter === 0) {
            $('#header_badge_count_notifications').remove();
        } else {
            $('#header_badge_count_notifications').text(counter);
        }
        $('#unread_counter').text(' ' + counter + ' ');
    };
}
