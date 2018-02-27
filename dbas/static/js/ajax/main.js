/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

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
    var csrf_token = $('#' + hiddenCSRFTokenId).val();
    $.ajax({
        url: url,
        method: method,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        headers: {'X-CSRF-Token': csrf_token}
    }).done(function (data) {
        ajaxDone(data);
    }).fail(function (data) {
        ajaxFail(data);
    });
}

/**
 * Validate content of recaptcha. True if invalid.
 * @returns {boolean}
 */
function invalid_recaptcha() {
    'use strict';
    var answer = parseInt($("#captcha-answer").val());
    var digit1 = parseInt($("#captcha-digit1")[0].innerText);
    var digit2 = parseInt($("#captcha-digit2")[0].innerText);
    var digit3 = parseInt($("#captcha-digit3")[0].innerText);
    var sum = digit1 + digit2 - digit3;
    return answer !== sum || isNaN(answer);
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
     *
     */
    this.login = function (user, password, showGlobalError) {
        var keep_login = $('#keep-login-box').prop('checked');
        $('#' + popupLoginFailed).hide();
        $('#' + popupLoginFailed + '-message').text('');
        $('#' + popupLoginInfo).hide();
        $('#' + popupLoginInfo + '-message').text('');

        var url = mainpage + 'user_login';
        var d = {
            user: user,
            password: password,
            redirect_url: window.location.href,
            keep_login: keep_login
        };
        var done = function ajaxLoginDone(data) {
            $('#' + loginPwId).val('');
            callbackIfDoneForLogin(data, showGlobalError);
        };
        var fail = function ajaxLoginFail(xhr) {
            $('#' + loginPwId).val('');
            if (xhr.status === 200) {
                location.reload(true);
            } else if (xhr.status === 302) {
                location.href = xhr.getResponseHeader('Location');
            } else {
                setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
            }
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     * @param service
     * @param redirect_uri
     */
    this.oauthLogin = function (service, redirect_uri) {
        $('#' + popupLoginFailed).hide();
        $('#' + popupLoginFailed + '-message').text('');
        $('#' + popupLoginInfo).hide();
        $('#' + popupLoginInfo + '-message').text('');

        var url = mainpage + 'user_login_oauth';
        var d = {
            service: service,
            redirect_uri: redirect_uri
        };
        var done = function ajaxOauthLoginDone(data) {
            if (data.error.length !== 0) {
                setGlobalErrorHandler('Ohh!', data.error);
            } else if ('missing' in data && data.missing.length !== 0) {
                new GuiHandler().showCompleteLoginPopup(data);
            } else if ('authorization_url' in data && data.authorization_url !== 0) {
                window.open(data.authorization_url, '_self');
            }
        };
        var fail = function ajaxOauthLoginFail(xhr) {
            if (xhr.status === 0 || xhr.status === 200) {
                location.reload(true);
            } else {
                setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
            }
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     */
    this.logout = function () {
        var url = mainpage + 'user_logout';
        var done = function ajaxLogoutDone() {
            location.reload(true);
        };
        var fail = function ajaxLogoutFail(xhr) {
            if (xhr.status === 200) {
                if (window.location.href.indexOf('settings') !== 0) {
                    window.location.href = mainpage + 'discuss';
                } else {
                    location.reload(true);
                }
            } else if (xhr.status === 403) {
                window.location.href = mainpage + 'discuss';
            } else {
                location.reload(true);
            }
        };
        ajaxSkeleton(url, 'POST', {}, done, fail);
    };

    this.registration = function () {
        $('#' + popupLoginRegistrationFailed).hide();
        if ($('#' + popupLoginInlineRadioGenderN).is(':checked')) {
            gender = 'n';
        }
        if ($('#' + popupLoginInlineRadioGenderM).is(':checked')) {
            gender = 'm';
        }
        if ($('#' + popupLoginInlineRadioGenderF).is(':checked')) {
            gender = 'f';
        }

        if (invalid_recaptcha()) {
            $('#' + popupLoginRegistrationFailed).show();
            $('#' + popupLoginRegistrationFailed + '-message').text(_t(wrongCaptcha));
            return;
        }

        var url = 'user_registration';
        var d = {
            firstname: $('#userfirstname-input').val(),
            lastname: $('#userlastname-input').val(),
            nickname: $('#nick-input').val(),
            gender: '',
            email: $('#email-input').val(),
            password: $('#' + popupLoginPasswordInputId).val(),
            passwordconfirm: $('#' + popupLoginPasswordconfirmInputId).val(),
            lang: getLanguage()
        };
        var done = function ajaxRegistrationDone(data) {
            callbackIfDoneForRegistration(data);
            $('#' + popupLoginPasswordInputId).val('');
            $('#' + popupLoginPasswordconfirmInputId).val('');
        };
        var fail = function ajaxRegistrationFail(data) {
            $('#' + popupLoginRegistrationFailed).show();
            $('#' + popupLoginPasswordInputId).val('');
            $('#' + popupLoginPasswordconfirmInputId).val('');
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     */
    this.passwordRequest = function () {
        var url = 'user_password_request';
        var d = {
            email: $('#password-request-email-input').val(),
            lang: getLanguage()
        };
        var fail = function ajaxPasswordRequestFail(data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, callbackIfDoneForPasswordRequest(data), fail);
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
