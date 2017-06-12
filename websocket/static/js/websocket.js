/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

var socket;
var port = 5222;

$(document).ready(function() {
	'use strict';
	
	
	// try to connect
	try {
		doConnect();
	} catch (e) {
	}
	
	// delete subscription on page unload events
	$(window).bind('beforeunload',function(){
		if (socket) {
			socket.emit('remove_name', $('#' + headerNicknameId).text());
		}
	});
	
});

/**
 * Connects the sockets and enables publishing
 */
function doConnect(){
	'use strict';
	
	// switch between a local (http) and a global (https) mode
	var dict = {query: 'nickname=' + $('#' + headerNicknameId).text(), secure: true};
	var address =  'http://localhost';
	if (mainpage.indexOf('localhost') === -1) {
		address = location.origin;
		dict.secure = true;
	}
	address = address.replace('https', 'wss').replace('http', 'ws');

	socket = io.connect(address + ':' + port, dict);
	
	socket.on('publish', function(data){
		doPublish(data);
	});
	
	socket.on('recent_review', function(data){
		doRecentReview(data);
	});
	
	enableTesting();
}

/**
 * Differentiate between the differen publication types
 * @param data dict
 */
function doPublish(data){
	'use strict';
	
	if (data.type === 'success') {	        handleMessage(data, 'Huray!', doSuccess);
	} else if (data.type === 'warning') {	handleMessage(data, 'Uhh!', doWarning);
	} else if (data.type === 'info') {	    handleMessage(data, 'Ooh!', doInfo);
	} else {                                setGlobalInfoHandler('Mhhh!', data.msg);
	}
}

/**
 *
 * @param data
 * @param intro
 * @param func
 */
function handleMessage(data, intro, func){
	'use strict';
	
	var msg = 'url' in data ? '<a target="_blank" href="' + data.url + '">' + data.msg + '</a>' : data.msg;
	func(intro, msg);
	if ('increase_counter' in data) {
		incrementCounter($('#' + headerBadgeCountNotificationsId));
		incrementCounter($('#' + menuBadgeCountNotificationsId));
	}
}

/**
 * Calls setGlobalSuccessHandler with given params
 * @param intro String
 * @param msg String
 */
function doSuccess(intro, msg){
	'use strict';
	
	setGlobalSuccessHandler(intro, msg);
}

/**
 * Calls setGlobalErrorHandler with given params
 * @param intro String
 * @param msg String
 */
function doWarning(intro, msg){
	'use strict';
	
	setGlobalErrorHandler(intro, msg);
}

/**
 * Calls setGlobalInfoHandler with given params
 * @param intro String
 * @param msg String
 */
function doInfo(intro, msg){
	'use strict';
	
	setGlobalInfoHandler(intro, msg);
}

/**
 *
 * @param data
 */
function doRecentReview(data){
	'use strict';
	
	if (window.location.href.indexOf('review') === -1) {
		return;
	}
	
	var queue = $('#' + data.queue);
	if (queue.length !== 0){
		// just push, if given user is not the last reviewer
		if (queue.find('a:last-child').length === 0){
			queue.find('span').remove();
		}
		
		if (queue.find('img[src^="' + data.img_url + '"]').length === 0) {
			queue.find('a:last-child').remove();
			var link = $('<a>').attr('target', '_blank').attr('title', data.reviewer_name).attr('href', '/user/' + data.reviewer_name);
			var img = $('<img>').addClass('img-circle').attr('src', data.img_url + '?d=wavatar&s=40').css('width', '40px').css('margin', '2px');
			link.append(img);
			queue.prepend(link);
		}
	}
}

/**
 * Increments the text counter in given element
 * @param element DOM-Element
 */
function incrementCounter(element){
	'use strict';
	
	element.text(parseInt(element.text()) + 1);
}

/**
 * Enables testing for the main page
 */
function enableTesting(){
	'use strict';
	
	socket.on('connect', function() {
		var field = $('#socketStatus');
		if (field) {
			field.text('Connected!');
		}
	});

    socket.on('disconnect', function() {
		var field = $('#socketStatus');
		if (field) {
			field.text('Disconnected!');
		}
    });

    socket.on('pong', function(ms){
    	var testCount = $('#testCount');
		var latency = $('#latency');
		if (latency) {
			latency.text(ms + 'ms');
		}
	    if (testCount) {
		    testCount.text(parseInt(testCount.text()) + 1);
	    }
    });
	
	setInterval(function(){
        socket.emit('ping', {});
	}, 100);
	
	socket.on('push_test', function(data) {
		if (data.type === 'success') {	        handleMessage(data, 'TEST!', doSuccess);
		} else if (data.type === 'warning') {	handleMessage(data, 'TEST!', doWarning);
		} else if (data.type === 'info') {	    handleMessage(data, 'TEST!', doInfo);
		}
	});
	
	// getting socket id from server
	socket.on('push_socketid', function(id){
		var field = $('#socketioId');
		
		if (field) {
			field.text(id);
		}
	});
	
	$('#test_success_btn,#test_danger_btn,#test_info_btn').click(function(){
		socket.emit('push_test', $(this).attr('data-type'), $('#test-input').val());
	});
}
