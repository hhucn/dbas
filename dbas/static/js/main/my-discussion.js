/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */
$(document).ready(function () {
    'use strict';
    
    var button_dict = {
    	'.discussion-enable-toggle': 'enable',
    	'.discussion-public-toggle': 'public',
    	'.discussion-writable-toggle': 'writable'
    };
    
    for (var key in button_dict) {
    	if (!{}.hasOwnProperty.call(button_dict, key)){
    		continue;
	    }
		$.each($(key), function(){
			$(this).change(function (){
				new AjaxDiscussionHandler().setDiscussionSettings($(this), button_dict[key]);
			});
		});
    }

	$.each($('.fa-clipboard'), function(){
		$(this).click(function(){
			var aux = document.createElement("input");
            aux.setAttribute("value", $(this).prev().text());
            document.body.appendChild(aux);
            aux.select();
            document.execCommand("copy");
            document.body.removeChild(aux);
            setGlobalSuccessHandler('Yeah!', _t_discussion(urlCopy));
        });
	});

	// ajax loading animation
	$(document).on({
		ajaxStart: function() {
			setTimeout("$('body').addClass('loading');", 0);
		},
		ajaxStop: function() {
			setTimeout("$('body').removeClass('loading');", 0);
		}
	});
});
