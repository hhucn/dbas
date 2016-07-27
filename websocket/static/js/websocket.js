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
	
	socket.on('testid', function(id){
		var field = $('#socketio_id');
		
		if (field)
			field.text(id);
	});
	
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
	
	$('#test_success_btn,#test_danger_btn,#test_info_btn').click(function(){
		socket.emit('test', $(this).attr('data-type'));
	});
	
	// delete subscription on page unload events
	$(window).bind('beforeunload',function(){
		socket.emit('remove_name', $('#header_nickname').text());
	});
});

/**
 *
 * @param element
 */
function incrementCounter(element){
	element.text(parseInt(element.text()) + 1);
}