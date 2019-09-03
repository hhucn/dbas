/**
 * Use this to call any url asynchronously
 *
 * @param url to call
 * @param method POST or GET
 * @param data for the body, will be json-decoded
 * @param ajaxDone is the function to call after ajax is done
 * @param ajaxFail is the function to call on fail
 */
function ajaxSkeleton(url, method, data, ajaxDone, ajaxFail) {
    'use strict';
    $.ajax({
        url: url,
        method: method,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        headers: {'X-CSRF-Token': $('#' + hiddenCSRFTokenId).val()}
    }).done(function (data_done) {
        ajaxDone(data_done);
    }).fail(function (data_fail) {
        if (data_fail.status === 200) {
            location.reload(true);
        } else if (data_fail.statusText === 'Bad CSRF Token' || data_fail.responseJSON && !('errors' in data_fail.responseJSON)) {
            setGlobalErrorHandler(_t(ohsnap), _t(requestFailedBadToken));
        } else {
            ajaxFail(data_fail);
        }
    });
}

function AjaxMainHandler() {
    'use strict';

    /**
     * Sends a request for language change
     * @param new_lang is the shortcut for the language
     */
    this.switchDisplayLanguage = function (new_lang) {
        var url = mainpage + 'switch_language';
        var data = {'lang': new_lang};
        var done = function ajaxSwitchDisplayLanguageDone() {
            setAnalyticsOptOutLink(new_lang);
            location.reload(true);
        };
        var fail = function ajaxSwitchDisplayLanguageFail(data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', data, done, fail);
    };

    /**
     * Get-Request for an roundhouse kick
     */
    this.roundhouseKick = function () {
        $.ajax({
            url: 'http://api.icndb.com/jokes/random',
            type: 'GET'
        }).done(function ajaxRoundhouseKickDone(data) {
            if (data.type === 'success') {
                displayConfirmationDialogWithoutCancelAndFunction('Chuck Norris Fact #' + data.value.id,
                    '<p>' + data.value.joke + '</p>' +
                    '<p class="pull-right">powered by ' +
                    '<a href="http://www.icndb.com/" target="_blank">http://www.icndb.com/</a>' +
                    '</p>');
            }
        });
    };
}
