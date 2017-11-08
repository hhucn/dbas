/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */
$(document).ready(function () {
    'use strict';

	$.each($('.discussion-enable-toggle'), function(){
		$(this).change(function (){
			console.log('toggle ' + $(this).data('uid'));
			new AjaxDiscussionHandler().enOrDisableDiscussion($(this));
		});
	});
	
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