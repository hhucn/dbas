$(document).ready(function() {

	var socket = io.connect('ws://localhost:9999');

	socket.on('publish', function(msg){
		console.log('publish ' + msg);
	});

	socket.on('subscribe', function(socket_id){
		subscribe(socket_id);
	});
	
	$(window).bind('beforeunload',function(){
		unsubscribe();
	});
});

function subscribe(socketid){
	var csrfToken = $('#' + hiddenCSRFTokenId).val();
	$.ajax({
		url: mainpage + 'ws/subscribe',
		method: 'GET',
		data: {
			socketid: socketid
		},
		dataType: 'json',
		headers: {
			'X-CSRF-Token': csrfToken
		}
	}).done(function () {
		console.log('subscribe done');
	}).fail(function () {
		console.log('subscribe fail');
	});
}

function unsubscribe(){
	var csrfToken = $('#' + hiddenCSRFTokenId).val();
	$.ajax({
		url: mainpage + 'ws/unsubscribe',
		method: 'GET',
		dataType: 'json',
		headers: {
			'X-CSRF-Token': csrfToken
		}
	}).done(function () {
		console.log('unsubscribe done');
	}).fail(function () {
		console.log('unsubscribe fail');
	});
}
