/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

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

function AjaxLoginHandler() {
    "use strict";
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
                $('#' + popupLoginFailed).show();
                $('#' + popupLoginFailed + '-message').text(_t(userPasswordNotMatch));
                setGlobalErrorHandler(_t_discussion(ohsnap), _t(userPasswordNotMatch));
            }
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     * @param service
     * @param redirect_uri
     */
    this.oauthLogin = function (service) {
        $('#' + popupLoginFailed).hide();
        $('#' + popupLoginFailed + '-message').text('');
        $('#' + popupLoginInfo).hide();
        $('#' + popupLoginInfo + '-message').text('');
        var url = mainpage + 'oauth';
        var d = {
            service: service,
            redirect_uri: window.location.href
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
        redirectAfterAjax(mainpage + 'user_logout');
    };
    /**
     *
     */
    this.registration = function (error_message) {
        $('#' + popupLoginRegistrationFailed).hide();
        var gender = 'n';
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
            gender: gender,
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
            $('#' + popupLoginRegistrationInfo).show();
            $('#' + popupLoginRegistrationInfo + '-message').text(error_message);
            $('#' + popupLoginPasswordInputId).val('');
            $('#' + popupLoginPasswordconfirmInputId).val('');
            if (data === null) {
                setGlobalErrorHandler(_t_discussion(ohsnap), error_message);
            }
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     */
    this.passwordRequest = function () {
        var url = 'user_password_request';
        var data = {
            email: $('#password-request-email-input').val(),
            lang: getLanguage()
        };
        var fail = function ajaxPasswordRequestFail(data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', data, callbackIfDoneForPasswordRequest, fail);
    };
}
