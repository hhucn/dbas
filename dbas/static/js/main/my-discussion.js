/**
 * Script for the discussion main page
 *
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function MyDiscussion() {
    'use strict';
    this.set_clipboard = function(_this){
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
}

$(document).ready(function () {
    'use strict';

    var button_dict = {
        '.discussion-enable-toggle': 'enable',
        '.discussion-public-toggle': 'public',
        '.discussion-writable-toggle': 'writable'
    };
    var md = new MyDiscussion();

    for (var key in button_dict) {
        if (!{}.hasOwnProperty.call(button_dict, key)) {
            continue;
        }
        $.each($(key), function () {
            $(this).change(function () {
                new AjaxDiscussionHandler().setDiscussionSettings($(this), button_dict[key]);
            });
        });
    }

    $.each($('.fa-clipboard'), function () {
        md.set_clipboard(this);
    });
});
