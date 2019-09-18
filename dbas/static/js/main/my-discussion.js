/**
 * Script for the discussion main page
 */

function MyDiscussion() {

}

MyDiscussion.prototype.set_clipboard = function (_this) {
    'use strict';
    $(_this).click(function () {
        var aux = document.createElement("input");
        aux.setAttribute("value", $(this).prev().text());
        document.body.appendChild(aux);
        aux.select();
        document.execCommand("copy");
        document.body.removeChild(aux);
        setGlobalSuccessHandler('Yeah!', _t_discussion(urlCopy));
    });
};

$(document).ready(function () {
    'use strict';

    var adh = new AjaxDiscussionHandler();
    $.each($('.issue-property'), function () {
        $(this).change(function () {
            adh.setDiscussionSettings($(this), $(this).data('keyword'));
        });
    });

    var md = new MyDiscussion();
    $.each($('.fa-clipboard'), function () {
        md.set_clipboard(this);
    });
});
