/**
 * main function
 */

/**
 *
 * @param data
 * @param showGlobalError
 */
function callbackIfDoneForLogin(data, showGlobalError) {
    'use strict';
    try {
        if ('error' in data && data.error.length !== 0) {
            if (showGlobalError) {
                setGlobalErrorHandler('Ohh!', data.error);
            } else {
                $('#' + popupLoginFailed).show();
                $('#' + popupLoginFailed + '-message').html(data.error);
            }
        } else if ('info' in data && data.info.length !== 0) {
            $('#' + popupLoginInfo).show();
            $('#' + popupLoginInfo + '-message').html(data.info);
        } else {
            $('#' + popupLogin).modal('hide');
        }
    } catch (err) {
        // session expired
    }
}

/**
 *
 * @param data
 */
function callbackIfDoneForRegistration(data) {
    'use strict';

    var success = $('#' + popupLoginSuccess); //popupLoginRegistrationSuccess);
    var failed = $('#' + popupLoginRegistrationFailed);
    var info = $('#' + popupLoginRegistrationInfo);
    success.hide();
    failed.hide();
    info.hide();

    if (data.success.length > 0) {
        // trigger click
        $('a[href="#login"]').trigger('click');
        success.show();
        $('#' + popupLoginSuccess + '-message').text(data.success);
    }
    if (data.error.length > 0) {
        failed.show();
        $('#' + popupLoginRegistrationFailed + '-message').text(data.error);
    }
    if (data.info.length > 0) {
        info.show();
        $('#' + popupLoginRegistrationInfo + '-message').text(data.info);
        $('#popup-login-spamanswer-input').attr('placeholder', data.spamquestion).val('');
    }
}

/**
 *
 * @param data
 */
function callbackIfDoneForRegistrationViaOauth(data) {
    'use strict';

    var success = $('#' + popupLoginSuccess);
    var failed = $('#popup-complete-login-failed');
    var info = $('#popup-complete-login-info');
    success.hide();
    info.hide();
    failed.hide();

    if ('success' in data && data.success.length > 0) {
        $('#popup-complete-login').modal('hide');
        $('#popup-login').modal('show');
        // trigger click
        $('a[href="#login"]').trigger('click');
        success.show();
        $('#' + popupLoginSuccess + '-message').text(data.success);
    }
    if ('error' in data && data.error.length > 0) {
        failed.show();
        $('#popup-complete-login-failed-message').text(data.error);
    }
    if ('info' in data && data.info.length > 0) {
        info.show();
        $('#popup-complete-login-info-message').text(data.info);
    }
}

/**
 *
 * @param data
 */
function callbackIfDoneForPasswordRequest(data) {
    'use strict';

    var success = $('#' + popupLoginSuccess);
    var failed = $('#' + popupLoginFailed);
    var info = $('#' + popupLoginInfo);
    success.hide();
    failed.hide();
    info.hide();
    $('#' + popupLoginForgotPasswordBody).hide();
    $('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
    success.show();
    $('#' + popupLoginSuccess + '-message').text(data.message);
}

$(document).ready(function mainDocumentReady() {
    'use strict';

    var classes = ['.btn-google', '.btn-facebook', '.btn-twitter', '.btn-github'];
    $.each(classes, function (key, value) {
        $(value).click(function () {
            new AjaxLoginHandler().oauthLogin($(this).data('service'));
        });
    });

    $('#nav-tab-login').click(function () {
        $('#' + popupLogin).find('.modal-footer').find('button').addClass('hidden');
    });

    $('#nav-tab-signup').click(function () {
        $('#' + popupLogin).find('.modal-footer').find('button').removeClass('hidden');
    });

    // restore login popup to default
    $('#' + popupLogin).on('hidden.bs.modal', function () {
        var list = $('#' + discussionSpaceListId);
        if (list.length !== 0) {
            var login_item = list.find('#item_login');
            if (login_item.length > 0) {
                login_item.prop('checked', false);
            }
        }
    }).on('shown.bs.modal', function () {
        $('#' + loginUserId).focus();
        $('#' + popupLogin).find('.modal-footer').find('button').addClass('hidden');
    });

    // check href for id's
    var url = window.location.href;
    var services = ['google', 'facebook', 'twitter', 'github'];
    $.each(services, function (key, value) {
        if (url.indexOf('service=' + value + '&') !== -1) {
            url = url.replace('service=' + value + '&', '');
            new AjaxLoginHandler().oauthLogin(value, url);
        }
    });
});
