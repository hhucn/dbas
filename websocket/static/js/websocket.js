$(document).ready(function() {

	var socket = io.connect('ws://localhost:9999');

	socket.on('publish', function(data){
		if (data.type == 'notifications'){
			var alink = '<a href="' + mainpage + data.type + '">' + data.msg + '</a>';
			setGlobalInfoHandler('Huray!', alink);
		}
		console.log('publish ' + data.type + ' ' + data.msg);
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
	console.log('subscribe start');
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
	console.log('unsubscribe start');
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
