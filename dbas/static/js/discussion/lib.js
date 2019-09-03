/**
 * Use the browser's built-in functionality to quickly and safely escape the string
 * Based on http://shebang.brandonmintern.com/foolproof-html-escaping-in-javascript/
 *
 * @param text to escape
 * @returns {*} escaped string
 */
function escapeHtml(text) {
    'use strict';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

/**
 * Returns the uid of current issue
 *
 * @returns {number}
 */
function getCurrentIssueId() {
    'use strict';
    var issue = $('#' + issueDropdownButtonID).attr('issue');
    if (!issue) {
        issue = $('#issue_info').data('issue');
    }
    return issue;
}

/**
 * Writes key-value-pair into local storage and returns boolean
 *
 * @param key
 * @param value
 * @returns {boolean}
 */
function setLocalStorage(key, value) {
    'use strict';
    try {
        localStorage.setItem(key, value);
        return true;
    } catch (_err) {
        return false;
    }
}

/**
 * Reads the entry of local storage by key
 *
 * @param key
 * @returns {undefined}
 */
function getLocalStorage(key) {
    'use strict';
    try {
        return localStorage.getItem(key);
    } catch (err) {
        return undefined;
    }
}

/**
 * Sets an anchor into the location
 *
 * @param anchor string
 */
function setAnchor(anchor) {
    'use strict';
    location.hash = anchor;
}

/**
 * Clears all anchors in the location
 */
function clearAnchor() {
    'use strict';
    location.hash = '';
}

/**
 * Returns true, if the used device is a mobile agent
 *
 * @returns {boolean}
 */
function isMobileAgent() {
    'use strict';
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 *
 * @param element
 * @returns {number}
 */
function getPaddingOfElement(element) {
    'use strict';
    if (typeof element !== "undefined" && typeof element.css('padding') !== "undefined") {
        var pt = parseInt(element.css('padding-top').replace('px', ''));
        var pb = parseInt(element.css('padding-bottom').replace('px', ''));
        return pt + pb;
    } else {
        return 0;
    }
}
