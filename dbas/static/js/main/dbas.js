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
 * add the cookie consent popup for new users
 */
function addCookieConsent() {
    'use strict';

    if (!Cookies.get('EU_COOKIE_LAW_CONSENT')){
        $('#privacy-policy-popup').show();
        $('#privacy-policy-text').text(_t(euCookiePopupText));
        $('#privacy-policy-link').html(_t(euCookiePopoupButton2));
        $('#privacy-policy-btn').text(_t(euCookiePopoupButton1)).click(function(){
            $('#privacy-policy-popup').hide();
            Cookies.set('EU_COOKIE_LAW_CONSENT', true, {expires: 180});
        });
    }
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
    return true;
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
        var src = mainpage + 'static/images/fallback/' + icons[t].name + '/' + no + '.svg';

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
function setScrollTrigger() {
    'use strict';
    // Smooth scrolling using jQuery easing by https://css-tricks.com/snippets/jquery/smooth-scrolling/
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) { // Does a scroll target exist?
                event.preventDefault(); // Only prevent default if animation is actually gonna happen
                $('html, body').animate({
                    scrollTop: target.offset().top - 50
                }, 1000, function () {
                    $(target).focus();
                    if ($(target).is(":focus")) { // Checking if the target was focused
                        return false;
                    }
                    $(target).attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                    $(target).focus(); // Set focus again
                });
            }
        }
        return true;
    });
    return true;
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
            $('#popup-login-registration-oauth-footer').show();

        } else {
            $('#' + popupLoginButtonLogin).hide();
            $('#' + popupLoginButtonRegister).show();
            fillCaptcha();
            $('#popup-login-registration-oauth-footer').hide();
        }
    });

    $('#' + popupLoginButtonLogin).show().click(function () {
        new AjaxLoginHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false);
    }).keypress(function (e) {
        if (e.which === 13) {
            new AjaxLoginHandler().registration();
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
            new AjaxLoginHandler().registration();
        } else {
            $('#' + popupLoginWarningMessage).fadeIn("slow");
            $('#' + popupLoginWarningMessageText).text(text);
            new AjaxLoginHandler().registration();
        }

    });

    // bind enter key
    var enterKey = 13;
    [
        '#' + loginUserId,
        '#' + loginPwId,
        '#admin-login-user',
        '#admin-login-pw'
    ].forEach(function (id) {
        $(id).keypress(function (e) {
            if (e.which === enterKey) {
                new AjaxLoginHandler().login($('#' + loginUserId).val(), $('#' + loginPwId).val(), false);
            }
        });

    });
    [
        '#' + popupLoginUserfirstnameInputId,
        '#' + popupLoginUserlastnameInputId,
        '#' + popupLoginEmailInputId,
        '#' + popupLoginPasswordconfirmInputId
    ].forEach(function (id) {
        $(id).keypress(function (e) {
            if (e.which === enterKey) {
                new AjaxLoginHandler().registration();
            }
        });
    });

    $('#' + popupLoginButtonRequest).click(function () {
        new AjaxLoginHandler().passwordRequest();
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
        __keyUpFuncForTextwatcher(element, field, minLength, maxLength, msg);
    });
}

function __keyUpFuncForTextwatcher(element, field, minLength, maxLength, msg){
    'use strict';
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

    addCookieConsent();
    setAnalyticsOptOutLink(lang);
    setEasterEggs();
    setGravatarFallback();
    setScrollTrigger();
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
        new AjaxLoginHandler().logout();
    });

    $(window).scroll(function () {
        if ($(document).scrollTop() > 50) {
            $('nav').addClass('shrink');
        } else {
            $('nav').removeClass('shrink');
        }
    });
});
