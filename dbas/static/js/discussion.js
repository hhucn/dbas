/*global $, jQuery, alert, addActiveLinksInNavBar, removeActiveLinksInNavBar*/
//jQuery(function ($) {
$(document).ready(function () {
	'use strict';

	// jump to chapter-function
	$('#start-discussion').on('click', function (e) {
		alert('Let\'s go');
		jQuery.ajax({
			url     : 'content_ajax',
			type    : 'POST',
			dataType: 'json',
			success : function(data){
				alert("Success. Got the message:\n "+ data.message)
			}
		});
	});

});