/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

var socket = undefined;

$(document).ready(function() {
	
	try {
		doConnect();
	} catch (e) {
		console.log('Error on connect.');
	}
	
	// delete subscription on page unload events
	$(window).bind('beforeunload',function(){
		if (socket)
			socket.emit('remove_name', $('#header_nickname').text());
	});
	
});

/**
 * Connects the sockets and enables publishing
 */
function doConnect(){
	socket = io.connect('ws://localhost:5001', {query: 'nickname=' + $('#header_nickname').text()});
	
	socket.on('publish', function(data){
		doPublish(data)
	});
	
	enableTesting();
}

/**
 * Differentiate between the differen publication types
 * @param data dict
 */
function doPublish(data){
	if (data.type == 'notifications'){
		doNotification(data);
	} else if (data.type == 'mention') {
		doMention(data);
	} else if (data.type == 'edittext') {
		doEditText(data);
	} else {
		setGlobalInfoHandler('Huray!', data.msg);
	}
	console.log('publish ' + data.type + ' ' + data.msg);
}

/**
 * Displays info popup line for notification
 * @param data dict
 */
function doNotification(data){
	var alink = '<a target="_blank" href="' + mainpage + data.type + '">' + data.msg + '</a>';
	setGlobalInfoHandler('Huray!', alink);
	incrementCounter($('#header_badge_count_notifications'));
	incrementCounter($('#menu_badge_count_notifications'));
}

/**
 * Displays info popup line for mention
 * @param data dict
 */
function doMention(data){
	var alink = '<a target="_blank" href="' + data.url + '">' + data.msg + '</a>';
	setGlobalInfoHandler('Huray!', alink);
}

/**
 * Displays info popup line for edit text notifications
 * @param data dict
 */
function doEditText(data){
	var alink = '<a target="_blank" href="' + data.url + '">' + data.msg + '</a>';
	setGlobalInfoHandler('Ooh!', alink);
}

/**
 * Increments the text counter in given element
 * @param element DOM-Element
 */
function incrementCounter(element){
	element.text(parseInt(element.text()) + 1);
}

/**
 * Enables testing for the main page
 */
function enableTesting(){
	socket.on('test', function(data) {
		if (data.type == 'success') {
			console.log('test success');
			setGlobalSuccessHandler('TEST', data.msg);
		} else if (data.type == 'warning') {
			console.log('test warning');
			setGlobalErrorHandler('TEST', data.msg);
		} else if (data.type == 'info') {
			console.log('test info');
			setGlobalInfoHandler('TEST', data.msg);
		} else {
			console.log('unknown test type');
		}
	});
	
	socket.on('testid', function(id){
		var field = $('#socketio_id');
		
		if (field)
			field.text(id);
	});
	
	$('#test_success_btn,#test_danger_btn,#test_info_btn').click(function(){
		socket.emit('test', $(this).attr('data-type'));
	});
}