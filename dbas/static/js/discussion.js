/*
var discussionSpaceId = 'discussions-space';

function GuiHandler() {
	'use strict';
}
function AjaxHandler() {
	'use strict';
}
function InteractionHandler() {
	'use strict';

	this.setRadioButtonExtraFunctions = function(){
		$('#' + discussionSpaceId + ' ul').children().last();
	}
}

$(document).ready(function () {
	var gh = new GuiHandler(), ah = new AjaxHandler(), ih = new InteractionHandler();

	ih.setRadioButtonExtraFunctions();
});

*/
// ajax loading animation
$(document).on({
	ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
	ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
});



/**
 * main function
 */
$(function () {

});