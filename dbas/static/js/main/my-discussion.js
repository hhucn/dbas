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