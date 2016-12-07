/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	let tabs = $('#review-tabs');
	let id;
	
	// action for each tab
	$.each(tabs.find('a'), function(){
		$(this).click(function () {
			id = $(this).attr('href');
			hideAll();
			$(id).show();
		});
	});
	
	// show first
	hideAll();
	id = tabs.find('a:first').attr('href');
	$(id).show();
});

/**
 *
 */
function hideAll(){
	let tabs = $('#review-tabs');
	let id;
	$.each(tabs.find('a'), function(){
		id = $(this).attr('href');
		$(id).hide();
	});
}