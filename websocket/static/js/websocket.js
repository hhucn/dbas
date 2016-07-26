$(document).ready(function() {

	var socket = io.connect('ws://localhost:5001');

	socket.on('publish', function(data){
		var alink = '';
		if (data.type == 'notifications'){
			alink = '<a target="_blank" href="' + mainpage + data.type + '">' + data.msg + '</a>';
			setGlobalInfoHandler('Huray!', alink);
			// increment counter
			incrementCounter($('#header_badge_count_notifications'));
			incrementCounter($('#menu_badge_count_notifications'));
			
		} else if (data.type == 'mention') {
			alink = '<a target="_blank" href="' + data.url + '">' + data.msg + '</a>';
			setGlobalInfoHandler('Huray!', alink);
			
		} else if (data.type == 'edit_text') {
			alink = '<a target="_blank" href="' + data.url + '">' + data.msg + '</a>';
			setGlobalInfoHandler('Ooh!', alink);
			
		} else {
			setGlobalInfoHandler('Huray!', data.msg);
		}
		console.log('publish ' + data.type + ' ' + data.msg);
	});

	socket.on('subscribe', function(socket_id){
		subscribe(socket_id);
	});
	
	// delete subscription on page unload events
	$(window).bind('beforeunload',function(){
		unsubscribe();
	});
});

/**
 *
 * @param element
 */
function incrementCounter(element){
	element.text(parseInt(element.text()) + 1);
}

/**
 *
 * @param socketid
 */
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

/**
 *
 */
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
