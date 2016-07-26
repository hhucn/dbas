$(document).ready(function() {

	var socket = io.connect('ws://localhost:5001', {query: 'nickname=' + $('#header_nickname').text()});

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
			
		} else if (data.type == 'edittext') {
			alink = '<a target="_blank" href="' + data.url + '">' + data.msg + '</a>';
			setGlobalInfoHandler('Ooh!', alink);
			
		} else {
			setGlobalInfoHandler('Huray!', data.msg);
		}
		console.log('publish ' + data.type + ' ' + data.msg);
	});
	
	// delete subscription on page unload events
	$(window).bind('beforeunload',function(){
		socket.emit('disconnect', socket.id);
	});
});

/**
 *
 * @param element
 */
function incrementCounter(element){
	element.text(parseInt(element.text()) + 1);
}