/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

/**
 * Src: http://stackoverflow.com/questions/11919065/sort-an-array-by-the-levenshtein-distance-with-best-performance-in-javascript
 * @param s1
 * @param s2
 */
function levensthein(s1, s2) {
    'use strict';
    var rowTwo = [];
    if (s1 === s2) {
        return 0;
    }

    var s1Len = s1.length,
        s2Len = s2.length;

    if (!s1Len  || !s2Len) {
        return s1Len + s2Len;
    }

    var i1 = 0, i2 = 0, a = 0, b = 0, c = 0, c2 = 0, row = rowTwo;
    while (i1 < s1Len) {
        ++i1;
        row[i1] = i1;
    }

    while (i2 < s2Len) {
    c2 = s2.charCodeAt(i2);
    a = i2;
    ++i2;
    b = i2;
    for (i1 = 0; i1 < s1Len; ++i1) {
        c = a + (s1.charCodeAt(i1) === c2 ? 0 : 1);
        a = row[i1];
        if (b < a) {
            b = b < c ? b + 1 : c;
        } else {
            b = a < c ? a + 1 : c;
        }
        row[i1] = b;
    }
    }
    return b;
}

function pxToEm(px) {
    'use strict';
    var baseSize = parseInt($("body").css('font-size').replace('px', ''));
    return px / parseInt(baseSize);
}

function emToPx(em) {
    'use strict';
    var baseSize = parseInt($("body").css('font-size').replace('px', ''));
    return em * parseInt(baseSize);
}

/**
 *
 * @param encodedString
 */
function decodeString(encodedString) {
    'use strict';
    return decodeURIComponent(encodedString);
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

function redirectAfterAjax(url) {
    'use strict';
    var done = function () {
        location.reload(true);
    };
    var fail = function (xhr) {
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
}
