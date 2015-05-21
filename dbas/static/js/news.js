/*global $, jQuery, alert*/

$(document).ready(function () {
	'use strict';

	$(".share-mail").click(function (event) {
		var textarray, container;
		container = $(this).parents(".newscontainer");
		textarray = container.html().split('<br>');
		alert("Share with mail:\n" + textarray[1]);
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