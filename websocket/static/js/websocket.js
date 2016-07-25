$(document).ready(function() {

	var socket = io.connect('ws://localhost:9999');

	//$('form').submit(function(){
	//	socket.emit('chat_message', $('#m').val());
	//	$('#m').val('');
	//	return false;
	//});

	socket.on('publish', function(msg){
		console.log('publish ' + msg);
	});

	socket.on('subscribe', function(socket_id){
		console.log('subscribe ' + socket_id);
		subscribe(socket_id);
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

function unsubscribe(socketid){
	var csrfToken = $('#' + hiddenCSRFTokenId).val();
	$.ajax({
		url: mainpage + 'ws/unsubscribe',
		method: 'GET',
		data: {
			socketid: socketid
		},
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