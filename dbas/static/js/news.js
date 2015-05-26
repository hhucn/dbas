/*global $, jQuery, alert*/

$(document).ready(function () {
	'use strict';

	$(".share-mail").click(function (event) {
		var textarray, container, subject, message, date, author;
		container = $(this).parents(".newscontainer");

		// get the subject
		textarray = container.html().split('<span class="font-semi-bold">');
		textarray = textarray[1].split('</span>');
		subject = "DBAS: " + textarray[0];

		// get the date
		textarray = container.html().split('<h3><p>');
		textarray = textarray[1].split('</p>');
		date = textarray[0];

		// get the author
		textarray = container.html().split('Author: ');
		textarray = textarray[1].split('</h4>');
		author = textarray[0];

		// get the message
		textarray = container.html().split('<br>');
		message="News from " + date + ", by " + author + ": " + textarray[1];

		window.location.href = "mailto:user@example.com?subject=" + subject + "&body=" + message
	});
	
	$(".share-twitter").click(function (event) {
		var textarray, container;
		container = $(this).parents(".newscontainer");
		textarray = container.html().split('<br>');
		alert("Share with twitter:\n" + textarray[1]);
	});
	
	$(".share-google").click(function (event) {
		var textarray, container;
		container = $(this).parents(".newscontainer");
		textarray = container.html().split('<br>');
		alert("Share with google:\n" + textarray[1]);
	});
	
	$(".share-facebook").click(function (event) {
		var textarray, container;
		container = $(this).parents(".newscontainer");
		textarray = container.html().split('<br>');
		alert("Share with facebook:\n" + textarray[1]);
	});
	

});