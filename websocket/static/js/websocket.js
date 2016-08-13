/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

var socket = undefined;
const port = 5001;

$(document).ready(function() {
	
	// try to connect
	try {
		doConnect();
	} catch (e) {
		console.log('Error on connect: ' + e.message);
	}
	
	// delete subscription on page unload events
	$(window).bind('beforeunload',function(){
		if (socket)
			socket.emit('remove_name', $('#' + headerNicknameId).text());
	});
	
});

/**
 * Connects the sockets and enables publishing
 */
function doConnect(){
	// switch between a local (http) and a global (https) mode
	var dict = {query: 'nickname=' + $('#' + headerNicknameId).text(), secure: true};
	var address =  'http://localhost:';
	if (mainpage.indexOf('localhost') == -1) {
		address = 'https://dbas.cs.uni-duesseldorf.de:';
		dict['secure'] = true;
	}
	socket = io.connect(address + port, dict);
	
	socket.on('publish', function(data){
		doPublish(data)
	});
	
	console.log('Socket.io connected.');
	enableTesting();
}

/**
 * Differentiate between the differen publication types
 * @param data dict
 */
function doPublish(data){
	if (data.type == 'success') {	        handleMessage(data, 'Huray!', doSuccess);
	} else if (data.type == 'warning') {	handleMessage(data, 'Uhh!', doWarning);
	} else if (data.type == 'info') {	    handleMessage(data, 'Ooh!', doInfo);
	} else {                                setGlobalInfoHandler('Mhhh!', data.msg);
	}
	console.log('publish ' + data.type + ' ' + data.msg);
}

function handleMessage(data, intro, func){
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
	setGlobalSuccessHandler(intro, msg);
}

/**
 * Calls setGlobalErrorHandler with given params
 * @param intro String
 * @param msg String
 */
function doWarning(intro, msg){
	setGlobalErrorHandler(intro, msg);
}

/**
 * Calls setGlobalInfoHandler with given params
 * @param intro String
 * @param msg String
 */
function doInfo(intro, msg){
	setGlobalInfoHandler(intro, msg);
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
		if (data.type == 'success') {	        handleMessage(data, 'TEST!', doSuccess);
		} else if (data.type == 'warning') {	handleMessage(data, 'TEST!', doWarning);
		} else if (data.type == 'info') {	    handleMessage(data, 'TEST!', doInfo);
		} else {                                console.log('unknown test type');
		}
	});
	
	// getting socket id from server
	socket.on('testid', function(id){
		var field = $('#socketio_id');
		
		if (field)
			field.text(id);
	});
	
	$('#test_success_btn,#test_danger_btn,#test_info_btn').click(function(){
		socket.emit('test', $(this).attr('data-type'), $('#test-input').val());
	});
}
