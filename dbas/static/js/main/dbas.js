/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

/**
 *
 * @param linkname name of the link
 */
function setLinkActive(linkname) {
    'use strict';

    $('#navbar-right').find('>li').each(function () {
        $(this).removeClass('active');
    });
    $(linkname).addClass('active');
}

/**
 * Adds a small border to the active navbar element
 */
function addBorderToActiveNavbar() {
    'use strict';

    var activeElement = $('.navbar-right > .active');
    if (activeElement.length === 0) {
        return;
    }
    var borderSize = '2';

    // replace padding of the inner element
    var innerElement = activeElement.find('a');
    var padTop = parseInt(innerElement.css('padding-top').replace('px', ''));
    var padBottom = parseInt(innerElement.css('padding-bottom').replace('px', ''));
    innerElement.css('padding-top', (padTop - borderSize / 2) + 'px');
    innerElement.css('padding-bottom', (padBottom - borderSize / 2) + 'px');

    // add border to the navbar element
    activeElement.css('border-top', borderSize + 'px solid #2196F3');
}

/**
 * Display smiley as fallback on (connection) errors
 */
function setGravatarFallback() {
    'use strict';

    var body = $('body');
    var img = body.find('.img-circle');
    if (img.length === 0) {
        return true;
    }

    var src = body.find('.img-circle')[0].src;
    $.get(src, function () {
        replaceGravtarWithDefaultImage(true);
    }).fail(function () {
        replaceGravtarWithDefaultImage(false);
    });
}

/**
 *
 * @param onlyOnError
 */
function replaceGravtarWithDefaultImage(onlyOnError) {
    'use strict';

    $('body').find('.img-circle').each(function () {
        var icons =
            [{
                'name': 'faces', 'length': 98
            }, {
                'name': 'flat-smileys', 'length': 32
            }, {
                'name': 'human', 'length': 81
            }, {'name': 'lego', 'length': 10}];
        var t = 3;
        var no = Math.floor(Math.random() * icons[t].length);
        var src = mainpage + 'static/images/fallback-' + icons[t].name + '/' + no + '.svg';

        if (onlyOnError) {
            $(this).attr('onerror', 'this.src="' + src + '"');
        } else {
            $(this).attr('src', src);
        }
        // resize fallback avatar
        if ($(this).closest('#user-menu-dropdown').length === 1 || window.location.href.indexOf('/review') !== -1) {
            $(this).css('width', '25px');
        }
    });
}

/**
 *
 * @param titleText
 * @param bodyText
 * @param functionForAccept
 * @param functionForRefuse
 * @param smallDialog
 */
function displayConfirmationDialog(titleText, bodyText, functionForAccept, functionForRefuse, smallDialog) {
    'use strict';

    // display dialog
    var dialog = $('#' + popupConfirmDialogId);
    dialog.find('#confirm-dialog-accept-btn').show();
    dialog.find('#confirm-dialog-refuse-btn').show();
    if (smallDialog) {
        dialog.find('.modal-dialog').addClass('modal-sm');
    }
    dialog.modal('show');
    $('#' + popupConfirmDialogId + ' h4.modal-title').html(titleText);
    $('#' + popupConfirmDialogId + ' div.modal-body').html(bodyText);
    $('#' + popupConfirmDialogAcceptBtn).show().click(function () {
        $('#' + popupConfirmDialogId).modal('hide');
        if (functionForAccept) {
            functionForAccept();
        }
    });
    $('#' + popupConfirmDialogRefuseBtn).show().click(function () {
        $('#' + popupConfirmDialogId).modal('hide');
        if (functionForRefuse) {
            functionForRefuse();
        }
    });
    dialog.on('hidden.bs.modal', function () {
        $('#' + popupConfirmDialogRefuseBtn).show();
        dialog.find('.modal-dialog').removeClass('modal-sm');
        dialog.find('#confirm-dialog-accept-btn').text(_t(okay));
        dialog.find('#confirm-dialog-refuse-btn').text(_t(cancel));
        // unload buttons
        $('#' + popupConfirmDialogAcceptBtn).off('click');
        $('#' + popupConfirmDialogRefuseBtn).off('click');

    });
}

/**
 * Displays dialog
 *
 * @param titleText
 * @param bodyText
 */
function displayConfirmationDialogWithoutCancelAndFunction(titleText, bodyText) {
    'use strict';

    // display dialog
    $('#' + popupConfirmDialogId).modal('show');
    $('#' + popupConfirmDialogId + ' h4.modal-title').html(titleText);
    $('#' + popupConfirmDialogId + ' div.modal-body').html(bodyText);
    $('#' + popupConfirmDialogAcceptBtn).show().click(function () {
        $('#' + popupConfirmDialogId).modal('hide').find('.modal-dialog').removeClass('modal-sm');
    }).removeClass('btn-success');
    $('#' + popupConfirmDialogRefuseBtn).hide();
}

/**
 * Displays dialog with checkbox
 * @param titleText
 * @param bodyText
 * @param checkboxText
 * @param functionForAccept
 * @param isRestartingDiscussion
 */
function displayConfirmationDialogWithCheckbox(titleText, bodyText, checkboxText, functionForAccept, isRestartingDiscussion) {
    'use strict';

    // display dialog only if the cookie was not set yet
    if (Cookies.get(WARNING_CHANGE_DISCUSSION_POPUP)) {
        window.location.href = functionForAccept;
    } else {
        $('#' + popupConfirmChecbkoxDialogId).modal('show');
        $('#' + popupConfirmChecbkoxDialogId + ' h4.modal-title').text(titleText);
        $('#' + popupConfirmChecbkoxDialogId + ' div.modal-body').html(bodyText);
        $('#' + popupConfirmChecbkoxDialogTextId).text(checkboxText);
        $('#' + popupConfirmChecbkoxDialogAcceptBtn).click(function () {
            $('#' + popupConfirmChecbkoxDialogId).modal('hide');
            // maybe set a cookie
            if ($('#' + popupConfirmChecbkoxId).prop('checked')) {
                Cookies.set(WARNING_CHANGE_DISCUSSION_POPUP, true, {expires: 7});
            }

            if (isRestartingDiscussion) {
                window.location.href = functionForAccept;
            } else {
                functionForAccept();
            }

        });
        $('#' + popupConfirmChecbkoxDialogRefuseBtn).click(function () {
            $('#' + popupConfirmChecbkoxDialogId).modal('hide');
        });
    }
}

/**
 *
 * @param lang
 */
function setAnalyticsOptOutLink(lang) {
    'use strict';

    var src = mainpage + 'analytics/index.php?module=CoreAdminHome&action=optOut&idsite=1&language=' + lang;
    $('#analytics-opt-out-iframe').attr('src', src);
}

/**
 *
 */
function setEasterEggs() {
    'use strict';

    $('#roundhousekick').click(function () {
        new AjaxMainHandler().roundhouseKick();
    });
    $('#logo_dbas, #logo_dbas_s, #homeHeading').click(function () {
        if (!$(this)) {
            return;
        }
        var homeHeading = $('#homeHeading');
        var counter = parseInt(homeHeading.data('counter'));
        counter += 1;
        if (counter === 5) {
            $('body').find('span,p,h1,h2,h3,h4,h5,a').each(function () {
                if ($(this).text().trim().length) {
                    $(this).text(dolanTranslate(dolanDictionary, $(this).text()));
                }
            });
        }
        homeHeading.data('counter', counter);
    });
}

/**
 * Fill captcha in registration-form
 */
function fillCaptcha() {
    'use strict';
    var numOne = Math.floor(Math.random() * 10) + 1;
    var numTwo = Math.floor(Math.random() * 10) + 1;
    var numThree = Math.floor(Math.random() * 10) + 1;
    document.getElementById("captcha-digit1").innerHTML = numOne;
    document.getElementById("captcha-digit2").innerHTML = numTwo;
    document.getElementById("captcha-digit3").innerHTML = numThree;
}

/**
 * Prepares the login popup
 */
function prepareLoginRegistrationPopup() {
    'use strict';

    // hide on startup
    new PopupHandler().hideExtraViewsOfLoginPopup();

    // switching tabs
    $('.tab-login a').on('click', function (e) {
        e.preventDefault();
        $(this).parent().addClass('active');
        $(this).parent().siblings().removeClass('active');
        var target = $(this).attr('href');
        $('.tab-content > div').not(target).hide();
        $(target).fadeIn(600);

        if ($(this).attr('href').indexOf('signup') === -1) {
            $('#' + popupLoginButtonLogin).show();
            $('#' + popupLoginButtonRegister).hide();
        } else {
            $('#' + popupLoginButtonLogin).hide();
            $('#' + popupLoginButtonRegister).show();
            fillCaptcha();
        }
    });

    $('#' + popupLoginButtonLogin).show().click(function () {
        new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false);
    }).keypress(function (e) {
        if (e.which === 13) {
            new AjaxMainHandler().registration();
        }
    });

    $('#' + popupLoginForgotPasswordText).click(function () {
        var body = $('#' + popupLoginForgotPasswordBody);
        if (body.is(':visible')) {
            body.fadeOut();
            $('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
            $('#' + popupLoginFailed).fadeOut();
            $('#' + popupLoginSuccess).fadeOut();
            $('#' + popupLoginInfo).fadeOut();
        } else {
            body.fadeIn();
            $('#' + popupLoginForgotPasswordText).text(_t(hidePasswordRequest));
        }
    });

    $('#' + popupLoginCloseButton1 + ',#' + popupLoginCloseButton2).click(function () {
        new PopupHandler().hideExtraViewsOfLoginPopup();
        $('#' + popupLogin).modal('hide');
        $('#' + popupLoginButtonLogin).show();
    });

    $('#' + popupLoginButtonRegister).click(function () {
        var userfirstname = $('#' + popupLoginUserfirstnameInputId).val();
        var userlastname = $('#' + popupLoginUserlastnameInputId).val();
        var nick = $('#' + popupLoginNickInputId).val();
        var email = $('#' + popupLoginEmailInputId).val();
        var password = $('#' + popupLoginPasswordInputId).val();
        var passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val();
        var text = '';
        var i;
        var fields = [userfirstname, userlastname, nick, email, password, passwordconfirm];
        var tvalues = [_t(checkFirstname), _t(checkLastname), _t(checkNickname), _t(checkEmail), _t(checkPassword),
            _t(checkConfirmation), _t(checkPasswordConfirm)];

        // check all fields for obivous errors
        for (i = 0; i < fields.length; i++) {
            if (!fields[i] || /^\s*$/.test(fields[i]) || 0 === fields[i].length) {
                text = tvalues[i];
                break;
            }
        }

        if (text === '') {
            $('#' + popupLoginWarningMessage).hide();
            new AjaxMainHandler().registration();
        } else {
            $('#' + popupLoginWarningMessage).fadeIn("slow");
            $('#' + popupLoginWarningMessageText).text(text);
        }

    });

    // bind enter key
    var enterKey = 13;
    [
        '#' + loginUserId,
        '#' + loginPwId,
        '#admin-login-user',
        '#admin-login-pw'
    ].forEach(function(id) {
        $(id).keypress(function (e) {
            if (e.which === enterKey) {
                new AjaxMainHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false);
            }
        });
        
    });
    [
        '#' + popupLoginUserfirstnameInputId,
        '#' + popupLoginUserlastnameInputId,
        '#' + popupLoginEmailInputId,
        '#' + popupLoginPasswordconfirmInputId
    ].forEach(function(id) {
        $(id).keypress(function (e) {
            if (e.which === enterKey) {
                new AjaxMainHandler().registration();
            }
        });
    });

    $('#' + popupLoginButtonRequest).click(function () {
        new AjaxMainHandler().passwordRequest();
    });
}

/**
 *
 * @param element
 * @param displayAtTop
 */
function setTextWatcherInputLength(element, displayAtTop) {
    'use strict';

    var minLength = element.data('min-length');
    var maxLength = element.data('max-length');
    if (!maxLength) {
        maxLength = 1000;
    }
    var id = element.attr('id') + '-text-counter';
    var msg = _t_discussion(textMinCountMessageBegin1) + ' ' + minLength + ' ' + _t_discussion(textMinCountMessageBegin2);
    var field = $('<span>').text(msg).attr('id', id).addClass('text-info').addClass('text-counter-input');
    if (displayAtTop) {
        field.insertBefore(element);
    } else {
        field.insertAfter(element);
    }

    element.keyup(function () {
        var text = element.val().trim();
        var currentLength = text.length;

        if (currentLength === 0) {
            field.addClass('text-info');
            field.removeClass('text-danger');
            field.text(msg);
        } else if (currentLength < minLength) {
            field.removeClass('text-danger');
            field.text((minLength - currentLength) + ' ' + _t_discussion(textMinCountMessageDuringTyping));
        } else {
            field.removeClass('text-info');
            if (currentLength > maxLength * 3 / 4) {
                field.addClass('text-danger');
            } else {
                field.removeClass('text-danger');
            }
            var left = maxLength < currentLength ? 0 : maxLength - currentLength;
            field.text(left + ' ' + _t_discussion(textMaxCountMessage));
            if (maxLength <= currentLength) {
                field.removeClass('text-danger');
                field.addClass('text-info');
                field.text(_t_discussion(textMaxCountMessageError));
            }
        }
    });
}

/**
 * Sets data for the global success field
 *
 * @param heading text
 * @param body text
 */
function setGlobalErrorHandler(heading, body) {
    'use strict';

    $('#' + requestFailedContainer).fadeIn();
    $('#' + requestFailedContainerClose).click(function () {
        $('#' + requestFailedContainer).fadeOut();
    });
    $('#' + requestFailedContainerHeading).html(decodeString(heading));
    $('#' + requestFailedContainerMessage).html(decodeString(body));
    setTimeout(function () {
        $('#' + requestFailedContainer).fadeOut();
    }, 5000);
}

/**
 * Sets data for the global success field
 *
 * @param heading text
 * @param body text
 */
function setGlobalSuccessHandler(heading, body) {
    'use strict';

    $('#' + requestSuccessContainer).fadeIn();
    $('#' + requestSuccessContainerClose).click(function () {
        $('#' + requestSuccessContainer).fadeOut();
    });
    $('#' + requestSuccessContainerHeading).html(decodeString(heading));
    $('#' + requestSuccessContainerMessage).html(decodeString(body));
    setTimeout(function () {
        $('#' + requestSuccessContainer).fadeOut();
    }, 5000);
}

/**
 * Sets data for the global info field
 *
 * @param heading text
 * @param body text
 */
function setGlobalInfoHandler(heading, body) {
    'use strict';

    $('#' + requestInfoContainer).fadeIn();
    $('#' + requestInfoContainerClose).click(function () {
        $('#' + requestInfoContainer).fadeOut();
    });
    $('#' + requestInfoContainerHeading).html(decodeString(heading));
    $('#' + requestInfoContainerMessage).html(decodeString(body));
    setTimeout(function () {
        $('#' + requestInfoContainer).fadeOut();
    }, 5000);
}

/**
 *
 * @param encodedString
 */
function decodeString(encodedString) {
    'use strict';

    return decodeURIComponent(encodedString);
}

// *********************
//	CALLBACKS
// *********************

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
    if (data.success) {
        $('#' + popupLoginForgotPasswordBody).hide();
        $('#' + popupLoginForgotPasswordText).text(_t(forgotPassword) + '?');
        success.show();
        $('#' + popupLoginSuccess + '-message').text(data.message);
    } else {
        info.show();
        $('#' + popupLoginInfo + '-message').text(data.message);
    }
}

// *********************
//	MAIN
// *********************
$(document).ready(function () {
    'use strict';

    // ajax loading animation
    var timer;
    $(document).on({
        ajaxStart: function ajaxStartFct() {
            timer && clearTimeout(timer);
            timer = setTimeout(function () {
                $('body').addClass('loading');
            }, 150);
        },
        ajaxStop: function ajaxStopFct() {
            clearTimeout(timer);
            $('body').removeClass('loading');
        }
    });

    var path = window.location.href;
    var lang = $('#hidden_language').val();

    setAnalyticsOptOutLink(lang);
    setEasterEggs();
    setGravatarFallback();
    setTimeout(function () {
        addBorderToActiveNavbar();
    }, 150);
    $('#' + popupLogin).on('shown.bs.modal', function (e) {
        new PopupHandler().showLoginPopup();
    });
    var counter = $('.counter');
    if (counter.length > 0) {
        counter.counterUp({delay: 5, time: 1000});
    }

    // set current file to active
    if (path.indexOf(urlContact) !== -1) {
        setLinkActive('#' + contactLink);
    }
    else if (path.indexOf(urlLogin) !== -1) {
        setLinkActive('#' + loginLinkId);
    }
    else if (path.indexOf(urlDiscussions) !== -1) {
        setLinkActive('#' + myDiscussionsLink);
    }
    else if (path.indexOf(urlContent) !== -1) {
        setLinkActive('#' + contentLink);
    }
    else if (path.indexOf(urlReview) !== -1) {
        setLinkActive('#' + reviewLinkId);
    }
    else {
        setLinkActive('');
    }

    // gui preparation
    prepareLoginRegistrationPopup();

    // add minimal text length field
    $('input[data-min-length]').each(function () {
        setTextWatcherInputLength($(this), false);
    });
    $('textarea[data-min-length]').each(function () {
        setTextWatcherInputLength($(this), false);
    });

    // session expired popup
    if ($('#' + sessionExpiredContainer).length === 1) {
        setTimeout(function () {
            $('#' + sessionExpiredContainer).fadeOut();
        }, 3000);
    }

    // start guided tour, if the cookie is not set
    var href = window.location.href;
    var index = href.indexOf('/discuss/');
    if (!Cookies.get(GUIDED_TOUR) && index !== -1 && href.length > index + '/discuss/'.length + 1) {
        new GuidedTour().start();
    }

    $('#contact_on_error').click(function () {
        window.location.href = $('#contact-link').find('a').attr('href');
    });

    // language switch
    $('#' + translationLinkDe).click(function () {
        new GuiHandler().lang_switch('de');
    });
    $('#' + translationLinkEn).click(function () {
        new GuiHandler().lang_switch('en');
    });
    $('#' + translationLinkDe + ' img').click(function () {
        new GuiHandler().lang_switch('de');
    });
    $('#' + translationLinkEn + ' img').click(function () {
        new GuiHandler().lang_switch('en');
    });
    $('#' + logoutLinkId).click(function (e) {
        e.preventDefault();
        new AjaxMainHandler().logout();
    });

    $(window).scroll(function () {
        if ($(document).scrollTop() > 50) {
            $('nav').addClass('shrink');
        } else {
            $('nav').removeClass('shrink');
        }
    });
});
